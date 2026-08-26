# Ada Viral Guide Evolution — Cycle 034

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 6.08/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.00 |
| Visual Appeal | 7.50 |
| Diversity | 4.00 |
| Repetition Control | 3.00 |
| Micro Story | 6.50 |
| Animation Potential | 6.50 |

## Verdict

The set fails primarily due to poor repetition control. While individual premises in b01 and parts of b04 are strong, the inclusion of an entire duplicate batch (b03 mirroring b02) drastically reduces diversity and violates the 'Unique Core Mechanic' rule.

## Strengths

- Strong adherence to character identity facts (blindfold, gloves, dress details) across all premises.
- Good use of specific physical causes in the first batch (b01), such as wires snagging or wind gusts.
- Dynamic category verbs are varied and distinct where they appear (vault, pivot, roll).

## Failures

- Severe repetition: Batch b03 is an exact duplicate of Batch b02 for Medium, Fullbody, Dynamic, and Cinematic categories.
- Batch b04 Closeup repeats the 'wind/hair' motif from b01 Fullbody without sufficient differentiation in cause or reaction intensity.
- Cinematic premises often default to passive observation ('scanning', 'striding') rather than active engagement with the scale/contrast.
- Medium category relies heavily on the same 'torso twist/wrenching object' mechanic across b01, b02, and b03.

## Desired patterns

- Unique core physical interaction mechanisms for each premise in the batch.
- Active verbs that imply immediate follow-through or consequence (e.g., 'catching', 'dodging', 'climbing') rather than static states ('standing', 'scanning').
- Distinct environmental textures and locations to prevent visual monotony.

## Undesired patterns

- Exact duplicate premises across different batch IDs.
- Passive balance or bracing without a clear, immediate threat or active correction motion.
- Locomotion filler (striding/walking) used as the primary action in cinematic shots.
- Atmospheric elements (dust, wind) serving as the sole hook without specific physical interaction.

## Repetition clusters

- **Exact Duplicate: Medium Wrenching Object**: `e034_b02_medium`, `e034_b03_medium`
- **Exact Duplicate: Fullbody Beam Balance**: `e034_b02_fullbody`, `e034_b03_fullbody`
- **Exact Duplicate: Dynamic Chain Pivot**: `e034_b02_dynamic`, `e034_b03_dynamic`
- **Exact Duplicate: Cinematic Pillar Striding**: `e034_b02_cinematic`, `e034_b03_cinematic`

## Recommendations for the next cycle

- Eliminate all exact duplicates; ensure every premise in the set of 20 has a unique core mechanic.
- For Cinematic shots, replace passive 'scanning/striding' with active interactions like 'climbing', 'leaping across chasms', or 'emerging from dust clouds'.
- Vary the Medium category mechanics: instead of repeating 'wrenching/pulling', use 'bracing against impact', 'manipulating controls', or 'catching falling debris'.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e034_b01_closeup` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Strong causal link between wires and blindfold. 'Squinting through fabric' is slightly ambiguous but acceptable for an android context. |
| `e034_b01_medium` | medium | 9.0 | 8.0 | 7.0 | 7.0 | Good physical tension. 'Rusted gear' is a generic prop but fits the industrial aesthetic without breaking canon. |
| `e034_b01_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 8.0 | Clear environmental force (wind) causing a balance challenge. Good silhouette usage. |
| `e034_b01_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Distinct motion verb (sliding vault). Clear obstacle avoidance. |
| `e034_b01_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | 'Gravitational pull' is an abstract force; 'bracing' against it is passive. The mechanical eye is a strong visual hook but the character's action is weak. |
| `e034_b02_closeup` | closeup | 8.0 | 6.0 | 5.0 | 4.0 | Dust settling is a slow process. 'Blinking rapidly' is a micro-reaction but lacks the punch of a physical impact or force. Feels like an atmosphere piece. |
| `e034_b02_medium` | medium | 9.0 | 8.0 | 7.0 | 7.0 | Similar to b01_medium but with a different prop (cable vs gear). 'Viscous black cable' adds texture interest. |
| `e034_b02_fullbody` | fullbody | 9.0 | 7.0 | 6.0 | 5.0 | 'Standing on tiptoes' is a static pose. 'Sudden jolt' is the cause, but the reaction (rigid/elongated) is passive bracing rather than active correction. |
| `e034_b02_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 8.0 | Backward pivot is a distinct mechanic. Good use of hair/dress flow. |
| `e034_b02_cinematic` | cinematic | 8.0 | 7.0 | 5.0 | 4.0 | 'Striding purposefully' is locomotion filler. 'Scanning shadows' is passive observation. Fails the 'active role' requirement for cinematic. |
| `e034_b03_closeup` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Strong cause (welder flash) and reaction (pulling strap tight). Good tension. |
| `e034_b03_medium` | medium | 9.0 | 8.0 | 7.0 | 7.0 | Near-duplicate of b02_medium. 'Wrench a heavy... grate' vs 'wrench a sticky... cable'. The core mechanic (torso twist to pull object from housing) is identical. |
| `e034_b03_fullbody` | fullbody | 9.0 | 7.0 | 6.0 | 5.0 | Exact duplicate of b02_fullbody. Same pose, same cause (jolt), same location type. |
| `e034_b03_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 8.0 | Exact duplicate of b02_dynamic. Same pivot, same chain evasion. |
| `e034_b03_cinematic` | cinematic | 8.0 | 7.0 | 5.0 | 4.0 | Exact duplicate of b02_cinematic. Same striding/scanning in stone pillars. |
| `e034_b04_closeup` | closeup | 9.0 | 7.0 | 6.0 | 5.0 | Wind whipping hair is a common trope. 'Squinting' and 'tightening jaw' are similar to b01/b03 closeups but less specific than the wire/flash causes. |
| `e034_b04_medium` | medium | 9.0 | 8.0 | 7.0 | 7.0 | Crouching for traction is a distinct mechanic from the 'wrenching' of b01/b02/b03. Good interaction with environment (water/moss). |
| `e034_b04_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 8.0 | Balance on spire tip is distinct from the beam in b02/b03. Updraft cause is clear. |
| `e034_b04_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Rolling is a distinct motion verb. Clear cause (falling masonry). |
| `e034_b04_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | Climbing is active, but 'escape rising smoke' is a bit generic. Still better than the passive striding in b02/b03. |

## Premises

### e034_b01_closeup — closeup

2B's gloved hand sharply snags a tangle of frayed electrical wires pulling against her black blindfold, her jaw tightening as she squints through the fabric to assess the sparking connection point.

### e034_b01_medium — medium

2B leans back against a crumbling stone pillar for support, her puffy sleeves straining as she pulls a heavy, rusted gear from the rubble above, her body twisted to counterbalance the unexpected weight.

### e034_b01_fullbody — fullbody

2B maintains perfect balance on a narrow, slippery moss-covered ledge, leaning heavily into a sudden gust of wind that flares her dress hem and threatens to push her off the edge.

### e034_b01_dynamic — dynamic

2B executes a low, sliding vault over a jagged debris field, her boots kicking up dust and gravel as she tucks her chin to avoid an overhead swinging beam.

### e034_b01_cinematic — cinematic

2B is silhouetted against the massive, glowing iris of a colossal mechanical eye in the distance, her small figure bracing against the sheer gravitational pull emanating from the machine's activation.

### e034_b02_closeup — closeup

A close-up on 2B's face as a fine layer of abrasive red dust settles onto her black blindfold, causing her to blink rapidly and subtly twitch her jaw in irritation while a single strand of loose hair clings to the fabric.

### e034_b02_medium — medium

2B twists her torso sharply to wrench a sticky, viscous black cable free from a corroded machine housing, her puffy sleeves stretching taut as she uses the leverage of her hips to pull against the resistant suction.

### e034_b02_fullbody — fullbody

2B stands on tiptoes on a high, narrow metal beam, extending one arm upward to steady herself against a sudden jolt from the structure below, her body rigid and elongated in an effort to maintain equilibrium.

### e034_b02_dynamic — dynamic

2B executes a rapid backward pivot on one heel to evade a low-hanging swinging chain, her dress hem and hair whipping in the air as she spins away from the impact zone with precise timing.

### e034_b02_cinematic — cinematic

From a low angle, 2B is seen striding purposefully through a towering forest of ancient, moss-covered stone pillars, her small figure dwarfed by the massive structures as she scans the shadows for movement.

### e034_b03_closeup — closeup

2B's gloved fingers firmly grasp the strap of her black blindfold, pulling it taut against a sudden, blinding flash from an off-screen welder, her jaw clenched tight to suppress a flinch as sweat beads on her forehead.

### e034_b03_medium — medium

2B twists her torso sharply to wrench a heavy, rusted iron grate free from a corroded machine housing, her puffy sleeves stretching taut as she uses the leverage of her hips to pull against the resistant suction.

### e034_b03_fullbody — fullbody

2B stands on tiptoes on a high, narrow metal beam, extending one arm upward to steady herself against a sudden jolt from the structure below, her body rigid and elongated in an effort to maintain equilibrium.

### e034_b03_dynamic — dynamic

2B executes a rapid backward pivot on one heel to evade a low-hanging swinging chain, her dress hem and hair whipping in the air as she spins away from the impact zone with precise timing.

### e034_b03_cinematic — cinematic

From a low angle, 2B is seen striding purposefully through a towering forest of ancient, moss-covered stone pillars, her small figure dwarfed by the massive structures as she scans the shadows for movement.

### e034_b04_closeup — closeup

A macro shot of 2B's white hair as a sudden, violent gust from a ruptured ventilation shaft whips the strands against her black blindfold, causing her to squint and tighten her jaw in suppressed irritation while a loose strand clings stubbornly to the fabric.

### e034_b04_medium — medium

2B crouches low, using one gloved hand to press firmly against a slick, moss-covered stone wall for traction while her other arm reaches down to grasp the hem of her dress, preventing it from dragging into the murky water below as she navigates a narrow, slippery gap.

### e034_b04_fullbody — fullbody

2B maintains a rigid, elongated posture on the tip of a crumbling stone spire, her weight shifted entirely to one leg as she extends the other forward for balance, her dress hem and puffy sleeves billowing violently in an updraft that threatens to topple her off the narrow peak.

### e034_b04_dynamic — dynamic

2B executes a swift, low-slung roll across a dusty, sun-baked plaza to evade a falling chunk of masonry, her hair and dress trailing in the dust cloud as she pushes off the ground with both palms to gain momentum for the next leap.

### e034_b04_cinematic — cinematic

From a high angle, 2B is seen climbing up the vertical face of a massive, overgrown concrete ruin, her small figure dwarfed by the scale of the structure as she reaches for a higher ledge to escape the rising smoke filling the valley below.
