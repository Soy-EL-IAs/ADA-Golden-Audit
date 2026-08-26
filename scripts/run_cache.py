import json
import os
from character_refs import CharacterReferenceFinder
from local_search import SearXNGClient
from character_ref_cache import CharacterReferenceCache

os.environ["PIPELINE_LOCAL_SEARCH"] = "1"
os.environ["SEARXNG_URL"] = "http://127.0.0.1:8080"

finder = CharacterReferenceFinder(SearXNGClient())
cache = CharacterReferenceCache(finder)
result = cache.cache("Ghislaine Dedoldia")
print(json.dumps(result, indent=2))
