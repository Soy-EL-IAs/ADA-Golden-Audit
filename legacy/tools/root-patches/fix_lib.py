import re
with open('ada_app/asset_library.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = re.sub(r'except Exception:\n                    continue\n                            source_run_id=.*?\}\)\n                        \)\)', 'except Exception:\n                    continue', text, flags=re.DOTALL)
text = text.replace('"COMPLETE"', '"APPROVED"')

with open('ada_app/asset_library.py', 'w', encoding='utf-8') as f:
    f.write(text)
