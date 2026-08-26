#!/usr/bin/env python3
"""Build a compact local gallery from completed reusable Klein batch records."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from urllib.parse import quote


def file_url(path: Path) -> str:
    return "file:///" + quote(path.resolve().as_posix(), safe="/:_")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--comfy-output", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    records = [
        record for record in manifest.get("records", [])
        if record.get("status") == "complete" and record.get("compare")
    ]
    cards = []
    for record in records:
        descriptor = record["compare"][0]
        image_path = args.comfy_output / descriptor.get("subfolder", "") / descriptor["filename"]
        cards.append(
            f'<article><h2>{record["index"]:03d} · {html.escape(record["id"])}</h2>'
            f'<a href="{file_url(image_path)}"><img loading="lazy" src="{file_url(image_path)}" '
            f'alt="{html.escape(record["id"])} Illustrious y Klein"></a></article>'
        )
    stopped = [record for record in manifest.get("records", []) if record.get("status") != "complete"]
    stopped_text = ", ".join(html.escape(str(record.get("id"))) for record in stopped) or "ninguno"
    document = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Illustrious → Klein · {html.escape(manifest['batch_id'])}</title>
<style>
:root{{color-scheme:dark;background:#0c0d10;color:#f6f6f6;font-family:Inter,system-ui,sans-serif}}
body{{margin:0;padding:24px}}header{{position:sticky;top:0;z-index:2;background:#0c0d10e8;backdrop-filter:blur(12px);padding:8px 0 18px}}
h1{{margin:0 0 6px;font-size:24px}}p{{margin:0;color:#aeb4c0}}main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(480px,1fr));gap:18px;margin-top:18px}}
article{{background:#17191f;border:1px solid #292d36;border-radius:14px;overflow:hidden;box-shadow:0 10px 30px #0007}}
h2{{font-size:14px;margin:0;padding:11px 14px;color:#d8dce6}}img{{display:block;width:100%;height:auto;background:#111}}
@media(max-width:560px){{body{{padding:10px}}main{{grid-template-columns:1fr}}}}
</style></head><body><header><h1>Illustrious → Klein</h1>
<p>{len(records)} resultados completos · detenido en: {stopped_text} · clic para abrir en tamaño completo</p></header>
<main>{''.join(cards)}</main></body></html>"""
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(document, encoding="utf-8")
    print(json.dumps({"status": "ok", "completed": len(records), "output": str(args.output.resolve())}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
