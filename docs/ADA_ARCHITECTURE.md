# ADA — arquitectura actual

## Current production renderer baseline

New missions resolve `Character Contract + Concept Proposal` to a `Resolved Render
Spec`, then run the single renderer selected by the user. **Lustify Krea2** is the
general default and Miaomiao Anima16 is the explicit anime route. For a character whose
registry marks Lustify direct as unreliable, ADA first creates and validates a
same-concept Miaomiao identity source, then runs the verified Lustify latent Img2Img
recipe. Each output owns an
independent plan, prompt, receipt and review; selection is renderer-generic and human
overrides remain authoritative. `Illustrious → Klein` below documents historical and
specialized compatibility behavior, not the default pipeline.

Current semantic detail: new work emits Hook Premise v2 and Resolved Render Spec v2,
with an explicit render intent and a renderer-specific compiler. See
`docs/architecture/HOOK_PREMISE_V2_AND_RENDER_INTENT.md` and
`docs/features/REINTERPRET_WITH_CHARACTER_V1.md`. Decision history is indexed in
`docs/CHANGELOG.md`.

# ADA — arquitectura futura

ADA es la capa de orquestación del sistema. No es un modelo, ComfyUI, el Master ni el Worker. La base v1 sigue siendo ejecutable de forma headless y conserva el pipeline actual sin introducir servicios nuevos.

```text
                      ADA UI
                         |
                      Ada API
                         |
                   Orchestrator
                         |
              Job / Run state layer
                         |
          +--------------+--------------+
          |              |              |
        Master         ComfyUI        Worker
          |                              |
          +---------- future nodes ------+
```

La UI futura será una vista y control del sistema, no el lugar donde viva la lógica. El flujo será `UI → Ada API → Orchestrator → Jobs/Runs → execution nodes`. El mismo núcleo deberá funcionar sin UI.

## Concepto futuro de Run

Un Run será la unidad central de trazabilidad y podrá reunir:

- `run_id`
- `created_at`
- `status`
- `pipeline`
- `character`
- `inputs`
- `outputs`
- `artifacts`
- `reviews`
- `timings`
- `errors`

Los manifests actuales no se migran a un schema nuevo en ADA v1. Esta lista es dirección arquitectónica, no una implementación ni un contrato definitivo.

## Evolución posible

La arquitectura puede incorporar más adelante un editor visual de workflows, biblioteca de personajes, galería, cola de revisión, historial de runs, scheduler y nodos distribuidos con capacidades declaradas. Los nodos previstos conceptualmente incluyen la RTX 5070 Ti principal, una RTX 3070 Ti secundaria y un mini-servidor coordinador 24/7. También pueden aparecer Wake-on-LAN, MiniMax y un asistente futuro.

Nada de lo anterior está implementado en esta migración. ADA v1 no agrega API web, frontend, base de datos, cola distribuida, daemon ni multi-PC.

## Especialistas por contrato (base implementada)

ADA puede reutilizar un mismo modelo de LM Studio con contextos frescos y responsabilidades separadas:

```text
Master / Orchestrator
  -> Premise Agent -> PremiseSpec
  -> Illustrious Agent -> IllustriousResult
  -> render Illustrious
  -> VisualReview
  -> Klein Agent -> KleinResult
  -> render Klein
  -> VisualReview final
  -> MiniMax Agent opcional -> MiniMaxResult
```

Los contratos viven en `schemas/`. `scripts/agent_contracts.py` los aplica localmente y construye el `response_format` estricto para LM Studio. `scripts/specialist_agents.py` define los cuatro contextos aislados; no crea cuatro modelos residentes. `scripts/specialist_orchestrator.py` mantiene las fronteras y `scripts/ada_run_state.py` persiste etapa, seeds y artefactos.

Los seeds pertenecen al runtime y no al contenido generado por el LLM.

El workflow combinado histórico sigue disponible. `scripts/split_klein_pipeline.py` permite compilarlo en dos grafos: Illustrious primero y Klein después, cargando como archivo la imagen Illustrious ya revisada. Esta separación es opt-in mientras se completa la integración operativa.

MiniMax permanece fuera del camino de creación de imágenes y sólo puede compilarse después de una imagen final aprobada.

### Visual Review como frontera dura

La política por defecto es `review_policy="strict"`:

```text
ILLUSTRIOUS_RENDERED
  -> review válido -> ILLUSTRIOUS_REVIEWED -> Klein permitido
  -> review vacío/inválido -> conservar ILLUSTRIOUS_RENDERED + error recuperable -> detener
```

Un retry o reinicio vuelve a ejecutar solamente Visual Review. No recrea la premise, el prompt ni la imagen Illustrious. Los transportes controlados guardan respuestas crudas cuando reciben un directorio de diagnóstico. El camino hacia Klein permanece bloqueado hasta que exista un `VisualReview` válido.

`review_policy="best_effort"` queda reservado como opción explícita del run; no habilita todavía ningún bypass silencioso.

## Principios preservados

### Creative intent and compact production contracts

New Create requests persist a `CreativeIntentEnvelope`. Its precedence is
`USER LOCKED INTENT > CHARACTER CONTRACT IMMUTABLES > SELECTED CREATIVE CONCEPT > RENDERER PREFERENCES`.
M1 produces compact sketches, M3/M4 select them, and only selected sketches expand into a
`ResolvedRenderSpec v3`. The deterministic linter runs before the renderer; a locked visible
setting requires environmental anchors. Visual Review v3 evaluates only expected visibility,
returns compact subscores and defects, and ADA—not the model—calculates the aggregate rating.
Older v1/v2 artifacts remain readable without fabricated ratings.

- Master, Worker y ComfyUI no compiten por VRAM.
- ComfyUI y LM Studio continúan siendo dependencias externas configurables.
- Datasets, manifests y resultados históricos permanecen legibles e inmutables.
- La ubicación del proyecto se resuelve mediante `scripts/ada_paths.py`.
- Los endpoints y roots externos aceptan overrides por entorno o configuración local.
- Las rutas históricas del antiguo proyecto se resuelven por compatibilidad, sin reescribir provenance.
