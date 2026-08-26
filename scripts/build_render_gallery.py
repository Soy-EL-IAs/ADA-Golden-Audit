#!/usr/bin/env python3
"""Create a local side-by-side HTML gallery for a render-only batch."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

if __package__:
    from .ada_paths import resolve_legacy_path
else:
    from ada_paths import resolve_legacy_path


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def relative_url(target: Path, gallery_dir: Path) -> str:
    return target.resolve().relative_to(gallery_dir.resolve()).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("gallery.html"))
    args = parser.parse_args()

    batch_dir = args.batch_dir.resolve()
    output = (batch_dir / args.output).resolve() if not args.output.is_absolute() else args.output.resolve()
    batch = load_json(batch_dir / "batch_manifest.json")
    cards: list[str] = []
    for item in batch["runs"]:
        run_dir = resolve_legacy_path(item["run_dir"])
        manifest = load_json(run_dir / "manifest.json")
        if manifest.get("status") != "unreviewed_render_only":
            continue
        if not manifest.get("illustrious_candidates") or not manifest.get("krea_candidates"):
            continue
        ill = resolve_legacy_path(manifest["illustrious_candidates"][0]["image_path"])
        krea = resolve_legacy_path(manifest["krea_candidates"][0]["image_path"])
        premise = load_json(run_dir / "premise.json")
        title = f"{item['sequence']:03d} — {premise['character']}"
        cards.append(
            "<article class='card' data-name='{name}'>"
            "<h2>{title}</h2><p>{premise}</p><div class='pair'>"
            "<figure><a href='{ill}' target='_blank'><img src='{ill}' loading='lazy'></a><figcaption>Illustrious</figcaption></figure>"
            "<figure><a href='{krea}' target='_blank'><img src='{krea}' loading='lazy'></a><figcaption>Krea</figcaption></figure>"
            "</div></article>".format(
                name=html.escape(title.lower()),
                title=html.escape(title),
                premise=html.escape(premise["premise"]),
                ill=html.escape(relative_url(ill, output.parent)),
                krea=html.escape(relative_url(krea, output.parent)),
            )
        )

    page = """<!doctype html>
<html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Render-only gallery</title><style>
body{margin:0;background:#111;color:#eee;font:15px system-ui,sans-serif}header{position:sticky;top:0;z-index:2;padding:14px 5vw;background:#181818;border-bottom:1px solid #333}h1{margin:0 0 8px;font-size:20px}input{width:min(460px,90vw);padding:9px;border-radius:7px;border:1px solid #555;background:#222;color:#fff}.gallery{max-width:1500px;margin:auto;padding:18px;display:grid;gap:18px}.card{background:#1b1b1b;border:1px solid #333;border-radius:10px;padding:13px}.card h2{margin:0;font-size:17px}.card p{color:#bbb;margin:7px 0 13px}.pair{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}figure{margin:0;text-align:center}img{width:100%;max-height:720px;object-fit:contain;background:#000;border-radius:6px}figcaption{padding:6px;color:#ccc}@media(max-width:700px){.pair{grid-template-columns:1fr}}
</style></head><body><header><h1>Illustrious → Krea · __COUNT__ pruebas</h1><input id='filter' placeholder='Filtrar por personaje o número'></header><main class='gallery'>__CARDS__</main><script>
const q=document.querySelector('#filter');q.oninput=()=>document.querySelectorAll('.card').forEach(c=>c.hidden=!c.dataset.name.includes(q.value.toLowerCase()));
</script></body></html>""".replace("__COUNT__", str(len(cards))).replace("__CARDS__", "\n".join(cards))
    output.write_text(page, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
