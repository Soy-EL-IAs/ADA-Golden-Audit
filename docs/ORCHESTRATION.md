# Orquestación Master/Worker y VRAM

Esta capa es **opt-in**. No modifica batches, manifests, workflows ni corridas existentes. Se activa únicamente al iniciar el operador o MCP con `PIPELINE_ORCHESTRATION=1`.

## Roles configurados

| Rol | Modelo configurado | Uso |
|---|---|---|
| MASTER / SMART | `Qwen3.8-27B-Uncensored` | Operación, decisiones y segunda opinión profunda. |
| VISION WORKER | `Qwen3-VL-8B` | Revisión visual estructurada de resultados. |

La clave del modelo debe coincidir exactamente con la que muestra LM Studio. Si su instalación usa otro identificador, se cambia sólo `config/orchestration.json`; no hace falta tocar scripts.

Configuración recomendada actual del Master: contexto `8192`, reasoning budget `512` para operación normal y MTP activado. El archivo registra esos valores de intención; el endpoint nativo de carga sólo recibe los parámetros oficialmente expuestos por LM Studio (por ahora, contexto). MTP y reasoning budget deben confirmarse/configurarse en el preset o interfaz de LM Studio antes de usarlo.

El worker 8B queda **pendiente de benchmark**: no se asume todavía latencia, calidad ni umbrales de aprobación.

## Máquina de estados

```text
IDLE_CHAT
  -> PREPARING_BATCH -> GENERATING -> IDLE_CHAT
  -> REVIEWING -> IDLE_CHAT
  -> DEEP_REVIEW -> IDLE_CHAT
  -> WAITING (si falla un preflight o hay espera no resuelta)
```

`run_batch` con orquestación activa hace obligatoriamente:

1. Resuelve el JSONL dentro de `prompts/`, valida todas sus entradas contra el workflow, obtiene la cantidad real y comprueba que el directorio del batch no exista. Todo esto ocurre antes de tocar modelos o consultar ComfyUI.
2. `PREPARING_BATCH`: descarga todos los LLMs mediante la API v1 de LM Studio.
3. Espera y consulta hasta que LM Studio no reporte modelos cargados.
4. Consulta la cola de ComfyUI y exige `idle: true`.
5. Sólo entonces pasa a `GENERATING` y llama al runner existente con la cantidad validada.
6. Mientras el runner espera o genera no se ejecuta inferencia LLM desde el operador/MCP.
7. Cuando el runner termina, sale de `GENERATING`, restaura el Master con su configuración y recién entonces devuelve el resultado de la tool al host MCP.

LM Studio conserva abierta la petición de chat mientras ejecuta una tool MCP y normalmente vuelve al Master para producir el mensaje final. Por eso el Master no se restaura durante ComfyUI, pero sí antes de devolver el resultado de `run_batch`. La tool queda pendiente localmente durante la generación; no queda pendiente ninguna inferencia LLM. Si falla el preflight, el estado `WAITING` se cierra y se intenta restaurar el Master antes de propagar el error al host.

Para `review_batch`, se descarga todo, se espera la liberación, se carga el worker y se entra a `REVIEWING`. Para `deep_review_batch`, el mismo mecanismo descarga el worker y carga el Master antes de entrar a `DEEP_REVIEW`.

## Herramientas nuevas

- `orchestration_status`: estado y modelos que LM Studio reporta, sin cambios.
- `load_master` / `unload_master`.
- `load_worker` / `unload_worker`.
- `unload_all_llms`: descarga y confirma liberación; no inicia ComfyUI.
- `deep_review_batch(batch_id, limit)`: segunda opinión con Master.

La interfaz es `run_batch(dataset, batch_id)`: `dataset` puede ser un nombre de archivo o ruta contenida en `prompts/`. No recibe un tamaño; lo calcula del JSONL. Cuando `PIPELINE_ORCHESTRATION` no está activada conserva las mismas validaciones y protecciones, omitiendo únicamente el control de LM Studio.

## TTL y auto-evict

El TTL definido en `config/orchestration.json` se envía con las peticiones de inferencia OpenAI-compatibles como red de seguridad. Auto-Evict/JIT se habilita en LM Studio Server Settings si está disponible. Ninguno reemplaza la descarga explícita previa a ComfyUI.

## TODO / sin probar

- Confirmar que la versión instalada de LM Studio expone `/api/v1/models`, `/load` y `/unload` y cuál es exactamente su formato de inventario de modelos cargados.
- Confirmar los IDs reales de Master y Worker en esa instalación.
- Verificar soporte efectivo de TTL, JIT y Auto-Evict en la versión instalada.
- Confirmar que `context_length=8192`, MTP y reasoning budget `512` aplican al build/preset concreto del Master.
- Ejecutar el benchmark comparativo 8B vs 27B con la misma imagen y prompt; no fue ejecutado.
- Hacer una prueba controlada de preflight y ejecutar el piloto de 12 sólo después de validar los puntos anteriores.
- Revisar el comportamiento del chat de LM Studio tras devolver una tool: el propio chat puede volver a cargar su modelo para redactar la respuesta; no se considera parte de la ventana `GENERATING`.
