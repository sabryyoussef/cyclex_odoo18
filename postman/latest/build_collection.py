#!/usr/bin/env python3
"""Generate CycleX latest API Postman collection (Bearer token, July 2026 routes)."""
from __future__ import annotations

import json
import uuid
from pathlib import Path

OUT = Path(__file__).with_name("CycleX.latest.postman_collection.json")


def rid():
    return str(uuid.uuid4())


def hdrs(*extra):
    items = [
        {"key": "Content-Type", "value": "application/json"},
        {"key": "Accept", "value": "application/json"},
    ]
    items.extend(extra)
    return items


BEARER = {
    "key": "Authorization",
    "value": "Bearer {{customer_token}}",
    "type": "text",
}
COLLECTOR_BEARER = {
    "key": "Authorization",
    "value": "Bearer {{collector_token}}",
    "type": "text",
}
HELPER = {"key": "X-Helper-Token", "value": "{{helper_token}}", "type": "text"}


def tests(*lines):
    return [{"listen": "test", "script": {"type": "text/javascript", "exec": list(lines)}}]


def prereq(*lines):
    return [{"listen": "prerequest", "script": {"type": "text/javascript", "exec": list(lines)}}]


def req(name, method, url, body=None, headers=None, extra_events=None, query=None):
    item = {
        "name": name,
        "request": {
            "method": method,
            "header": headers if headers is not None else hdrs(),
            "url": {
                "raw": url,
                "host": ["{{base_url}}"] if url.startswith("{{base_url}}") else (
                    ["{{helper_url}}"] if url.startswith("{{helper_url}}") else [url]
                ),
            },
        },
        "event": extra_events or [],
    }
    # Keep Postman URL object simple: use raw only
    item["request"]["url"] = url
    if query:
        item["request"]["url"] = url  # already includes query
    if body is not None:
        item["request"]["body"] = {
            "mode": "raw",
            "raw": body if isinstance(body, str) else json.dumps(body, indent=2),
            "options": {"raw": {"language": "json"}},
        }
    return item


OK_TRUE = [
    "const j = pm.response.json();",
    "pm.test('HTTP 2xx', () => pm.expect(pm.response.code).to.be.within(200, 299));",
    "pm.test('JSON status true', () => pm.expect(j.status).to.eql(true));",
    "pm.test('message present', () => pm.expect(j.message).to.be.a('string'));",
]


def folder(name, items, description=""):
    return {"name": name, "item": items, "description": description}


collection = {
    "info": {
        "_postman_id": rid(),
        "name": "CycleX Latest API (Bearer / July 2026)",
        "description": (
            "Newman suite for branch cursor/implement-cyclex-api-endpoints-8b1d.\n"
            "Auth: Authorization Bearer token (not session cookies).\n"
            "phase_7/postman remains historical and is not modified.\n"
            "TARGET MUST BE an Odoo 18 TEST database. Do not run against production."
        ),
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "variable": [
        {"key": "customer_token", "value": ""},
        {"key": "collector_token", "value": ""},
        {"key": "expired_token", "value": ""},
        {"key": "customer_phone", "value": ""},
        {"key": "collector_phone", "value": ""},
        {"key": "customer_password", "value": ""},
        {"key": "category_id", "value": ""},
        {"key": "product_id", "value": ""},
        {"key": "product_name", "value": ""},
        {"key": "working_area_id", "value": ""},
        {"key": "request_id", "value": ""},
        {"key": "cancel_request_id", "value": ""},
        {"key": "reject_request_id", "value": ""},
        {"key": "qr_code", "value": ""},
        {"key": "pickup_date", "value": ""},
        {"key": "otp", "value": ""},
        {"key": "collector_otp", "value": ""},
    ],
    "item": [],
}

# --- folders ---
f_boot = folder("00 — Test harness (local XML-RPC helper)", [
    req("Helper health", "GET", "{{helper_url}}/health", headers=[HELPER], extra_events=tests(
        "pm.test('helper HTTP 200', () => pm.expect(pm.response.code).to.eql(200));",
        "const j = pm.response.json();",
        "pm.test('helper ok', () => pm.expect(j.ok).to.eql(true));",
        "pm.test('cyclex installed', () => pm.expect(j.module && j.module.state).to.eql('installed'));",
    )),
    req("Allocate unique phones", "GET", "{{helper_url}}/allocate-phones", headers=[HELPER], extra_events=tests(
        "const j = pm.response.json();",
        "pm.test('phones allocated', () => pm.expect(j.ok).to.eql(true));",
        "pm.collectionVariables.set('customer_phone', j.customer_phone);",
        "pm.collectionVariables.set('collector_phone', j.collector_phone);",
        "pm.collectionVariables.set('customer_password', j.password);",
        "const d = new Date(); d.setDate(d.getDate() + 3);",
        "pm.collectionVariables.set('pickup_date', d.toISOString().slice(0,10));",
    )),
    req("List working areas", "GET", "{{helper_url}}/working-areas", headers=[HELPER], extra_events=tests(
        "const j = pm.response.json();",
        "pm.test('areas returned', () => { pm.expect(j.ok).to.eql(true); pm.expect(j.items.length).to.be.above(0); });",
        "pm.collectionVariables.set('working_area_id', String(j.items[0].id));",
    )),
], "Local 127.0.0.1 helper. Not a CycleX product endpoint.")

f_health = folder("01 — Health", [
    req("GET /api/cyclex/health", "GET", "{{base_url}}/api/cyclex/health", extra_events=tests(
        *OK_TRUE,
        "pm.test('payload status ok', () => pm.expect(pm.response.json().data.status).to.eql('ok'));",
        "pm.test('version present', () => pm.expect(pm.response.json().data.version).to.be.a('string'));",
    )),
])

f_catalog = folder("02 — Catalog", [
    req("GET /api/cyclex/categories", "GET", "{{base_url}}/api/cyclex/categories", extra_events=tests(
        *OK_TRUE,
        "const cats = pm.response.json().data.categories;",
        "pm.test('categories non-empty', () => pm.expect(cats.length).to.be.above(0));",
        "const leaf = cats.find(c => c.parent_id);",
        "pm.collectionVariables.set('category_id', String((leaf || cats[0]).id));",
    )),
    req("GET /api/cyclex/products", "GET", "{{base_url}}/api/cyclex/products", extra_events=tests(
        *OK_TRUE,
        "const items = pm.response.json().data.items;",
        "pm.test('products non-empty', () => pm.expect(items.length).to.be.above(0));",
        "pm.test('product has details fields', () => {",
        "  const p = items[0];",
        "  pm.expect(p).to.include.keys('id','name','category_id','price_per_kg','currency');",
        "});",
        "const copper = items.find(p => /copper/i.test(p.name)) || items[0];",
        "pm.collectionVariables.set('product_id', String(copper.id));",
        "pm.collectionVariables.set('product_name', copper.name);",
        "pm.collectionVariables.set('category_id', String(copper.category_id));",
    )),
    req("GET /api/cyclex/products?search=", "GET", "{{base_url}}/api/cyclex/products?search={{product_name}}", extra_events=tests(
        *OK_TRUE,
        "pm.test('search hits', () => pm.expect(pm.response.json().data.items.length).to.be.above(0));",
    )),
    req("GET /api/cyclex/products?category_id=", "GET", "{{base_url}}/api/cyclex/products?category_id={{category_id}}", extra_events=tests(
        *OK_TRUE,
        "const items = pm.response.json().data.items;",
        "pm.test('filtered products', () => pm.expect(items.length).to.be.above(0));",
        "pm.test('category matches', () => items.forEach(p => pm.expect(String(p.category_id)).to.eql(pm.collectionVariables.get('category_id'))));",
    )),
])

f_val = folder("03 — Validation errors", [
    req("POST login missing fields", "POST", "{{base_url}}/api/cyclex/login", body={}, extra_events=tests(
        "const j = pm.response.json();",
        "pm.test('HTTP 400', () => pm.expect(pm.response.code).to.eql(400));",
        "pm.test('status false', () => pm.expect(j.status).to.eql(false));",
        "pm.test('missing_fields', () => pm.expect(j.code).to.eql('missing_fields'));",
    )),
    req("POST register missing fields", "POST", "{{base_url}}/api/cyclex/register", body={"name": "X"}, extra_events=tests(
        "const j = pm.response.json();",
        "pm.test('HTTP 400', () => pm.expect(pm.response.code).to.eql(400));",
        "pm.test('missing_fields', () => pm.expect(j.code).to.eql('missing_fields'));",
    )),
    req("POST register password mismatch", "POST", "{{base_url}}/api/cyclex/register",
        body={"name": "X", "phone": "01999999999", "password": "abcdef", "confirm_password": "zzzzzz"},
        extra_events=tests(
            "const j = pm.response.json();",
            "pm.test('HTTP 400', () => pm.expect(pm.response.code).to.eql(400));",
            "pm.test('password_mismatch', () => pm.expect(j.code).to.eql('password_mismatch'));",
        )),
    req("POST register weak password", "POST", "{{base_url}}/api/cyclex/register",
        body={"name": "X", "phone": "01999999998", "password": "123", "confirm_password": "123"},
        extra_events=tests(
            "pm.test('weak_password', () => { const j = pm.response.json(); pm.expect(pm.response.code).to.eql(400); pm.expect(j.code).to.eql('weak_password'); });",
        )),
    req("POST request/create without token", "POST", "{{base_url}}/api/cyclex/request/create",
        body={"category_id": 1, "product_id": 1, "quantity": 1, "weight": 1, "pickup_date": "2099-01-01"},
        extra_events=tests(
            "const j = pm.response.json();",
            "pm.test('HTTP 401', () => pm.expect(pm.response.code).to.eql(401));",
            "pm.test('unauthorized', () => pm.expect(j.code).to.eql('unauthorized'));",
        )),
    req("GET wallet with junk token", "GET", "{{base_url}}/api/cyclex/wallet/balance",
        headers=hdrs({"key": "Authorization", "value": "Bearer not-a-real-token", "type": "text"}),
        extra_events=tests(
            "pm.test('invalid token 401', () => { pm.expect(pm.response.code).to.eql(401); pm.expect(pm.response.json().code).to.eql('unauthorized'); });",
        )),
])

f_cust_auth = folder("04 — Customer registration & auth", [
    req("POST /api/cyclex/register customer", "POST", "{{base_url}}/api/cyclex/register",
        body={
            "name": "Newman Customer",
            "phone": "{{customer_phone}}",
            "password": "{{customer_password}}",
            "confirm_password": "{{customer_password}}",
            "language": "en",
        }, extra_events=tests(
            "const j = pm.response.json();",
            "pm.test('HTTP 201', () => pm.expect(pm.response.code).to.eql(201));",
            "pm.test('verification required', () => { pm.expect(j.status).to.eql(true); pm.expect(j.data.verification_required).to.eql(true); });",
        )),
    req("POST /api/cyclex/register duplicate phone", "POST", "{{base_url}}/api/cyclex/register",
        body={
            "name": "Newman Customer Dup",
            "phone": "{{customer_phone}}",
            "password": "{{customer_password}}",
            "confirm_password": "{{customer_password}}",
        }, extra_events=tests(
            "const j = pm.response.json();",
            "pm.test('duplicate rejected', () => { pm.expect(pm.response.code).to.eql(400); pm.expect(j.status).to.eql(false); pm.expect(j.code).to.eql('validation_error'); });",
        )),
    req("POST login before OTP", "POST", "{{base_url}}/api/cyclex/login",
        body={"phone": "{{customer_phone}}", "password": "{{customer_password}}"},
        extra_events=tests(
            "const j = pm.response.json();",
            "pm.test('unverified or inactive denied', () => {",
            "  pm.expect(pm.response.code).to.be.oneOf([401,403]);",
            "  pm.expect(j.status).to.eql(false);",
            "});",
        )),
    req("POST /api/cyclex/resend-code", "POST", "{{base_url}}/api/cyclex/resend-code",
        body={"phone": "{{customer_phone}}"}, extra_events=tests(*OK_TRUE)),
    req("Helper fetch customer OTP", "GET", "{{helper_url}}/otp?phone={{customer_phone}}", headers=[HELPER], extra_events=tests(
        "const j = pm.response.json();",
        "pm.test('otp present', () => { pm.expect(j.ok).to.eql(true); pm.expect(j.partner.verification_code).to.match(/^\\d{6}$/); });",
        "pm.collectionVariables.set('otp', j.partner.verification_code);",
    )),
    req("POST verify invalid OTP", "POST", "{{base_url}}/api/cyclex/verify",
        body={"phone": "{{customer_phone}}", "verification_code": "000000"},
        extra_events=tests(
            "pm.test('invalid_code', () => { const j = pm.response.json(); pm.expect(pm.response.code).to.eql(400); pm.expect(j.code).to.eql('invalid_code'); });",
        )),
    req("POST /api/cyclex/verify customer OTP", "POST", "{{base_url}}/api/cyclex/verify",
        body={"phone": "{{customer_phone}}", "verification_code": "{{otp}}"}, extra_events=tests(
            "const j = pm.response.json();",
            "pm.test('HTTP 200 verify', () => pm.expect(pm.response.code).to.eql(200));",
            "pm.test('token issued', () => { pm.expect(j.status).to.eql(true); pm.expect(j.data.token).to.be.a('string').and.not.empty; });",
            "pm.collectionVariables.set('customer_token', j.data.token);",
        )),
    req("POST login invalid password", "POST", "{{base_url}}/api/cyclex/login",
        body={"phone": "{{customer_phone}}", "password": "WrongPass999"},
        extra_events=tests(
            "const j = pm.response.json();",
            "pm.test('invalid credentials 401', () => { pm.expect(pm.response.code).to.eql(401); pm.expect(j.code).to.eql('invalid_credentials'); });",
        )),
    req("POST /api/cyclex/login customer success", "POST", "{{base_url}}/api/cyclex/login",
        body={"phone": "{{customer_phone}}", "password": "{{customer_password}}"}, extra_events=tests(
            "const j = pm.response.json();",
            "pm.test('login 200', () => pm.expect(pm.response.code).to.eql(200));",
            "pm.test('bearer token', () => { pm.expect(j.data.token).to.be.a('string'); pm.expect(j.data.user.user_type).to.eql('customer'); });",
            "pm.collectionVariables.set('customer_token', j.data.token);",
            "pm.collectionVariables.set('expired_token', j.data.token);",
        )),
])

def authed(name, method, path, body=None, tok="customer"):
    h = hdrs(BEARER if tok == "customer" else COLLECTOR_BEARER)
    return req(name, method, "{{base_url}}" + path, body=body, headers=h)

f_req = folder("05 — Customer requests", [
    authed("POST request/create missing fields", "POST", "/api/cyclex/request/create", body={"category_id": 1})
])
f_req["item"][0]["event"] = tests(
    "const j = pm.response.json();",
    "pm.test('missing_fields 400', () => { pm.expect(pm.response.code).to.eql(400); pm.expect(j.code).to.eql('missing_fields'); });",
)
f_req["item"].extend([
    authed("POST /api/cyclex/request/create (complete later)", "POST", "/api/cyclex/request/create", body={
        "category_id": "{{category_id}}",
        "product_id": "{{product_id}}",
        "quantity": 1,
        "weight": 25,
        "pickup_date": "{{pickup_date}}",
        "gps_latitude": 30.0444,
        "gps_longitude": 31.2357,
    }),
])
f_req["item"][-1]["event"] = tests(
    "const j = pm.response.json();",
    "pm.test('created 201', () => pm.expect(pm.response.code).to.eql(201));",
    "pm.test('pending + qr', () => { pm.expect(j.status).to.eql(true); pm.expect(j.data.status).to.eql('pending'); pm.expect(j.data.qr_code).to.be.a('string'); });",
    "pm.collectionVariables.set('request_id', String(j.data.id));",
    "pm.collectionVariables.set('qr_code', j.data.qr_code);",
)
f_req["item"].extend([
    authed("POST request/create (to cancel)", "POST", "/api/cyclex/request/create", body={
        "category_id": "{{category_id}}",
        "product_id": "{{product_id}}",
        "quantity": 1,
        "weight": 2,
        "pickup_date": "{{pickup_date}}",
    }),
])
f_req["item"][-1]["event"] = tests(
    "const j = pm.response.json();",
    "pm.test('cancel target 201', () => pm.expect(pm.response.code).to.eql(201));",
    "pm.collectionVariables.set('cancel_request_id', String(j.data.id));",
)
f_req["item"].extend([
    authed("POST request/create (collector reject flow)", "POST", "/api/cyclex/request/create", body={
        "category_id": "{{category_id}}",
        "product_id": "{{product_id}}",
        "quantity": 1,
        "weight": 3,
        "pickup_date": "{{pickup_date}}",
    }),
])
f_req["item"][-1]["event"] = tests(
    "pm.test('reject target 201', () => pm.expect(pm.response.code).to.eql(201));",
    "pm.collectionVariables.set('reject_request_id', String(pm.response.json().data.id));",
)
f_req["item"].extend([
    authed("GET /api/cyclex/request/list", "GET", "/api/cyclex/request/list"),
])
f_req["item"][-1]["event"] = tests(
    *OK_TRUE,
    "pm.test('list has items', () => pm.expect(pm.response.json().data.items.length).to.be.at.least(3));",
)
f_req["item"].extend([
    authed("GET /api/cyclex/request/details/:id", "GET", "/api/cyclex/request/details/{{request_id}}"),
])
f_req["item"][-1]["event"] = tests(
    *OK_TRUE,
    "pm.test('details id matches', () => pm.expect(String(pm.response.json().data.id)).to.eql(pm.collectionVariables.get('request_id')));",
)
f_req["item"].extend([
    authed("POST /api/cyclex/request/cancel/:id", "POST", "/api/cyclex/request/cancel/{{cancel_request_id}}"),
])
f_req["item"][-1]["event"] = tests(
    *OK_TRUE,
    "pm.test('cancelled', () => pm.expect(pm.response.json().data.status).to.eql('cancelled'));",
)
f_req["item"].extend([
    authed("POST cancel already cancelled (idempotency)", "POST", "/api/cyclex/request/cancel/{{cancel_request_id}}"),
])
f_req["item"][-1]["event"] = tests(
    "const j = pm.response.json();",
    "pm.test('second cancel rejected', () => { pm.expect(pm.response.code).to.eql(400); pm.expect(j.code).to.eql('invalid_status'); });",
)

f_coll = folder("06 — Collector registration, pending, approval", [
    req("POST /api/cyclex/collector/register missing fields", "POST", "{{base_url}}/api/cyclex/collector/register",
        body={"name": "C"}, extra_events=tests(
            "pm.test('missing_fields', () => { pm.expect(pm.response.code).to.eql(400); pm.expect(pm.response.json().code).to.eql('missing_fields'); });",
        )),
    req("POST /api/cyclex/collector/register", "POST", "{{base_url}}/api/cyclex/collector/register",
        body='{\n  "name": "Newman Collector",\n  "phone": "{{collector_phone}}",\n  "password": "{{customer_password}}",\n  "confirm_password": "{{customer_password}}",\n  "id_number": "29901011234567",\n  "vehicle_type": "motorcycle",\n  "working_area_ids": [{{working_area_id}}]\n}'),
])
f_coll["item"][-1]["event"] = tests(
    "const j = pm.response.json();",
    "pm.test('HTTP 201', () => pm.expect(pm.response.code).to.eql(201));",
    "pm.test('pending approval', () => pm.expect(j.data.collector_approval_status).to.eql('pending'));",
)
f_coll["item"].extend([
    req("Helper fetch collector OTP", "GET", "{{helper_url}}/otp?phone={{collector_phone}}", headers=[HELPER], extra_events=tests(
        "const j = pm.response.json();",
        "pm.test('otp', () => pm.expect(j.partner.verification_code).to.match(/^\\d{6}$/));",
        "pm.collectionVariables.set('collector_otp', j.partner.verification_code);",
    )),
    req("POST verify collector OTP", "POST", "{{base_url}}/api/cyclex/verify",
        body={"phone": "{{collector_phone}}", "verification_code": "{{collector_otp}}"}, extra_events=tests(
            "const j = pm.response.json();",
            "pm.test('collector token', () => { pm.expect(pm.response.code).to.eql(200); pm.expect(j.data.token).to.be.a('string'); });",
            "pm.collectionVariables.set('collector_token', j.data.token);",
        )),
    authed("GET available-orders while pending approval", "GET", "/api/cyclex/collector/available-orders", tok="collector"),
])
f_coll["item"][-1]["event"] = tests(
    "const j = pm.response.json();",
    "pm.test('pending collector 403', () => { pm.expect(pm.response.code).to.eql(403); pm.expect(j.code).to.eql('collector_not_approved'); });",
)
f_coll["item"].extend([
    req("Admin approve collector", "POST", "{{helper_url}}/approve-collector", headers=[HELPER],
        body={"phone": "{{collector_phone}}"}, extra_events=tests(
            "const j = pm.response.json();",
            "pm.test('approved', () => { pm.expect(j.ok).to.eql(true); pm.expect(j.partner.collector_approval_status).to.eql('approved'); });",
        )),
    req("POST collector login after approval", "POST", "{{base_url}}/api/cyclex/login",
        body={"phone": "{{collector_phone}}", "password": "{{customer_password}}"}, extra_events=tests(
            "const j = pm.response.json();",
            "pm.test('collector login', () => { pm.expect(pm.response.code).to.eql(200); pm.expect(j.data.user.user_type).to.eql('collector'); });",
            "pm.collectionVariables.set('collector_token', j.data.token);",
        )),
])

f_flow = folder("07 — Collector orders: list, accept, reject, QR, complete", [
    authed("GET /api/cyclex/collector/available-orders", "GET", "/api/cyclex/collector/available-orders", tok="collector"),
])
f_flow["item"][-1]["event"] = tests(
    *OK_TRUE,
    "pm.test('pending orders exist', () => pm.expect(pm.response.json().data.items.length).to.be.above(0));",
)
f_flow["item"].extend([
    authed("POST accept reject-target", "POST", "/api/cyclex/collector/accept-order/{{reject_request_id}}", tok="collector"),
])
f_flow["item"][-1]["event"] = tests(
    *OK_TRUE,
    "pm.test('assigned', () => pm.expect(pm.response.json().data.status).to.eql('assigned'));",
)
f_flow["item"].extend([
    authed("POST /api/cyclex/collector/reject-order/:id", "POST", "/api/cyclex/collector/reject-order/{{reject_request_id}}", tok="collector"),
])
f_flow["item"][-1]["event"] = tests(
    *OK_TRUE,
    "pm.test('back to pending', () => pm.expect(pm.response.json().data.status).to.eql('pending'));",
)
f_flow["item"].extend([
    authed("POST /api/cyclex/collector/accept-order/:id (complete flow)", "POST", "/api/cyclex/collector/accept-order/{{request_id}}", tok="collector"),
])
f_flow["item"][-1]["event"] = tests(
    *OK_TRUE,
    "pm.test('assigned main', () => pm.expect(pm.response.json().data.status).to.eql('assigned'));",
    "if (pm.response.json().data.qr_code) { pm.collectionVariables.set('qr_code', pm.response.json().data.qr_code); }",
)
f_flow["item"].extend([
    authed("POST scan-qr missing", "POST", "/api/cyclex/collector/scan-qr", body={}, tok="collector"),
])
f_flow["item"][-1]["event"] = tests(
    "pm.test('missing qr', () => { pm.expect(pm.response.code).to.eql(400); pm.expect(pm.response.json().code).to.eql('missing_fields'); });",
)
f_flow["item"].extend([
    authed("POST scan-qr invalid", "POST", "/api/cyclex/collector/scan-qr", body={"qr_code": "not-a-real-qr"}, tok="collector"),
])
f_flow["item"][-1]["event"] = tests(
    "pm.test('invalid qr 404', () => { pm.expect(pm.response.code).to.eql(404); pm.expect(pm.response.json().code).to.eql('invalid_qr'); });",
)
f_flow["item"].extend([
    authed("POST /api/cyclex/collector/scan-qr", "POST", "/api/cyclex/collector/scan-qr", body={"qr_code": "{{qr_code}}"}, tok="collector"),
])
f_flow["item"][-1]["event"] = tests(
    *OK_TRUE,
    "pm.test('qr valid', () => pm.expect(pm.response.json().data.valid).to.eql(true));",
)
f_flow["item"].extend([
    authed("POST /api/cyclex/collector/complete-order/:id", "POST", "/api/cyclex/collector/complete-order/{{request_id}}", tok="collector"),
])
f_flow["item"][-1]["event"] = tests(
    *OK_TRUE,
    "pm.test('collected', () => pm.expect(pm.response.json().data.status).to.eql('collected'));",
)

f_wallet = folder("08 — Wallet & withdraw", [
    authed("GET /api/cyclex/wallet/balance", "GET", "/api/cyclex/wallet/balance"),
])
f_wallet["item"][-1]["event"] = tests(
    *OK_TRUE,
    "const d = pm.response.json().data;",
    "pm.test('balance numeric', () => pm.expect(d.balance).to.be.a('number'));",
    "pm.test('threshold present', () => pm.expect(d.withdrawal_threshold).to.be.a('number'));",
)
f_wallet["item"].extend([
    authed("GET /api/cyclex/wallet/transactions", "GET", "/api/cyclex/wallet/transactions"),
])
f_wallet["item"][-1]["event"] = tests(
    *OK_TRUE,
    "pm.test('credit from completed order', () => pm.expect(pm.response.json().data.items.length).to.be.above(0));",
)
f_wallet["item"].extend([
    authed("POST withdraw missing amount", "POST", "/api/cyclex/wallet/withdraw", body={}),
])
f_wallet["item"][-1]["event"] = tests(
    "pm.test('missing amount', () => { pm.expect(pm.response.code).to.eql(400); pm.expect(pm.response.json().code).to.eql('missing_fields'); });",
)
f_wallet["item"].extend([
    authed("POST withdraw below threshold", "POST", "/api/cyclex/wallet/withdraw", body={"amount": 1}),
])
f_wallet["item"][-1]["event"] = tests(
    "const j = pm.response.json();",
    "pm.test('below_threshold', () => { pm.expect(pm.response.code).to.eql(400); pm.expect(j.code).to.eql('below_threshold'); });",
)
f_wallet["item"].extend([
    req("Helper credit wallet if below threshold", "POST", "{{helper_url}}/credit-wallet", headers=[HELPER],
        body={"phone": "{{customer_phone}}", "amount": 1500}, extra_events=tests(
            "pm.test('credit helper 200 or already enough', () => pm.expect(pm.response.code).to.be.oneOf([200,404,500]););",
        )),
])
# fix typo in test
f_wallet["item"][-1]["event"] = tests(
    "pm.test('credit helper executed', () => pm.expect(pm.response.code).to.be.oneOf([200,404,500]));",
)
f_wallet["item"].extend([
    authed("POST /api/cyclex/wallet/withdraw", "POST", "/api/cyclex/wallet/withdraw", body={"amount": 1000}),
])
f_wallet["item"][-1]["event"] = tests(
    "const j = pm.response.json();",
    "pm.test('withdraw 200', () => pm.expect(pm.response.code).to.eql(200));",
    "pm.test('status true', () => pm.expect(j.status).to.eql(true));",
)

f_rate = folder("09 — Rating", [
    authed("POST rate missing", "POST", "/api/cyclex/order/rate/{{request_id}}", body={}),
])
f_rate["item"][-1]["event"] = tests(
    "pm.test('rating required', () => { pm.expect(pm.response.code).to.eql(400); pm.expect(pm.response.json().code).to.eql('missing_fields'); });",
)
f_rate["item"].extend([
    authed("POST rate invalid value", "POST", "/api/cyclex/order/rate/{{request_id}}", body={"rating": "9"}),
])
f_rate["item"][-1]["event"] = tests(
    "pm.test('invalid_rating', () => { pm.expect(pm.response.code).to.eql(400); pm.expect(pm.response.json().code).to.eql('invalid_rating'); });",
)
f_rate["item"].extend([
    authed("POST /api/cyclex/order/rate/:id", "POST", "/api/cyclex/order/rate/{{request_id}}",
           body={"rating": "5", "comments": "Newman test rating"}),
])
f_rate["item"][-1]["event"] = tests(
    *OK_TRUE,
    "pm.test('rated 5', () => pm.expect(pm.response.json().data.rating).to.eql('5'));",
)
f_rate["item"].extend([
    authed("POST rate duplicate", "POST", "/api/cyclex/order/rate/{{request_id}}", body={"rating": "4"}),
])
f_rate["item"][-1]["event"] = tests(
    "pm.test('already_rated', () => { pm.expect(pm.response.code).to.eql(400); pm.expect(pm.response.json().code).to.eql('already_rated'); });",
)

f_role = folder("10 — Role access & expired token", [
    authed("Customer cannot access collector available-orders", "GET", "/api/cyclex/collector/available-orders", tok="customer"),
])
f_role["item"][-1]["event"] = tests(
    "const j = pm.response.json();",
    "pm.test('customer forbidden on collector API', () => { pm.expect(pm.response.code).to.eql(403); pm.expect(j.code).to.eql('forbidden'); });",
)
f_role["item"].extend([
    authed("Collector cannot access customer wallet", "GET", "/api/cyclex/wallet/balance", tok="collector"),
])
f_role["item"][-1]["event"] = tests(
    "pm.test('collector forbidden on wallet', () => { pm.expect(pm.response.code).to.eql(403); pm.expect(pm.response.json().code).to.eql('forbidden'); });",
)
f_role["item"].extend([
    req("Admin expire customer token", "POST", "{{helper_url}}/expire-token", headers=[HELPER],
        body={"token": "{{customer_token}}"}, extra_events=tests(
            "pm.test('expired recorded', () => pm.expect(pm.response.json().ok).to.eql(true));",
        )),
    authed("GET wallet with expired token", "GET", "/api/cyclex/wallet/balance"),
])
f_role["item"][-1]["event"] = tests(
    "pm.test('expired token 401', () => { pm.expect(pm.response.code).to.eql(401); pm.expect(pm.response.json().code).to.eql('unauthorized'); });",
)

collection["item"] = [f_boot, f_health, f_catalog, f_val, f_cust_auth, f_req, f_coll, f_flow, f_wallet, f_rate, f_role]

OUT.write_text(json.dumps(collection, indent=2))
print("wrote", OUT, "requests", sum(len(f["item"]) for f in collection["item"]))
