# Cache de referencias de personajes

`cache_character_refs` guarda aquí una colección pequeña y reusable de referencias seleccionadas por `find_character_refs`.

Estructura prevista:

```text
data/references/<character_slug>/<version_slug>/
  manifest.json
  refs/
    ref_01.ext
    ref_02.ext
```

Si no se indicó versión se usa `default`. Un cache con al menos dos archivos presentes y hashes válidos se reutiliza sin buscar ni descargar de nuevo. Una carpeta existente pero incompleta o inválida nunca se sobrescribe: requiere revisión manual.

Se descargan primero referencias `auto`; `review` sólo se usa cuando hace falta llegar al mínimo de dos. Cada URL se intenta una sola vez, el máximo es cinco y contenidos idénticos se deduplican por SHA-256 antes de escribir el segundo archivo. `manifest.schema.json` define el contrato y `_template/manifest.json` conserva una plantilla vacía.
