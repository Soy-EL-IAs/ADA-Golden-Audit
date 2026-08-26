# Problemas frecuentes

**ComfyUI no está idle.** Esperá a que finalice o cancelá manualmente desde ComfyUI. No lances otro batch en paralelo.

**"Batch already exists".** Es una protección. Elegí otro `batch_id`; no borres el manifest existente para reutilizarlo.

**Un batch queda `failed`.** Leé `manifest.json`, anotá el ID y el error. No lo reintentes automáticamente. `production100_reusable_v1` es precisamente un historial fallido que se debe conservar.

**No se ven imágenes en LM Studio.** Es una limitación conocida del tipo `Image`/enlaces locales. Ejecutá `build_gallery` y abrí `gallery.html` con un navegador.

**El MCP no aparece.** Revisá que el Python y la ruta del script en `lmstudio_mcp_entry.json` existan, recargá MCP/LM Studio y activá el servidor en el chat. También podés usar `START_LOCAL_OPERATOR.cmd` como alternativa.

**El modelo local compite por VRAM con ComfyUI.** Descargá/ejectá el modelo de LM Studio manualmente antes de generar y volvé a cargarlo para revisar. La automatización de load/unload todavía no existe.
