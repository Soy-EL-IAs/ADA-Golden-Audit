# ADA — Lustify primary with character-aware routing

> Current production baseline (2026-08-24): **Lustify Krea2 direct**. Create Images
> selects exactly one requested renderer; **Miaomiao Anima16** is the anime option.
> Since 2026-08-25, characters explicitly marked unreliable for Lustify direct use the
> validated **Miaomiao → Lustify latent Img2Img** fallback. The former
> Illustrious → Klein path is historical/specialized and remains readable for
> provenance; it is not the default for new missions. See
> `docs/decisions/RENDERER_BASELINE_20260824.md` and
> `docs/decisions/CHARACTER_AWARE_LUSTIFY_FALLBACK_20260825.md`.
>
> Recent changes and their reasons: `docs/CHANGELOG.md`.

## ADA 1.0 Alpha audit status

The current app starts with `START_ADA_APP.cmd` and serves the UI/API at
`http://127.0.0.1:8000`. It requires the separately managed LM Studio service at
`127.0.0.1:1234` and ComfyUI at `127.0.0.1:8188`; model files are not stored in
this repository.

The Alpha audit distinguishes two real production surfaces: the current app
renderer route (Lustify primary, conditional Lustify Img2Img, optional Miaomiao)
and the split specialist/headless route (Premise → Illustrious → review → Klein
→ final review). They are not yet one UI-driven pipeline. Therefore the exact
Golden E2E requested for the release is **not certified yet**, and the release
tag must not be created until that architecture decision and the remaining test
failures are resolved.

Current evidence and boundaries:

- `docs/releases/ADA_1.0_ALPHA_ARCHITECTURE.md`
- `docs/releases/ADA_1.0_ALPHA_CONFIG.md`
- `docs/releases/ADA_1.0_ALPHA_CERTIFICATION.md`
- `docs/releases/ADA_1.0_ALPHA_KNOWN_ISSUES.md`
- `docs/audit/PROJECT_INVENTORY.md`
- `docs/audit/FUNCTIONAL_CATALOG.md`
- `audit_evidence/README.md`

Runtime state is persisted under `data/` and the various run directories. A
queued request is not a running task, and an HTTP response is not proof of a
completed render. Historical and rejected assets are preserved for provenance;
the active Library view filters them rather than deleting their physical files.

# Illustrious -> Klein: paquete operativo histórico

Este es el paquete local para generar pares **Illustrious -> Klein** con un unico workflow reutilizable. Los personajes, prompts y seeds viven en JSONL; no se crea un workflow por personaje.

## Root ADA

La ubicación permanente de esta copia es `D:\IA\Ada`. `scripts/ada_paths.py` centraliza los roots y endpoints activos. La precedencia es variables de entorno, `config/ada.local.json` y defaults derivados del propio proyecto.

Overrides soportados: `ADA_ROOT`, `ADA_COMFYUI_ROOT`, `ADA_LMSTUDIO_URL` y `ADA_COMFYUI_URL`. ComfyUI y LM Studio siguen siendo dependencias externas; modelos, checkpoints y LoRAs no viven dentro de Ada. Los paths absolutos de manifests históricos no se reescriben y se resuelven mediante compatibilidad legacy cuando corresponde.

La estrategia y rollback completos están en `migration/MIGRATION_REPORT.md`; la dirección futura está en `docs/ADA_ARCHITECTURE.md`.

## Inicio rapido

1. Abrí **ComfyUI** y esperá a que termine de cargar sus modelos.
2. Abrí **LM Studio**, cargá tu modelo y activá su servidor local en `http://127.0.0.1:1234`.
3. En LM Studio, activá el MCP **Illustrious -> Klein Local** para el chat (ver `lmstudio_mcp_entry.json`). Alternativamente, ejecutá `START_LOCAL_OPERATOR.cmd`.
4. Pedile al operador: `Comprobá ComfyUI.` Debe devolver `idle: true`.
5. Para probar un dataset nuevo: `Ejecutá prompts/tifa_lockhart_ff7_remake_pilot_12.jsonl con batch id prueba_xxx.`
6. Revisá todas las comparaciones del piloto y sólo entonces ejecutá un dataset mayor ya aprobado.
7. Terminada la corrida: `Revisá el batch lote_xxx y construí la galería.` Abrí el `gallery.html` generado en un navegador normal.

Los IDs de batch deben ser nuevos y sólo pueden usar letras, números, `_` y `-`.

## Arquitectura actual

```text
prompts/klein_batch_*.jsonl
        |
        v
workflow reutilizable (Illustrious: identidad, ropa, pose, encuadre)
        |
        v
handoff/encode de la imagen de referencia
        |
        v
Klein (acabado realista; prompt breve, sin reconstruir al personaje)
        |
        v
ComfyUI output + manifest por batch + comparación
        |
        +--> review.json opcional, hecho por el modelo de visión de LM Studio
        +--> gallery.html para revisión humana
```

Cada línea del JSONL contiene una pareja indivisible: `id`, `character`, ambos prompts y ambos seeds. Illustrious fija identidad/composición; Klein debe preservarlas y mejorar el acabado.

### Convención para prompts futuros

Cuando un prompt indique composición, debe describir sólo el `viewpoint` y el `framing`, nunca el dispositivo físico. Usar `eye-level view`, `low-angle view`, `slightly elevated viewpoint` o `tight close-up framing`; evitar expresiones como `camera at eye level`, `low camera angle`, `camera above her`, así como menciones a `lens`, `photographer` o equipo de filmación. Esta regla no se aplica retroactivamente a datasets existentes.

El negative base de Illustrious incluye `camera, handheld camera, photography equipment, filming equipment, visible lens` para impedir que esos objetos aparezcan en la escena.

## Orquestación Master/Worker (opt-in, sin pruebas todavía)

Hay una capa local, separada del runner, para controlar de forma determinista los LLMs de LM Studio y la VRAM:

```text
MASTER Qwen3.8-27B-Uncensored (SMART)
        |  operación / DEEP_REVIEW
        v
unload_all -> confirmar VRAM libre -> ComfyUI idle
        v
Illustrious -> Klein (GENERATING; sin inferencia LLM)
        v
WORKER Qwen3-VL-8B (REVIEWING)
```

Por defecto está desactivada y no cambia batches actuales. Para activarla en el launcher/MCP agregá `PIPELINE_ORCHESTRATION=1`; revisá antes los identificadores de modelo en `config/orchestration.json`. El detalle operativo, estados y TODO de validación está en [docs/ORCHESTRATION.md](docs/ORCHESTRATION.md).

## Dónde está cada cosa

| Ruta | Uso |
|---|---|
| `workflows/production/illustrious_only_api.json` | Workflow de producción Illustrious aislado. |
| `workflows/production/klein_only_api.json` | Workflow de producción Klein aislado; recibe un artifact Illustrious explícito. |
| `workflows/legacy/illustrious_to_klein_batch_base_ui.json` | Evidencia histórica/debug; contiene ramas combinadas y no debe ejecutarse en producción. |
| `prompts/klein_batch_trial_3.jsonl` | Dataset fijo de prueba (3 registros). |
| `prompts/klein_batch_100.jsonl` | Dataset fijo completo (100 registros). |
| `scripts/run_klein_jsonl_batch.py` | Runner determinista: liga prompts/seeds al workflow, envía a ComfyUI y mantiene el manifest. |
| `scripts/lmstudio_operator.py` | Operador por consola y lógica cerrada de las tools. |
| `scripts/lmstudio_mcp_server.py` | Expone esas tools a LM Studio por MCP. |
| `scripts/lmstudio_controller.py` | Controlador de modelos/VRAM de LM Studio v1, sin acciones al importarlo. |
| `scripts/local_search.py` | Cliente opt-in de SearXNG; devuelve URLs/metadatos y no descarga imágenes. |
| `scripts/character_ref_cache.py` | Descarga conservadora de 2–5 referencias y escritura del manifest sin sobrescrituras ni retries. |
| `scripts/run_klein_ab_test.py` | Runner Klein-only para comparar LoRA reutilizando outputs Illustrious existentes. |
| `scripts/build_klein_gallery.py` | Generador de galería por consola. El operador también tiene `build_gallery`. |
| `klein_batch_runs/<batch_id>/manifest.json` | Fuente de verdad de una corrida: estado, prompt IDs y archivos generados. |
| `klein_batch_runs/<batch_id>/gallery.html` | Revisión visual en navegador. |
| `lmstudio_mcp_entry.json` | Entrada MCP mínima para importar/configurar en LM Studio. |
| `lmstudio_mcp_searxng.json` | Entrada MCP con búsqueda local gratuita activada y sin Brave. |
| `lmstudio_mcp_full.json` | Ejemplo ampliado; Brave permanece opcional y requiere su propia API key. |
| `config/pipeline.json` | Rutas y parámetros actuales de ComfyUI/modelos. No cambiar durante una corrida. |
| `config/klein_presets_*.json` | Planes opcionales por ID para pasos y cadena de LoRAs de Klein; preservan el formato JSONL estándar. |
| `config/orchestration.json` | Roles Master/Worker y configuración opt-in de la orquestación. |
| `config/search.json` | URL, límites y switches de búsqueda local. |
| `config/character_refs.json` | Dominios oficiales, exclusiones y reglas deterministas de ranking. |
| `character_refs/` | Cache reusable por personaje/versión, con `refs/` y `manifest.json`. |
| `klein_ab_tests/<test_id>/` | Salida autocontenida de tests Klein-only; fuentes copiadas, condiciones y manifest. |
| `experimental*`, `render_only_runs/`, `runs/` | Historial/experimentos anteriores, no son el camino operativo del batch actual. |

## Operador de LM Studio

La identidad base local puede venir de booru-characters: generate_character_dataset adjunta un character_profile crudo si encuentra un tag inequívoco y compatible con la versión. El Master lo usa como hechos visuales, sin pegar los tags mecánicamente a los prompts. La consulta de inspección es get_character_profile; detalles en docs/CHARACTER_PROFILES.md.

La creación reusable de datasets usa staging por chunks: generate_character_dataset prepara el plan; el Master primero recibe Viral + un extracto de MiniMax para las premises, luego pide las guías Illustrious/Klein al construir prompts, envía 5-10 entradas con append_character_dataset_entries y finalize_character_dataset valida el conjunto y recién entonces guarda JSONL + plan Klein, sin renderizar. Las versiones activas de guías viven en config/prompt_guides.json; los defaults del dataset, en config/character_dataset.json y la implementación en scripts/character_dataset.py.

El launcher `START_LOCAL_OPERATOR.cmd` usa el modelo configurado en el propio archivo (hoy `qwen/qwen3-vl-4b`) y abre un operador de consola. Para usar MCP dentro del chat, importá o copiá la entrada de `lmstudio_mcp_entry.json`, reiniciá/recargá MCP si LM Studio lo solicita y activá **Illustrious -> Klein Local** en el chat.

Tools disponibles:

| Tool | Qué hace |
|---|---|
| `comfy_status` | Lee la cola de ComfyUI; no genera. |
| `batch_status(batch_id)` | Lee el manifest y resume progreso/errores. |
| `run_batch(dataset, batch_id, klein_preset_plan?)` | Valida un JSONL dentro de `prompts/`, obtiene su cantidad real y ejecuta exactamente todos sus registros. El plan opcional dentro de `config/` asigna pasos/LoRAs por ID sin cambiar el JSONL. Espera localmente y no usa tokens mientras renderiza. |
| `review_batch(batch_id, limit)` | El modelo de visión revisa comparaciones completas y escribe `review.json`. |
| `build_gallery(batch_id)` | Crea/actualiza `gallery.html` sin tocar las imágenes. |
| `show_comparisons` | Intenta mostrar hasta 6 imágenes en LM Studio; puede fallar en versiones que no aceptan el tipo `Image`. Usá la galería como alternativa. |
| `orchestration_status`, `load_*`, `unload_*` | Inventario y control explícito Master/Worker; requieren LM Studio API v1. |
| `deep_review_batch` | Segunda opinión con Master; Worker -> unload -> VRAM libre -> Master cuando la orquestación está activa. |
| `search_web`, `search_images` | Consultan SearXNG y devuelven metadatos/URLs; no descargan ni renderizan imágenes. |
| `find_character_refs` | Hace hasta dos búsquedas y selecciona referencias mecánicamente, sin delegar el filtrado al LLM. |
| `cache_character_refs` | Reutiliza un cache válido o descarga 2–5 referencias una sola vez, sin sobrescribir ni reintentar. |

## Cómo correr sin MCP

El runner JSONL combinado anterior quedó deshabilitado al cuarentenarse su workflow. Para producción, usar la entrada canónica, que hace una submission Illustrious y, tras review, una submission Klein por item:

```powershell
python ada.py run 2B --count 1 --version "NieR:Automata"
```

Para construir una galería manualmente, usá los valores de `comfy_root` de `config/pipeline.json` y `output` de ejemplo:

```powershell
python scripts/build_klein_gallery.py --manifest klein_batch_runs/lote_nuevo_001/manifest.json --comfy-output 'D:\IA\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable\ComfyUI\output' --output klein_batch_runs/lote_nuevo_001/gallery.html
```

## Estado y revisión

- Estado rápido: `batch_status("<batch_id>")` o abrí `klein_batch_runs/<batch_id>/manifest.json`.
- Galería: `build_gallery("<batch_id>")` y abrí el archivo HTML desde Explorer/Chrome/Edge. LM Studio no abre bien enlaces `file:///` y su visualización de `Image` puede fallar.
- Revisión humana: comparar identidad, cabello, outfit/accesorios, pose, encuadre, anatomía y si Klein cambió algo que no debía.
- Revisión local opcional: `review_batch("<batch_id>", <cantidad>)`, usando la cantidad del manifest. El resultado es `review.json`; no sustituye la curaduría humana.

## Seguridad: qué no sobrescribir ni tocar

- **Nunca reutilices un `batch_id`.** El operador lo bloquea; el runner directo crea el manifest con ese nombre y por eso debe recibir un ID nuevo.
- No modifiques `manifest.json`, prompts, seeds, workflow, modelo, LoRA, VAE, sampler, guidance o conexiones mientras un batch esté activo.
- No reintentes automáticamente un registro fallido: conservá el manifest/error y creá una corrida nueva sólo cuando decidas qué cambió.
- No confundas `production100_reusable_v1`: es histórico y está **fallido**, con 60 completos y 1 fallido (`blue_mary_001`). Está congelado para diagnóstico.
- `prueba_local_001` y `trial3_reusable_v1` son pruebas completas históricas; no se reutilizan como destino.
- No borres ni edites `experimental_runs/`, `render_only_runs/` o `runs/` si querés conservar trazabilidad de las pruebas anteriores.

## Próximas mejoras (no implementadas)

Nada de esta lista forma parte todavía del operador actual:

- **Qwen3.8** como operador/reviewer más fuerte y benchmark frente a los modelos actuales.
- **Reviewer visual estructurado**: score por identidad, outfit, pose, composición, anatomía y calidad; hoy sólo existe la revisión básica a `review.json`.
- **Piloto del cache de referencias**: ejecutar y revisar Tifa Lockhart / Final Fantasy VII Remake antes de usarlo en producción. Brave queda como alternativa opcional.
- **Banco de referencias para video**: separar vistas de identidad (frontal, perfil, espalda, etc.) de primeros frames cinematográficos para I2V/Ref2V.
- **Benchmark del worker 8B**: comparar calidad, tiempos y umbrales frente al Master 27B. La orquestación ya está implementada, pero no fue ejecutada/validada aún.
- Persistencia/analítica de reviews y comparación de experimentos.

## Lectura corta por tarea

- [Perfiles locales de personajes](docs/CHARACTER_PROFILES.md)

- [Crear datasets con el Master](docs/CHARACTER_DATASETS.md)

- [Operar un batch](docs/OPERATION.md)
- [Revisar resultados](docs/REVIEW.md)
- [Resolver problemas frecuentes](docs/TROUBLESHOOTING.md)
- [Operar Master/Worker y VRAM](docs/ORCHESTRATION.md)
- [Configurar búsqueda local SearXNG](docs/LOCAL_SEARCH.md)
