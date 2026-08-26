#!/usr/bin/env python3
"""Canonical ADA 1.0 application entry point."""

from __future__ import annotations

import argparse
import json

from scripts.ada_paths import path_summary


def main() -> int:
    parser = argparse.ArgumentParser(description="ADA 1.0")
    parser.add_argument("command", nargs="?", choices=("serve", "paths", "check"), default="serve")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()

    if args.command == "paths":
        print(json.dumps(path_summary(), ensure_ascii=False, indent=2))
        return 0
    if args.command == "check":
        from ada_app.asset_library import AssetLibrary
        from ada_app.main import app
        from ada_app.mission import MissionStore

        assets = AssetLibrary().get_assets()
        missions = MissionStore().list_all()
        print(json.dumps({
            "status": "ok",
            "app": app.title,
            "library_assets": len(assets),
            "missions": len(missions),
            "paths": path_summary(),
        }, ensure_ascii=False, indent=2))
        return 0

    import uvicorn

    uvicorn.run("ada_app.main:app", host=args.host, port=args.port, reload=args.reload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
