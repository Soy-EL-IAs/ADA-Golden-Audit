# Ada Viral Guide Evolution — Cycle 018

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.33/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.00 |
| Visual Appeal | 8.00 |
| Diversity | 7.00 |
| Repetition Control | 6.00 |
| Micro Story | 7.00 |
| Animation Potential | 7.00 |

## Verdict

Acceptable but needs refinement in closeup variety and hazard specificity. The set is strong on identity and full-body dynamics but falls short on batch-level diversity for the closeup category.

## Strengths

- Consistent adherence to 2B's identity facts (blindfold, dress cutout, gloves) across all premises.
- Strong causal logic in most premises; actions are triggered by specific environmental events rather than mood.
- Good variety in full-body poses (crouching, sliding, lunging, suspended), avoiding the 'balancing' trap of previous cycles.

## Failures

- Closeup category suffers from repetition: 3 out of 5 closeups involve a hand near the face/head or shielding the blindfold.
- Several dynamic premises rely on generic hazards (oil, spikes) that lack unique narrative flavor.
- Some 'causes' are slightly abstract (vibration, invisible wind resistance), weakening the micro-story clarity.

## Desired patterns

- Specific physical interactions with props or environment (catching beam, wiping fluid).
- Clear cause-and-effect chains visible in the frame.
- Use of clothing physics (sleeve flare, dress tension) to emphasize motion.

## Undesired patterns

- Repeated 'hand shielding face' or 'adjusting blindfold' compositions in closeups.
- Generic platformer-style obstacles (spikes, oil slicks) without deeper narrative context.
- Abstract causes like 'vibration' or 'invisible wind' that don't provide a clear visual anchor.

## Repetition clusters

- **Hand near face/head shielding or adjusting blindfold**: `e018_b01_closeup`, `e018_b02_closeup`, `e018_b03_closeup`, `e018_b04_closeup`
- **Defensive bracing/shielding against environmental burst (sparks, steam, gas)**: `e018_b01_medium`, `e018_b02_medium`, `e018_b03_medium`

## Recommendations for the next cycle

- Diversify closeup actions: include interactions with weapons, feet/boots, or distant objects rather than just face/hands.
- Replace generic hazards (oil, spikes) with more specific narrative elements (enemy debris, unique machine parts).
- Ensure all causes are visually concrete; avoid abstract terms like 'vibration' unless paired with a visible source.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e018_b01_closeup` | closeup | 9.0 | 7.0 | 8.0 | 6.0 | Strong identity with specific hairband detail. Good micro-reaction (knuckles white). Slight risk of 'gripping' anti-pattern but justified by the jolt. |
| `e018_b01_medium` | medium | 9.0 | 8.0 | 8.0 | 7.0 | Clear cause (sparks/debris) and active reaction (leaning/shielding). Good use of sleeve flare for motion. |
| `e018_b01_fullbody` | fullbody | 9.0 | 8.0 | 9.0 | 8.0 | Excellent active engagement (catching beam). Avoids generic balancing. Strong silhouette and strain. |
| `e018_b01_dynamic` | dynamic | 8.0 | 7.0 | 6.0 | 7.0 | Sidestepping oil is a valid cause. However, 'sliding patch of oil' feels slightly generic compared to other environmental hazards. |
| `e018_b01_cinematic` | cinematic | 9.0 | 9.0 | 7.0 | 6.0 | Strong scale contrast. Reaching for chandelier is a specific interaction. Good lighting usage. |
| `e018_b02_closeup` | closeup | 9.0 | 7.0 | 6.0 | 5.0 | Vibration cause is weak/abstract. 'Condensation' feels arbitrary without a clear source (like sweat or rain). Less impactful than b01_closeup. |
| `e018_b02_medium` | medium | 9.0 | 8.0 | 8.0 | 7.0 | Steam burst is a strong visual and physical cause. Good torso twist showing core engagement. |
| `e018_b02_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 8.0 | Sliding on knees is dynamic and distinct from standing/balancing. Clear cause (collapsing wall). |
| `e018_b02_dynamic` | dynamic | 8.0 | 7.0 | 5.0 | 6.0 | 'Invisible wind resistance' is a weak justification for arm tuck. Leaping over spikes is good but feels like standard platformer filler. |
| `e018_b02_cinematic` | cinematic | 9.0 | 8.0 | 7.0 | 6.0 | Snagged dress is a specific, character-relevant problem. Good tension in arms. |
| `e018_b03_closeup` | closeup | 9.0 | 7.0 | 6.0 | 5.0 | Wiping fluid is a good 'adjusting' action. However, it repeats the 'hand near face/head' composition of b01 and b02 closeups. |
| `e018_b03_medium` | medium | 9.0 | 7.0 | 7.0 | 6.0 | Toxic gas is a clear cause. Clapping hand over mouth is a standard reaction but effective here. |
| `e018_b03_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 7.0 | Lunging to catch cable is strong. Good use of leg definition and tension. |
| `e018_b03_dynamic` | dynamic | 8.0 | 7.0 | 6.0 | 7.0 | Dodging glass shard is specific. Rotation adds energy. |
| `e018_b03_cinematic` | cinematic | 9.0 | 8.0 | 7.0 | 5.0 | Fishing for data chip is a specific narrative beat. Good contrast of scale. |
| `e018_b04_closeup` | closeup | 9.0 | 7.0 | 6.0 | 5.0 | Hot air gust is a valid cause. However, 'hand shielding face' repeats the defensive pose of b02_medium and b01_closeup. |
| `e018_b04_medium` | medium | 9.0 | 7.0 | 6.0 | 6.0 | Tilting platform is a good cause. However, 'gripping railing' feels slightly passive compared to the active bracing of b01_medium. |
| `e018_b04_fullbody` | fullbody | 9.0 | 7.0 | 7.0 | 7.0 | Sliding under fence is dynamic. Sparks add visual interest. |
| `e018_b04_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 8.0 | Absorbing a punch is high-energy and specific. Good use of body arch. |
| `e018_b04_cinematic` | cinematic | 9.0 | 9.0 | 8.0 | 7.0 | Suspended by rope is a strong visual hook. Clear cause (catching crate) and consequence (straining). |

## Premises

### e018_b01_closeup — closeup

A tight close-up on 2B's gloved hand as she firmly presses her thumb against the hairband of her blindfold, correcting its position after a sudden jolt from a nearby machine malfunction; her knuckles are slightly white, and a single strand of short white hair has slipped loose onto her cheek, highlighting her controlled tension.

### e018_b01_medium — medium

A medium shot capturing 2B leaning sharply forward against a crumbling concrete pillar to shield her face from a burst of sparks and debris; her puffy feather-trimmed sleeves flare outward with the motion, and her black dress pulls tight across her torso as she braces for impact, revealing a glimpse of the cutout detail.

### e018_b01_fullbody — fullbody

A full-body view of 2B crouching low beneath a heavy, falling steel beam in a ruined corridor; her thigh-high boots are planted wide for stability while she extends one gloved hand to catch the edge of the beam before it hits the ground, emphasizing the definition of her legs and the strain in her posture.

### e018_b01_dynamic — dynamic

A high-energy dynamic shot of 2B mid-sidestep to avoid a sliding patch of oil on a metal floor; her body is twisted with momentum, motion blur trailing behind her, and her black dress hem flares dramatically as she pivots, capturing the precise moment before her foot regains traction.

### e018_b01_cinematic — cinematic

A wide cinematic angle framing 2B silhouetted against a massive, fractured skylight where sunlight streams down in sharp beams; she is actively reaching up with one arm to steady a swinging chandelier that has detached from the ceiling, her form centered and small against the scale of the collapsing architecture.

### e018_b02_closeup — closeup

A tight close-up on 2B's face as a sudden, sharp vibration from a nearby mechanical impact forces her to clench her jaw and slightly tilt her head; the black blindfold shifts minutely against her skin, and a single droplet of condensation falls onto her gloved hand which is raised defensively near her cheek, capturing her momentary loss of composure.

### e018_b02_medium — medium

A medium shot of 2B ducking low to avoid a horizontal blast of steam erupting from a broken pipe directly above her waist; her puffy feather-trimmed sleeves are pushed back by the pressure wave, and her black dress hem lifts slightly as she twists her torso to protect her core, her eyes narrowed in focused determination beneath the blindfold.

### e018_b02_fullbody — fullbody

A full-body view of 2B sliding on her knees across a polished marble floor, using one gloved hand to scrape against the surface for friction while her thigh-high boots kick up small debris; she is in the middle of a controlled slide to gain distance from a collapsing wall section behind her, her body low and streamlined.

### e018_b02_dynamic — dynamic

A high-energy dynamic shot of 2B mid-leap over a jagged spike of broken concrete protruding from the ground; her legs are extended forward in a tuck, and her black dress flows upward with the jump's momentum, while her arms are tucked tight to maintain balance against the invisible wind resistance of her rapid ascent.

### e018_b02_cinematic — cinematic

A wide cinematic angle showing 2B standing on a fractured balcony edge, leaning forward to catch the falling hem of her own dress which is snagged on a protruding rebar; she is small in frame against a vast, dark industrial sky, with a single spotlight beam highlighting her struggle and the tension in her arms as she pulls the fabric free.

### e018_b03_closeup — closeup

A tight close-up on 2B's gloved fingers as they meticulously wipe a smear of black hydraulic fluid from the strap of her blindfold; her jaw is set in a line of quiet irritation, and a stray wisp of white hair clings to the damp fabric near her temple, highlighting the contrast between her pristine uniform and the gritty mechanical residue.

### e018_b03_medium — medium

A medium shot capturing 2B twisting sharply away from a sudden burst of green toxic gas venting from a broken wall panel; her puffy feather-trimmed sleeves billow outward with the abrupt movement, and she claps one hand over her mouth and nose in a practiced motion, her body angled to shield her face while her stance remains grounded and controlled.

### e018_b03_fullbody — fullbody

A full-body view of 2B lunging forward to catch a loose, swinging cable that is whipping dangerously close to her face; her thigh-high boots are planted in a wide lunge for stability, and her arms are extended with precise tension as she snaps the wire taut, her body leaning into the pull to dampen its momentum.

### e018_b03_dynamic — dynamic

A high-energy dynamic shot of 2B mid-rotation as she dodges a flying shard of glass from a shattered window; her black dress flares dramatically around her waist, and her arms are tucked close to protect her blindfold, capturing the exact moment her back passes the point of impact with motion blur emphasizing the speed of her turn.

### e018_b03_cinematic — cinematic

A wide cinematic angle showing 2B standing on a precarious ledge above a deep chasm, leaning forward to fish a small, glowing data chip out of the rubble at her feet; the vast, dark industrial canyon looms below, but her focus is entirely downward, creating a striking contrast between the immense scale of the environment and her precise, delicate action.

### e018_b04_closeup — closeup

A tight close-up on 2B's face as a sudden gust of hot air from a ruptured boiler forces her to squint and tighten her jaw; the black blindfold presses firmly against her skin, while her gloved hand rises sharply to shield the fabric from the direct heat stream, highlighting the tension in her neck muscles.

### e018_b04_medium — medium

A medium shot of 2B bracing herself against a tilting metal platform that is sliding on oil; she grips the railing with one hand while twisting her upper body to counterbalance, causing her puffy feather-trimmed sleeves to bunch up and her black dress cutout to stretch slightly as her core engages.

### e018_b04_fullbody — fullbody

A full-body view of 2B performing a low, controlled slide under a swinging chain link fence to avoid its path; her thigh-high boots are dragging sparks on the concrete floor for friction, and her arms are tucked close to her sides to maintain an aerodynamic profile as she exits the frame.

### e018_b04_dynamic — dynamic

A high-energy dynamic shot of 2B mid-impact, absorbing a punch from an off-screen mechanical arm by leaning back and letting her gloved hand take the hit; her body is arched in a defensive reflex, with motion blur emphasizing the speed of the strike and the ripple through her black dress fabric.

### e018_b04_cinematic — cinematic

A wide cinematic angle showing 2B suspended by a single, fraying rope that is snapping under the weight of a collapsing crate she has just caught; her body hangs taut in mid-air against a backdrop of rising dust clouds, with every muscle visible as she strains to hold on.
