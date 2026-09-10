# Host-only starter. Mixed/firmware repos must add their documented target gate.
default:
    @just --list

fmt:
    cargo fmt --all

fmt-check:
    cargo fmt --all --check

lint:
    cargo clippy --locked --workspace --all-targets -- -D warnings

test-fast:
    cargo test --locked --workspace --lib --tests

test:
    cargo test --locked --workspace

build:
    cargo build --locked --workspace

check: fmt-check lint test build
