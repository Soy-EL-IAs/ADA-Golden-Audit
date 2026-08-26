# Datasets de personajes generados por el Master

La creación usa dos tools porque una tool MCP no debe invocar recursivamente al mismo Master que originó la llamada:

~~~text
generate_character_dataset
  -> crea un staging nuevo con distribución, reglas, destinos y contexto del cache

Master
  -> crea 5-10 premises, prompts y seeds originales
  -> append_character_dataset_entries por cada chunk

finalize_character_dataset
  -> valida el conjunto completo
  -> escribe JSONL + preset plan, sin sobrescribir
  -> compila localmente cada registro contra el workflow
  -> no ejecuta ComfyUI
~~~

## Interfaz

Primera fase:

~~~text
generate_character_dataset(
  character,
  version=None,
  count=20,
  dataset_id=None
)
~~~

La respuesta incluye la distribución requerida, las reglas de prompts, los paths propuestos y el manifest de referencias local si existe. También crea character_dataset_staging/<dataset_id>/ con metadata.json y entries.jsonl. No busca ni descarga referencias. Sólo usa un cache cuyo manifest tenga usable=true; si no es usable, devuelve refs_cache_used=false y refs_context=[].

`proposal_guidance` entrega la guía Viral completa y sólo los extractos de MiniMax necesarios para que la imagen pueda servir como semilla de video (primer fotograma, acción, identidad y continuidad). Las versiones activas quedan registradas en `prompt_guide_manifest` del staging.

Antes de convertir las premises elegidas en prompts, el Master debe pedir el segundo contexto:

~~~text
get_character_dataset_prompt_guidance(dataset_id)
~~~

Esa herramienta devuelve únicamente las guías versionadas de Illustrious y Klein. Así no se inyectan en la fase de ideas ni se cargan reglas de video completas durante la redacción de prompts de imagen.

Segunda fase, repetible con chunks de hasta 10:

~~~text
append_character_dataset_entries(
  dataset_id,
  entries
)
~~~

Cada entrada creativa contiene:

- id
- category: closeup, medium, fullbody, dynamic o cinematic
- premise
- illustrious_prompt
- klein_prompt
- illustrious_seed
- klein_seed

append valida estructura básica y bloquea IDs/seeds repetidos incluso contra chunks previos. No requiere beautiful: es una recomendación para el Master, nunca un motivo para invalidar el dataset.

Finalización:

~~~text
finalize_character_dataset(
  character,
  version,
  count,
  dataset_id
)
~~~

finalize valida count, distribución, IDs/seeds, categorías, prompts duplicados, términos físicos prohibidos, compilación del workflow y cobertura exacta del preset plan. Sólo si todo es válido crea los archivos finales. Si falla, conserva el staging para corregir el chunk afectado.

No se agregan adult, adult woman, mature adult ni equivalentes a los prompts positivos.

## Presets configurables

Los defaults viven en config/character_dataset.json:

- closeup: snofs 0.6 + A2R_Klein_Standard.safetensors 0.5, 4 steps.
- medium, fullbody, dynamic, cinematic: snofs 0.6 + anime2real-semi.safetensors 0.8, 8 steps.

El JSONL conserva el formato compatible con run_klein_jsonl_batch.py. category y premise son metadatos adicionales; la configuración de Klein permanece en su archivo separado.

## Ejemplo futuro: 2B

Pedido al Master:

~~~text
Creá un piloto para 2B, versión NieR:Automata, con 10 entradas y dataset_id 2b_nier_automata_pilot_10. No lo renderices.
~~~

El Master debe llamar primero:

~~~text
generate_character_dataset(character="2B", version="NieR:Automata", count=10, dataset_id="2b_nier_automata_pilot_10")
~~~

Después crea cinco entradas, las envía con append_character_dataset_entries, crea las otras cinco y las envía en un segundo append. Entonces llama:

~~~text
finalize_character_dataset(character="2B", version="NieR:Automata", count=10, dataset_id="2b_nier_automata_pilot_10")
~~~

Sólo tras revisión humana se ejecutaría, como acción separada:

~~~text
run_batch(
  dataset="prompts/2b_nier_automata_pilot_10.jsonl",
  batch_id="2b_nier_automata_pilot_10_001",
  klein_preset_plan="config/klein_presets_2b_nier_automata_pilot_10.json"
)
~~~

Este ejemplo no ejecuta búsquedas, descargas ni generaciones.

## Prueba dry-run: 20 proposals sin ComfyUI

Con el Master ya cargado en LM Studio, la siguiente prueba no crea staging, no llama al Worker y no contacta ComfyUI. Usa el perfil local de 2B si está disponible y exige exactamente 20 proposals con la distribución requerida:

~~~powershell
cd D:\IA\Ada
python scripts\dry_run_character_proposals.py
~~~

El resultado se guarda sin sobrescribir en `premises/dry_run_2b_nier_automata_20.json`. Si el archivo ya existe, indicá otro destino:

~~~powershell
python scripts\dry_run_character_proposals.py --output premises\dry_run_2b_nier_automata_20_rerun.json
~~~
