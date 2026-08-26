# Ada Viral Guide Evolution — Cycle 030

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.00/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 8.50 |
| Visual Appeal | 7.50 |
| Diversity | 6.00 |
| Repetition Control | 5.50 |
| Micro Story | 7.00 |
| Animation Potential | 7.50 |

## Verdict

The set shows strong identity and visual appeal in closeups and mediums but fails on diversity and repetition control, particularly in the Cinematic and Dynamic categories where static poses and repeated motion structures dominate. The causal logic is generally good but occasionally vague.

## Strengths

- Strong identity preservation across most premises, with clear references to blindfold, hair, and outfit details.
- Good use of specific physical causes (steam, coolant, magnetic clamp) in closeups and mediums.
- Dynamic categories generally show strong motion potential and kinetic energy.

## Failures

- Cinematic category suffers from severe repetition: three out of five are static 'standing still' poses with minimal character action.
- Direct gaze into the camera is used as a substitute for interaction in e030_b02_cinematic.
- Dynamic categories show repetition in pose structure (mid-air tucked knees) between b01 and b04.
- Some premises rely on vague or invisible causes ('invisible shockwave', 'atmosphere').
- Passive observation/inspection patterns persist in closeups and cinematics.

## Desired patterns

- Active physical interaction with the environment (grabbing, dodging, adjusting).
- Clear visible cause for every action.
- Distinct micro-reactions that reflect personality (controlled alarm vs. panic).

## Undesired patterns

- Static bracing or standing still without secondary movement.
- Direct gaze into the camera lens as a primary hook.
- Generic locomotion (walking, stepping) without narrative stake.
- Invisible or vague causes for motion.

## Repetition clusters

- **Static Cinematic Pose**: `e030_b01_cinematic`, `e030_b02_cinematic`, `e030_b04_cinematic`
- **Mid-Air Tucked Knees Dynamic**: `e030_b01_dynamic`, `e030_b04_dynamic`
- **Balancing/Leg Extension Fullbody**: `e030_b01_fullbody`, `e030_b04_fullbody`

## Recommendations for the next cycle

- Enforce the 'No Static Bracing' rule strictly for Cinematic and Fullbody categories; require a secondary active movement.
- Limit direct gaze into camera to max 1 per batch, and only if accompanied by a specific physical reaction.
- Ensure Dynamic premises have distinct pose structures (e.g., one spinning, one diving, one leaping) rather than repeating the same mid-air tuck.
- Replace vague causes like 'shockwave' or 'atmosphere' with visible physical objects or forces.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e030_b01_closeup` | closeup | 9.0 | 8.0 | 9.0 | 9.0 | Strong causal link (steam jet) and specific micro-reaction. Identity is clear with blindfold/hairband details. |
| `e030_b01_medium` | medium | 8.0 | 7.0 | 8.0 | 8.0 | Good dynamic twist and interaction with environment (crate). Avoids static bracing. |
| `e030_b01_fullbody` | fullbody | 9.0 | 9.0 | 7.0 | 8.0 | Strong silhouette and body appeal. The 'preparing to swing' action is slightly passive but the balance pose is strong. |
| `e030_b01_dynamic` | dynamic | 7.0 | 8.0 | 6.0 | 9.0 | 'Invisible shockwave' is a weak cause; the viewer cannot infer why she was launched. Motion blur helps but causality is vague. |
| `e030_b01_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | Static 'standing still' pose. Relies on environment scale rather than character action. Violates anti-pattern of passive observation. |
| `e030_b02_closeup` | closeup | 8.0 | 7.0 | 5.0 | 4.0 | 'Tilts head... rather than flinching' is a passive reaction to an ember. Lacks active physical consequence or strong causal urgency. |
| `e030_b02_medium` | medium | 8.0 | 7.0 | 8.0 | 7.0 | Good physical interaction (lever). Clear cause and effect. Identity maintained. |
| `e030_b02_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 9.0 | Excellent dynamic pose (slide). Clear cause (falling piston) and consequence (avoidance). Strong visual appeal. |
| `e030_b02_dynamic` | dynamic | 8.0 | 8.0 | 7.0 | 9.0 | Strong kinetic energy. Using a gear as a shield is a specific interaction. Good motion blur usage. |
| `e030_b02_cinematic` | cinematic | 7.0 | 6.0 | 4.0 | 3.0 | 'Looks up directly into camera' is a direct gaze substitute for interaction. Static pose. Weak micro-story. |
| `e030_b03_closeup` | closeup | 9.0 | 8.0 | 8.0 | 7.0 | Specific cause (coolant shard). Good micro-reaction (brushing away fragments). Identity clear. |
| `e030_b03_medium` | medium | 8.0 | 7.0 | 8.0 | 8.0 | Strong physical interaction with leaking pipe. Clear cause and reaction. |
| `e030_b03_fullbody` | fullbody | 9.0 | 8.0 | 6.0 | 7.0 | 'Step over sludge' is borderline generic locomotion. Lacks a strong narrative stake or immediate threat beyond the obstacle itself. |
| `e030_b03_dynamic` | dynamic | 8.0 | 8.0 | 7.0 | 9.0 | Mid-swing on cable is dynamic. Clear intent (vault over sparks). Good motion potential. |
| `e030_b03_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | 'Looks down at reflection' is passive observation. The ripple cause is weak. Static pose. |
| `e030_b04_closeup` | closeup | 9.0 | 8.0 | 8.0 | 8.0 | Strong cause (magnetic clamp). Specific physical effect on hair. Good micro-reaction. |
| `e030_b04_medium` | medium | 8.0 | 7.0 | 8.0 | 7.0 | Catching a swinging pipe is a good physical interaction. Clear cause and reaction. |
| `e030_b04_fullbody` | fullbody | 9.0 | 8.0 | 6.0 | 7.0 | 'Testing stability' is a passive preparatory action. Similar to b01_fullbody in structure (balancing/leg extension). |
| `e030_b04_dynamic` | dynamic | 8.0 | 7.0 | 6.0 | 9.0 | Very similar to e030_b01_dynamic (mid-air, tucked knees, flared sleeves). Repetition of the 'launched/leaping' dynamic pose. |
| `e030_b04_cinematic` | cinematic | 7.0 | 6.0 | 5.0 | 4.0 | Nearly identical to e030_b01_cinematic (low angle, standing still on grating/platform). Repetition of static cinematic pose. |

## Premises

### e030_b01_closeup — closeup

2B's black blindfold is being pushed aside by a sudden, high-pressure jet of steam erupting from a ruptured industrial valve near her shoulder; her left hand snaps up to steady the fabric against the heat while her visible eye widens in controlled alarm as scalding droplets splatter across her cheek and hairband.

### e030_b01_medium — medium

2B is caught mid-dodge from a swinging chain link hanging off a broken catwalk railing; her torso twists sharply to the left, pulling her black dress against her body as she grips the edge of a metal crate for leverage, her expression tight with focus rather than panic.

### e030_b01_fullbody — fullbody

2B is balancing on one leg atop a crumbling concrete pillar in an overgrown urban ruin, stretching her other leg high to hook onto a low-hanging vine; the twist emphasizes her silhouette and thigh-high stockings as she prepares to swing across a gap where the ground has just collapsed.

### e030_b01_dynamic — dynamic

2B is in mid-air, having been launched backward by an invisible shockwave; her puffy sleeves are flaring from the air resistance and her hair is whipping forward as she tucks her knees to protect herself, with motion blur trailing behind her to indicate rapid displacement.

### e030_b01_cinematic — cinematic

A low-angle shot from below looks up at 2B standing on a tilting, fractured platform in a vast industrial shaft; she remains perfectly still and composed while the structure groans and cracks around her feet, emphasizing her stability against the chaotic scale of the collapsing environment.

### e030_b02_closeup — closeup

A close-up of 2B's face as a stray, glowing ember from a nearby furnace drifts toward her; she tilts her head slightly to the side rather than flinching, letting the heat wash over her skin while her visible eye remains steady and unblinking, with faint wisps of smoke curling around the edge of her black blindfold.

### e030_b02_medium — medium

2B is waist-up, actively pulling a heavy, rusted lever with both gloved hands to counterbalance the tilt of a sinking cargo crate; her torso twists against the resistance, emphasizing the tension in her puffy sleeves and the cutout detail of her dress as she holds her breath in controlled effort.

### e030_b02_fullbody — fullbody

2B is captured mid-slide on one knee across a slick, oily metal floor to avoid a falling hydraulic piston; her body is angled low with one leg extended forward and the other bent behind her, showcasing the length of her thigh-high stockings as she uses her momentum to pivot away from the impact zone.

### e030_b02_dynamic — dynamic

2B is spinning rapidly in a low crouch, using a large, broken gear as a shield against a volley of sparks; her hair and dress hem are whipped into a circular blur by the rotation, while her arm extends outward to grip the metal edge, capturing the raw kinetic energy of the defensive maneuver.

### e030_b02_cinematic — cinematic

A high-angle shot looking down through a circular industrial vent at 2B, who is standing on a narrow maintenance beam below; she looks up directly into the camera lens with composed intensity, her figure small but centered against the vast, dark machinery surrounding her, highlighting her isolation and focus.

### e030_b03_closeup — closeup

A close-up on 2B's face as a jagged shard of crystallized coolant shatters against the edge of her black blindfold; she does not flinch but her visible eye sharpens with cold precision, one gloved finger instinctively rising to brush away the refracting fragments before they slide down her cheek.

### e030_b03_medium — medium

2B is waist-up, leaning forward to steady a heavy, leaking pipe that has snapped free and is spraying pressurized water directly into her face; she grips the metal with both hands, her torso twisting against the sudden torque as droplets bead on her skin and hairband.

### e030_b03_fullbody — fullbody

2B is captured in a deep lunge, one leg extended far forward to step over a rising wave of viscous sludge while her back leg pushes off the ground; her dress hem lifts slightly with the motion, highlighting the tension in her thigh-high stockings and boots as she maintains perfect balance.

### e030_b03_dynamic — dynamic

2B is mid-swing on a broken cable, her body extended horizontally with one arm fully outstretched; her puffy sleeves catch the air and flare outward, creating a dramatic silhouette as she uses momentum to vault over a low barrier of sparks.

### e030_b03_cinematic — cinematic

A Dutch-angle shot tilts the horizon, showing 2B standing on a fractured metal grating; she looks down at her reflection in a puddle of oil that is rippling from a nearby impact, her composed expression contrasting with the distorted, wavering image below.

### e030_b04_closeup — closeup

A close-up of 2B's face as a heavy, magnetic clamp descends rapidly from above; her head tilts back sharply to avoid the impact, causing her short white hair to puff outward against the force while her visible eye squints in sharp, controlled focus, and a thin strand of hair is visibly pulled upward by the static charge.

### e030_b04_medium — medium

2B is waist-up, leaning backward with one arm extended to catch a heavy, swinging pipe that has just broken free; her torso arches against the sudden weight, tightening the fabric of her black dress across her shoulders as her gloved hand grips the metal firmly, her expression locked in intense concentration rather than surprise.

### e030_b04_fullbody — fullbody

2B is captured mid-crouch on a narrow ledge, extending one leg far forward to test the stability of a cracked stone before committing her weight; her body is low and centered, emphasizing the length of her thigh-high stockings and boots as she prepares to leap across a widening chasm where the floor has just given way.

### e030_b04_dynamic — dynamic

2B is in mid-air, having just leaped over a burst of pressurized steam; her puffy sleeves are flared outward from the impact and her hair is whipping backward as she tucks her knees to protect herself, with motion blur trailing behind her to indicate rapid displacement away from the scalding cloud.

### e030_b04_cinematic — cinematic

A low-angle shot looks up at 2B standing on a fractured metal grating, her figure silhouetted against a vast, dark industrial shaft; she remains perfectly still and composed while a massive gear turns slowly behind her, emphasizing her stability and focus against the chaotic scale of the moving machinery.
