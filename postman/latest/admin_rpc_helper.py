#!/usr/bin/env python3
"""Local TEST-only XML-RPC helper for CycleX Newman flows.

Binds to 127.0.0.1 only. Does not touch production. Credentials come from
environment variables — never from the committed Postman template.
"""
from __future__ import annotations

import json
import os
import time
import xmlrpc.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

HOST = os.environ.get("CYCLEX_HELPER_HOST", "127.0.0.1")
PORT = int(os.environ.get("CYCLEX_HELPER_PORT", "18019"))
TOKEN = os.environ.get("CYCLEX_HELPER_TOKEN", "cyclex-test-helper")
URL = os.environ.get("CYCLEX_ODOO_URL", "http://127.0.0.1:18018")
DB = os.environ.get("CYCLEX_ODOO_DB", "cyclex_api_test_20260815")
LOGIN = os.environ.get("CYCLEX_ODOO_ADMIN_LOGIN", "admin")
PASSWORD = os.environ.get("CYCLEX_ODOO_ADMIN_PASSWORD", "admin")


def _rpc():
    common = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/common", allow_none=True)
    uid = common.authenticate(DB, LOGIN, PASSWORD, {})
    if not uid:
        raise RuntimeError("XML-RPC authenticate failed")
    models = xmlrpc.client.ServerProxy(f"{URL}/xmlrpc/2/object", allow_none=True)
    return uid, models


def execute(model, method, *args, **kwargs):
    uid, models = _rpc()
    return models.execute_kw(DB, uid, PASSWORD, model, method, list(args), kwargs)


def json_ok(handler, payload, status=200):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def require_token(handler):
    got = handler.headers.get("X-Helper-Token") or handler.headers.get("Authorization", "")
    if got.startswith("Bearer "):
        got = got[7:]
    return got == TOKEN


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[helper]", self.address_string(), fmt % args)

    def _body(self):
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        raw = self.rfile.read(length)
        try:
            return json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            return {}

    def _deny(self):
        json_ok(self, {"ok": False, "error": "forbidden"}, 403)

    def do_GET(self):
        if not require_token(self):
            return self._deny()
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        path = parsed.path.rstrip("/") or "/"
        try:
            if path in ("/", "/health"):
                version = execute("ir.module.module", "search_read",
                                  [("name", "=", "cyclex")],
                                  fields=["name", "latest_version", "state"], limit=1)
                json_ok(self, {
                    "ok": True,
                    "db": DB,
                    "url": URL,
                    "module": version[0] if version else None,
                })
                return
            if path == "/allocate-phones":
                suffix = str(int(time.time()))[-8:]
                json_ok(self, {
                    "ok": True,
                    "customer_phone": f"011{suffix}",
                    "collector_phone": f"012{suffix}",
                    "password": os.environ.get("CYCLEX_TEST_USER_PASSWORD", "Test1234"),
                })
                return
            if path == "/otp":
                phone = (qs.get("phone") or [None])[0]
                recs = execute("res.partner", "search_read",
                               [("phone", "=", phone), ("is_cyclex_user", "=", True)],
                               fields=["id", "phone", "verification_code", "phone_verified",
                                       "collector_approval_status", "cyclex_user_type"],
                               limit=1)
                json_ok(self, {"ok": True, "partner": recs[0] if recs else None})
                return
            if path == "/working-areas":
                recs = execute("cyclex.working.area", "search_read", [],
                               fields=["id", "name", "governorate"], limit=20)
                json_ok(self, {"ok": True, "items": recs})
                return
            json_ok(self, {"ok": False, "error": "not_found"}, 404)
        except Exception as exc:
            json_ok(self, {"ok": False, "error": str(exc)}, 500)

    def do_POST(self):
        if not require_token(self):
            return self._deny()
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        body = self._body()
        try:
            if path == "/approve-collector":
                phone = body.get("phone")
                ids = execute("res.partner", "search",
                              [("phone", "=", phone), ("cyclex_user_type", "=", "collector")])
                if not ids:
                    json_ok(self, {"ok": False, "error": "collector not found"}, 404)
                    return
                execute("res.partner", "action_approve_collector", ids)
                rec = execute("res.partner", "read", ids,
                              fields=["id", "phone", "collector_approval_status", "account_status"])
                json_ok(self, {"ok": True, "partner": rec[0]})
                return
            if path == "/expire-token":
                token = body.get("token")
                ids = execute("cyclex.api.token", "search", [("token", "=", token)])
                if not ids:
                    json_ok(self, {"ok": False, "error": "token not found"}, 404)
                    return
                execute("cyclex.api.token", "write", ids, {
                    "expiry_date": "2000-01-01 00:00:00",
                    "active": True,
                })
                json_ok(self, {"ok": True, "expired_ids": ids})
                return
            if path == "/credit-wallet":
                phone = body.get("phone")
                amount = float(body.get("amount") or 0)
                partners = execute("res.partner", "search",
                                   [("phone", "=", phone), ("cyclex_user_type", "=", "customer")])
                if not partners:
                    json_ok(self, {"ok": False, "error": "customer not found"}, 404)
                    return
                wallets = execute("cyclex.wallet", "search", [("user_id", "=", partners[0])])
                if not wallets:
                    json_ok(self, {"ok": False, "error": "wallet not found"}, 404)
                    return
                tx_id = execute("cyclex.wallet.transaction", "create", {
                    "wallet_id": wallets[0],
                    "amount": amount,
                    "transaction_type": "credit",
                    "description": "TEST harness credit for withdrawal threshold",
                })
                rec = execute("cyclex.wallet", "read", wallets,
                              fields=["id", "balance", "withdrawal_threshold"])
                json_ok(self, {"ok": True, "transaction_id": tx_id, "wallet": rec[0] if rec else None})
                return
            json_ok(self, {"ok": False, "error": "not_found"}, 404)
        except Exception as exc:
            json_ok(self, {"ok": False, "error": str(exc)}, 500)


def main():
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"CycleX TEST admin helper http://{HOST}:{PORT} db={DB} url={URL}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
