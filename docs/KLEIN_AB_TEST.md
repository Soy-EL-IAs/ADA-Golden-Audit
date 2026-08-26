# Test A/B Klein-only

El runner `scripts/run_klein_ab_test.py` compara condiciones de Klein reutilizando outputs Illustrious de un batch completo. No contiene ni ejecuta la rama Illustrious.

El plan actual es `config/klein_ab_tifa_remake_001.json`:

- fuente: `tifa_remake_pilot_001`;
- casos: `tifa_remake_closeup_02`, `tifa_remake_fullbody_02`, `tifa_remake_dynamic_01`;
- `baseline`: sin ningún LoRA;
- `anime2real`: `flux/A2R_Klein_Standard.safetensors`, weight `0.8`;
- `anime2real_semi`: `flux/anime2real-semi.safetensors`, weight `0.9`.

La metadata embebida de los dos LoRA confirma base `flux2_klein_9b`, pero no declara triggers. Por eso el plan usa `trigger: null` y conserva exactamente los prompts Klein originales.

## Validar sin generar

```powershell
python scripts/run_klein_ab_test.py --plan config/klein_ab_tifa_remake_001.json --validate-only
```

Esto comprueba el batch fuente, dataset, tres imágenes Illustrious, workflow, LoRA instalados, grafo Klein-only y ausencia de carpetas destino. No consulta ComfyUI ni LM Studio y no crea archivos.

## Ejecutar

Con ComfyUI iniciado y `PIPELINE_ORCHESTRATION=1` para mantener el flujo determinista de VRAM:

```powershell
$env:PIPELINE_ORCHESTRATION = "1"
python scripts/run_klein_ab_test.py --plan config/klein_ab_tifa_remake_001.json
```

El test hace nueve ejecuciones: tres casos por tres condiciones. No reintenta fallos y rechaza cualquier `klein_ab_tests/tifa_remake_ab_001/` o staging de entrada ya existente.

La salida queda en:

```text
klein_ab_tests/tifa_remake_ab_001/
  source/
  baseline/
  anime2real/
  anime2real_semi/
  manifest.json
```

El manifest conserva el batch y dataset fuente, rutas Illustrious originales y copiadas, settings Klein comunes, condición, LoRA, weight, trigger, seed, prompt Klein y output final. Los archivos originales de `tifa_remake_pilot_001` sólo se leen.
