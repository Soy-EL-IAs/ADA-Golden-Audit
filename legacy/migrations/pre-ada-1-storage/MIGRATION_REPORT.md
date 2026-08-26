# ADA Base Migration v1 — Migration Report

## 1. Source original

`C:\Users\ELIAS\Documents\Codex\2026-08-20\referenced-chatgpt-conversation-this-is-an\outputs\luna_pipeline`

## 2. Destination

`D:\IA\Ada`

## 3. Fecha y snapshot

- Snapshot: `2026-08-21T17:26:45.826068-03:00`
- Archivos fuente: 1190
- Tamaño fuente: 588912653 bytes
- Archivos con SHA256 completo: 804
- Copia inicial: 0 faltantes, 0 tamaños distintos, 0 hashes distintos

Verificación final del source: PASS. El árbol original conserva exactamente 1190 archivos y coincide con el snapshot pre-migración en tamaño, mtime y cada hash SHA256 registrado. No hay archivos faltantes, extra ni modificados en el source.

## 4. Estructura final

Se preservó la estructura reconocible: `scripts`, `config`, `workflows`, `docs`, `data`, `prompts`, `character_refs`, `character_dataset_staging`, `klein_batch_runs`, `visual_review_runs`, `runs`, `render_only_runs`, `klein_ab_tests` y demás históricos. Se agregaron `migration` y `assets/generated` con documentación concreta; no se crearon servicios o capas vacías.

## 5. Archivos creados

- `scripts/ada_paths.py`
- `config/ada.local.json`
- `config/ada.example.json`
- `docs/ADA_ARCHITECTURE.md`
- `assets/generated/README.md`
- `migration/inventory.md`
- `migration/inventory.json`
- `migration/pre_migration_manifest.json`
- `migration/copy_verification.json`
- `migration/source_integrity_final.json`
- `migration/ada_delta_from_snapshot.json`
- `migration/run_data_smoke.py`
- `migration/data_smoke_results.json`
- `migration/run_lmstudio_smoke.py`
- `migration/lmstudio_smoke_results.json`
- `prompts/ada_migration_smoke_2.jsonl`
- `config/klein_presets_ada_migration_smoke_2.json`
- staging `character_dataset_staging/ada_migration_smoke_2/`

## 6. Archivos modificados

- `README.md`
- `lmstudio_mcp_entry.json`
- `lmstudio_mcp_full.json`
- `lmstudio_mcp_searxng.json`
- `scripts/build_chained_ui_workflow.py`
- `scripts/build_render_gallery.py`
- `scripts/character_dataset.py`
- `scripts/character_profile.py`
- `scripts/character_ref_cache.py`
- `scripts/character_refs.py`
- `scripts/diagnose_master_visual_review.py`
- `scripts/lmstudio_controller.py`
- `scripts/lmstudio_operator.py`
- `scripts/local_search.py`
- `scripts/luna_pipeline.py`
- `scripts/query_booru_characters.py`
- `scripts/run_klein_ab_test.py`
- `scripts/run_klein_jsonl_batch.py`
- `scripts/run_visual_review_benchmark.py`
- `scripts/run_visual_review_comparison.py`
- `scripts/visual_reviewer.py`

Los cambios se limitan a resolución de paths/endpoints e imports compatibles. No se cambiaron prompts, workflows, LoRAs, strengths, steps, samplers, seeds, IDs, schemas, scoring, thresholds ni semántica MCP.

## 7. Paths hardcodeados encontrados

El inventario registró 1542 hits. La mayoría son metadata histórica dentro de runs/manifests. Los activos relevantes eran los tres entrypoints MCP con el source absoluto, la raíz externa de ComfyUI en `config/pipeline.json`, endpoints loopback y roots derivados localmente en varios scripts.

## 8. Paths runtime centralizados

`scripts/ada_paths.py` resuelve `ADA_ROOT`, data, assets, prompts, workflows, refs, staging, Klein runs, visual-review runs, character DB, endpoints LM Studio/ComfyUI y el root externo de ComfyUI. Precedencia: entorno → `config/ada.local.json` → configuración/defaults derivados.

Variables disponibles: `ADA_ROOT`, `ADA_COMFYUI_ROOT`, `ADA_LMSTUDIO_URL`, `ADA_COMFYUI_URL`. Se mantienen `LM_STUDIO_URL` y las interfaces anteriores por compatibilidad.

## 9. Paths legacy conservados

No se reescribieron manifests, benchmarks, prompts, provenance ni metadata de imágenes. `resolve_legacy_path()` traduce paths internos del antiguo root a la copia equivalente en Ada cuando existe. `LunaKleinBatch` se conserva como prefix interno compatible con ComfyUI.

## 10. Dependencias externas

- ComfyUI: `D:\IA\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI`
- API ComfyUI: `http://127.0.0.1:8188`
- LM Studio: `http://127.0.0.1:1234`
- SearXNG local opcional: `http://127.0.0.1:8080`
- Python local configurado en los entrypoints MCP
- Checkpoints, modelos, LoRAs, CUDA/Python portable y model storage permanecen externos y no fueron duplicados.

## 11. Datos copiados

Se copiaron los 1190 archivos del proyecto: character DB, aliases, refs/cache, datasets, staging, configs, workflows, manifests, runs, reviews, benchmarks y assets internos pequeños/históricos. La copia inicial totalizó 588912653 bytes. No se copiaron instalaciones o modelos externos.

## 12. Generated assets strategy

El output real `ComfyUI/output/LunaKleinBatch` contiene 337 archivos y 558619022 bytes. Es una carpeta física normal. ADA v1 la deja intacta y centraliza su root mediante configuración. `assets/generated` documenta el destino futuro preferido.

## 13. Junction

No se creó junction. Crear una habría requerido copiar otros ~559 MB, verificar, renombrar la carpeta activa de ComfyUI y cambiar su topología. Esa operación se difirió por reversibilidad y riesgo. No se movió ni renombró ningún output.

## 14–15. Smoke tests y resultados

- Syntax/import validation: PASS (`compileall` e imports desde `D:\IA\Ada`).
- A — Path resolution: PASS. Ada, ComfyUI, character DB, prompts, runs y workflows resuelven desde D:.
- B — Character profile: PASS. `2B / NieR:Automata`, `character_profile_used=true`, `matched_tag=2b_(nier:automata)` desde la DB local.
- C — Dataset pipeline: PASS. `prepare → append → finalize` con 2 entradas `ada_migration_smoke_2`; JSONL, seeds, IDs, presets y compilación validados; ComfyUI no ejecutado.
- D — Visual Reviewer: PASS. Una imagen existente revisada una vez por `qwen/qwen3-vl-8b`, JSON válido, sin cambiar reviewer.
- E — VRAM orchestration: PASS. Inicial Master; luego sólo Worker; finalmente sólo Master. Nunca coexistieron.
- F — Existing data: PASS. Se leyeron dataset, preset plan, generation manifest y resultado visual histórico sin modificarlos.
- G — Runner validation: PASS. Workflow, dataset, preset plan y output prefix compilaron para un registro; no se ejecutó batch.
- H — Generated asset: PASS. Una PNG histórica se resolvió por compatibilidad legacy desde Ada; no se necesitó junction.

El output externo `ComfyUI/output/LunaKleinBatch` permaneció en 337 archivos y 558619022 bytes después de la validación.

Resultados completos: `migration/data_smoke_results.json` y `migration/lmstudio_smoke_results.json`.

## 16. Warnings

- `config/ada.local.json` es machine-local y contiene paths de esta PC.
- Los entrypoints MCP contienen el path absoluto `D:\IA\Ada` porque LM Studio necesita una ruta ejecutable concreta.
- La carpeta externa de outputs permanece bajo ComfyUI en esta v1.
- Los `.pyc` pueden regenerarse según la versión local de Python y no son datos autoritativos.

## 17. Known issues

El Master Visual Reviewer 27B no produce JSON con fiabilidad total. Structured Output puede gastar el presupuesto en `reasoning_content`, terminar con `finish_reason=length` y dejar `message.content` vacío. El fallback Master con `reasoning=off` funciona parcialmente, pero aún existen errores de parseo. Este bug se documenta y no se corrigió durante la migración.

## 18. Deliberadamente no implementado

No se agregó FastAPI, Flask, frontend, base de datos, Docker, colas, multi-PC, Wake-on-LAN, scheduler, daemon, RAG, búsqueda nueva, tuning, regeneración automática ni cambios del reviewer. Tampoco se hizo mass rename o limpieza de históricos.

## 19. Rollback exacto

1. Detener cualquier proceso iniciado desde Ada.
2. Configurar LM Studio/MCP para volver a usar los JSON/entrypoints del source original en C:.
3. Ejecutar el pipeline desde el source original, que no fue movido ni borrado.
4. No hay junction que desactivar ni output de ComfyUI que restaurar: `LunaKleinBatch` nunca se modificó.
5. Si Ada contiene datos nuevos que deban conservarse, copiarlos de forma selectiva a nombres nuevos bajo `prompts`, `config`, `character_dataset_staging`, `klein_batch_runs` o `visual_review_runs`; verificar antes y no sobrescribir históricos.
6. No copiar de vuelta `ada_paths.py` ni configs Ada salvo decisión explícita.

No se ejecutó rollback.

## 20. Próximo paso recomendado

Usar Ada como root operativo durante un ciclo pequeño real y confirmar que LM Studio/MCP se inicia desde sus nuevos entrypoints. Después, abordar por separado la fiabilidad JSON del Master. La junction de generated assets debe seguir siendo una tarea independiente con copia, hashes y backup físico previo.
