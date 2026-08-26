# Operador local (LM Studio)

La guía completa está en [README.md](README.md). Este archivo sólo resume cómo iniciar el operador.

1. Abrí LM Studio, cargá el modelo configurado y activá el servidor local en el puerto `1234`.
2. Ejecutá `START_LOCAL_OPERATOR.cmd` desde esta carpeta.
3. Escribí órdenes en español; usá `salir` para cerrar.

Para usar las mismas tools dentro del chat de LM Studio, configurá `lmstudio_mcp_entry.json` y activá **Illustrious -> Klein Local** para ese chat.

Ejemplos seguros, siempre con un ID inexistente:

```text
Comprobá ComfyUI. Ejecutá prompts/tifa_lockhart_ff7_remake_pilot_12.jsonl con batch id prueba_nueva_001.
```

```text
Comprobá ComfyUI y ejecutá prompts/klein_batch_100.jsonl con batch id lote_nuevo_001. Al finalizar, construí la galería.
```

El operador acepta cualquier JSONL válido dentro de `prompts/`, obtiene su cantidad real y ejecuta todos sus registros. Espera localmente mientras ComfyUI renderiza, no sobrescribe batches existentes y no reintenta fallos automáticamente.

## Master/Worker (opt-in)

Para habilitar el preflight determinista de VRAM, agregá `PIPELINE_ORCHESTRATION=1` al entorno del launcher o de la entrada MCP. Antes de `run_batch`, descarga los LLMs, espera que LM Studio confirme que no quedan cargados y exige ComfyUI idle. Consultá [docs/ORCHESTRATION.md](docs/ORCHESTRATION.md) antes del primer uso: esta integración no fue probada todavía.
