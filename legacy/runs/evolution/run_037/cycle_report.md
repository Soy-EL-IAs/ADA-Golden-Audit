# Ada Viral Guide Evolution — Cycle 037

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 6.83/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.00 |
| Visual Appeal | 8.00 |
| Diversity | 6.00 |
| Repetition Control | 4.00 |
| Micro Story | 7.00 |
| Animation Potential | 7.00 |

## Verdict

The set shows strong individual premise quality in identity and visual appeal, but fails significantly on repetition control due to multiple exact duplicates across batches. The causal logic is generally good but occasionally vague.

## Strengths

- Strong identity preservation across all premises with consistent use of blindfold, hair, and dress details.
- Good variety in causal forces (mechanical, elemental, biological) within the first two batches.
- Dynamic and Cinematic categories generally feature high-energy, clear motion vectors.

## Failures

- Severe repetition: Batch 03 is a near-complete copy of Batch 02 for Fullbody, Dynamic, and Cinematic categories.
- Batch 04 Cinematic duplicates Batch 01 Cinematic exactly.
- Some premises rely on 'unseen' or vague causes (e.g., 'unseen weight', 'static charge') which weakens the visual causality rule.
- Cinematic category leans heavily on vertical climbing/hanging, violating the guide's correction to avoid this as a default.

## Desired patterns

- Visible physical causes that interact directly with the character's body or clothing.
- Distinct locations and micro-interactions for each premise.
- Clear 'before and after' narrative implication in every frame.

## Undesired patterns

- Exact text duplication across different batch IDs.
- Vague atmospheric causes (sound, static) without visible physical manifestation on the character.
- Passive locomotion (walking/stepping) without a specific obstacle or narrative consequence.

## Repetition clusters

- **Dragonfly on bridge**: `e037_b02_fullbody`, `e037_b03_fullbody`
- **Vaulting over fence**: `e037_b02_dynamic`, `e037_b03_dynamic`
- **Walking on light beam**: `e037_b02_cinematic`, `e037_b03_cinematic`
- **Climbing cathedral pillar**: `e037_b01_cinematic`, `e037_b04_cinematic`

## Recommendations for the next cycle

- Implement a strict uniqueness check to prevent exact or near-exact text duplication across batches.
- Require all causes to be visible within the frame; avoid 'unseen' forces unless their effect is clearly depicted (e.g., wind moving hair).
- Diversify Cinematic hooks beyond vertical climbing; use horizontal scale, light interaction, or environmental pressure more creatively.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e037_b01_closeup` | closeup | 9.0 | 8.0 | 8.0 | 7.0 | Strong causal link between water burst and damp hair/blindfold shift. Good micro-expression. |
| `e037_b01_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Clear mechanical cause (jammed door). Fabric tension is well-integrated with the twisting action. |
| `e037_b01_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 6.0 | Balance challenge on mossy archway is distinct. Wind cause is visible and affects clothing. |
| `e037_b01_dynamic` | dynamic | 9.0 | 8.0 | 8.0 | 9.0 | High energy dodge with clear threat (debris). Motion vectors are strong. |
| `e037_b01_cinematic` | cinematic | 9.0 | 9.0 | 8.0 | 7.0 | Vertical climb in cathedral provides good scale contrast. Active engagement with environment. |
| `e037_b02_closeup` | closeup | 9.0 | 8.0 | 8.0 | 6.0 | Biological cause (vine) is specific. Interaction with glove fabric adds detail. |
| `e037_b02_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Bracing against sliding slab is a strong physical reaction. Sleeve bunching adds realism. |
| `e037_b02_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 5.0 | Unique biological interaction (dragonfly). Stillness is justified by the need not to startle. |
| `e037_b02_dynamic` | dynamic | 9.0 | 8.0 | 8.0 | 9.0 | Vaulting over collapsing fence is dynamic. Clear cause and consequence (fence falling). |
| `e037_b02_cinematic` | cinematic | 9.0 | 8.0 | 6.0 | 5.0 | Walking on light beam is visually striking but borders on 'locomotion filler' without a stronger narrative hook. |
| `e037_b03_closeup` | closeup | 9.0 | 8.0 | 6.0 | 5.0 | Reaction to sound is less visually concrete than physical impacts. 'Static charge' is vague. |
| `e037_b03_medium` | medium | 9.0 | 8.0 | 6.0 | 5.0 | 'Unseen weight' weakens the causal link. Viewer cannot infer the specific cause from the frame alone. |
| `e037_b03_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 5.0 | Exact duplicate of e037_b02_fullbody. Major repetition failure. |
| `e037_b03_dynamic` | dynamic | 9.0 | 8.0 | 8.0 | 9.0 | Exact duplicate of e037_b02_dynamic. Major repetition failure. |
| `e037_b03_cinematic` | cinematic | 9.0 | 8.0 | 6.0 | 5.0 | Exact duplicate of e037_b02_cinematic. Major repetition failure. |
| `e037_b04_closeup` | closeup | 9.0 | 8.0 | 7.0 | 5.0 | Spores are a good biological hook. Holding breath is a clear micro-story element. |
| `e037_b04_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Fracturing glass provides excellent visual tension and causal clarity. |
| `e037_b04_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 6.0 | Explosion shockwave is a strong cause. Balance on sloping roof is distinct from previous fullbody poses. |
| `e037_b04_dynamic` | dynamic | 9.0 | 8.0 | 8.0 | 9.0 | Diving away from steam is dynamic. Clear threat source visible in frame. |
| `e037_b04_cinematic` | cinematic | 9.0 | 9.0 | 8.0 | 7.0 | Exact duplicate of e037_b01_cinematic. Major repetition failure. |

## Premises

### e037_b01_closeup — closeup

2B's face is framed tightly as she winces against the sudden chill of a burst water pipe, her short white hair clinging damp to her cheek while her black blindfold shifts slightly from the moisture, capturing the micro-expression of controlled discomfort before she blinks away the condensation.

### e037_b01_medium — medium

A waist-up view shows 2B bracing against a heavy, rusted door handle that has just jammed shut, her torso twisted sharply to the side as she twists her gloved hand with effort, causing the fabric of her black dress's cutout and puffy sleeves to stretch taut across her midsection in response to the mechanical resistance.

### e037_b01_fullbody — fullbody

2B is captured in a full-body stance on the slick, moss-covered edge of a crumbling stone archway, her weight shifted entirely onto one thigh-high boot as she reaches out with both hands to steady herself against a sudden gust of wind that lifts her dress hem and stockings, highlighting her precarious balance against the organic growths.

### e037_b01_dynamic — dynamic

Mid-air, 2B executes a sharp lateral dodge away from a falling chunk of debris visible in the upper corner, her body twisted into a tight spiral with one leg extended forward and arms crossed defensively, capturing the peak moment of evasion as her hair and clothing trail behind her in a blur of motion.

### e037_b01_cinematic — cinematic

Set against the vast, shadowed interior of a collapsed cathedral, 2B is seen from a low angle as she climbs vertically up a jagged pillar of exposed rebar and concrete, her small silhouette contrasting with the immense scale of the ruin while she pulls herself upward, driven by the need to reach a distant light source at the apex.

### e037_b02_closeup — closeup

A tight close-up captures 2B's face as a thick, pulsating bioluminescent vine wraps around her wrist, its sticky secretion beginning to adhere to the fabric of her black glove; she holds her breath with visible tension in her jaw and a slight furrow in her brow behind the blindfold, eyes narrowed against the faint green glow illuminating the underside of her chin.

### e037_b02_medium — medium

From a waist-up perspective, 2B leans back aggressively to brace herself as a heavy, moss-covered stone slab slides down a narrow vertical shaft toward her; her gloved hands press firmly against the rough wall behind her for leverage, causing the puffy feather-trimmed sleeves to bunch up at her elbows while the cutout in her black dress stretches taut across her midsection under the strain of the counter-weight.

### e037_b02_fullbody — fullbody

In a full-body shot on the edge of a crumbling wooden bridge, 2B is crouched low to minimize her profile as a large, translucent dragonfly with iridescent wings lands heavily on the plank just inches from her face; her weight is shifted entirely onto her left thigh-high boot for stability while her right leg hovers slightly off the ground, and she holds perfectly still with focused intensity, her white hair hanging motionless to avoid startling the creature.

### e037_b02_dynamic — dynamic

Captured at the peak of a vaulting maneuver, 2B launches herself over a low, rusted iron fence as it begins to collapse inward under her momentum; her body is arched mid-air with legs split in an agile leap, one arm extended forward for balance while the other trails back, and her black dress flares dramatically behind her due to the rapid upward acceleration, contrasting with the sharp downward angle of the falling metal.

### e037_b02_cinematic — cinematic

Set in a vast, sun-drenched atrium filled with floating dust motes and broken glass shards, 2B is seen from a wide horizontal angle as she walks carefully across a narrow beam of intense light that cuts through the darkened room; her silhouette is sharply defined by the backlighting, highlighting the outline of her hairband and blindfold, while she navigates the precarious path with deliberate steps to avoid stepping on the scattered debris below.

### e037_b03_closeup — closeup

A tight close-up captures 2B's face as she recoils from a sudden, sharp crackling sound, her jaw tightening and brow furrowing behind the black blindfold while a single drop of sweat traces down her temple, highlighting the micro-expression of controlled alertness before she blinks away the static charge in the air.

### e037_b03_medium — medium

From a waist-up perspective, 2B leans forward aggressively as an unseen weight pulls at her outstretched hands, causing her torso to twist sharply to the side; this force stretches the fabric of her black dress's cutout taut across her midsection while her puffy feather-trimmed sleeves bunch up against her arms, emphasizing the mechanical strain on her posture.

### e037_b03_fullbody — fullbody

In a full-body shot on the edge of a crumbling wooden bridge, 2B is crouched low to minimize her profile as a large, translucent dragonfly with iridescent wings lands heavily on the plank just inches from her face; her weight is shifted entirely onto her left thigh-high boot for stability while her right leg hovers slightly off the ground, and she holds perfectly still with focused intensity, her white hair hanging motionless to avoid startling the creature.

### e037_b03_dynamic — dynamic

Captured at the peak of a vaulting maneuver, 2B launches herself over a low, rusted iron fence as it begins to collapse inward under her momentum; her body is arched mid-air with legs split in an agile leap, one arm extended forward for balance while the other trails back, and her black dress flares dramatically behind her due to the rapid upward acceleration, contrasting with the sharp downward angle of the falling metal.

### e037_b03_cinematic — cinematic

Set in a vast, sun-drenched atrium filled with floating dust motes and broken glass shards, 2B is seen from a wide horizontal angle as she walks carefully across a narrow beam of intense light that cuts through the darkened room; her silhouette is sharply defined by the backlighting, highlighting the outline of her hairband and blindfold, while she navigates the precarious path with deliberate steps to avoid stepping on the scattered debris below.

### e037_b04_closeup — closeup

A tight close-up captures 2B's face as a cluster of bioluminescent spores drifts toward her, causing her to hold her breath with visible tension in her jaw and a slight furrow in her brow behind the blindfold; a single spore adheres to the edge of her hairband, glowing faintly against her white hair while she maintains rigid composure to avoid inhaling the organic dust.

### e037_b04_medium — medium

From a waist-up perspective, 2B leans heavily against a cracked, transparent pane of reinforced glass that is slowly fracturing under the weight of her outstretched palm; the impact causes hairline cracks to spiderweb outward from her glove, and her torso twists slightly as she braces for shatter, stretching the fabric of her black dress's cutout taut across her midsection while her puffy sleeves bunch against her arms in resistance.

### e037_b04_fullbody — fullbody

In a full-body shot on the narrow, sloping roof of a crumbling rooftop structure, 2B is crouched low with her weight shifted onto one thigh-high boot to counterbalance a sudden shift in gravity caused by a distant explosion; her other leg is extended for stability while her hands grip the edge of the eave, highlighting the precarious balance as debris rains down around her and her dress hem flutters from the shockwave.

### e037_b04_dynamic — dynamic

Mid-air, 2B executes a sharp downward dive away from a sudden burst of steam venting from a broken pipe in the upper frame, her body twisted into a tight spiral with one leg extended forward and arms crossed defensively; capturing the peak moment of evasion as her hair and clothing trail behind her in a blur of motion, contrasting with the rising white cloud that obscures the source of the threat.

### e037_b04_cinematic — cinematic

Set against the vast, shadowed interior of a collapsed cathedral, 2B is seen from a low angle as she climbs vertically up a jagged pillar of exposed rebar and concrete, her small silhouette contrasting with the immense scale of the ruin while she pulls herself upward, driven by the need to reach a distant light source at the apex.
