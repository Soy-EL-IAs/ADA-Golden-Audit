# Ada Viral Guide Evolution — Cycle 020

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.00/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.00 |
| Visual Appeal | 8.00 |
| Diversity | 6.00 |
| Repetition Control | 5.00 |
| Micro Story | 7.00 |
| Animation Potential | 7.00 |

## Verdict

Solid foundation with strong identity preservation and good causal logic in most shots. However, repetition in Closeup and Medium categories, along with weak static Cinematic poses, lowers the overall diversity score. Needs tighter control over hook families and stronger motion implications in wide shots.

## Strengths

- Strong adherence to character identity facts (blindfold, gloves, dress details) across all premises.
- Most premises have clear causal triggers (broken cable, falling gear, swinging piston).
- Good variety in action verbs for full-body and dynamic shots (sliding, lunging, sweeping, spiraling).

## Failures

- Significant repetition in Closeup category: b01_01 and b04_01 are nearly identical concepts (gripping sword during vibration/jolt).
- Repetition in Medium category: b01_02, b03_02, and b04_02 all involve dodging/interacting with industrial hazards causing sleeve flare/sparks.
- Cinematic shots b02_05 and b04_05 are weak 'dangling/clinging' poses that lack clear next-step motion or consequence, bordering on static wallpaper energy.
- Atmospheric elements (mist, dust) often replace specific physical interactions in the cinematic shots.

## Desired patterns

- Causal chains where the environment actively forces a unique character reaction.
- Distinct visual hooks for each category to avoid template fatigue.
- Clear 'next step' implication in all shots, especially static or wide ones.

## Undesired patterns

- Repeated 'hand grip + vibration' closeups.
- Repeated 'industrial hazard + sleeve flare' medium shots.
- Static 'dangling/clinging' cinematic poses without active movement or clear threat progression.
- Atmospheric filler (mist, dust) masking lack of specific interaction.

## Repetition clusters

- **Gripping sword hilt/pommel during vibration/jolt**: `e020_b01_01`, `e020_b04_01`
- **Dodging/Interacting with industrial hazard causing sleeve flare/sparks**: `e020_b01_02`, `e020_b03_02`, `e020_b04_02`
- **Dangling/Clinging to edge with atmospheric filler**: `e020_b02_05`, `e020_b04_05`

## Recommendations for the next cycle

- Differentiate Closeup shots: One should focus on facial micro-expression (b02_01, b03_01 are good), the other on a different physical interaction (e.g., adjusting blindfold due to sweat/dirt, not just gripping sword).
- Vary Medium shot hazards: Avoid three consecutive industrial 'twist/pull' actions. Introduce non-industrial or more personal interactions (e.g., catching a falling object from an ally, reacting to a sudden sound).
- Strengthen Cinematic shots: Replace static dangling with active movement (climbing up, sliding down, jumping off) or clear environmental interaction (wind pushing her against the wall, water rushing past).
- Reduce atmospheric filler: Ensure dust/mist/steam has a specific source and physical effect on the character's position or clothing.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e020_b01_01` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Strong causal link (cable jolt) and specific identity details (gloves, blindfold strap). Good tension. |
| `e020_b01_02` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Clear interaction with environment (piston). Sleeve flare adds visual interest. Slightly generic 'twist to avoid' but effective. |
| `e020_b01_03` | fullbody | 9.0 | 8.0 | 8.0 | 9.0 | Excellent full-body momentum. Catching a crate provides narrative purpose beyond mere locomotion. |
| `e020_b01_04` | dynamic | 8.0 | 7.0 | 6.0 | 7.0 | Steam is a common hazard. 'Navigating the obstacle' is slightly vague on consequence. Hair whipping is a repeated hook. |
| `e020_b01_05` | cinematic | 8.0 | 9.0 | 7.0 | 8.0 | Strong cinematic scale. Sprinting to escape gives clear motivation. Good use of lighting. |
| `e020_b02_01` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Direct hit from water creates immediate physical reaction. 'Controlled discomfort' fits personality well. |
| `e020_b02_02` | medium | 9.0 | 8.0 | 7.0 | 7.0 | Specific interaction with cable. Sparks add danger. Similar to b01_02 in terms of 'avoiding industrial hazard' but distinct action (pulling vs twisting). |
| `e020_b02_03` | fullbody | 9.0 | 8.0 | 7.0 | 8.0 | Low crouch-dodge is a clear action. Wrecking ball is a strong visual anchor. Good weight distribution implied. |
| `e020_b02_04` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | High energy. Deflecting glass shard provides a specific target/consequence. Motion blur enhances dynamic feel. |
| `e020_b02_05` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | Dangling is a static pose unless she's actively climbing or slipping. 'Swirling mist' is atmospheric filler. Lacks clear next step (is she falling? holding on?). |
| `e020_b03_01` | closeup | 9.0 | 7.0 | 8.0 | 7.0 | Gear falling between feet is a specific, close-range threat. Flinch reaction is well-defined. |
| `e020_b03_02` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Very similar to b02_02 (sparking wire/cable near sleeve). Repetition of 'sparks/sleeve' hook. Action is slightly slower/less dynamic than previous medium shots. |
| `e020_b03_03` | fullbody | 9.0 | 8.0 | 8.0 | 7.0 | Lunging to catch a panel is a strong active verb. Saving the light source adds narrative depth. |
| `e020_b03_04` | dynamic | 9.0 | 8.0 | 7.0 | 8.0 | Sweep kick is distinct from previous actions. Shattering glass provides clear consequence. Good dynamic flow. |
| `e020_b03_05` | cinematic | 8.0 | 7.0 | 6.0 | 6.0 | Balancing on a tilting beam is good, but 'arms outstretched' can look like a generic pose. Dust raining down is atmospheric filler. |
| `e020_b04_01` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Very similar to b01_01 (gripping sword hilt/pommel during a jolt/vibration). Repetition of 'hand grip + vibration' hook. |
| `e020_b04_02` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Similar to b01_02 (dodging industrial hazard, sleeve flare). Rebar vs Piston is a minor variation. Repetition of 'twist/lean back + sleeve' hook. |
| `e020_b04_03` | fullbody | 9.0 | 8.0 | 7.0 | 8.0 | Side-step to avoid barrel is clear. 'Maintains perfect balance' is a bit static for the end state, but the motion is implied. |
| `e020_b04_04` | dynamic | 9.0 | 8.0 | 7.0 | 8.0 | Spiral descent is a unique dynamic move. Deflecting concrete chunk is a strong consequence. |
| `e020_b04_05` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | Very similar to b02_05 (dangling/clinging to edge). 'Body stretched out horizontally' is a static pose. Dust/debris filler. |

## Premises

### e020_b01_01 — closeup

Extreme close-up on 2B's gloved hand tightly gripping the hilt of her sword as a sudden jolt from a broken elevator cable vibrates through the metal, causing her knuckles to whiten and her blindfold strap to snap taut against her temple.

### e020_b01_02 — medium

Medium shot of 2B twisting her torso sharply to avoid a swinging industrial piston, causing the puffy feather-trimmed sleeves of her dress to flare outward and revealing the tension in her black gloves as she braces against the impact.

### e020_b01_03 — fullbody

Full-body view of 2B sliding across a polished marble floor to catch a falling crate before it shatters, her thigh-high boots screeching against the surface and her dress hem lifting high due to the momentum.

### e020_b01_04 — dynamic

Mid-air action shot of 2B leaping over a burst pipe jetting superheated steam, her hair whipping wildly in the vapor cloud and her sword drawn with motion blur as she navigates the obstacle.

### e020_b01_05 — cinematic

Wide low-angle shot of a massive rusted gantry collapsing toward 2B, who is small in the frame but illuminated by emergency lights as she sprints across the catwalk to escape the falling debris.

### e020_b02_01 — closeup

Extreme close-up of 2B's face as a sudden burst of high-pressure water from a ruptured pipe hits her directly, forcing her to squint tightly behind the black blindfold and clench her jaw in controlled discomfort while droplets splash off her short white hair.

### e020_b02_02 — medium

Medium shot of 2B forcefully pulling a loose, sparking electrical cable away from her chest to prevent it from tangling in the puffy feather-trimmed sleeves of her dress, her black gloves gripping the metal conduit with visible strain as sparks fly near her shoulder.

### e020_b02_03 — fullbody

Full-body view of 2B performing a low crouch-dodge to slip beneath a swinging wrecking ball in an industrial yard, her thigh-high boots gripping the uneven gravel for traction while her dress hem lifts sharply due to the rapid downward movement.

### e020_b02_04 — dynamic

Dynamic mid-action shot of 2B spinning rapidly to deliver a slash, causing her short white hair and the hem of her black dress to blur into a circular motion as she deflects a thrown shard of glass that shatters against her sword blade.

### e020_b02_05 — cinematic

Wide high-angle shot of 2B dangling from the edge of a crumbling concrete ledge, her arms taut as she hangs over a chasm filled with swirling mist, illuminated by a single flickering emergency light above that highlights her silhouette against the dark void.

### e020_b03_01 — closeup

Extreme close-up of 2B's face as a heavy, rusted gear falls from above and embeds itself in the concrete floor directly between her feet, causing her to flinch with a sharp intake of breath and her short white hair to tremble slightly from the shockwave while she maintains a rigid stare forward.

### e020_b03_02 — medium

Medium shot of 2B forcefully twisting her torso to rip a tangled, sparking wire from the puffy feather-trimmed sleeve of her dress as it begins to char, her black gloved hand gripping the fabric tight while sparks sizzle against her shoulder and her expression remains tightly controlled.

### e020_b03_03 — fullbody

Full-body view of 2B lunging forward to catch a collapsing metal panel with one hand, her other leg extended for balance and her thigh-high boots digging into the dusty ground as she uses her body weight to stop the heavy sheet from crushing a flickering light source beneath it.

### e020_b03_04 — dynamic

Mid-action shot of 2B executing a low sweep kick to shatter a cluster of glass shards on the floor, her short white hair whipping back from the sudden acceleration and her black dress hem flaring upward as she rotates through the motion with intense focus.

### e020_b03_05 — cinematic

Wide low-angle shot of 2B standing on a narrow, suspended beam as the structure groans and begins to tilt violently, her arms outstretched for balance against the dark industrial ceiling above while dust rains down around her small but centered silhouette.

### e020_b04_01 — closeup

Extreme close-up of 2B's gloved hand firmly gripping the pommel of her sword to steady herself against a violent jolt, as a sudden hydraulic hiss from a nearby valve forces her short white hair to ripple and her blindfold strap to tighten with visible tension.

### e020_b04_02 — medium

Medium shot of 2B leaning back sharply to dodge a snapping rebar that whips past her shoulder, causing the puffy feather-trimmed sleeves of her dress to bunch up and revealing the tension in her black gloves as she braces for impact.

### e020_b04_03 — fullbody

Full-body view of 2B executing a deep side-step to avoid a rolling barrel, her thigh-high boots gripping the slick concrete for traction while her dress hem lifts high to reveal her stockings as she maintains perfect balance.

### e020_b04_04 — dynamic

Mid-air action shot of 2B twisting her torso in a spiral descent, using the momentum to deflect a falling concrete chunk with her sword blade as sparks fly and her short white hair blurs into a circular motion.

### e020_b04_05 — cinematic

Wide high-angle shot of 2B clinging to the edge of a rusted industrial platform as it tilts violently, her body stretched out horizontally against the dark machinery below while dust and debris rain down around her small but centered silhouette.
