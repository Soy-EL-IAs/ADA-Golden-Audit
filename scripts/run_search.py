import json
import os
from local_search import SearXNGClient

os.environ["PIPELINE_LOCAL_SEARCH"] = "1"
os.environ["SEARXNG_URL"] = "http://127.0.0.1:8080"

client = SearXNGClient()
res = client.web('"Ghislaine Dedoldia"')
print(json.dumps([r['page_url'] for r in res.get('results', [])[:10]], indent=2))
