#!/usr/bin/env python3
"""Convert Postman-converted XML files into readable HTML files.

Places HTML output in the html_output/ directory next to this script.
"""
import os
import xml.etree.ElementTree as ET
import html
from datetime import datetime

INPUT_DIR = os.path.join(os.path.dirname(__file__), "xml")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "html_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def text_of(elem):
    return elem.text.strip() if elem is not None and elem.text else ''

def find_all_requests(root):
    # Try common node names used for requests in various Postman exports
    requests = root.findall('.//request')
    if requests:
        return requests
    # fallback: look for item nodes containing method/url
    items = root.findall('.//item')
    candidates = []
    for it in items:
        if it.find('.//request') is not None:
            candidates.append(it.find('.//request'))
        elif it.find('.//url') is not None or it.find('.//method') is not None:
            candidates.append(it)
    return candidates

def render_request_html(elem):
    method = None
    url = None
    description = None
    headers = []
    body = None

    if elem.tag == 'request' or elem.find('method') is not None or elem.find('.//url') is not None:
        method = text_of(elem.find('method')) or elem.get('method')
        url_node = elem.find('.//url') or elem.find('url')
        if url_node is not None:
            raw = url_node.find('raw')
            url = text_of(raw) if raw is not None else text_of(url_node)
        for hdr in elem.findall('.//header'):
            k = hdr.find('key')
            v = hdr.find('value')
            headers.append((text_of(k), text_of(v)))
        body_node = elem.find('body')
        if body_node is not None:
            btext = text_of(body_node.find('raw')) or text_of(body_node)
            body = btext
        description = text_of(elem.find('description')) or text_of(elem.find('.//description'))
    else:
        method = elem.get('method') or ''
        url = text_of(elem.find('url')) or elem.get('url') or ''
        description = text_of(elem.find('description')) or ''
        for hdr in elem.findall('.//header'):
            headers.append((text_of(hdr.find('key')), text_of(hdr.find('value'))))
        body = text_of(elem.find('.//body'))

    s = []
    s.append('<div class="request">')
    s.append(f'<h3>{html.escape(method or "REQUEST")}: <span class="url">{html.escape(url or "")}</span></h3>')
    if description:
        s.append(f'<p class="desc">{html.escape(description)}</p>')
    if headers:
        s.append('<details><summary>Headers</summary><table class="hdr"><thead><tr><th>Key</th><th>Value</th></tr></thead><tbody>')
        for k, v in headers:
            s.append(f'<tr><td>{html.escape(k)}</td><td>{html.escape(v)}</td></tr>')
        s.append('</tbody></table></details>')
    if body:
        s.append('<details open><summary>Body</summary><pre class="body">{}</pre></details>'.format(html.escape(body)))
    raw_xml = ET.tostring(elem, encoding='unicode')
    s.append('<details><summary>Raw XML</summary><pre class="raw">{}</pre></details>'.format(html.escape(raw_xml)))
    s.append('</div>')
    return '\n'.join(s)

HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Converted XML - {name}</title>
<style>
body{{font-family:Arial,Helvetica,sans-serif;margin:20px;background:#f7f9fb;color:#222}}
h1{{color:#2a7f62}}
.request{{background:white;padding:15px;margin:12px 0;border-radius:8px;box-shadow:0 2px 6px rgba(0,0,0,0.06)}}
.request h3{{margin:0 0 8px 0}}
.url{{font-weight:600;color:#0b6e4f}}
.desc{{margin:6px 0;color:#555}}
.hdr{{width:100%;border-collapse:collapse;margin-top:8px}}
.hdr th,.hdr td{{border:1px solid #e6eef0;padding:6px 8px;text-align:left;font-size:0.95em}}
pre{{background:#07203a;color:#d6f7ff;padding:10px;border-radius:6px;overflow:auto}}
.details summary{{cursor:pointer}}
.meta{{font-size:0.9em;color:#666;margin-bottom:12px}}
</style>
</head>
<body>
<h1>Converted: {name}</h1>
<div class="meta">Converted on {ts} — Source file: {source}</div>
{content}
</body>
</html>
"""

def process_file(path):
    name = os.path.basename(path)
    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except Exception as e:
        # Try a forgiving parse: read file, remove illegal XML control characters and retry
        print(f"Initial parse failed for {path}: {e}. Attempting to clean and reparse.")
        try:
            with open(path, 'rb') as fb:
                raw = fb.read()
            # decode with replacement to avoid decode errors
            text = raw.decode('utf-8', errors='replace')
            # remove ASCII control chars that are invalid in XML (0x00-0x08, 0x0B-0x0C, 0x0E-0x1F)
            import re
            cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', '', text)
            # Additionally, unescaped ampersands in attribute values (e.g. "A & B") are common
            # and cause parse errors. We must escape ampersands that are NOT part of entities,
            # but we must NOT change text inside CDATA sections.
            parts = re.split(r'(<!\[CDATA\[.*?\]\]>)', cleaned, flags=re.DOTALL)
            for i, part in enumerate(parts):
                # only replace in non-CDATA parts
                if not part.startswith('<![CDATA['):
                    # replace '&' that is not followed by an entity name or #number and semicolon
                    parts[i] = re.sub(r'&(?!#?\w+;)', '&amp;', part)
            cleaned = ''.join(parts)
            root = ET.fromstring(cleaned)
            # wrap in ElementTree for compatibility
            tree = ET.ElementTree(root)
            print(f"Reparse after cleaning succeeded for {path}.")
        except Exception as e2:
            print(f"Reparse failed for {path}: {e2}")
            return
    requests = find_all_requests(root)
    content_parts = []
    if requests:
        for idx, req in enumerate(requests, 1):
            content_parts.append(f'<h2>Request #{idx}</h2>')
            content_parts.append(render_request_html(req))
    else:
        content_parts.append('<pre>{}</pre>'.format(html.escape(ET.tostring(root, encoding='unicode'))))

    out_html = HTML_TEMPLATE.format(
        name=name,
        ts=datetime.utcnow().isoformat() + "Z",
        source=html.escape(path),
        content='\n'.join(content_parts)
    )

    out_name = os.path.splitext(name)[0] + ".html"
    out_path = os.path.join(OUTPUT_DIR, out_name)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(out_html)
    print(f"Wrote {out_path}")

def main():
    if not os.path.isdir(INPUT_DIR):
        print("Input directory not found:", INPUT_DIR)
        return
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith('.xml')]
    if not files:
        print("No .xml files found in", INPUT_DIR)
        return
    for f in files:
        process_file(os.path.join(INPUT_DIR, f))
    print("Done. HTML files are in:", OUTPUT_DIR)

if __name__ == "__main__":
    main()
