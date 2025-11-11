# Converted Collections

This folder contains tools and outputs used to convert Postman-style XML collections (rbc format) into readable HTML files.

Files
- `xml/` — source XML files (e.g. `CycleX_API_Collection.rbc.xml`, `CycleX_Environment.rbc.xml`).
- `convert_xml_to_html.py` — Python script that converts XML files in `xml/` into HTML files written to `html_output/`.
- `html_output/` — generated HTML files (`*.html`). These are generated artifacts; you can remove them from git if you prefer to keep only the converter script in the repository.

Usage

From the repository root run:

```bash
python3 postman_collections/cyclex-api-collection-project/converted_collections/convert_xml_to_html.py
```

This will read all `.xml` files inside `postman_collections/cyclex-api-collection-project/converted_collections/xml/` and write `.html` files to `postman_collections/cyclex-api-collection-project/converted_collections/html_output/`.

Notes
- The converter is forgiving: it attempts to clean invalid control characters and escape stray ampersands outside CDATA blocks before parsing XML.
- The converter preserves JSON bodies inside CDATA sections and includes a "Raw XML" section per request for debugging.
- If you prefer not to commit generated HTML files, add `converted_collections/html_output/` to `.gitignore` and commit only the converter script and this README.

Suggested follow-ups
- Add CI step to regenerate HTML during deployment or documentation build.
- Generate a single index.html that links all converted files for easier browsing.

If you want me to remove the generated HTML files from the repo and add a `.gitignore` entry instead, say so and I'll update the branch.
