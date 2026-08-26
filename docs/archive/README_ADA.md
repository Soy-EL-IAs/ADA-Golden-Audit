# ADA — mapa sencillo del sistema

## Baseline actual de render

Las Missions nuevas usan `lustify_krea2_primary_v1` como renderer principal. La UI
elige un único renderer y puede pedir explícitamente `miaomiao_anima16_secondary_v1`
como ruta anime. Si el Character Capability marca Lustify directo como no fiable, ADA
usa la ruta validada Miaomiao → Lustify latent Img2Img. Illustrious, Klein y Anima se preservan como historia
y Model Lab, pero ya no son opciones normales de Create Images. La selección y los
valores congelados viven en `config/pipeline.json`; la decisión está documentada en
`docs/decisions/RENDERER_BASELINE_20260824.md` y
`docs/decisions/CHARACTER_AWARE_LUSTIFY_FALLBACK_20260825.md`.

El resumen cronológico de cambios y motivos vive en `docs/CHANGELOG.md`.

Este documento explica qué es ADA, dónde está cada componente y cómo debería funcionar cuando esté terminada.

## La idea central

ADA es el programa que coordina todo. No es un modelo de lenguaje ni un modelo de imágenes.

Su trabajo es recibir una intención del usuario y administrar, en el orden correcto:

1. el Master de LM Studio;
2. los archivos del proyecto;
3. la memoria de la corrida;
4. la VRAM;
5. ComfyUI;
6. la revisión visual;
7. el resultado final.

El objetivo operativo es que el usuario pueda iniciar ADA y pedir:

> Creá una corrida completa de 2B con la guía v2, hacé un piloto, generá las imágenes, revisalas y mostrame el informe.

ADA debería completar el flujo sin necesitar Codex ni intervención manual entre etapas.

## Dos caminos que conviven

### Legacy / compatibility path

Este camino se conserva para reproducir batches históricos:

```text
Master
  -> escribe Illustrious + Klein antes del render
  -> ADA asigna el dataset al runner combinado
  -> ComfyUI genera Illustrious -> Klein en un solo workflow
```

El código principal de compatibilidad es `scripts/run_klein_jsonl_batch.py`. No es la arquitectura objetivo para nuevas corridas especializadas.

### New specialist path

Este es el camino nuevo y recomendado:

```text
Premise Agent
  -> contrato PremiseSpec
Illustrious Agent
  -> contrato IllustriousResult
Illustrious render
Visual Review obligatorio
Klein Agent
  -> contrato KleinResult basado en la imagen y review reales
Klein render
Final Review
MiniMax Agent opcional, sólo para video
```

Los especialistas pueden reutilizar el mismo Qwen. Cada llamada usa contexto fresco y solamente la guía de su etapa. ADA, no el LLM, asigna las seeds.

## Roles

### ADA — orquestador

ADA decide qué componente debe trabajar, valida sus resultados y mantiene el estado de la corrida.

ADA debe realizar de forma determinista las tareas que no necesitan creatividad:

- crear carpetas e identificadores nuevos;
- validar JSONL;
- comprobar que ComfyUI esté libre;
- cargar y descargar modelos;
- liberar VRAM;
- enviar workflows a ComfyUI;
- esperar resultados;
- construir galerías;
- guardar manifests y reportes;
- detenerse ante errores sin sobrescribir resultados.

### Master — orquestador y decisor

Modelo configurado actualmente:

`qwen3.8-27b-uncensored`

En el camino nuevo, el Master se ocupa de:

- interpretar la petición;
- decidir qué especialista debe ejecutarse;
- entregar a cada especialista solamente su contexto;
- interpretar revisiones y estados persistidos;
- detener, reanudar o aprobar una corrida;
- evaluar riesgos narrativos y visuales;
- tomar la decisión final después de la revisión.

Premise Agent, Illustrious Agent, Klein Agent y MiniMax Agent realizan el contenido especializado. Las seeds, schemas, rutas y transiciones pertenecen a ADA.

Su system prompt principal está en:

`scripts/lmstudio_operator.py`

Las tareas experimentales pueden añadir instrucciones específicas sin modificar permanentemente ese system prompt.

### ComfyUI — generador de imágenes

ComfyUI produce los píxeles. No toma decisiones narrativas.

Recibe de ADA:

- el workflow;
- el prompt Illustrious;
- el prompt Klein;
- las seeds;
- los parámetros validados;
- la ruta de salida.

Los workflows de producción son dos grafos API independientes:

- `workflows/production/illustrious_only_api.json`
- `workflows/production/klein_only_api.json`

El antiguo grafo combinado está en `workflows/legacy/` sólo como evidencia/debug y no es seleccionable por el runtime de producción.

### Worker visual — inspector

Modelo configurado actualmente:

`qwen/qwen3-vl-8b`

El Worker no genera imágenes. Inspecciona resultados y puntúa aspectos como:

- identidad;
- anatomía;
- sujeto único;
- atractivo visual;
- hook viral;
- potencial de animación;
- diferencias entre Illustrious y Klein.

Su contrato de revisión está implementado en:

`scripts/visual_reviewer.py`

El Master también puede hacer una revisión visual profunda cuando se necesita una decisión más fuerte.

## Flujo nuevo

```text
Usuario inicia ADA
        |
        v
ADA crea una corrida nueva y carga su estado
        |
        v
Premise Agent crea o estructura la premise
        |
        v
ADA valida PremiseSpec y asigna seeds
        |
        v
Illustrious Agent crea únicamente el prompt Illustrious
        |
        v
ADA descarga los LLMs y confirma VRAM libre
        |
        v
ComfyUI genera únicamente Illustrious
        |
        v
Visual Review comprueba la imagen Illustrious
        |
        v
Klein Agent recibe premise + imagen/review reales y crea su prompt
        |
        v
ComfyUI refina la imagen con Klein
        |
        v
Final Review y decisión del Master
        |
        v
ADA guarda manifest, informe y galería
```

Visual Review es una frontera dura por defecto. Si devuelve vacío, JSON inválido o falla el transporte, ADA conserva `ILLUSTRIOUS_RENDERED`, registra `review_failed` y se detiene. Al reanudar, vuelve a intentar la revisión sin regenerar la premise ni Illustrious.

Las etapas persistentes del camino especialista son:

```text
CREATED
  -> PREMISES_READY
  -> ILLUSTRIOUS_PROMPTS_READY
  -> ILLUSTRIOUS_RENDERED
  -> ILLUSTRIOUS_REVIEWED
  -> KLEIN_PROMPTS_READY
  -> KLEIN_RENDERED
  -> FINAL_REVIEWED
  -> COMPLETE
```

Un fallo recuperable de revisión no avanza ni reinicia esta secuencia: conserva la última etapa completada y adjunta el error y los diagnósticos al `ada_run.json`.

## Estados de ADA

Los estados operativos existentes son:

| Estado | Significado |
|---|---|
| `IDLE_CHAT` | ADA espera una orden. |
| `PREPARING_BATCH` | Valida archivos, modelos, cola y VRAM. |
| `GENERATING` | ComfyUI está renderizando. No debe ejecutarse otro LLM en la misma VRAM. |
| `REVIEWING` | El Worker visual está revisando. |
| `DEEP_REVIEW` | El Master realiza una revisión profunda. |
| `WAITING` | Hay una condición que requiere espera o intervención. |

Los estados de recursos de `scripts/lmstudio_controller.py` siguen viviendo en memoria. Las etapas y artefactos del camino especialista ya se persisten en `ada_run.json` mediante `scripts/ada_run_state.py`, lo que permite retomar desde la última frontera completada.

## Dónde está cada cosa

### Entrada y configuración

| Ruta | Contenido |
|---|---|
| `START_LOCAL_OPERATOR.cmd` | Inicio actual del operador local. |
| `lmstudio_mcp_entry.json` | Conexión MCP mínima para LM Studio. |
| `config/ada.local.json` | Ubicaciones locales de ComfyUI y LM Studio. |
| `config/orchestration.json` | Modelos Master/Worker y control de VRAM. |
| `config/pipeline.json` | Modelos y parámetros del pipeline de imágenes. |
| `config/prompt_guides.json` | Versiones de guías consideradas activas. |

### Guías

| Ruta | Función |
|---|---|
| `config/prompt_guides/` | Guías versionadas para premisas, Illustrious, Klein y video. |
| `config/prompt_guides/illustrious_prompt_guide_v1.md` | Traduce intención narrativa a información visible. |
| `config/prompt_guides/klein_prompt_guide_v1.md` | Preserva la imagen y mejora su acabado. |

Una guía de premisas define **qué sucede**. La guía Illustrious define **qué debe verse**. La guía Klein define **qué debe preservarse y mejorarse**.

### Datos intermedios

| Ruta | Contenido |
|---|---|
| `premises/` | Premisas generadas en pruebas. |
| `evolution_runs/` | Ciclos de evolución, validaciones dirigidas y evidencia. |
| `character_dataset_staging/` | Dataset incompleto mientras el Master trabaja por bloques. |
| `prompts/` | Datasets JSONL finalizados y aptos para render. |
| `character_refs/` | Referencias locales conservadas por personaje y versión. |

### Render y resultados

| Ruta | Contenido |
|---|---|
| `workflows/` | Workflows reutilizables de ComfyUI. |
| `klein_batch_runs/<batch_id>/manifest.json` | Fuente de verdad del render. |
| `klein_batch_runs/<batch_id>/gallery.html` | Galería visual del batch. |
| `klein_batch_runs/<batch_id>/` | Estado y descriptores de cada imagen. |
| `ComfyUI/output/LunaKleinBatch/` | Archivos de imagen producidos por ComfyUI. |

### Código principal

| Ruta | Función |
|---|---|
| `scripts/lmstudio_operator.py` | Agente conversacional local y herramientas del Master. |
| `scripts/lmstudio_mcp_server.py` | Expone las herramientas dentro de LM Studio. |
| `scripts/lmstudio_controller.py` | Carga/descarga modelos y administra estados/VRAM. |
| `scripts/character_dataset.py` | Staging, validación y finalización de datasets. |
| `scripts/run_klein_jsonl_batch.py` | Ejecuta un dataset completo en ComfyUI. |
| `scripts/visual_reviewer.py` | Revisión visual estructurada. |
| `scripts/build_klein_gallery.py` | Construye la galería local. |

## Qué persiste y qué se pierde

### Ya persiste

- premisas;
- guías candidatas;
- datasets;
- seeds;
- staging;
- imágenes;
- manifests;
- revisiones;
- galerías;
- errores de render;
- evidencia de ciclos experimentales.

### Todavía no persiste de forma suficiente

- la conversación completa del Master al reiniciar;
- el estado operativo exacto del controlador después de cerrar ADA;
- una cola general de trabajos pendientes;
- decisiones finales del Master como memoria reutilizable entre proyectos;
- recuperación automática de una corrida interrumpida.

## Cómo se inicia hoy

El inicio actual es:

1. abrir ComfyUI;
2. abrir LM Studio y activar su servidor local;
3. ejecutar `START_LOCAL_OPERATOR.cmd` o activar el MCP de ADA en LM Studio;
4. dar órdenes al operador.

Este mecanismo funciona como base técnica, pero todavía exige conocer demasiado del pipeline y a veces separar manualmente creación, render y revisión.

## Cómo debe iniciarse después de la próxima etapa

La experiencia objetivo es:

1. abrir ComfyUI y LM Studio;
2. ejecutar un único inicio de ADA;
3. escribir una petición normal;
4. esperar el informe y la galería.

ADA debería ofrecer una orden integral equivalente a:

```text
run_full_pipeline(
  character,
  version,
  guide,
  count,
  run_id,
  review_mode
)
```

Internamente esa orden debe crear un plan persistente y avanzar sola por todas las etapas, sin pedir al usuario que conozca scripts, JSONL, batch IDs o administración de VRAM.

## Próximo paso recomendado

Convertir la validación integral actual en una función productiva y reutilizable de ADA.

La siguiente etapa debe incluir:

1. una orden única `run_full_pipeline`;
2. estado persistente por corrida;
3. selección explícita y registrada de guías;
4. staging y validación automáticos;
5. piloto automático antes de una corrida grande;
6. descarga y carga segura de modelos;
7. render en ComfyUI;
8. revisión visual automática;
9. decisión final del Master;
10. galería e informe entregados al usuario;
11. reanudación segura después de cerrar o interrumpir ADA;
12. un launcher sencillo que compruebe dependencias y explique cualquier problema en lenguaje claro.

La prueba `render_validation_001/master_full_run_001` es una validación aislada de este futuro flujo. No debe confundirse todavía con el modo productivo definitivo.

## Base de especialistas disponible

La separación interna ya tiene una primera implementación compatible:

| Ruta | Función |
|---|---|
| `schemas/*_v1.schema.json` | Contratos versionados entre etapas. |
| `scripts/agent_contracts.py` | Validación estructural y structured output. |
| `scripts/specialist_agents.py` | Contextos frescos de Premise, Illustrious, Klein y MiniMax. |
| `scripts/specialist_orchestrator.py` | Orden y fronteras entre especialistas. |
| `scripts/ada_run_state.py` | Estado persistente, artefactos y seeds del runtime. |
| `scripts/specialist_visual_reviewer.py` | Revisión específica entre Illustrious y Klein. |
| `scripts/split_klein_pipeline.py` | Pausa real entre los dos renders del workflow. |

El runner combinado anterior se conserva para compatibilidad. La siguiente integración operativa debe exponer esta base mediante una sola orden de ADA y un launcher sencillo.

## Regla de seguridad fundamental

ADA nunca debe sobrescribir una corrida existente ni reintentar silenciosamente un render fallido.

Cada corrida necesita:

- un identificador nuevo;
- entradas congeladas;
- modelo y versiones de guías registrados;
- seeds conservadas;
- manifest propio;
- estado final verificable.

Así, cualquier resultado puede reproducirse, compararse o diagnosticarse sin perder evidencia.
