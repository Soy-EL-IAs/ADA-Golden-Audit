# Búsqueda local gratuita con SearXNG

Esta integración es opt-in y no usa API keys. Las tools de búsqueda consultan SearXNG por JSON y sólo devuelven URLs/metadatos. La descarga ocurre únicamente al invocar explícitamente `cache_character_refs`.

## Qué instalar

En Windows, instalar **Docker Desktop** con Docker Compose. No hacen falta paquetes Python, cuentas ni servicios pagos. Al iniciar por primera vez, Docker descargará la imagen oficial `searxng/searxng`.

## Iniciar y detener

Desde `_pipeline/search/searxng`:

```powershell
docker compose up -d
docker compose down
```

Si se modifica `settings.yml`, aplicar el cambio con `docker compose restart searxng`.

Para detener conservando el cache interno se usa `down` sin `-v`. Para ver estado o logs:

```powershell
docker compose ps
docker compose logs --tail 100 searxng
```

El servicio sólo se publica en `http://127.0.0.1:8080`. `settings.yml` habilita explícitamente las respuestas JSON requeridas por el cliente. No expongas esta configuración a la red: el limiter está desactivado porque se diseñó exclusivamente para localhost.

## Activar en el operador/MCP

Después de iniciar SearXNG, agregar al entorno del operador:

```text
PIPELINE_LOCAL_SEARCH=1
SEARXNG_URL=http://127.0.0.1:8080
```

También se puede usar `lmstudio_mcp_searxng.json`, que ya contiene esos valores. Tools:

- `search_web(query, limit)`: resultados web con URL, título, extracto y motores.
- `search_images(query, limit)`: URL de página, URL de imagen, miniatura y metadatos disponibles.
- `find_character_refs(character, version=None, limit=6)`: ejecuta como máximo dos búsquedas externas —una web y, sólo si hace falta, una de imágenes— y aplica selección mecánica determinista, sin LLM ni descargas.
- `cache_character_refs(character, version=None, limit=None)`: reutiliza un cache usable o descarga una sola vez entre dos y cinco referencias seleccionadas.

Las tools no devuelven objetos `Image` de MCP y no dependen del render inline de LM Studio.

### Selección determinista de referencias

Las reglas viven en `config/character_refs.json`. La selección:

- excluye los dominios configurados (incluidos Pinterest/Pinimg, DeviantArt, Zerochan, RenderHub y CGTrader);
- excluye cosplay y resultados marcados como AI-generated, Stable Diffusion, Midjourney o NovelAI;
- deduplica por URL de imagen; una misma página oficial puede aportar varios assets visuales distintos;
- da prioridad a dominios oficiales configurados y a resoluciones razonables;
- devuelve `source_url`, `image_url`, `resolution`, `domain`, `source_trust`, `character_relevance`, `image_quality`, `final_score` y `trust_reason`.

La estrategia tiene dos etapas: primero busca páginas web oficiales/confiables y examina únicamente su HTML para localizar `og:image`, `twitter:image`, `image_src`, renders y screenshots. Dentro del presupuesto configurado también sigue enlaces relevantes —character, media, press, gallery, artwork, product— del mismo ecosistema oficial/confiable. Así puede reunir varias vistas canónicas desde páginas de personaje, prensa o producto sin asumir que un dominio sólo aporta una referencia. Sólo si no reúne suficientes candidatos usa una segunda búsqueda general de imágenes. Nunca hace más de dos búsquedas SearXNG; inspeccionar páginas y assets enlazados del mismo ecosistema no cuenta como una búsqueda adicional y no descarga los archivos de imagen.

`final_score` pondera `source_trust=55%`, `character_relevance=40%` e `image_quality=5%`. Por ello una imagen de alta resolución alojada en un dominio no verificado no puede convertirse sólo por resolución en una referencia de alta confianza.

El fallback acepta como máximo dos candidatos por dominio. La selección final prioriza diversidad: recorre primero el mejor candidato de cada dominio y después un segundo. Si todavía quedan lugares, sólo permite resultados adicionales provenientes de la inspección de páginas oficiales/confiables; el fallback general nunca usa esa excepción. No se admiten wallpapers ni fanart para completar el cupo. Sólo devuelve resultados con `final_score >= 55`, por lo que puede entregar menos que `limit`. Cada referencia incluye una recomendación mecánica: `auto` desde 85, `review` desde 60 y `reject` entre 55 y 59; los valores inferiores a 55 no se devuelven.

La allowlist de dominios oficiales es deliberadamente editable. Un dominio no incluido puede aparecer como candidato, pero se marca `unverified_domain` y no recibe el bonus de confianza. La palabra “official” en un título no convierte por sí sola un dominio desconocido en oficial.

## Cache local de referencias

El cache se guarda en `character_refs/<character_slug>/<version_slug>/`, con las imágenes dentro de `refs/` y un `manifest.json`. Si no hay versión se usa `default`.

La selección prioriza `auto`; si hay menos de dos permite `review`. Descarga como máximo cinco archivos, valida formatos JPEG/PNG/WebP/AVIF, limita cada archivo a 20 MB y deduplica contenido idéntico por SHA-256. No hace retries. Si ya existe un manifest usable devuelve ese cache sin búsquedas ni redescargas. Si la carpeta existe pero no es usable, se detiene sin sobrescribirla.

Ejemplo futuro, cuando se autorice una descarga real:

```text
cache_character_refs(character="Tifa Lockhart", version="Final Fantasy VII Remake", limit=5)
```

Brave permanece como ejemplo opcional en `lmstudio_mcp_full.json`; SearXNG no lo necesita ni lo invoca.

## Pendiente de verificar

- Arranque de Docker Desktop y del compose en esta máquina.
- Motores web e imágenes disponibles según región y bloqueos externos.
- Forma exacta de los resultados de cada motor; el cliente tolera campos ausentes.
- Piloto real de cache con Tifa Lockhart / Final Fantasy VII Remake.
