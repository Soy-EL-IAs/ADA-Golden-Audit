# Ada Viral Guide Evolution — Cycle 033

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 6.67/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.00 |
| Visual Appeal | 8.00 |
| Diversity | 5.00 |
| Repetition Control | 4.00 |
| Micro Story | 7.00 |
| Animation Potential | 7.00 |

## Verdict

The set has strong individual premise quality regarding identity and causality, but fails significantly on batch-level diversity due to three exact duplicates and repetitive mechanical hooks. The cinematic category is weak on narrative consequence.

## Strengths

- Strong adherence to character identity and personality guardrails across all premises.
- Effective use of fabric physics (sleeves, dress hem) to enhance visual appeal and imply motion.
- Clear causal triggers in most premises, avoiding abstract 'vibes'.
- Good variety in dynamic verbs (vault, dive, backflip).

## Failures

- Three exact duplicates in the b03 block (fullbody, dynamic, cinematic) copied from previous blocks.
- Repetition of 'prying' mechanic in medium shots (b02 and b03).
- Cinematic shots tend to be passive or lack strong narrative consequence (hanging, stepping over debris).
- Location distinction rule likely violated with multiple industrial/ruined facility settings without clear differentiation.

## Desired patterns

- Unique mechanical hooks for each premise.
- Active character agency in cinematic shots rather than passive observation or simple locomotion.
- Distinct environmental contexts that change the type of interaction (e.g., water, fire, gravity shift) rather than just 'industrial ruins'.

## Undesired patterns

- Exact copy-paste of premises across blocks.
- Passive balancing or locomotion without narrative stake.
- Repeating the same physical interaction type (prying, catching) too frequently.

## Repetition clusters

- **Exact Duplicate: Stepping off crumbling ledge onto narrow beam**: `e033_b01_fullbody`, `e033_b03_fullbody`
- **Exact Duplicate: Low-dive beneath swinging chain of debris**: `e033_b02_dynamic`, `e033_b03_dynamic`
- **Exact Duplicate: Hanging from frayed cable in industrial shaft**: `e033_b02_cinematic`, `e033_b03_cinematic`
- **Similar Mechanic: Prying open jammed/rusted object with gloved hands**: `e033_b02_medium`, `e033_b03_medium`

## Recommendations for the next cycle

- Eliminate all exact duplicates; ensure each premise has a unique core mechanic.
- Vary the 'medium' shot interactions beyond prying/bracing (e.g., manipulating controls, inspecting damage, interacting with another entity).
- Strengthen cinematic shots by adding specific narrative stakes or active problem-solving rather than just scale or locomotion.
- Ensure location diversity is explicit and distinct (e.g., one in a flooded basement, one on a rooftop garden, one inside a server room) to avoid the 'industrial ruin' monotony.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e033_b01_closeup` | closeup | 9.0 | 8.0 | 9.0 | 7.0 | Strong causal link (shard impact). 'Controlled frustration' fits personality. Dust adds visual texture. |
| `e033_b01_medium` | medium | 9.0 | 8.0 | 8.0 | 7.0 | Good use of fabric physics (sleeves billowing). Clear cause (steam/pressure). |
| `e033_b01_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 7.0 | Specific balance challenge. Cause (slip on gravel) is visible and logical. |
| `e033_b01_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | High energy. 'Vault' is a distinct verb. Clear obstacle (snapping conduit). |
| `e033_b01_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | Scale is good, but 'reaching down' from a high platform to pull a cable on the ground is physically awkward without more context. Slightly static. |
| `e033_b02_closeup` | closeup | 9.0 | 8.0 | 8.0 | 6.0 | Steam/heat cause is clear. Condensation on blindfold is a nice detail. |
| `e033_b02_medium` | medium | 9.0 | 8.0 | 8.0 | 7.0 | Prying action is specific. Strain is visible in sleeves and posture. |
| `e033_b02_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 8.0 | Leap across gap is dynamic. 'Split position' might be slightly unrealistic for a quick leap but visually striking. |
| `e033_b02_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Low-dive is distinct. Friction sparks add visual interest. |
| `e033_b02_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | Hanging from cable is a common trope. 'Swinging wide' is passive compared to active dodging. |
| `e033_b03_closeup` | closeup | 9.0 | 7.0 | 8.0 | 6.0 | Mud splatter is a strong visual hook. 'Calculated frustration' fits well. |
| `e033_b03_medium` | medium | 9.0 | 8.0 | 8.0 | 7.0 | Prying grate is similar to b02_medium (prying hatch). Repetition of 'pry' mechanic. |
| `e033_b03_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 7.0 | EXACT DUPLICATE of e033_b01_fullbody. Major repetition failure. |
| `e033_b03_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | EXACT DUPLICATE of e033_b02_dynamic. Major repetition failure. |
| `e033_b03_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | EXACT DUPLICATE of e033_b02_cinematic. Major repetition failure. |
| `e033_b04_closeup` | closeup | 9.0 | 8.0 | 8.0 | 6.0 | Coolant drip is a good specific cause. 'Controlled shock' fits personality. |
| `e033_b04_medium` | medium | 9.0 | 8.0 | 8.0 | 7.0 | Twisting to avoid sliding panel is a good dynamic reaction. Distinct from previous mediums. |
| `e033_b04_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 8.0 | Catching toolbox is a 'catching object' hook. Distinct from balance/leap hooks. |
| `e033_b04_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Backflip is a distinct verb. Good kinetic energy. |
| `e033_b04_cinematic` | cinematic | 8.0 | 7.0 | 5.0 | 4.0 | 'Stepping over debris' is flagged as 'Locomotion Filler' in the guide. Weak micro-story. |

## Premises

### e033_b01_closeup — closeup

Close-up on 2B's face as a sharp shard of glass shatters against her blindfold, causing her to wince and tighten her jaw in controlled frustration; the impact sends a fine spray of dust particles drifting across her cheek, catching the light while she remains still to assess the damage.

### e033_b01_medium — medium

Medium shot of 2B bracing her gloved hand against a vibrating industrial pipe that is leaking steam; she leans into the force with focused determination, her puffy feather-trimmed sleeves billowing outward from the pressure wave, while she twists her torso to steady her balance.

### e033_b01_fullbody — fullbody

Full-body view of 2B stepping off a crumbling ledge onto a narrow beam, her weight shifting sharply to the left as one thigh-high boot slips on loose gravel; she extends an arm to catch herself against the adjacent wall, her dress hem flaring from the sudden deceleration.

### e033_b01_dynamic — dynamic

2B vaults over a sparking electrical conduit that snaps upward, twisting her body mid-air to clear the arc; her hairband holds her short white hair in place as she tucks her knees, creating a tight silhouette against the chaotic background of flying debris.

### e033_b01_cinematic — cinematic

Low-angle cinematic shot looking up at 2B as she stands on a high platform, reaching down to pull a dangling cable that is dragging across the ground below; the scale of the ruined tower dwarfs her figure, emphasizing her isolated agency as she yanks the line with visible effort.

### e033_b02_closeup — closeup

Extreme close-up of 2B's profile as a burst of hot steam from a fractured valve forces her to tilt her head sharply back; the sudden heat causes visible beads of condensation to form and slide down her black blindfold, while her jaw tightens in stoic endurance against the scalding mist.

### e033_b02_medium — medium

Medium shot of 2B leaning forward to pry open a jammed maintenance hatch with her gloved hands; she braces her feet against the corroded floor, her puffy sleeves compressing under the muscular strain as she twists her wrists to overcome the rusted lock's resistance.

### e033_b02_fullbody — fullbody

Full-body view of 2B mid-stride, leaping across a widening gap in the floor where a support beam has snapped; her legs are fully extended in a split position to bridge the distance, her dress hem whipping upward from the momentum as she reaches for the solid ground on the other side.

### e033_b02_dynamic — dynamic

2B executes a rapid low-dive beneath a swinging chain of debris, flattening her torso against the rough concrete ground; friction sends sparks and dust flying from her thigh-high boots as she slides across the surface to escape the descending weight.

### e033_b02_cinematic — cinematic

High-angle cinematic shot looking down into a deep industrial shaft where 2B hangs from a single frayed cable, swinging wide to avoid a falling crate; the massive scale of the surrounding machinery emphasizes her precarious position as she grips the rope with one hand, her body rotating in mid-air.

### e033_b03_closeup — closeup

Extreme close-up of 2B's face as a heavy clump of wet mud splatters directly onto her black blindfold, obscuring her vision; she tilts her head slightly to the side in calculated frustration, tightening the muscles around her jaw as she blinks rapidly through the hairband to clear the moisture from her lashes.

### e033_b03_medium — medium

Medium shot of 2B crouching low over a cracked floor panel, using her gloved hands to pry up a loose metal grate that is vibrating from an unseen impact below; the sudden release of pressure sends a puff of dust into her face, causing her to pinch her nose and hold her breath while her puffy sleeves gather around her arms.

### e033_b03_fullbody — fullbody

Full-body view of 2B stepping off a crumbling ledge onto a narrow beam, her weight shifting sharply to the left as one thigh-high boot slips on loose gravel; she extends an arm to catch herself against the adjacent wall, her dress hem flaring from the sudden deceleration.

### e033_b03_dynamic — dynamic

2B executes a rapid low-dive beneath a swinging chain of debris, flattening her torso against the rough concrete ground; friction sends sparks and dust flying from her thigh-high boots as she slides across the surface to escape the descending weight.

### e033_b03_cinematic — cinematic

High-angle cinematic shot looking down into a deep industrial shaft where 2B hangs from a single frayed cable, swinging wide to avoid a falling crate; the massive scale of the surrounding machinery emphasizes her precarious position as she grips the rope with one hand, her body rotating in mid-air.

### e033_b04_closeup — closeup

Extreme close-up of 2B's face as a single drop of thick, viscous coolant drips from an overhead pipe directly onto her black blindfold; the sudden cold impact causes her eyes to widen slightly behind the fabric and her breath to hitch in controlled shock, while fine droplets of condensation bead up on the dark material before sliding down toward her jaw.

### e033_b04_medium — medium

Medium shot of 2B twisting sharply to her right as a loose panel of corrugated metal slides out from under her foot; she pivots on the ball of one thigh-high boot to maintain balance, her puffy feather-trimmed sleeves flaring outward with the momentum as she grips the edge of a nearby console for stability, her expression tight with focused urgency.

### e033_b04_fullbody — fullbody

Full-body view of 2B lunging forward to catch a heavy steel toolbox that is tumbling off a high shelf; her arms are extended fully, palms open and ready to absorb the impact, while her weight shifts aggressively onto the balls of her feet, causing her dress hem to lift and reveal the top of her thigh-high stockings in a dynamic display of effort and precision.

### e033_b04_dynamic — dynamic

2B executes a rapid backflip over a low-hanging cable that snaps taut across her path; her body rotates in mid-air, hairband keeping her short white hair secure as she tucks her knees to minimize profile, creating a tight, controlled silhouette against the blurred background of sparking wires.

### e033_b04_cinematic — cinematic

Wide-angle low shot from behind a massive fallen girder as 2B emerges from the dust cloud, stepping over the debris with deliberate precision; her figure is framed against the towering, broken architecture of the ruined facility, emphasizing her steady advance through the chaotic wreckage as she scans for further instability.
