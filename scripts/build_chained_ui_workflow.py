#!/usr/bin/env python3
"""Convert the chained API prompt into a canvas-importable ComfyUI workflow."""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

if __package__:
    from .ada_paths import COMFYUI_BASE_URL
else:
    from ada_paths import COMFYUI_BASE_URL


POSITIONS = {
    "1": (720, 160), "2": (720, 300), "3": (720, 500), "4": (720, 700), "5": (1040, 350), "6": (1340, 350), "7": (1570, 220),
    "8": (1570, 470), "10": (1890, 130), "11": (1890, 280), "12": (1890, 430), "13": (2210, 300), "14": (2510, 260),
    "15": (2840, 200), "16": (2840, 420), "17": (3140, 150), "18": (3430, 260), "19": (3730, 260), "20": (3960, 180), "21": (3960, 430), "22": (4250, 430),
}

GROUPS = [
    (1, "INPUT / JSON", (0, 80, 610, 780), "#3f789e"),
    (2, "ILLUSTRIOUS FAST", (680, 80, 850, 850), "#5f8f49"),
    (3, "VRAM HANDOFF", (1540, 400, 270, 210), "#a87843"),
    (4, "KREA", (1860, 60, 2080, 700), "#84529b"),
    (5, "OUTPUTS / COMPARE", (3940, 80, 590, 650), "#3f789e"),
    (6, "METRICS", (0, 890, 610, 170), "#777777"),
]


def is_link(value: object) -> bool:
    return isinstance(value, list) and len(value) == 2 and isinstance(value[0], str) and isinstance(value[1], int)


def widget_values(node_type: str, inputs: dict) -> list:
    """Enough canonical widgets for a canvas import; API values remain authoritative."""
    if node_type == "KSampler":
        return [inputs["seed"], "fixed", inputs["steps"], inputs["cfg"], inputs["sampler_name"], inputs["scheduler"], inputs["denoise"]]
    order = {
        "CheckpointLoaderSimple": ["ckpt_name"], "CLIPTextEncode": ["text"], "EmptyLatentImage": ["width", "height", "batch_size"],
        "SaveImage": ["filename_prefix"], "UNETLoader": ["unet_name", "weight_dtype"], "CLIPLoader": ["clip_name", "type", "device"],
        "VAELoader": ["vae_name"], "ImageScale": ["upscale_method", "width", "height", "crop"],
        "Easy_QwenEdit2509": ["auto_resize", "vl_size", "prompt", "system_prompt"],
        "FluxKontextMultiReferenceLatentMethod": ["reference_latents_method"], "Krea2OstrisEditModelPatch": ["kv_cache"],
        "easy imageConcat": ["direction", "match_image_size"],
    }.get(node_type, [])
    return [inputs[name] for name in order if name in inputs and not is_link(inputs[name])]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    api = json.loads(args.api.read_text(encoding="utf-8"))
    object_info = json.load(urllib.request.urlopen(f"{COMFYUI_BASE_URL}/object_info"))
    nodes: list[dict] = []
    links: list[list] = []
    link_id = 1
    output_slots: dict[tuple[int, int], dict] = {}
    for order, (node_id, spec) in enumerate((item for item in api.items() if not item[0].startswith("_"))):
        node_type, inputs = spec["class_type"], spec["inputs"]
        definition = object_info[node_type]
        input_defs = {**definition.get("input", {}).get("required", {}), **definition.get("input", {}).get("optional", {})}
        input_names = list(inputs)
        ui_inputs = []
        for index, name in enumerate(input_names):
            value = inputs[name]
            linked = is_link(value)
            input_type = input_defs.get(name, ["*"])[0]
            if isinstance(input_type, list):
                input_type = "COMBO"
            ui_inputs.append({"name": name, "type": input_type, "link": None if not linked else link_id})
            if linked:
                source_id, source_slot = value
                source_type = output_slots.get((int(source_id), source_slot), {"type": "*"})["type"]
                links.append([link_id, int(source_id), source_slot, int(node_id), index, source_type])
                link_id += 1
        outputs = []
        for slot, output_type in enumerate(definition.get("output", [])):
            output = {"name": definition.get("output_name", [])[slot], "type": output_type, "slot_index": slot, "links": []}
            outputs.append(output)
            output_slots[(int(node_id), slot)] = output
        nodes.append({
            "id": int(node_id), "type": node_type, "pos": list(POSITIONS.get(node_id, (0, 0))), "size": [260, 150],
            "flags": {}, "order": order, "mode": 0, "inputs": ui_inputs, "outputs": outputs,
            "properties": {"Node name for S&R": node_type}, "widgets_values": widget_values(node_type, inputs),
        })
    for current_link in links:
        output_slots[(current_link[1], current_link[2])]["links"].append(current_link[0])
    ui = {"last_node_id": max(node["id"] for node in nodes), "last_link_id": link_id - 1, "nodes": nodes, "links": links,
          "groups": [{"id": gid, "title": title, "bounding": list(bounds), "color": color, "flags": {}} for gid, title, bounds, color in GROUPS],
          "config": {}, "extra": {"ds": {"scale": 0.65, "offset": [40, 40]}, "workflow_api_source": str(args.api)}, "version": 0.4}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(ui, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
