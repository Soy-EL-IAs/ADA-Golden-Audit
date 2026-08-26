# Operación segura

1. Abrí ComfyUI y LM Studio. Confirmá con `comfy_status` que ComfyUI está libre.
2. Elegí un ID nuevo, por ejemplo `prueba_prompt_v2_001`; nunca reutilices uno existente.
3. Corré `run_batch("tifa_lockhart_ff7_remake_pilot_12.jsonl", "prueba_tifa_remake_001")`.
4. Mirá la galería del piloto y decidí manualmente si todos los resultados sirven.
5. Sólo si pasa, ejecutá el JSONL mayor aprobado con un batch ID nuevo.
6. Consultá `batch_status` al terminar, generá la galería y revisá los resultados.

El operador restringe el dataset a `prompts/`, valida completamente sus registros y workflow, obtiene la cantidad real y bloquea cualquier directorio de batch existente antes de tocar la VRAM. Después comprueba que ComfyUI esté libre. Si hay un fallo, preservá el `manifest.json`; no reintentes de forma automática.
