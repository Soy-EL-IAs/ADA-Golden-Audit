import json
wf = json.load(open('workflows/illustrious_to_klein_batch_base_ui.json'))

print('=== Klein Nodes ===')
for n in wf['nodes']:
    if n['id'] in (40, 51, 54, 47, 53, 38, 41, 43):
        print(f"Node {n['id']} ({n['type']})")
        print(f"  Inputs: {[i.get('name') for i in n.get('inputs',[])]}")
        print(f"  Widgets: {n.get('widgets_values',[])}")

print('=== Links involving Node 40 (VAEEncode) ===')
for l in wf['links']:
    if l[1] == 40 or l[3] == 40:
        print(l)
print('=== Links involving Node 54 (Sampler) ===')
for l in wf['links']:
    if l[1] == 54 or l[3] == 54:
        print(l)
print('=== Links involving Node 51 (ReferenceLatent) ===')
for l in wf['links']:
    if l[1] == 51 or l[3] == 51:
        print(l)
