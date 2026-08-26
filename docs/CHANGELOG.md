# ADA Change Log

Este archivo responde qué cambió recientemente y por qué. Las decisiones de arquitectura
conservan su explicación extensa en `docs/decisions/`; los receipts de cada ejecución
siguen siendo la evidencia de cómo se produjo una imagen; `config/roadmap.json` contiene
el trabajo futuro. No se reescriben artefactos históricos.

## 2026-08-25

### Characters catalog and identity routing

- Se agregó una sección Characters con referencia, nombre, franquicia, cantidad de imágenes,
  canonical prompt/tags y estado de compatibilidad por personaje.
- Los estados son evidence-backed: verde usa Lustify directo; amarillo usa
  Miaomiao → Lustify Img2Img; rojo bloquea porque ambos modelos fallaron; gris significa que
  todavía no existe evaluación suficiente.
- La selección explícita de Miaomiao continúa ejecutando sólo Miaomiao. Una solicitud Lustify
  para un personaje amarillo nunca envía Lustify directo.
- Yoruichi quedó verde mediante su evaluación humana de Model Lab; Ghislaine permanece
  amarilla. No se inventaron estados para los personajes todavía no evaluados.
- Diseño y política: `docs/features/CHARACTERS_CATALOG_V1.md`.

### Fallback de identidad Miaomiao → Lustify Img2Img

- Se promovió la Recipe B validada en Model Lab a preset condicional
  `lustify_krea2_img2img_v1`.
- Motivo: Lustify directo produce buena calidad general pero no reconoce de forma fiable
  a Ghislaine Dedoldia; Miaomiao sí conserva su identidad.
- Para un personaje marcado `Lustify.direct = unreliable`, una solicitud explícita a
  Lustify genera primero una referencia Miaomiao del mismo concepto. Sólo si esa imagen
  supera el control de identidad, Lustify usa su latent real mediante VAE Img2Img con
  `denoise 0.55`.
- La imagen Miaomiao intermedia conserva lineage como `identity_reference` y no se publica
  como resultado final de Library. El receipt final identifica `lustify_img2img`, su fuente,
  preset y modo `LATENT_IMG2IMG`.
- Las Recipes A y C permanecen en Model Lab: A produjo artefactos severos y C conservó
  demasiado el aspecto anime.
- Evidencia: `experimental_runs/model_lab/lustify_identity_reference_ghislaine_001/`.
- Decisión: `docs/decisions/CHARACTER_AWARE_LUSTIFY_FALLBACK_20260825.md`.

### Selección de renderer y control de identidad

- Create Images elige Lustify o Miaomiao de forma excluyente; ya no genera ambos por un
  checkbox ambiguo. Al elegir Miaomiao, el Look queda fijado en Anime.
- Se agregó compatibilidad personaje/renderer. Ghislaine figura como confirmada para
  Miaomiao directo y no fiable para Lustify directo; no se generalizó ese juicio a otros
  personajes sin evidencia.
- Visual Review endureció la identidad como condición de aceptación. Una imagen visualmente
  buena que no representa al personaje no puede recibir una aprobación perfecta ni avanzar
  silenciosamente.

### Fiabilidad de contratos y transporte LM Studio

- Se endureció el contrato M1 → M2 para aceptar únicamente el objeto `concepts`, extraer JSON
  rodeado de texto, normalizar controles y conservar la respuesta cruda cuando no puede
  recuperarse.
- Visual Review valida verdict/schema y conserva diagnósticos en fallos duros en lugar de
  aceptar contenido vacío o inválido.
- Se mantiene el handoff de VRAM entre ComfyUI y LM Studio antes de cambiar de etapa.

### Library y experiencia de producto

- Se agregó selección múltiple en las galerías de imágenes: modo Select, indicador visual,
  contador, papelera y una única confirmación. Remove cambia las imágenes a `REJECTED` de
  forma atómica; conserva archivos, receipts y lineage para poder restaurarlas.
- Los resultados combinados Miaomiao → Lustify/Krea muestran Compare con la referencia de
  identidad Miaomiao y el resultado final, aunque la referencia intermedia siga excluida de
  la galería normal.
- Recent Assets pasó a ordenar imágenes individuales por creación, no un único resultado por
  personaje.
- Se añadió filtro visible de Collection en Library para que una navegación desde Home pueda
  quitarse sin quedar bloqueada.
- Character Cards usan recorte centrado en el rostro; Active Missions es colapsable.
- Favorite, Set as hero y Compare persisten o abren un flujo utilizable. Generate Alternative
  conserva el asset fuente. Reinterpret inicia la infraestructura existente; queda pendiente
  reemplazar su compilación basada en tags por un agente semántico.
- Library distingue imágenes de un mismo generation y conserva lineage por renderer. Los
  outputs intermedios de identidad y Model Lab no se promueven automáticamente.
- El botón "Select images" se alineó a la derecha y se ocultó en la vista de Rejected, tanto en Library general como en Character Workspace.

### Registro operativo

- Se creó este changelog y se enlazó desde los README.
- Se actualizó Roadmap para separar capacidades terminadas, integración parcial y deuda futura.

## 2026-08-24

### Onboarding de personajes y Missions

- ADA App recuperó el alta explícita de personajes usando el pipeline existente:
  profile booru → SearXNG local → cache → manifest → `config/characters.json`.
- El registro sólo ocurre con profile y manifest utilizables; no se escanea
  `character_refs/` para registrar evidencia histórica.
- Create Images carga el selector desde `/api/characters`. Se eliminaron las opciones
  hardcodeadas y el personaje recién agregado queda seleccionado.
- La barra de comandos bloquea personajes desconocidos con `character_not_registered`.
- Se corrigió la versión del personaje usando la fuente registrada y se eliminó el fallback
  silencioso a 2B.
- Delete Mission permite borrar estados terminales, bloquea Missions activas y no elimina
  referencias compartidas ni assets publicados de Library.

### Contratos semánticos y ejecución

- Se introdujeron Character Contract, Resolved Render Spec, Stage Render Plan, Prompt Artifact,
  Render Receipt, Review Observation y Routing Decision como artefactos versionados.
- M1 conserva intención creativa; cada renderer compila su propio prompt desde el spec.
- `AdaRunState.create()` dejó de confundir un directorio de candidate ya creado con un run
  existente: la exclusión depende de `ada_run.json`.
- Los fallos determinísticos de setup/contract no consumen retries de render y conservan tipo,
  mensaje, traceback, etapa, intento y candidate.

### Baseline de render y Model Lab

- El benchmark controlado promovió Lustify Krea2 directo como renderer general de producción y
  mantuvo Miaomiao Anima16 como ruta anime explícita.
- Illustrious, Klein y Anima quedaron fuera del camino normal sin perder lectura histórica.
- Model Lab recibió contratos de casos, receipts reproducibles, evaluación por capacidades y
  galería comparativa, aislados de Missions y workflows productivos.
- El baseline Klein semi-realistic quedó documentado como capacidad histórica especializada.

### Library basada en imágenes

- Library pasó de representar sólo candidates seleccionados a representar cada output de
  renderer como Library Image individual, unido al mismo generation/lineage.
- Los outputs experimentales permanecen fuera hasta una futura acción explícita Promote to
  Library.

### Added
- Feature: Hard Re-Evaluator v0.1
  - New explicit POST endpoint /api/library/hard-reevaluate to trigger hard reviews for selected images.
  - New vision evaluation logic measuring 'viral hook', heavily focused on female form and erotic context rather than generic art quality.
  - New vision contract hard_visual_review_v1 defining scoring rules (20% basic, 55% primary hook, 25% contextual hook).
  - New UI: 'Hard Re-Evaluate' button in the Library's multi-select actions.
  - New UI: Score label 'Score 91 · Hard ✓' directly on asset cards.
  - New UI: Detailed modal display for Hard Ratings including subscores and textual reasons without replacing the standard agent rating.
  - New UI: Added Gallery Statistics panel for 'Hard Reviewed' items, showing count, averages, and distribution inside the Library.


- Added Hard Re-Evaluator directly inside the asset details modal.
  - Shows 'Hard Re-Evaluate' or 'Re-Evaluate Again' button right beneath Agent Rating.
  - Executes evaluation for the single asset seamlessly without page reload.
  - Explicitly requested \primary_hook_targets\ and \context_hook_types\ from the Vision worker and displays them cleanly in the modal.
  - Ensured Vision worker does not receive \gent_rating\, \original_score\ or \delta\ in its prompt, maintaining an independent audit.


- Feature: Dataset / Auto Concepts mode added to Create Images.
  - Adds a toggle in the Scene tab to switch between 'Directed Scene' and 'Dataset / Auto Concepts'.
  - In Dataset mode, specific scene details (What happens? / Where?) are hidden and ignored.
  - Allows selection of one, multiple, or 'ALL' registered characters.
  - Dynamically changes 'Number of images' label to 'Images per character'.
  - Automatically handles multiplying missions natively through ADA's productive pipeline without ad-hoc scripts.
  - Displays a confirmation summary (Characters, Images per character, Target final images) before executing batch creation.

