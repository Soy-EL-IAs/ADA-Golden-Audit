# Ada Viral Guide Evolution — Cycle 035

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.17/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 8.50 |
| Visual Appeal | 7.50 |
| Diversity | 6.00 |
| Repetition Control | 5.50 |
| Micro Story | 7.50 |
| Animation Potential | 8.00 |

## Verdict

Solid batch with strong identity and animation potential, but suffers from repetitive hook families (wind/industrial hazards) and limited emotional range. Needs more diverse causes and active interactions to avoid monotony.

## Strengths

- Strong adherence to character identity facts (blindfold, gloves, dress details) across all premises.
- Most premises have clear visible causes for the action (steam, debris, oil, wind).
- Good variety in motion verbs (slide, vault, spin, lunge, twist).
- Effective use of clothing physics (sleeves billowing, hem flaring) to enhance visual appeal.

## Failures

- Repetition of 'wind/air pressure' as a primary hook in b01_medium and b04_fullbody.
- Several premises rely on passive bracing or static aftermath rather than active interaction (b02_closeup, b03_cinematic).
- Locations are often generic industrial ruins without specific unique props to distinguish them.
- Emotional range is limited; most premises show 'focus' or 'irritation', lacking surprise, fear, or playfulness.

## Desired patterns

- Specific mechanical interactions (gears, levers, valves) that directly impact the character's body or gear.
- Clear causal chains where the environment actively threatens or challenges the character.
- Use of clothing and hair to convey motion and force rather than just static aesthetics.

## Undesired patterns

- Generic 'standing in wind' without a specific source (vent, fan) or consequence (clothing distortion).
- Passive observation (watching drone) instead of active reaction.
- Aftermath shots where the action has already concluded (wiping oil) rather than capturing the peak of the event.

## Repetition clusters

- **Wind/Air Pressure Force**: `e035_b01_medium`, `e035_b04_fullbody`
- **Industrial Hazard (Steam/Debris/Cable)**: `e035_b01_medium`, `e035_b02_medium`, `e035_b03_medium`

## Recommendations for the next cycle

- Reduce reliance on wind/air pressure as a primary hook; use more solid mechanical objects (falling gears, snapping chains).
- Introduce more distinct emotional states such as surprise (startling noise), fear (immediate threat), or determination (overcoming obstacle).
- Ensure cinematic shots involve active interaction with the scale element rather than just being small against it.
- Vary locations beyond generic industrial ruins; consider specific NieR environments like the White Tree, Pod stations, or enemy bases.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e035_b01_closeup` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Strong tactile cause (dust) and specific reaction. 'Narrowed eyes beneath' blindfold is a slight visual stretch but acceptable for micro-expression focus. |
| `e035_b01_medium` | medium | 9.0 | 8.0 | 7.0 | 9.0 | Good use of steam as a physical force. Sleeve billowing adds visual interest. Slightly generic 'bracing' but the specific valve rupture saves it. |
| `e035_b01_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 7.0 | Balance challenge is clear. 'Stone ledge' feels slightly out of place for NieR's industrial aesthetic but works as a hazard. |
| `e035_b01_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Clear cause (debris) and consequence (slide). Good motion blur implication. |
| `e035_b01_cinematic` | cinematic | 8.0 | 8.0 | 7.0 | 8.0 | Scale contrast is effective. 'Rotating gear' provides a clear mechanical threat. |
| `e035_b02_closeup` | closeup | 9.0 | 7.0 | 8.0 | 6.0 | Strong narrative detail (oil stain). Animation potential is lower because the action (wiping) has already happened; it's a static aftermath shot. |
| `e035_b02_medium` | medium | 9.0 | 8.0 | 7.0 | 9.0 | Excellent dynamic twist. Cable whip is a specific, visible cause. |
| `e035_b02_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 7.0 | Crouching under conduit is a good spatial interaction. 'Steady gaze forward' is slightly passive but justified by gauging clearance. |
| `e035_b02_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Vaulting over glass is a clear action. Good silhouette emphasis. |
| `e035_b02_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 8.0 | Hanging from crane hook is a classic trope but effective here. 'Crosswind' adds environmental context. |
| `e035_b03_closeup` | closeup | 9.0 | 6.0 | 8.0 | 7.0 | Very specific cause (condensation drop). Visual appeal is lower because it's a very subtle action, but the micro-story is strong. |
| `e035_b03_medium` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Gripping a vibrating lever is a good mechanical interaction. Counter-balance adds body mechanics. |
| `e035_b03_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 9.0 | Skidding on grease is a clear physical hazard. Good weight distribution shift. |
| `e035_b03_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Crouch-spin to dodge laser is a distinct motion verb. Good use of centrifugal force on hair/cloth. |
| `e035_b03_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 6.0 | Pressing back against tower is passive. 'Watching drone' is a weak interaction; she should be reacting to the drone's proximity or heat. |
| `e035_b04_closeup` | closeup | 9.0 | 7.0 | 8.0 | 7.0 | Audio cause (feedback) translated to visual vibration is clever. Good personality expression (suppressed concentration). |
| `e035_b04_medium` | medium | 9.0 | 7.0 | 6.0 | 7.0 | Bending to retrieve component is a valid action but feels slightly generic. 'Stationary machine part' lacks specific hazard. |
| `e035_b04_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 7.0 | Wind from vent is a repeated hook family (see b01_medium). 'Standing rigid' is passive bracing. |
| `e035_b04_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Lunging to catch hook is a strong dynamic action. Clear cause and consequence. |
| `e035_b04_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 7.0 | Hanging from cable over chasm is a high-stakes situation. 'Begins to pull' implies motion. |

## Premises

### e035_b01_closeup — closeup

2B's gloved fingers tense as she pinches the edge of her black blindfold, pulling it slightly askew to wipe away a fine layer of metallic dust that has settled on the fabric, revealing a flash of irritation in her narrowed eyes beneath.

### e035_b01_medium — medium

2B leans her upper body sharply against a rusted vertical pipe to brace herself as a sudden burst of steam from a ruptured valve pushes against her back, causing the puffy feather-trimmed sleeves of her dress to billow outward and distort her silhouette.

### e035_b01_fullbody — fullbody

2B balances precariously on one leg atop a narrow, cracked stone ledge, shifting her center of gravity to keep from slipping as the surface tilts beneath her thigh-high boot, forcing her arms out for stability while maintaining a composed posture.

### e035_b01_dynamic — dynamic

2B executes a rapid low slide across a slick concrete floor to avoid a falling debris chunk, her black dress hem flaring dramatically around her legs and her short white hair blurring with the speed of the maneuver.

### e035_b01_cinematic — cinematic

2B is seen as a small figure clinging to the side of a massive, rotating industrial gear structure, her body pressed flat against the metal as she reaches for a handhold just before the mechanism swings past her position.

### e035_b02_closeup — closeup

2B's black glove is stained with a smear of thick, viscous green oil from a ruptured coolant line she has just wiped against her thigh, causing the fabric of her dress to darken slightly as she frowns in focused concentration at the grime on her knuckles.

### e035_b02_medium — medium

2B twists her torso sharply to the left, pulling her right arm back as a loose cable snaps taut and whips past her ear, causing the puffy feather-trimmed sleeve on that side to stretch tight against her bicep while her hairband resists the pull of her short white hair.

### e035_b02_fullbody — fullbody

2B crouches low to slide under a low-hanging, sparking electrical conduit, her thighs compressed against the tight fit of her stockings and the hem of her dress riding up slightly as she maintains a steady gaze forward to gauge the clearance for her next step.

### e035_b02_dynamic — dynamic

2B vaults over a jagged shard of broken glass, her body airborne and legs tucked tightly to avoid the debris below, with her black dress hem flaring upward from the upward momentum of the jump and her boots pointing toward the landing zone ahead.

### e035_b02_cinematic — cinematic

2B hangs by one hand from a massive, rusted crane hook swinging violently in a crosswind, her body dangling parallel to the ground as she waits for the momentum to reverse before pulling herself up onto the steel beam above.

### e035_b03_closeup — closeup

A single, thick drop of condensation falls from a leaking pipe directly onto the center of 2B's black blindfold, causing her to hold her breath and slightly tilt her chin down as she waits for the fabric to absorb the moisture before it drips into her eye, her jaw tightening with suppressed annoyance.

### e035_b03_medium — medium

2B twists her upper body sharply to the right, extending her left arm fully to grip a vibrating control lever, causing the puffy feather-trimmed sleeve on that side to compress and bunch up while her torso arcs in an exaggerated counter-balance to stabilize her stance against the machine's hum.

### e035_b03_fullbody — fullbody

2B freezes mid-step on a polished, wet metal floor where a layer of grease has caused her right thigh-high boot to skid sideways, forcing her left leg to lunge forward and her arms to swing wildly for balance as she fights to keep her hips from rotating out of alignment.

### e035_b03_dynamic — dynamic

2B performs a rapid, low crouch-spin to dodge a horizontal laser tripwire, her black dress hem whipping in a circular blur around her legs and her short white hair fanning out from the centrifugal force of the turn as she completes the rotation.

### e035_b03_cinematic — cinematic

2B is silhouetted against a towering, glowing coolant tower, pressing her back flat against its cold surface to avoid the heat shimmer rising from below, her arms pinned tight to her sides as she watches a heavy maintenance drone drift slowly past at eye level.

### e035_b04_closeup — closeup

2B's black glove presses firmly against her temple as a high-pitched feedback screech from a nearby broken speaker vibrates through the air, causing the fabric of her blindfold to tremble visibly and her jaw to clench in suppressed concentration.

### e035_b04_medium — medium

2B bends deeply at the waist to retrieve a small, loose component from beneath a heavy, stationary machine part, her torso compressing and the puffy feather-trimmed sleeves of her dress bunching tightly against her upper arms as she reaches with focused precision.

### e035_b04_fullbody — fullbody

2B stands rigid on a narrow, elevated metal beam while a violent gust of wind from an open vent pushes against her broad shoulders, forcing her to widen her stance and plant her thigh-high boots firmly into the grating to prevent being swept off balance.

### e035_b04_dynamic — dynamic

2B lunges forward with explosive speed to catch a swinging industrial hook before it crashes down, her body stretched horizontally in mid-air and her black dress hem streaming backward from the rapid acceleration as she extends one gloved hand to grasp the metal.

### e035_b04_cinematic — cinematic

2B is seen small against a vast, dark chasm where a thin rope bridge has snapped, gripping the fraying end of a cable with one hand while her legs dangle over the abyss as she begins to pull herself upward toward safety.
