#!/usr/bin/env python3
"""Render JPEG evidence from the existing sanitized Newman HTML. Does not re-run tests."""
from __future__ import annotations

import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "report/cyclex-latest-20260815T125224-report.sanitized.html"
SHOT = ROOT / "screenshots"
STAMP = "20260815T125224"

FOLDERS = {
    "auth": [
        "folder-collapse-07eccfbc-cac0-4c1a-8e80-e0172a1c5d0e-iteration-0",
    ],
    "customer": [
        "folder-collapse-b948f248-be98-49a5-bb42-b5006f802031-iteration-0",
    ],
    "collector": [
        "folder-collapse-15dc0b4e-4216-4564-a61c-7f9a02a27305-iteration-0",
        "folder-collapse-ca3bf6a0-34c7-4e0e-b72f-70efb6f32548-iteration-0",
    ],
    "wallet_rating": [
        "folder-collapse-3026b6f4-517d-4520-a647-c6d4f5e6d07b-iteration-0",
        "folder-collapse-e494d174-046d-43d1-8caf-871ecb7d0339-iteration-0",
    ],
}

EXTRA_CSS = """
<style>
body.theme-dark { background: #1e2730 !important; }
#pills-requests .card .collapse .card-body { display: none !important; }
.tab-pane { display: none !important; }
.tab-pane.show.active { display: block !important; }
.collapse { display: none !important; }
.collapse.show { display: block !important; }
</style>
"""


def rewrite(html: str, *, summary: bool, folders: list[str] | None) -> str:
    html = html.replace('class="theme-dark"', 'class="theme-light"', 1)
    html = html.replace("</head>", EXTRA_CSS + "</head>", 1)
    if summary:
        return html
    html = html.replace(
        'id="pills-summary" role="tabcard" aria-labelledby="pills-summary-tab" class="tab-pane fade show active"',
        'id="pills-summary" role="tabcard" aria-labelledby="pills-summary-tab" class="tab-pane fade"',
        1,
    )
    html = html.replace(
        'id="pills-requests" role="tabcard" aria-labelledby="pills-requests-tab" class="tab-pane fade"',
        'id="pills-requests" role="tabcard" aria-labelledby="pills-requests-tab" class="tab-pane fade show active"',
        1,
    )
    # htmlextra may order attributes differently
    html = html.replace(
        '<div class="tab-pane fade show active" id="pills-summary"',
        '<div class="tab-pane fade" id="pills-summary"',
        1,
    )
    html = html.replace(
        '<div class="tab-pane fade" id="pills-requests"',
        '<div class="tab-pane fade show active" id="pills-requests"',
        1,
    )
    for fid in folders or []:
        html = html.replace(
            f'id="{fid}" class="collapse"',
            f'id="{fid}" class="collapse show"',
        )
    return html


def render(html: str, dest: Path, height: int) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(html)
        tmp_path = tmp.name
    cmd = [
        "wkhtmltoimage",
        "--width", "1400",
        "--crop-h", str(height),
        "--quality", "70",
        "--format", "jpg",
        "--enable-local-file-access",
        tmp_path,
        str(dest),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    Path(tmp_path).unlink(missing_ok=True)
    print("wrote", dest, dest.stat().st_size)


def main():
    src = HTML.read_text(encoding="utf-8", errors="replace")
    SHOT.mkdir(exist_ok=True)
    render(rewrite(src, summary=True, folders=None), SHOT / f"{STAMP}_01_newman_summary.jpg", 1250)
    render(rewrite(src, summary=False, folders=FOLDERS["auth"]), SHOT / f"{STAMP}_02_authentication.jpg", 1600)
    render(rewrite(src, summary=False, folders=FOLDERS["customer"]), SHOT / f"{STAMP}_03_customer_requests.jpg", 1500)
    render(rewrite(src, summary=False, folders=FOLDERS["collector"]), SHOT / f"{STAMP}_04_collector_workflow.jpg", 1800)
    render(rewrite(src, summary=False, folders=FOLDERS["wallet_rating"]), SHOT / f"{STAMP}_05_wallet_rating.jpg", 1700)


if __name__ == "__main__":
    main()
