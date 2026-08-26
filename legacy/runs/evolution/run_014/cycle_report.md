# Ada Viral Guide Evolution — Cycle 014

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 6.93/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 8.20 |
| Visual Appeal | 7.60 |
| Diversity | 6.50 |
| Repetition Control | 5.80 |
| Micro Story | 6.40 |
| Animation Potential | 7.10 |

## Verdict

Solid batch with strong identity and visual appeal, but suffers from repetitive dynamic actions and cinematic hooks. Needs more variety in causal interactions and less reliance on generic evasion or atmospheric mood pieces.

## Strengths

- Consistent adherence to 2B's visual identity (blindfold, dress, sleeves).
- Strong use of clothing as a causal agent in several premises.
- Dynamic shots have high motion potential and clear directional energy.

## Failures

- Repetition of 'dodging/evasion' dynamic actions across multiple batches.
- Cinematic shots lean heavily on 'catching small object' (petal, butterfly) in ruins, creating a repetitive pattern.
- Some premises rely on atmospheric elements (rain, sun) without strong causal interaction.
- Locomotion filler present in fullbody shots (stepping over cracks, jumping barriers).

## Desired patterns

- Specific object interactions that imply narrative history (e.g., the briefcase, the bird).
- Clothing reacting to physical forces rather than just posing.
- Clear cause-and-effect chains visible in the frame.

## Undesired patterns

- Generic industrial hazards without specific context.
- Static poses in scenic locations (cinematic shots often fail this).
- Repetitive 'dodge' mechanics for dynamic shots.
- Atmospheric mood pieces where the character is passive.

## Repetition clusters

- **Dodging/Evasion Dynamic Action**: `e014_b01_dynamic`, `e014_b02_dynamic`, `e014_b04_dynamic`
- **Catching Small Object in Ruins (Cinematic)**: `e014_b01_cinematic`, `e014_b04_cinematic`
- **Clothing Snag/Interaction (Medium)**: `e014_b01_medium`, `e014_b02_medium`

## Recommendations for the next cycle

- Vary dynamic actions beyond dodging (e.g., throwing, pulling, pushing, climbing).
- Diversify cinematic hooks; avoid 'catching small object' as a default.
- Ensure locomotion shots have clear narrative consequences (escape, pursuit) rather than just obstacle clearance.
- Reduce reliance on atmospheric weather elements unless they directly impact the character's action.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e014_b01_closeup` | closeup | 8.0 | 7.0 | 8.0 | 9.0 | Strong causal link (pulling free). 'Crack in blindfold' is a minor factual stretch but acceptable as damage. Good tension. |
| `e014_b01_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Clothing as causal agent (hem catching). Good visual hook. Slightly generic 'corridor' setting. |
| `e014_b01_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 8.0 | Catching a book is a specific micro-story. Balance on crumbling ledge adds stakes. |
| `e014_b01_dynamic` | dynamic | 8.0 | 7.0 | 6.0 | 9.0 | Industrial hazard (steam). High motion. 'Blindfold displaced' is a strong visual beat. |
| `e014_b01_cinematic` | cinematic | 8.0 | 9.0 | 6.0 | 5.0 | Atmospheric risk. Catching a petal is delicate but low-stakes. 'Sun-drenched' contrasts with typical NieR gloom but fits profile. |
| `e014_b02_closeup` | closeup | 8.0 | 7.0 | 6.0 | 5.0 | 'Glowing data-chip' is a specific prop not in profile but plausible. Defensive pose is slightly static. |
| `e014_b02_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Repeats 'clothing snag' family from b01_medium. Yanking cable is active. |
| `e014_b02_fullbody` | fullbody | 9.0 | 8.0 | 5.0 | 6.0 | Stretching to a switch is functional but lacks narrative tension. 'Elegant arc' is descriptive filler. |
| `e014_b02_dynamic` | dynamic | 8.0 | 7.0 | 6.0 | 9.0 | Dodge debris. Similar to b01_dynamic (dodging force). High energy. |
| `e014_b02_cinematic` | cinematic | 8.0 | 8.0 | 6.0 | 5.0 | Holding broken bird is a good micro-story. Rain splash adds motion. |
| `e014_b03_closeup` | closeup | 8.0 | 7.0 | 6.0 | 5.0 | Fluorescent light flash. 'Static discharge' on hair is a nice detail. |
| `e014_b03_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Prying hatch. Physical strain shows personality (controlled effort). Good use of sleeve bunching. |
| `e014_b03_fullbody` | fullbody | 8.0 | 7.0 | 5.0 | 6.0 | Stepping over crack. Borderline 'locomotion filler' but has balance stakes. |
| `e014_b03_dynamic` | dynamic | 8.0 | 7.0 | 6.0 | 9.0 | Catching briefcase. Specific object interaction. Good momentum. |
| `e014_b03_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | Swaying bridge. 'Hazy city skyline' is atmospheric. Steady against railing is active enough. |
| `e014_b04_closeup` | closeup | 8.0 | 7.0 | 5.0 | 4.0 | Raindrop on nose. Very static. 'Hovers' is physically unlikely without wind context. Weak cause. |
| `e014_b04_medium` | medium | 9.0 | 8.0 | 6.0 | 5.0 | Leaf in sleeve. Tactile irritation is a good micro-story. Slightly low stakes. |
| `e014_b04_fullbody` | fullbody | 8.0 | 7.0 | 5.0 | 7.0 | Jumping over barrier. Locomotion filler risk. 'Rusted barrier' is generic. |
| `e014_b04_dynamic` | dynamic | 8.0 | 7.0 | 6.0 | 9.0 | Ducking under chain. Similar to b01/b02 dynamic dodges. High motion. |
| `e014_b04_cinematic` | cinematic | 8.0 | 9.0 | 6.0 | 5.0 | Mechanical butterfly. Very similar to b01_cinematic (catching small object in ruins). Repetitive. |

## Premises

### e014_b01_closeup — closeup

2B's hand tightens on a jagged piece of broken machinery protruding from the floor, her knuckles white as she pulls it free; a subtle crack in her blindfold reveals one eye widening at the sudden metallic screech, with a smudge of oil visible on her glove.

### e014_b01_medium — medium

Mid-stride in a narrow corridor, 2B's black dress hem catches on a low-hanging wire, causing the fabric to lift and tauten around her waist; she leans slightly forward with focused determination, one hand reaching down to untangle the snare while her posture remains rigidly composed.

### e014_b01_fullbody — fullbody

2B is crouched low on a crumbling stone ledge, her weight shifted entirely onto one thigh-high boot to maintain balance; she reaches out with one gloved hand to catch a falling book from the adjacent shelf, her other arm extended for counterbalance, showcasing the tension in her puffy sleeves.

### e014_b01_dynamic — dynamic

In a blur of motion, 2B twists her torso sharply to dodge a burst of steam from a ruptured pipe; her short white hair whips back against the force, and her blindfold is momentarily displaced by the pressure wave, revealing a flash of surprise as she lands in a stable combat stance.

### e014_b01_cinematic — cinematic

Standing at the edge of a vast, sun-drenched ruined plaza, 2B tilts her head back to catch a single falling petal in her palm; the wide shot emphasizes her small silhouette against the massive archways, but her focused gaze and delicate hand gesture anchor the scene with quiet curiosity.

### e014_b02_closeup — closeup

A close-up on 2B's face as she leans in to inspect a cracked, glowing data-chip hovering just inches from her blindfold; the device emits a faint blue light that reflects sharply off her hairband and the edge of her glove, which is raised defensively near her cheek as if expecting it to spark.

### e014_b02_medium — medium

Waist-up shot showing 2B mid-motion as she yanks a loose, frayed cable free from the hem of her black dress; the fabric snaps taut against her hip, highlighting the cutout design, while her expression remains stoic despite the sudden physical tug, with her other hand gripping the edge of a nearby console for stability.

### e014_b02_fullbody — fullbody

Full-body view of 2B stretching upward to reach a high, illuminated switch on a wall; her arms are fully extended above her head, causing the puffy feather-trimmed sleeves to bunch and emphasize her shoulder width, while her weight shifts back onto one thigh-high boot, creating an elegant arc from her heels to fingertips.

### e014_b02_dynamic — dynamic

2B twists sharply in mid-air to avoid a falling debris shard; her short white hair and black dress hem blur with the rotational force, and one gloved hand is blurred in motion as it swats away a secondary fragment, capturing the peak moment of evasion with intense directional energy.

### e014_b02_cinematic — cinematic

Wide shot from a low angle showing 2B standing on a fractured balcony, her silhouette framed against a massive, storm-lit window; she holds a small, broken mechanical bird in one hand, looking down at it with quiet intensity as rain splashes around her boots but does not touch her, emphasizing her isolation and focus.

### e014_b03_closeup — closeup

2B's face is lit by the sudden, harsh flash of a cracking fluorescent light tube overhead; her blindfold tightens as she flinches slightly, one eye visible through a tear in the fabric narrowing against the glare, while a single strand of short white hair sticks to her temple from static discharge.

### e014_b03_medium — medium

Waist-up shot as 2B leans forward to pry open a jammed, rusted hatch panel with one gloved hand; the effort causes her puffy feather-trimmed sleeves to bunch at the elbows and her black dress cutout to stretch taut across her torso, highlighting her controlled strain as she grimaces slightly.

### e014_b03_fullbody — fullbody

2B is mid-step over a wide, jagged crack in the floor, one thigh-high boot planted firmly on the lower ledge while her other leg lifts high to clear the gap; her body twists slightly to maintain balance, and her hairband catches the light as she focuses intensely on not losing her footing.

### e014_b03_dynamic — dynamic

2B lunges forward to catch a slipping, heavy metal briefcase before it hits the ground; her momentum carries her into a deep lunge, her black dress hem flaring out from the rapid movement, and her gloves gripping the handle tightly as her weight shifts precariously onto her toes.

### e014_b03_cinematic — cinematic

A wide low-angle shot shows 2B standing on a suspended, swaying platform bridge; she reaches out to steady herself against the railing as the structure groans and tilts, her silhouette framed against a distant, hazy city skyline, emphasizing her small but determined presence amidst the instability.

### e014_b04_closeup — closeup

2B's face is captured in a tight close-up as a single, heavy raindrop hovers on the tip of her nose; she holds her breath with intense focus, her black blindfold taut against her skin as she resists the urge to blink, while water beads visibly on the fabric of her hairband and the edge of her glove raised near her chin.

### e014_b04_medium — medium

In a waist-up shot, 2B leans back against a textured stone pillar to shake loose a large, dry leaf stuck in the puffy feather-trim of her sleeve; her body arches slightly to dislodge it, causing the cutout of her black dress to stretch across her torso, while her expression remains stoic despite the tactile irritation.

### e014_b04_fullbody — fullbody

Full-body view of 2B mid-jump over a low, rusted barrier; her legs are extended in a high stride, showcasing the length of her thigh-high stockings and boots, while her arms swing forward for momentum. Her short white hair lifts with the upward velocity, and her dress hem flares out around her waist as she clears the obstacle.

### e014_b04_dynamic — dynamic

2B twists her torso violently to duck under a swinging chain; her black dress hem blurs with the rotational force, and one gloved hand smacks the air near her head to deflect a secondary impact. Her blindfold is slightly askew from the sudden movement, revealing a flash of intense concentration as she completes the evasion.

### e014_b04_cinematic — cinematic

A wide shot shows 2B standing on a narrow stone bridge, reaching out to catch a small, fluttering mechanical butterfly that is about to land on her fingertip; the scale of the ancient ruins behind her emphasizes her isolation, but her delicate hand gesture and focused gaze anchor the scene with quiet curiosity as the creature hovers.
