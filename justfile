default:
    @just --list

test:
    PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v

check: test
