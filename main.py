#!/usr/bin/env python3
"""The Houseplant Out-of-Office — make.fun entry.

Writes one line to /output/entry.txt: an out-of-office auto-reply
from a houseplant that has not been watered since March.

The entry must be exactly one line, 1-120 characters, with no
trailing newline. This version validates the line against the gate
before writing, then reads the file back and verifies its sha256.
"""

import hashlib
import os

ENTRY = "Out of office. You have not watered me since March, so I have not read your email since March either."

EXPECTED_SHA256 = "5f5626b3d0cac9c32bb828088c1aec8c1670197eb5a376259a889ea2a79f326c"


def main() -> None:
    line = ENTRY
    if not line or line.strip() == "":
        raise SystemExit("entry must not be blank")
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be a single line")
    encoded = line.encode("utf-8")
    if not 1 <= len(encoded) <= 120:
        raise SystemExit(f"entry must be 1-120 chars, got {len(encoded)}")
    if line != line.strip():
        raise SystemExit("entry must not have leading/trailing whitespace")

    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8", newline="") as f:
        f.write(line)

    with open("/output/entry.txt", "rb") as f:
        written = f.read()
    digest = hashlib.sha256(written).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"read-back sha256 mismatch: {digest}")
    print(f"wrote /output/entry.txt ({len(written)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
