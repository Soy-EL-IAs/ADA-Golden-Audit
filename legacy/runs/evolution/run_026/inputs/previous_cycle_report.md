# Ada Viral Guide Evolution — Cycle 025

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.35/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.20 |
| Visual Appeal | 7.50 |
| Diversity | 6.00 |
| Repetition Control | 5.50 |
| Micro Story | 7.80 |
| Animation Potential | 8.10 |

## Verdict

Solid batch with strong identity and animation potential, but penalized for conceptual repetition in medium and dynamic categories. Needs more variety in interaction types to meet diversity quotas strictly.

## Strengths

- Consistent adherence to the local identity profile (blindfold, hair, dress details).
- Strong animation potential across most premises due to clear kinetic energy.
- Good use of specific micro-stories in closeups (insect, sound reaction).

## Failures

- Repetition of 'catching falling heavy object' in medium shots (b01 vs b02).
- Repetition of 'mid-air rotation/dodge' in dynamic shots (b02 vs b03).
- One weak cinematic premise (b03) relying on vague 'shadow' cause.
- Full-body balance scene (b03) feels static and risks the 'precarious balance' trap.

## Desired patterns

- Specific, tangible causes for character reactions.
- Clear causal chains leading to visible consequences (clothing shift, debris movement).
- Distinct interaction types across categories.

## Undesired patterns

- Generic 'heavy object' interactions without unique narrative stakes.
- Atmospheric elements (shadow, wind) substituting for physical events.
- Repeated conceptual families (mid-air dodges, catching items).

## Repetition clusters

- **Catching/Bracing against falling heavy objects**: `e025_b01_medium`, `e025_b02_medium`
- **Mid-air rotation/dodge to avoid obstacle**: `e025_b02_dynamic`, `e025_b03_dynamic`

## Recommendations for the next cycle

- Differentiate medium-shot actions: replace one 'catching' scene with a 'pushing/pulling' or 'sliding' action.
- Vary dynamic shots: ensure at least one is grounded (slide/roll) and one is aerial, avoiding two mid-air rotations.
- Strengthen weak cinematic causes: replace vague shadows/wind with specific physical impacts or interactions.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e025_b01_closeup` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Strong causal link (ruptured line). Identity preserved. Good micro-reaction. |
| `e025_b01_medium` | medium | 9.0 | 8.0 | 7.0 | 7.0 | Clear action (catching core). Good tension in clothing. Slightly generic 'heavy object' cause. |
| `e025_b01_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 9.0 | Dynamic slide. Good use of environment (oil spill). Clear consequence. |
| `e025_b01_dynamic` | dynamic | 8.0 | 7.0 | 6.0 | 8.0 | Leap over pit. Good motion blur potential. Cause is clear (gap). |
| `e025_b01_cinematic` | cinematic | 9.0 | 7.0 | 6.0 | 7.0 | Wind/debris. Risk of 'atmospheric wallpaper' but character interaction (bracing) saves it. |
| `e025_b02_closeup` | closeup | 9.0 | 8.0 | 9.0 | 9.0 | Excellent micro-story (insect on blindfold). Unique interaction. High curiosity. |
| `e025_b02_medium` | medium | 9.0 | 8.0 | 6.0 | 7.0 | REPEATED CONCEPT: Catching falling heavy object. Nearly identical to e025_b01_medium (data core vs gear). Violates diversity. |
| `e025_b02_fullbody` | fullbody | 9.0 | 7.0 | 8.0 | 8.0 | Sliding under cable. Good specific obstacle. Distinct from previous full-body actions. |
| `e025_b02_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Mid-air rotation. Good kinetic energy. Clear cause (swinging chain). |
| `e025_b02_cinematic` | cinematic | 9.0 | 7.0 | 8.0 | 8.0 | Slab sliding away. Good narrative event (escape). Distinct from wind-based cinematic. |
| `e025_b03_closeup` | closeup | 9.0 | 7.0 | 6.0 | 7.0 | Wind in hair. Similar to e025_b01_cinematic cause (wind) but different scale/reaction. Acceptable but close. |
| `e025_b03_medium` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Bracing against chain. Good physical interaction. Distinct from 'catching' actions. |
| `e025_b03_fullbody` | fullbody | 9.0 | 7.0 | 6.0 | 7.0 | Stepping over gap. Risk of 'precarious balance' trap if not dynamic enough. Feels static compared to slide/leap. |
| `e025_b03_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Spinning mid-air. Very similar to e025_b02_dynamic (rotation/avoidance). Repetition of 'mid-air dodge' family. |
| `e025_b03_cinematic` | cinematic | 8.0 | 6.0 | 5.0 | 6.0 | Shadow falling. Weak cause ('massive shadow'). Feels like atmosphere replacing event. 'Composed curiosity' is vague. |
| `e025_b04_closeup` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Reaction to sound. Good 'off-screen' cause usage. Distinct from visual triggers. |
| `e025_b04_medium` | medium | 9.0 | 7.0 | 6.0 | 7.0 | Yanking lever. Violates 'Mechanical Jam' limit if counted with other mechanical interactions? No, only one here. But feels generic. |
| `e025_b04_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 9.0 | Diving for chip. Excellent specific goal. High animation potential. |
| `e025_b04_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Sliding under door. Good kinetic energy. Distinct from mid-air moves. |
| `e025_b04_cinematic` | cinematic | 9.0 | 7.0 | 8.0 | 8.0 | Chandelier crash. Clear cause and consequence. Good cinematic event. |

## Premises

### e025_b01_closeup — closeup

A close-up of 2B's face as she squints against a sudden blinding flash from a ruptured coolant line, her black blindfold tilting slightly off-center while a fine mist sprays across her cheek and hairband.

### e025_b01_medium — medium

A medium shot capturing 2B's torso twisting sharply to the left as she catches a heavy, falling data core with her gloved hand, the momentum pulling her puffy sleeves back and straining the fabric of her dress across her waist.

### e025_b01_fullbody — fullbody

A full-body view of 2B lunging forward with one leg planted firmly on a cracked tile, the other extended back for balance as she slides across a slick oil spill to avoid a swinging pipe, her thigh-high stockings contrasting against the dark grime.

### e025_b01_dynamic — dynamic

A low-angle dynamic freeze-frame of 2B mid-leap over a jagged rubble pit, her white hair and dress hem flaring upward with the lift, her expression locked in focused intensity as she clears the gap.

### e025_b01_cinematic — cinematic

A wide cinematic shot of 2B standing on a crumbling balcony edge, leaning back slightly to brace herself against a gust of wind from a distant collapsing tower, her blindfold whipping violently as debris rains down around her.

### e025_b02_closeup — closeup

A tight close-up of 2B's face as a single, large mechanical insect lands on her black blindfold; she holds perfectly still with narrowed eyes visible beneath the fabric, her breath hitching slightly as her gloved hand rises slowly to flick it away.

### e025_b02_medium — medium

A medium shot of 2B's torso twisting sharply as she catches a heavy, rusted gear that has fallen from above; the impact jars her shoulders back, causing her puffy feather-trimmed sleeves to flare outward and her black dress cutout to stretch slightly under the strain.

### e025_b02_fullbody — fullbody

A full-body view of 2B crouching low on one knee in a narrow, dusty corridor, her body coiled tightly to slide under a hanging low-hazard cable; her thigh-high boots grip the uneven ground firmly while her white hair and blindfold brush against the dust cloud kicked up by her movement.

### e025_b02_dynamic — dynamic

A high-speed dynamic freeze-frame of 2B rotating in mid-air to avoid a swinging chain link, her white hair whipping upward and her black dress hem flaring wide with the centrifugal force; her expression is locked in intense focus as she clears the obstacle by inches.

### e025_b02_cinematic — cinematic

A wide cinematic shot of 2B standing on a fractured ledge, leaning forward to brace her gloved hands against the crumbling edge as a massive stone slab slides away behind her; debris rains down around her, and she looks back over her shoulder with composed urgency.

### e025_b03_closeup — closeup

A tight close-up of 2B's face as a sudden, sharp gust from a cracked wall vent blows her short white hair across her black blindfold; her eyes widen slightly in surprise before narrowing with controlled intensity as she tilts her head to keep the fabric in place.

### e025_b03_medium — medium

A medium shot of 2B's torso arching backward to brace against a heavy, swinging chain that grazes her shoulder; the impact pulls her puffy feather-trimmed sleeves up and strains the fabric of her black dress cutout as she maintains her grip on a nearby support beam.

### e025_b03_fullbody — fullbody

A full-body view of 2B stepping carefully over a narrow, unstable gap in the floor; her weight is shifted entirely onto one leg while the other hovers just above the void, her thigh-high stockings visible against the dark drop below as she keeps her arms out for balance.

### e025_b03_dynamic — dynamic

A dynamic freeze-frame of 2B spinning mid-air to avoid a falling debris block; her white hair and dress hem flare outward with the rotation, creating a circular blur that contrasts with her focused, determined expression as she clears the obstacle.

### e025_b03_cinematic — cinematic

A wide cinematic shot of 2B standing in a narrow alleyway as a massive shadow falls over her from above; she looks up with composed curiosity, one gloved hand raised slightly to shield her eyes from the sudden change in light, while dust motes swirl around her.

### e025_b04_closeup — closeup

A tight close-up of 2B's face as a sudden, high-pitched screech from an off-screen predator causes her to flinch; her black blindfold shifts slightly down her nose, revealing the whites of her eyes widening in controlled shock while a single strand of white hair falls across her cheek.

### e025_b04_medium — medium

A medium shot of 2B's torso twisting sharply to the right as she yanks a heavy, rusted lever from a wall panel; the effort pulls her puffy feather-trimmed sleeves taut and strains the fabric of her black dress cutout across her waist, while her gloved hand grips the handle with visible tension.

### e025_b04_fullbody — fullbody

A full-body view of 2B diving forward to catch a small, glowing data chip that has popped out of a broken terminal; her body is stretched horizontally in mid-air, one leg extended back and the other bent, with her thigh-high stockings contrasting against the dusty floor as she reaches for the object.

### e025_b04_dynamic — dynamic

A dynamic freeze-frame of 2B sliding across a polished metal surface to avoid a closing blast door; her body is low and parallel to the ground, one hand trailing along the floor for friction while her white hair and dress hem blur with the speed of her movement.

### e025_b04_cinematic — cinematic

A wide cinematic shot of 2B standing in a large, open atrium as a massive, broken chandelier crashes down around her; she is frozen in the center, arms outstretched to brace for impact, with debris raining down and dust clouds billowing outward from the point of collision.
