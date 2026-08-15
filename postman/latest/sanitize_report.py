#!/usr/bin/env python3
"""Redact tokens, passwords, OTPs, and session cookies from Newman JSON reports."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

KEYS = re.compile(
    r"(token|password|otp|verification_code|session_id|cookie|authorization|secret)",
    re.I,
)
BEARER = re.compile(r"Bearer\s+[A-Za-z0-9\-._~+/]+=*", re.I)


def scrub(obj):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if KEYS.search(str(k)):
                if isinstance(v, (dict, list)):
                    out[k] = scrub(v)
                elif v in (None, "", False, True):
                    out[k] = v
                else:
                    out[k] = "[REDACTED]"
            else:
                out[k] = scrub(v)
        return out
    if isinstance(obj, list):
        return [scrub(x) for x in obj]
    if isinstance(obj, str):
        return BEARER.sub("Bearer [REDACTED]", obj)
    return obj


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    data = json.loads(src.read_text())
    dst.write_text(json.dumps(scrub(data), indent=2))
    print("sanitized", dst)


if __name__ == "__main__":
    main()
