#!/usr/bin/env python3
"""Redact passwords, Bearer tokens, session cookies, OTPs, and private headers.

Works on Newman JSON and htmlextra HTML. Does not re-run tests.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SECRET_KEY = re.compile(
    r"(token|password|otp|verification_code|session_id|cookie|authorization|"
    r"secret|x-helper-token|set-cookie)",
    re.I,
)
BEARER = re.compile(r"Bearer\s+[A-Za-z0-9\-._~+/=]+", re.I)
SESSION = re.compile(r"session_id[=:][^\s;&\"'<]+", re.I)
HELPER_TOKEN = re.compile(r"cyclex-test-helper", re.I)
TEST_PASSWORD = re.compile(r"Test1234")
JSON_TOKEN = re.compile(r'("(?:token|access_token|refresh_token|customer_token|collector_token)"\s*:\s*")[^"]+(")', re.I)
JSON_PASSWORD = re.compile(r'("(?:password|confirm_password|old_password)"\s*:\s*")[^"]*(")', re.I)
JSON_OTP = re.compile(r'("(?:otp|verification_code|collector_otp)"\s*:\s*")[^"]*(")', re.I)
HTML_JSON_OTP = re.compile(
    r'((?:&quot;|")(?:otp|verification_code|collector_otp)(?:&quot;|")\s*:\s*)(?:&quot;|")[^"&]+(?:&quot;|")',
    re.I,
)
HTML_JSON_PASSWORD = re.compile(
    r'((?:&quot;|")(?:password|confirm_password)(?:&quot;|")\s*:\s*)(?:&quot;|")[^"&]*(?:&quot;|")',
    re.I,
)
HTML_JSON_TOKEN = re.compile(
    r'((?:&quot;|")(?:token|access_token|refresh_token)(?:&quot;|")\s*:\s*)(?:&quot;|")[^"&]+(?:&quot;|")',
    re.I,
)
HEX_COOKIE = re.compile(r"(session_id&#x3[dD];)[^<&\s]+", re.I)
HTML_HEADER_VALUE = re.compile(
    r"(<(?:td|code|pre)[^>]*>)([^<]*(?:Bearer|session_id|Test1234|cyclex-test-helper|verification_code)[^<]*)(</(?:td|code|pre)>)",
    re.I,
)


def redact_text(s: str) -> str:
    if not s:
        return s
    s = BEARER.sub("Bearer [REDACTED]", s)
    s = SESSION.sub("session_id=[REDACTED]", s)
    s = HEX_COOKIE.sub(r"\1[REDACTED]", s)
    s = HELPER_TOKEN.sub("[REDACTED]", s)
    s = TEST_PASSWORD.sub("[REDACTED]", s)
    s = JSON_TOKEN.sub(r"\1[REDACTED]\2", s)
    s = JSON_PASSWORD.sub(r"\1[REDACTED]\2", s)
    s = JSON_OTP.sub(r"\1[REDACTED]\2", s)
    s = HTML_JSON_TOKEN.sub(r"\1&quot;[REDACTED]&quot;", s)
    s = HTML_JSON_PASSWORD.sub(r"\1&quot;[REDACTED]&quot;", s)
    s = HTML_JSON_OTP.sub(r"\1&quot;[REDACTED]&quot;", s)
    return s


def drop_private_headers(headers):
    if not isinstance(headers, list):
        return headers
    out = []
    for h in headers:
        if not isinstance(h, dict):
            out.append(h)
            continue
        key = str(h.get("key") or h.get("name") or "")
        item = dict(h)
        if SECRET_KEY.search(key):
            item["value"] = "[REDACTED]"
        elif isinstance(item.get("value"), str):
            item["value"] = redact_text(item["value"])
        out.append(item)
    return out


def decode_stream(stream):
    if isinstance(stream, dict) and isinstance(stream.get("data"), list):
        try:
            return bytes(stream["data"]).decode("utf-8", errors="replace")
        except Exception:
            return None
    if isinstance(stream, (bytes, bytearray)):
        return bytes(stream).decode("utf-8", errors="replace")
    if isinstance(stream, str):
        return stream
    return None


def scrub(obj):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            kl = str(k)
            if kl in {"cookie", "cookies"}:
                out[k] = []
                continue
            if kl == "stream":
                text = decode_stream(v)
                out[k] = {"sanitized_text": redact_text(text) if text is not None else "[REDACTED]"}
                continue
            if kl in {"header", "headers"}:
                out[k] = drop_private_headers(v)
                continue
            if SECRET_KEY.search(kl) and not isinstance(v, (dict, list)):
                out[k] = "[REDACTED]" if v not in (None, "", True, False) else v
                continue
            out[k] = scrub(v)
        return out
    if isinstance(obj, list):
        return [scrub(x) for x in obj]
    if isinstance(obj, str):
        return redact_text(obj)
    return obj


def sanitize_html(html: str) -> str:
    html = redact_text(html)
    # Cookie / Set-Cookie / Authorization / X-Helper-Token table values
    html = re.sub(
        r"(<(?:td|span|code)[^>]*>)(\s*)(Bearer\s+\[REDACTED\]|session_id=\[REDACTED\]|\[REDACTED\])",
        r"\1\2\3",
        html,
    )
    html = re.sub(
        r"(<td class=\"text-nowrap\">(?:Cookie|Set-Cookie|Authorization|X-Helper-Token)</td>\s*<td[^>]*>)(.*?)(</td>)",
        r"\1[REDACTED]\3",
        html,
        flags=re.I | re.S,
    )
    return html


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        print("usage: sanitize_report.py SRC DST [SRC DST ...]", file=sys.stderr)
        sys.exit(2)
    pairs = list(zip(args[0::2], args[1::2]))
    for src_s, dst_s in pairs:
        src, dst = Path(src_s), Path(dst_s)
        raw = src.read_text(encoding="utf-8", errors="replace")
        if src.suffix.lower() == ".json" or raw.lstrip().startswith("{"):
            data = json.loads(raw)
            dst.write_text(json.dumps(scrub(data), indent=2), encoding="utf-8")
        else:
            dst.write_text(sanitize_html(raw), encoding="utf-8")
        print("sanitized", dst)


if __name__ == "__main__":
    main()
