#!/usr/bin/env python3
"""Run a small, explicit live JEV batch; never invoked by normal checks."""

import argparse
import http.client
import json
import os
from pathlib import Path
import sys
import time

from jev_audit import Invalid, answer_from, canonical, cases_from, decode_json, load_json, prepare, require

HOST = "api.typesafe.ai"
ENDPOINT = "/v1/systemone"
MAX_RESPONSE_BYTES = 64_000
MAX_CALLS = 6
TIMEOUT_SECONDS = 20


def api_key(path=None):
    """Read one literal credential without evaluating shell or dotenv syntax."""
    if path is None:
        key = os.environ.get("TYPESAFE_API_KEY", "")
    else:
        with Path(path).open("r") as stream:
            content = stream.read(8193)
        require(len(content) <= 8192, "credential file exceeds size limit")
        lines = [line.strip() for line in content.splitlines() if line.strip() and not line.lstrip().startswith("#")]
        require(len(lines) == 1 and lines[0].startswith("TYPESAFE_API_KEY="), "credential file must contain only TYPESAFE_API_KEY=value")
        key = lines[0].partition("=")[2]
    require(bool(key) and len(key) <= 4096 and all(33 <= ord(char) <= 126 for char in key), "missing or invalid TYPESAFE_API_KEY")
    return key


def post(body, key):
    """One HTTPS attempt to a fixed host, without redirects or retries."""
    connection = http.client.HTTPSConnection(HOST, timeout=TIMEOUT_SECONDS)
    try:
        connection.request("POST", ENDPOINT, body=canonical(body).encode(), headers={
            "Authorization": f"Bearer {key}", "Content-Type": "application/json",
        })
        response = connection.getresponse()
        if response.status != 200:
            # Never print provider error bodies or request headers.
            raise Invalid(f"HTTP {response.status}; batch stopped without retry")
        payload = response.read(MAX_RESPONSE_BYTES + 1)
        require(len(payload) <= MAX_RESPONSE_BYTES, "response exceeds byte limit")
        # The offline evaluator also checks the saved JSON's structure.
        return decode_json(payload)
    finally:
        connection.close()


def run(cases, model, key, output, max_calls, send=post):
    """Persist every attempt; stop on first failure and retain missing cases."""
    requests = prepare(cases, model)["requests"]
    require(type(max_calls) is int and 1 <= max_calls <= MAX_CALLS, "max-calls must be between 1 and 6")
    require(len(requests) <= max_calls, "case count exceeds explicit call budget")
    recording = {"version": 1, "origin": "live", "observations": []}
    # Exclusive creation refuses old recordings and symlinks before any paid call.
    descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w") as stream:
        def save():
            serialized = json.dumps(recording, indent=2, allow_nan=False)
            stream.seek(0)
            stream.write(serialized + "\n")
            stream.truncate()
            stream.flush()
            os.fsync(stream.fileno())

        save()
        for request in requests:
            started = time.monotonic()
            observation = {"id": request["id"], "request_sha256": request["request_sha256"]}
            failed = False
            try:
                response = send(request["body"], key)
                # Refuse non-JSON numbers before persisting the response.
                canonical(response)
                observation["response"] = response
                answer_from(response, model)
            except Invalid as error:
                failed = True
                if "response" not in observation:
                    observation["error"] = str(error)
            except (OSError, http.client.HTTPException, UnicodeError, ValueError):
                failed = True
                observation["error"] = "transport or JSON failure; batch stopped without retry"
            finally:
                observation["elapsed_ms"] = round((time.monotonic() - started) * 1000, 3)
            recording["observations"].append(observation)
            save()
            if failed:
                return False
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key-file", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-calls", type=int, required=True)
    args = parser.parse_args(argv)
    try:
        cases = cases_from(load_json(args.cases))
        complete = run(cases, args.model, api_key(args.api_key_file), args.output, args.max_calls)
        print("Recording saved; evaluate it with jev_audit.py." if complete else "Batch stopped on failure; evaluate the partial recording.")
        return 0 if complete else 1
    except (Invalid, OSError, ValueError) as error:
        # Avoid arbitrary OS/provider error text that could contain credentials.
        message = str(error) if isinstance(error, Invalid) else "could not read inputs or create recording"
        print(f"jev-audit-live: {message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
