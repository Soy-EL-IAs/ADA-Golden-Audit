# Ada Viral Guide Evolution — Cycle 027

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.83/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.00 |
| Visual Appeal | 8.50 |
| Diversity | 7.00 |
| Repetition Control | 6.00 |
| Micro Story | 8.00 |
| Animation Potential | 8.50 |

## Verdict

Strong batch with high visual appeal and animation potential. Main weakness is mechanical repetition in climbing/wind interactions across categories. Identity preservation is excellent.

## Strengths

- Strong adherence to the 'Causal Premise Requirement' with visible causes for most actions.
- Excellent use of secondary motion (hair, fabric, debris) to enhance animation potential.
- Consistent preservation of character identity traits (blindfold, gloves, dress details).
- High kinetic energy in Dynamic and Fullbody categories.

## Failures

- Repetition of 'pulling oneself up/climbing' mechanic across multiple Cinematic and Medium shots (b01_cinematic, b02_cinematic, b04_cinematic).
- Overuse of 'wind/gust' as a primary environmental force in Closeup and Cinematic categories.
- Some premises rely on generic industrial elements (pipes, gears, beams) without distinct location variety.
- Minor canon drifts regarding eye visibility through blindfold.

## Desired patterns

- Active interaction with props or environment that alters the character's position.
- Clear direction of force and secondary motion effects.
- Distinct emotional registers (stoic, focused, strained) rather than generic intensity.

## Undesired patterns

- Passive standing or static poses without causal trigger.
- Repeated 'climbing/pulling up' mechanics in wide shots.
- Atmospheric elements (wind/rain) replacing specific physical interactions.

## Repetition clusters

- **Climbing/Pulling Up on Vertical/Horizontal Structures**: `e027_b01_cinematic`, `e027_b02_cinematic`, `e027_b04_cinematic`
- **Wind/Gust Interaction with Hair/Clothing**: `e027_b01_closeup`, `e027_b01_medium`, `e027_b04_cinematic`
- **Industrial Machinery/Prop Interaction (Pipes, Gears, Turbines)**: `e027_b02_medium`, `e027_b02_cinematic`, `e027_b03_cinematic`

## Recommendations for the next cycle

- Limit 'climbing/pulling up' to one premise per batch; use other vertical mechanics like hanging, swinging, or descending.
- Vary environmental forces beyond wind; include magnetic fields, gravity shifts, or biological elements (vines, roots).
- Introduce more distinct location types (forest, interior office, rooftop) to break the industrial loop.
- Ensure closeups have stronger physical causality than just 'looking' or 'static charge'.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e027_b01_closeup` | closeup | 9.0 | 8.0 | 7.0 | 9.0 | Strong wind interaction. 'Narrowed eyes visible above the fabric' is a minor canon risk (blindfold usually covers eye area), but acceptable as a stylistic choice for visibility. |
| `e027_b01_medium` | medium | 9.0 | 8.0 | 6.0 | 7.0 | Good prop interaction (railing). The 'unseen object' is a weak causal link; the viewer doesn't know what she's looking at. |
| `e027_b01_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 9.0 | Excellent kinetic energy. Sliding mechanic is distinct and well-executed with clear cause (skidding around corner). |
| `e027_b01_dynamic` | dynamic | 8.0 | 9.0 | 7.0 | 9.0 | High kinetic energy. 'Spinning recovery' is a strong dynamic pose. Slight risk of generic combat feel, but the specific action helps. |
| `e027_b01_cinematic` | cinematic | 8.0 | 9.0 | 8.0 | 8.0 | Violates the 'Balancing Loop' anti-pattern slightly by using a beam/rebar, but it's an active pull-up rather than static balance. Good scale. |
| `e027_b02_closeup` | closeup | 9.0 | 8.0 | 8.0 | 6.0 | Strong micro-story (glass shard). However, 'static hair' contradicts the impact event; hair should react. Low animation potential due to static nature. |
| `e027_b02_medium` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Good prop interaction (hydraulic pipe). Clear cause and effect. Water mist adds visual interest. |
| `e027_b02_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 7.0 | Crouching/Dodging mechanic. Good contrast between rigid upper body and pooled dress hem. |
| `e027_b02_dynamic` | dynamic | 9.0 | 9.0 | 8.0 | 9.0 | Excellent 'falling arrest' mechanic. Vine is a generic but visually coherent element. Strong secondary motion (hair swinging up). |
| `e027_b02_cinematic` | cinematic | 8.0 | 9.0 | 8.0 | 8.0 | Scaling a rotating gear is a strong environmental interaction. Distinct from previous climbing actions. |
| `e027_b03_closeup` | closeup | 9.0 | 7.0 | 6.0 | 5.0 | Reflection in mirror is a bit passive. 'Static charge' for hair strand is weak causality compared to physical impact. |
| `e027_b03_medium` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Pulling tarp is a good active gesture. Clear interaction with prop. |
| `e027_b03_fullbody` | fullbody | 9.0 | 9.0 | 8.0 | 9.0 | Mid-leap split position is visually striking. Clear cause (clearing gap) and consequence (pebbles falling). |
| `e027_b03_dynamic` | dynamic | 8.0 | 9.0 | 7.0 | 9.0 | Side-step from sparks is good. Motion blur usage is appropriate. |
| `e027_b03_cinematic` | cinematic | 8.0 | 9.0 | 8.0 | 8.0 | Pressing against turbine blade is a strong 'interacting with large machinery' example. High tension. |
| `e027_b04_closeup` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Droplet on hairband is a nice detail. 'Pupils contract behind gaps' is a slight canon stretch but acceptable for visual clarity. |
| `e027_b04_medium` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Twisting cable with sparks is a good active gesture. Clear cause and effect. |
| `e027_b04_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 8.0 | Crouching to shield from crate crash. Good use of shockwave dust. |
| `e027_b04_dynamic` | dynamic | 9.0 | 9.0 | 8.0 | 9.0 | Vaulting over barrier. Strong kinetic energy and clear trajectory. |
| `e027_b04_cinematic` | cinematic | 8.0 | 9.0 | 8.0 | 8.0 | Pulling up onto ledge while fighting wind. Combines two forces (gravity and wind) for high tension. |

## Premises

### e027_b01_closeup — closeup

A close-up of 2B's face as a sudden, sharp gust from a broken ventilation shaft forces her short white hair to whip violently across her black blindfold; she tilts her head slightly back with narrowed eyes visible above the fabric, maintaining a stoic expression while her hairband strains against the turbulence.

### e027_b01_medium — medium

A waist-up shot of 2B gripping a rusted metal railing with her black-gloved hands as she leans forward into the wind, her puffy feather-trimmed sleeves billowing out behind her; her posture is tense but controlled, eyes fixed on an unseen object falling past her shoulder.

### e027_b01_fullbody — fullbody

2B is captured mid-slide across a slick, moss-covered stone floor in her thigh-high boots and stockings, knees bent low to absorb the impact of skidding around a corner; debris scatters from her heels as she uses one hand to push off a crumbling wall for stability.

### e027_b01_dynamic — dynamic

A high-kinetic frame showing 2B in the midst of a spinning recovery after dodging an overhead strike, her black dress flaring wide with centrifugal force; motion blur trails behind her swinging arm and fluttering hair as she twists to face the source of the attack.

### e027_b01_cinematic — cinematic

A wide shot from a low angle showing 2B standing on a precarious, tilted beam of rebar extending over a deep chasm; she is actively pulling herself upward using only her upper body strength, legs dangling below the edge as dust and small rocks dislodge from the crumbling structure beneath her boots.

### e027_b02_closeup — closeup

A close-up of 2B's upper torso and face as a jagged shard of black glass embeds itself in the fabric of her puffy sleeve just inches from her shoulder; she holds her breath, jaw tight, eyes narrowing slightly above her blindfold to assess the threat, while fine dust particles from the impact hover suspended in the air around her static hair.

### e027_b02_medium — medium

A waist-up shot of 2B bracing against a sudden hydraulic surge from a ruptured pipe, her black-gloved hand pressed flat against the vibrating metal casing to steady herself; her hairband shifts slightly under the pressure, and her expression remains composed despite the spray of water misting over her dark dress.

### e027_b02_fullbody — fullbody

2B is captured in a deep crouch, one knee pressing into a patch of wet moss on a stone floor as she shields her face with her arm against a shower of falling pebbles from a cracking ceiling; her thigh-high boots grip the slippery surface firmly, and the hem of her dress pools around her legs, contrasting with the rigid tension in her upper body.

### e027_b02_dynamic — dynamic

A high-kinetic frame showing 2B arrested mid-fall by a thick vine wrapped around her wrist, her body suspended horizontally in the air; gravity pulls her legs downward while her hair swings upward against the force of the stop, and leaves scatter from her disturbed stance as she strains to pull herself closer.

### e027_b02_cinematic — cinematic

A wide shot from a low angle showing 2B scaling the side of a massive, rotating industrial gear; she is actively pulling herself upward using her upper body strength, her black dress flapping in the updraft generated by the turning machinery, while debris rains down around her isolated figure against the vast, dark background.

### e027_b03_closeup — closeup

A tight close-up on 2B's face as she sharply turns her head to the side, catching a fleeting glimpse of her own reflection in a shattered mirror pane; her expression is one of sharp, cold scrutiny rather than surprise, with a single strand of white hair sticking out from under her blindfold due to static charge.

### e027_b03_medium — medium

A waist-up shot of 2B aggressively pulling the hem of a torn, heavy industrial tarp away from her torso; her black-gloved hand grips the wet fabric tightly as it flaps violently in the draft, revealing the tension in her shoulder muscles and the crispness of her puffy sleeves against the chaotic movement.

### e027_b03_fullbody — fullbody

2B is captured mid-leap over a wide, rusted drainage grate, her body stretched horizontally in a split position to clear the gap; her thigh-high boots are extended forward while her hands trail back for balance, with small pebbles falling from the edge of the grate she has just cleared.

### e027_b03_dynamic — dynamic

A high-kinetic frame showing 2B executing a rapid side-step to avoid a sweeping arc of sparks from a grinding saw blade; her body is twisted sharply in profile, motion blur trailing behind her swinging arm and the fluttering hem of her dress as she moves into open space.

### e027_b03_cinematic — cinematic

A wide shot from a low angle showing 2B pressing both palms flat against a massive, spinning turbine blade to slow its rotation; her body is braced against the immense torque, hair whipping sideways in the updraft she creates, while dust and oil spray off the metal surface around her.

### e027_b04_closeup — closeup

A tight close-up on 2B's face as a high-pitched mechanical whine causes her pupils to contract sharply behind the gaps of her black blindfold; a single, sharp droplet of condensation from a dripping pipe above lands directly on her hairband, leaving a distinct wet mark that contrasts with the dry fabric, while her jaw remains rigidly set in silent calculation.

### e027_b04_medium — medium

A waist-up shot of 2B leaning heavily against a vibrating, rusted support pillar to steady her grip on a loose cable; her black-gloved hand twists the wire with intense focus as sparks fly from the contact point near her shoulder, illuminating the tension in her puffy feather-trimmed sleeves and the slight strain in her expression.

### e027_b04_fullbody — fullbody

2B is captured in a deep, low crouch on a patch of loose gravel, shielding her upper body with one arm as a heavy metal crate crashes onto the ground just behind her; her thigh-high boots dig into the shifting terrain to prevent sliding back, and her hair whips upward from the shockwave dust cloud rising around her static stance.

### e027_b04_dynamic — dynamic

A high-kinetic frame showing 2B mid-air after vaulting over a low barrier, her body stretched horizontally with legs extended forward and arms trailing back for momentum; motion blur streaks behind her as she twists to prepare for a landing on the unstable surface ahead, her dress flaring dramatically in the rush of air.

### e027_b04_cinematic — cinematic

A wide shot from a low angle showing 2B actively pulling herself up onto a precarious ledge using her upper body strength, with one leg still dangling in the void below; she is bracing against a sudden gust of wind that pushes her backward, causing her hair and dress to snap violently as she fights to maintain her grip on the crumbling edge.
