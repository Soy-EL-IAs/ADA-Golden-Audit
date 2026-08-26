# Ada Viral Guide Evolution — Cycle 022

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

The set is strong in identity preservation and visual appeal but suffers from moderate repetition in specific action verbs (prying, fluid blasts) and reliance on atmospheric filler. The causal chains are generally clear, but some reactions are passive. With minor adjustments to break the repetition clusters, this would be a high-quality batch.

## Strengths

- Strong adherence to character identity facts (blindfold, gloves, dress details) across all premises.
- Most premises have clear causal triggers (valve resistance, projectile, steam burst).
- Good variety in camera angles and shot types as required by the dataset structure.

## Failures

- Significant repetition of 'prying/opening jammed metal' concepts in b03_medium and b04_medium.
- Repetition of 'fluid blast causing head tilt' in b02_closeup and b03_closeup.
- Several premises rely on 'dust/sparks' as the primary visual hook rather than the character's action (b01_cinematic, b03_cinematic).
- Some actions are passive reactions (holding breath, tilting head) rather than active physical manipulation.

## Desired patterns

- Active verbs like 'bracing', 'catching', 'pulling', 'prying' that show the character exerting force.
- Clear secondary consequences of actions (clothing snagging, hair whipping, boots sliding).
- Distinct environmental interactions that are not just 'standing in ruins'.

## Undesired patterns

- Repeated use of 'prying open jammed panels'.
- Repeated use of 'fluid/steam blasts causing head tilt'.
- Atmospheric filler (dust, sparks) replacing specific physical interactions.
- Passive poses like 'gripping a cable' without visible resistance or change.

## Repetition clusters

- **Prying/Open Jammed Metal**: `e022_b03_medium`, `e022_b04_medium`
- **Fluid Blast/Head Tilt**: `e022_b02_closeup`, `e022_b03_closeup`
- **Heavy Door/Hatch Interaction**: `e022_b01_medium`, `e022_b02_cinematic`

## Recommendations for the next cycle

- Replace one of the 'prying' premises with a different upper-body dynamic, such as 'striking', 'shielding', or 'reaching'.
- Differentiate the closeup fluid blasts by changing the reaction (e.g., one is active dodging, the other is bracing against pressure).
- Reduce reliance on dust/sparks; focus more on the character's physical strain and clothing interaction.
- Ensure 'gripping' actions have a visible counter-force or movement to avoid static poses.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e022_b01_closeup` | closeup | 8.0 | 7.0 | 8.0 | 6.0 | Strong causal link (resisting valve). Good identity markers. Slight risk of 'strain' becoming generic if not visually distinct. |
| `e022_b01_medium` | medium | 9.0 | 8.0 | 9.0 | 7.0 | Excellent dual-action (bracing + catching). Clear cause and consequence. Strong personality expression through multitasking under pressure. |
| `e022_b01_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 7.0 | Good use of environment (vent duct). Clothing interaction is logical. Avoids static pose. |
| `e022_b01_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | High energy. Clear cause (projectile). Motion is well-described with specific physical consequences (hair, boots). |
| `e022_b01_cinematic` | cinematic | 8.0 | 7.0 | 7.0 | 6.0 | Active interaction (pulling lever). However, 'dust plumes' is a common filler element. The action is strong but visually standard for the genre. |
| `e022_b02_closeup` | closeup | 8.0 | 7.0 | 6.0 | 5.0 | Steam burst is a valid cause. However, 'tilting head back' and 'holding breath' are somewhat passive reactions compared to active physical manipulation. |
| `e022_b02_medium` | medium | 9.0 | 8.0 | 8.0 | 6.0 | Good defensive action. Shielding face is a clear reaction to light. Sparks on sleeves add visual texture. |
| `e022_b02_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 6.0 | Stepping over rebar is a minor obstacle. The 'snagging' adds consequence, but it borders on the 'Locomotion Filler' anti-pattern if not clearly part of an escape sequence. |
| `e022_b02_dynamic` | dynamic | 9.0 | 8.0 | 8.0 | 8.0 | Catching a falling gear is a strong active verb. The physical strain (arms pulled down) creates good visual tension. |
| `e022_b02_cinematic` | cinematic | 8.0 | 7.0 | 7.0 | 6.0 | Pushing a closing hatch is active. However, it shares the 'heavy metal door' conceptual family with b01_medium and b04_medium. |
| `e022_b03_closeup` | closeup | 8.0 | 7.0 | 6.0 | 5.0 | Very similar to b02_closeup (steam/coolant jet causing head tilt). Repetition of the 'fluid blast' hook. |
| `e022_b03_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Prying panels is a strong action. However, it overlaps conceptually with b04_medium (prying open jammed panel). Repetition of 'prying' verb. |
| `e022_b03_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 7.0 | Sliding on a ledge is dynamic. Good use of weight shift and clothing flare. |
| `e022_b03_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 8.0 | Spinning to evade is high energy. Clear cause (chain). Good motion description. |
| `e022_b03_cinematic` | cinematic | 9.0 | 8.0 | 7.0 | 6.0 | Hanging from a ladder is distinct. Good silhouette. However, 'dust rains down' is filler. |
| `e022_b04_closeup` | closeup | 8.0 | 7.0 | 6.0 | 5.0 | Gripping a cable is static. Lacks the 'resistance' or 'change' seen in b01_closeup (valve turning). Feels like a pose rather than an event. |
| `e022_b04_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Direct repetition of the 'prying open jammed panel' concept from b03_medium. The verb 'pry' is used again. |
| `e022_b04_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 6.0 | Crawling is a good variation. However, 'scanning for an exit' is vague. The physical action (crawling) is the main hook. |
| `e022_b04_dynamic` | dynamic | 9.0 | 8.0 | 6.0 | 7.0 | Leaping over a crack is a clear action. However, 'minimizing air resistance' is a bit technical/unnatural for the character's style. |
| `e022_b04_cinematic` | cinematic | 9.0 | 8.0 | 7.0 | 6.0 | Hanging by one hand is a strong silhouette. Distinct from other cinematic shots. |

## Premises

### e022_b01_closeup — closeup

Close-up on 2B's gloved hand gripping a rusted control valve as it resists turning, her knuckles whitening with strain while a single bead of sweat traces down her temple, revealing the tightness in her jaw behind her black blindfold.

### e022_b01_medium — medium

Medium shot showing 2B bracing her shoulder against a heavy sliding steel door to keep it from closing, her puffy sleeves bunching as she pushes with one arm while catching a falling data chip in her other hand.

### e022_b01_fullbody — fullbody

Full-body view of 2B crouching low under a sparking ventilation duct, dragging the hem of her black dress across the metal grate as she reaches forward to grab a loose cable for leverage.

### e022_b01_dynamic — dynamic

Dynamic shot of 2B mid-dodge, her body twisted sharply to the left as a projectile grazes her shoulder, causing her short white hair to whip forward and her thigh-high boots to slide against the concrete floor.

### e022_b01_cinematic — cinematic

Wide cinematic angle of 2B pulling on a massive rusted lever to release hydraulic pressure, her entire body weight thrown back against the resistance as dust plumes erupt from the mechanism around her boots.

### e022_b02_closeup — closeup

Close-up on 2B's face as a sudden burst of steam from a ruptured pipe blasts upward, forcing her to tilt her head back sharply; the force ripples through her short white hair and presses against her black blindfold, revealing a single crack in her composure as she holds her breath.

### e022_b02_medium — medium

Medium shot of 2B shielding her face with one gloved hand against a blinding flash of light from a malfunctioning console, while her other hand grips the edge of the metal panel to steady herself as sparks shower down onto her puffy feather-trimmed sleeves.

### e022_b02_fullbody — fullbody

Full-body view of 2B stepping over a low, jagged rebar trap on the floor, her black dress hem snagging briefly on a sharp edge before she yanks free with a controlled motion, her thigh-high stockings stretching as she maintains balance without breaking stride.

### e022_b02_dynamic — dynamic

Dynamic shot of 2B lunging forward to catch a falling mechanical gear with both hands, her body stretched low and taut as the weight pulls her arms down, causing her hairband to slip slightly and her boots to slide backward on the slick concrete.

### e022_b02_cinematic — cinematic

Wide cinematic angle of 2B pushing open a massive, rusted steel hatch that is slowly beginning to close on her, her body braced against the heavy door as hydraulic hisses erupt from the sides and dust swirls around her boots.

### e022_b03_closeup — closeup

Close-up on 2B's face as a sudden, high-pressure jet of coolant erupts from a fractured pipe directly in front of her, forcing her to tilt her head sharply upward; the cold mist beads on her skin and clumps her short white hair against her cheeks, while her jaw clenches tight behind the black blindfold to maintain composure.

### e022_b03_medium — medium

Medium shot of 2B reaching up with both arms extended high to pry apart two jammed, rusted metal panels that are slowly squeezing together; her puffy feather-trimmed sleeves stretch taut as she applies force, and a single drop of sweat rolls from her brow onto the back of her black glove.

### e022_b03_fullbody — fullbody

Full-body view of 2B sliding sideways along a narrow, unstable ledge to avoid a collapsing section of the floor ahead; her thigh-high boots grip the edge for traction while her black dress flares out from the sudden shift in weight, revealing the tension in her posture as she navigates the drop.

### e022_b03_dynamic — dynamic

Dynamic shot of 2B spinning rapidly to evade a swinging chain link that slams into the concrete floor just inches from her heels; her hair whips in a full arc, creating a blurred white streak, while her body remains low and centered to minimize her silhouette.

### e022_b03_cinematic — cinematic

Wide cinematic angle of 2B pulling down a massive, corroded fire escape ladder from above; her entire body is suspended in mid-air, arms fully extended to support the heavy iron weight, as dust rains down onto the concrete floor below and her legs dangle freely against the dark background.

### e022_b04_closeup — closeup

Close-up on 2B's gloved hand as she firmly grips a frayed electrical cable, her fingers digging into the rubber insulation to stop it from slipping off a corroded terminal post; the tension in her wrist pulls at the cuff of her black glove while a stray spark sizzles near her knuckles.

### e022_b04_medium — medium

Medium shot of 2B leaning forward aggressively, using both hands to pry open a jammed maintenance panel that is stuck shut by dried rust; her puffy feather-trimmed sleeves compress as she applies downward force, and her expression remains tightly controlled despite the strain visible in her shoulders.

### e022_b04_fullbody — fullbody

Full-body view of 2B crawling on all fours through a low, debris-filled trench to avoid overhead hazards; her black dress hem drags across the rough gravel, and her thigh-high boots slide backward as she pushes forward with one arm while scanning for an exit.

### e022_b04_dynamic — dynamic

Dynamic shot of 2B leaping over a sudden crack in the floor, her body stretched horizontally in mid-air as she clears the gap; her short white hair flows backward from the momentum, and her boots are pointed forward to minimize air resistance during the jump.

### e022_b04_cinematic — cinematic

Wide cinematic angle of 2B hanging by one hand from a broken overhead beam, swinging her body to reach across a chasm; her legs dangle freely with feet pointed down, and her other arm is fully extended toward a protruding metal handle on the opposite side.
