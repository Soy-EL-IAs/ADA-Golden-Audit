# Perfiles locales de personajes

La fuente local data/character_db/booru_characters/ se consulta antes de que generate_character_dataset entregue el contexto al Master. No usa red, embeddings, RAG ni referencias web.

La interfaz es:

~~~text
get_character_profile(character, version=None)
~~~

El perfil conserva sin filtrar los campos fuente:

- matched_tag
- gender
- copyright
- characteristics
- clothing
- relationships

La resolución es conservadora: tag/nombre normalizado exacto, copyright exacto para la versión y aliases nominales pequeños en config/character_aliases.json. Si no hay una coincidencia inequívoca compatible con la versión, character_profile_used es false y el Master continúa sin perfil local.

generate_character_dataset guarda el resultado en su metadata de staging y lo devuelve al Master cuando character_profile_used es true. El perfil define hechos visuales de identidad; el Master sigue redactando prompts semánticos y no concatena los tags como texto de prompt.

La base es un export de tags de Danbooru, no una fuente oficial. Sus tags no se filtran ni reinterpretan en esta primera integración.
