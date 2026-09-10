# Merge into a Node/TypeScript repository's justfile.
# Package scripts own the checks; keep pnpm check independent from just check.
default:
    @just --list

fmt:
    pnpm run format

fmt-check:
    pnpm run format:check

lint:
    pnpm run lint

typecheck:
    pnpm run typecheck

test:
    pnpm run test

build:
    pnpm run build

check:
    pnpm check
