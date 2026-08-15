# CycleX latest API — Newman test results

**Verdict: `CYCLEX_LATEST_API_ALL_TESTS_PASS`**

| Field | Value |
|-------|--------|
| **Date / time** | 2026-08-15 15:52 (UTC+3) / 12:52 UTC |
| **Tested branch** | `test/latest-api-newman-20260815` (from `cursor/implement-cyclex-api-endpoints-8b1d`) |
| **Base commit** | `eb762e68ae51dc0f60dfca95751b8beb2ab4fdf0` |
| **Odoo version** | 18.0 Community (`server_version_info` 18.0.0 final) |
| **CycleX module** | `cyclex` **18.0.1.0.1** (installed) |
| **TEST URL** | `http://127.0.0.1:18018` (loopback only) |
| **TEST database** | `cyclex_api_test_20260815` |
| **Auth** | Bearer token (`Authorization: Bearer …`) |
| **Runner** | Newman 6.2.2 + newman-reporter-htmlextra 1.23.1 |
| **Collection** | `postman/latest/CycleX.latest.postman_collection.json` |
| **Production?** | **No.** Odoo 19 `odoo_test` on `:8069` was not used or modified. |

Credentials, tokens, and OTPs are **not** recorded in this document.

---

## 1. Newman totals (passing run `20260815T125224`)

| Metric | Executed | Failed |
|--------|----------|--------|
| Iterations | 1 | 0 |
| Requests | **60** | **0** |
| Test scripts | 60 | 0 |
| Assertions | **130** | **0** |
| Skipped | 0 | — |
| Duration | 34.4s | |
| Avg response | 299 ms | |

Reproduce:

```bash
cd postman/latest
bash run_newman.sh
```

---

## 2. July 2026 routes vs `phase_7` Postman

`phase_7/postman/` is **unchanged** (historical). New suite lives under `postman/latest/`.

| Area | phase_7 (session cookie, mixed JSON-RPC/HTTP paths) | July 2026 PR #1 (Bearer) |
|------|------------------------------------------------------|---------------------------|
| Health | GET/POST `/api/cyclex/health` | **GET** `/api/cyclex/health` |
| Auth | `/api/cyclex/auth/login`, cookie `session_id` | **POST** `/api/cyclex/login` Bearer token |
| Register | signup collections | **POST** `/api/cyclex/register` |
| OTP | `/verify-otp`, `/resend-otp` | **POST** `/api/cyclex/verify`, `/api/cyclex/resend-code` |
| Catalog | `/api/cyclex/catalog/categories`, category item paths | **GET** `/api/cyclex/categories`, **GET** `/api/cyclex/products` |
| Product details | dedicated category-item collections | **No separate `/product/:id` route.** Details asserted from product list payload (`id, name, category_id, price_per_kg, currency`). |
| Requests | mixed `/orders` HTTP mapper | **POST/GET** `/api/cyclex/request/create\|list\|details/:id\|cancel/:id` |
| Collector | `/collector/*` mapper + cookie | **POST/GET** `/api/cyclex/collector/{register,available-orders,accept-order/:id,reject-order/:id,scan-qr,complete-order/:id}` |
| Wallet | `/wallet` mapper | **GET** `/api/cyclex/wallet/balance\|transactions`, **POST** `/withdraw` |
| Rating | `/rating-order` | **POST** `/api/cyclex/order/rate/:id` |

---

## 3. Endpoint-by-endpoint result (passing run)

Classification: PASS = assertion(s) succeeded. Expected 401/403/400 counted as PASS when that was the scenario.

| # | Scenario | HTTP | Class |
|---|----------|------|-------|
| 1 | Helper health / allocate phones / working areas | 200 | Harness |
| 2 | GET `/api/cyclex/health` | 200 | PASS |
| 3 | GET `/api/cyclex/categories` | 200 | PASS |
| 4 | GET `/api/cyclex/products` (+ search, category filter) | 200 | PASS |
| 5 | Login/register/request validation (missing/mismatch/weak) | 400 | PASS (validation) |
| 6 | Request create without token / junk Bearer | 401 | PASS (expected deny) |
| 7 | Customer register | 201 | PASS |
| 8 | Duplicate phone register | 400 | PASS (idempotency / unique phone) |
| 9 | Login before OTP | 403 | PASS (expected deny) |
| 10 | Resend verification code | 200 | PASS |
| 11 | Invalid OTP | 400 | PASS (validation) |
| 12 | Verify OTP → Bearer | 200 | PASS |
| 13 | Invalid login | 401 | PASS (expected deny) |
| 14 | Successful customer login | 200 | PASS |
| 15 | Customer request create / list / details | 201/200 | PASS |
| 16 | Cancel pending request | 200 | PASS |
| 17 | Cancel already cancelled | 400 `invalid_status` | PASS (idempotency) |
| 18 | Collector register | 201 pending | PASS |
| 19 | Collector OTP verify | 200 | PASS |
| 20 | Available-orders while pending approval | 403 `collector_not_approved` | PASS |
| 21 | Admin approve collector (XML-RPC helper) | 200 | Harness |
| 22 | Collector login after approval | 200 | PASS |
| 23 | Available orders | 200 | PASS |
| 24 | Accept then reject | 200 / pending | PASS |
| 25 | Accept main order | 200 assigned | PASS |
| 26 | Scan QR missing / invalid / valid | 400 / 404 / 200 | PASS |
| 27 | Complete order | 200 collected | PASS |
| 28 | Wallet balance + transactions | 200 | PASS |
| 29 | Withdraw missing / below threshold | 400 | PASS (validation) |
| 30 | Withdraw ≥ threshold | 200 | PASS |
| 31 | Rate missing / invalid / success / duplicate | 400 / 400 / 200 / 400 | PASS |
| 32 | Customer hits collector API | 403 | PASS (role) |
| 33 | Collector hits customer wallet | 403 | PASS (role) |
| 34 | Expired Bearer on wallet | 401 | PASS |

**No confirmed remaining bugs** on this TEST run after the minimal fixes below.

---

## 4. Minimal code fixes applied (test-required)

Documented first from failing runs, then patched, then **full suite re-run**.

1. **`res.partner.create_cyclex_user`** — `customer_rank` is not a field on Community `res.partner` (no `sale`/`account`). Register returned HTTP 500. Skip unknown fields.
2. **Collector `working_area_ids`** — coerce list values to `int`.
3. **`cyclex.request` complete-order** — collector user lacked ACL to create `cyclex.wallet.transaction` / commission. Complete returned 400 and could leave `collected` without a credit because the controller catches `UserError`/`AccessError` and returns JSON (HTTP layer commits). Financial writes now use `sudo()`.
4. **ACL / groups** — CycleX Customer implies Internal User; mail/attachment ACL rows added so `mail.thread` request create works for mobile users.
5. **Missing module asset** — copied `static/description/icon.png` to `static/src/img/icon.png` (referenced by `__manifest__.py`).

Module version bumped **18.0.1.0.0 → 18.0.1.0.1**.

OTP is still written to Odoo logs (`_send_verification_sms` placeholder). Tests read OTP via a **localhost XML-RPC helper** (`postman/latest/admin_rpc_helper.py`), not SMS Misr.

---

## 5. Confirmed bugs (after rerun)

None remaining in the passing suite.

---

## 6. Side effects

| Action | TEST DB only |
|--------|----------------|
| Customer + collector users | Created with unique phones `011…` / `012…` |
| Requests | Created / cancelled / assigned / collected |
| Wallet | Credited on complete; test withdrawal |
| Collector | Approved via admin XML-RPC helper |

**No production data was changed.** Process bound to `127.0.0.1:18018`. Database `odoo_test` (Odoo 19 / `:8069`) was not opened for writes.

---

## 7. Artifacts

| File | Description |
|------|-------------|
| `postman/latest/CycleX.latest.postman_collection.json` | Unified Bearer collection |
| `postman/latest/CycleX.latest.postman_environment.template.json` | Sanitized env template (no secrets) |
| `postman/latest/run_newman.sh` | Newman command |
| `postman/latest/admin_rpc_helper.py` | Local TEST OTP / approve / expire helper |
| `postman/latest/report/cyclex-latest-20260815T125224-report.sanitized.html` | htmlextra, tokens redacted |
| `postman/latest/report/cyclex-latest-20260815T125224-report.sanitized.json` | Newman JSON, tokens redacted |
| `postman/latest/screenshots/20260815T125224_newman_summary.jpg` | Summary screenshot |

Unsanitized HTML/JSON stay local (gitignored) because they contain Bearer tokens.

---

## 8. Known gaps (not failures)

- No dedicated GET `/api/cyclex/products/<id>` in PR #1. Product details were verified from the list payload.
- No idempotency key on request create; two creates succeed (by design). Duplicate **phone register** and **second cancel** are rejected.
- SMS Misr is not live; OTP retrieved via TEST helper from `res.partner.verification_code`.
