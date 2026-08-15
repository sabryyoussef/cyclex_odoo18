# CycleX latest API — Newman test results

**Verdict: `CYCLEX_LATEST_API_ALL_TESTS_PASS`**

Evidence is the **August 2026** Newman run `20260815T125224`. This is not the November 2025 `phase_7` report.

Newman was **not re-run** for this handoff. Existing JSON/HTML were sanitized, screenshots were taken from the sanitized HTML, and this document was completed from that run.

| Field | Value |
|-------|--------|
| **Date / time** | 2026-08-15 15:52:25–15:52:59 (UTC+3) / 12:52:25–12:52:59 UTC |
| **Test branch** | `test/latest-api-newman-20260815` |
| **July API base SHA** | `eb762e68ae51dc0f60dfca95751b8beb2ab4fdf0` (`cursor/implement-cyclex-api-endpoints-8b1d`) |
| **Suite commit (original reports)** | `f89356655b6694b05fa79c3e99297f87913d4cb0` |
| **Odoo version** | `18.0` Community (`xmlrpc/2/common.version` on the TEST URL; Newman JSON does not include an Odoo version field) |
| **CycleX module (helper health during the run)** | `cyclex` **18.0.1.0.0**, state `installed` |
| **CycleX source on this branch** | `__manifest__.py` version **18.0.1.0.1** (test-required patches; `ir.module.module.latest_version` was not refreshed) |
| **TEST URL** | `http://127.0.0.1:18018` (loopback only) |
| **TEST database** | `cyclex_api_test_20260815` |
| **Admin helper** | `http://127.0.0.1:18019` (OTP, collector approve, wallet credit, token expire) |
| **Auth** | Bearer token (`Authorization: Bearer …`) |
| **Runner** | Newman 6.2.2 + newman-reporter-htmlextra 1.23.1 |
| **Collection** | `postman/latest/CycleX.latest.postman_collection.json` |
| **Production?** | **No.** Odoo 19 `odoo_test` on `:8069` was not used or modified. |

Credentials, tokens, session cookies, and OTPs are **not** recorded in this document.

---

## Evidence checks

| Check | Result |
|-------|--------|
| Newman JSON/HTML exist for stamp `20260815T125224` | Yes |
| CLI console log file | **Not persisted.** Totals below come from Newman JSON `run.stats` and the HTML dashboard. |
| Reports name the July API branch | Yes — collection description: `cursor/implement-cyclex-api-endpoints-8b1d` |
| Reports embed git commit SHA | **No.** Newman does not record git SHA. SHAs in this file come from `git`. |
| Target port `18018` | Yes — 51 of 60 requests hit `127.0.0.1:18018` |
| Target database `cyclex_api_test_20260815` | Yes — environment `db_name` and helper health body `{"db":"cyclex_api_test_20260815"}` |
| Authenticated customer/collector flows used helper `:18019` | Yes — 9 harness calls (health, phones, areas, customer OTP, collector OTP, approve, credit wallet, expire token) |

---

## 1. Newman totals (run `20260815T125224`)

| Metric | Total | Failed |
|--------|-------|--------|
| Iterations | 1 | 0 |
| Requests | **60** | **0** |
| Test scripts | 60 | 0 |
| Assertions | **130** | **0** |
| Skipped | **0** | — |
| Duration | 34.4s | |
| Avg response | 299 ms | |

Reproduce (TEST only, local secrets file required):

```bash
cd postman/latest
bash run_newman.sh
```

---

## 2. Endpoint-by-endpoint results

Classification: **PASS** = Newman assertion(s) succeeded. Expected 400/401/403 counted as PASS when that was the scenario. Helper rows are harness, not product endpoints.

| # | Request | Target | HTTP | Class |
|---|---------|--------|------|-------|
| 1 | Helper health | `:18019/health` | 200 | Harness |
| 2 | Allocate unique phones | `:18019/allocate-phones` | 200 | Harness |
| 3 | List working areas | `:18019/working-areas` | 200 | Harness |
| 4 | GET `/api/cyclex/health` | `:18018` | 200 | PASS |
| 5 | GET `/api/cyclex/categories` | `:18018` | 200 | PASS |
| 6 | GET `/api/cyclex/products` | `:18018` | 200 | PASS |
| 7 | GET `/api/cyclex/products?search=` | `:18018` | 200 | PASS |
| 8 | GET `/api/cyclex/products?category_id=` | `:18018` | 200 | PASS |
| 9 | POST login missing fields | `:18018` | 400 | PASS (validation) |
| 10 | POST register missing fields | `:18018` | 400 | PASS (validation) |
| 11 | POST register password mismatch | `:18018` | 400 | PASS (validation) |
| 12 | POST register weak password | `:18018` | 400 | PASS (validation) |
| 13 | POST request/create without token | `:18018` | 401 | PASS (expected deny) |
| 14 | GET wallet with junk token | `:18018` | 401 | PASS (expected deny) |
| 15 | POST `/api/cyclex/register` customer | `:18018` | 201 | PASS |
| 16 | POST register duplicate phone | `:18018` | 400 | PASS (unique phone) |
| 17 | POST login before OTP | `:18018` | 403 | PASS (expected deny) |
| 18 | POST `/api/cyclex/resend-code` | `:18018` | 200 | PASS |
| 19 | Helper fetch customer OTP | `:18019/otp` | 200 | Harness |
| 20 | POST verify invalid OTP | `:18018` | 400 | PASS (validation) |
| 21 | POST `/api/cyclex/verify` customer OTP | `:18018` | 200 | PASS |
| 22 | POST login invalid password | `:18018` | 401 | PASS (expected deny) |
| 23 | POST `/api/cyclex/login` customer success | `:18018` | 200 | PASS |
| 24 | POST request/create missing fields | `:18018` | 400 | PASS (validation) |
| 25 | POST `/api/cyclex/request/create` (complete later) | `:18018` | 201 | PASS |
| 26 | POST request/create (to cancel) | `:18018` | 201 | PASS |
| 27 | POST request/create (collector reject flow) | `:18018` | 201 | PASS |
| 28 | GET `/api/cyclex/request/list` | `:18018` | 200 | PASS |
| 29 | GET `/api/cyclex/request/details/4` | `:18018` | 200 | PASS |
| 30 | POST `/api/cyclex/request/cancel/5` | `:18018` | 200 | PASS |
| 31 | POST cancel already cancelled | `:18018` | 400 | PASS (idempotency) |
| 32 | POST collector/register missing fields | `:18018` | 400 | PASS (validation) |
| 33 | POST `/api/cyclex/collector/register` | `:18018` | 201 | PASS |
| 34 | Helper fetch collector OTP | `:18019/otp` | 200 | Harness |
| 35 | POST verify collector OTP | `:18018` | 200 | PASS |
| 36 | GET available-orders while pending | `:18018` | 403 | PASS (pending approval) |
| 37 | Admin approve collector | `:18019/approve-collector` | 200 | Harness |
| 38 | POST collector login after approval | `:18018` | 200 | PASS |
| 39 | GET `/api/cyclex/collector/available-orders` | `:18018` | 200 | PASS |
| 40 | POST accept reject-target | `:18018` | 200 | PASS |
| 41 | POST `/api/cyclex/collector/reject-order/:id` | `:18018` | 200 | PASS |
| 42 | POST `/api/cyclex/collector/accept-order/:id` | `:18018` | 200 | PASS |
| 43 | POST scan-qr missing | `:18018` | 400 | PASS (validation) |
| 44 | POST scan-qr invalid | `:18018` | 404 | PASS (validation) |
| 45 | POST `/api/cyclex/collector/scan-qr` | `:18018` | 200 | PASS |
| 46 | POST `/api/cyclex/collector/complete-order/:id` | `:18018` | 200 | PASS |
| 47 | GET `/api/cyclex/wallet/balance` | `:18018` | 200 | PASS |
| 48 | GET `/api/cyclex/wallet/transactions` | `:18018` | 200 | PASS |
| 49 | POST withdraw missing amount | `:18018` | 400 | PASS (validation) |
| 50 | POST withdraw below threshold | `:18018` | 400 | PASS (validation) |
| 51 | Helper credit wallet if below threshold | `:18019/credit-wallet` | 200 | Harness |
| 52 | POST `/api/cyclex/wallet/withdraw` | `:18018` | 200 | PASS |
| 53 | POST rate missing | `:18018` | 400 | PASS (validation) |
| 54 | POST rate invalid value | `:18018` | 400 | PASS (validation) |
| 55 | POST `/api/cyclex/order/rate/:id` | `:18018` | 200 | PASS |
| 56 | POST rate duplicate | `:18018` | 400 | PASS (idempotency) |
| 57 | Customer cannot access collector available-orders | `:18018` | 403 | PASS (role) |
| 58 | Collector cannot access customer wallet | `:18018` | 403 | PASS (role) |
| 59 | Admin expire customer token | `:18019/expire-token` | 200 | Harness |
| 60 | GET wallet with expired token | `:18018` | 401 | PASS (expired Bearer) |

---

## 3. Mandatory scenarios vs this run

| Mandatory scenario | Result |
|--------------------|--------|
| Health endpoint | PASS (`#4`) |
| Categories list | PASS (`#5`) |
| Products list | PASS (`#6–8`) |
| Product details | PASS via list payload (`id, name, category_id, price_per_kg, currency`). Dedicated `GET /api/cyclex/products/<id>` is **NOT_TESTED** — that route is not implemented in the July API. |
| Customer registration | PASS (`#15`) |
| OTP verification | PASS (`#21`) |
| Resend verification code | PASS (`#18`) |
| Successful customer login | PASS (`#23`) |
| Invalid login | PASS (`#22`) |
| Expired or invalid Bearer token | PASS (`#14`, `#60`) |
| Customer request creation | PASS (`#25–27`) |
| Customer request list and details | PASS (`#28–29`) |
| Customer request cancellation | PASS (`#30`) |
| Collector registration | PASS (`#33`) |
| Collector pending-approval restriction | PASS (`#36`) |
| Collector approval using a test admin workflow | PASS (`#37` helper + `#38` login) |
| Collector available orders | PASS (`#39`) |
| Collector accept and reject | PASS (`#40–42`) |
| QR scanning | PASS (`#43–45`) |
| Collector order completion | PASS (`#46`) |
| Wallet balance | PASS (`#47`) |
| Wallet transactions | PASS (`#48`) |
| Withdrawal request | PASS (`#52`) |
| Rating a completed order | PASS (`#55`) |
| Role-access validation | PASS (`#57–58`) |
| Validation errors for missing/invalid parameters | PASS (`#9–12`, `#24`, `#32`, `#43–44`, `#49–50`, `#53–54`) |
| Duplicate-request / idempotency | Duplicate **phone register** PASS (`#16`). Second **cancel** PASS (`#31`). Duplicate **rating** PASS (`#56`). Create-request idempotency key: **NOT_TESTED** (API has no idempotency key; two creates succeeded by design). |
| JSON envelope and HTTP status codes | PASS (assertions on `status` / `message` / `data` / `code` and status codes) |

---

## 4. Tested customer and collector workflows

**Customer:** register → resend code → verify OTP via helper → login → create requests → list → details → cancel → rate completed order → wallet denied for collector role.

**Collector:** register → verify OTP via helper → blocked while pending → admin approve on `:18019` → login → available orders → accept/reject → scan QR → complete → wallet balance/transactions → withdraw.

---

## 5. Limitations / NOT_TESTED

- Dedicated `GET /api/cyclex/products/<id>`: **NOT_TESTED** (route absent in July API).
- SMS Misr delivery of OTP: **NOT_TESTED**. OTP was read from `res.partner.verification_code` through the localhost helper.
- Newman CLI stdout log: **not saved** as a separate file.
- Git commit SHA is **not inside** Newman JSON/HTML.

---

## 6. Minimal code fixes applied before the passing run

Documented from earlier failing stamps `T124833` / `T124950`, then patched, then **this full suite** (`T125224`) was executed.

1. Skip `customer_rank` on Community `res.partner` (register HTTP 500).
2. Coerce collector `working_area_ids` to `int`.
3. Complete-order wallet/commission writes use `sudo()` (collector ACL).
4. CycleX Customer group / mail ACL so `mail.thread` request create works.
5. Copied module icon asset referenced by the manifest.

---

## 7. Production confirmation

No production data was accessed or changed. The TEST process is bound to `127.0.0.1:18018` / database `cyclex_api_test_20260815`. Database `odoo_test` on `:8069` was not opened for writes.

---

## 8. Artifacts

| File | Description |
|------|-------------|
| `postman/latest/CycleX.latest.postman_collection.json` | Unified Bearer collection |
| `postman/latest/CycleX.latest.postman_environment.template.json` | Sanitized env template (empty secrets) |
| `postman/latest/run_newman.sh` | Newman command |
| `postman/latest/admin_rpc_helper.py` | Local TEST OTP / approve / expire helper |
| `postman/latest/report/cyclex-latest-20260815T125224-report.sanitized.html` | htmlextra, secrets redacted |
| `postman/latest/report/cyclex-latest-20260815T125224-report.sanitized.json` | Newman JSON, secrets redacted |
| `postman/latest/report/cyclex-latest-20260815T125224.run-meta.json` | Run stamp, URLs, DB, totals (no secrets) |
| `postman/latest/screenshots/20260815T125224_01_newman_summary.jpg` | Overall Newman summary |
| `postman/latest/screenshots/20260815T125224_02_authentication.jpg` | Customer registration & auth |
| `postman/latest/screenshots/20260815T125224_03_customer_requests.jpg` | Customer request workflow |
| `postman/latest/screenshots/20260815T125224_04_collector_workflow.jpg` | Collector registration + orders |
| `postman/latest/screenshots/20260815T125224_05_wallet_rating.jpg` | Wallet, withdraw, rating |

Unsanitized HTML/JSON stay local (gitignored) because they contained Bearer tokens, session cookies, passwords, and OTPs.

`phase_7/postman` was not modified.
