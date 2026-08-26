# Ada Viral Guide Evolution — Cycle 017

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.83/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 8.50 |
| Visual Appeal | 8.20 |
| Diversity | 7.50 |
| Repetition Control | 6.50 |
| Micro Story | 8.00 |
| Animation Potential | 8.30 |

## Verdict

The set is strong overall with good identity preservation and clear micro-stories. However, there is noticeable repetition in the fullbody/cinematic balancing poses and closeup gripping actions. Diversifying these categories will improve batch-level variety.

## Strengths

- Strong use of specific environmental causes (lasers, gears, water, electricity) rather than generic atmosphere.
- Good integration of character-specific details like the blindfold and feather-trimmed sleeves into the action.
- Most premises have clear directional energy suitable for animation.

## Failures

- Repetition of 'balancing on an unstable surface' in fullbody/cinematic shots (e017_b01_fullbody, e017_b02_fullbody, e017_b04_cinematic).
- Several closeups focus on 'gripping something dangerous' which feels repetitive (e017_b01_closeup, e017_b04_closeup).
- Some premises rely heavily on hair movement as a visual hook without varying the cause significantly.

## Desired patterns

- Specific physical interactions with environmental objects.
- Clear personality expression through micro-reactions (e.g., jaw tightening, suppressed annoyance).
- Use of character-specific clothing details to enhance motion and visual appeal.

## Undesired patterns

- Generic balancing poses without a specific force or threat.
- Repetitive closeup hooks involving gripping heavy/dangerous objects.
- Hair movement as the primary visual hook without a distinct cause.

## Repetition clusters

- **Balancing on unstable/tilted surfaces**: `e017_b01_fullbody`, `e017_b02_fullbody`, `e017_b04_cinematic`
- **Gripping dangerous/heavy objects in closeup**: `e017_b01_closeup`, `e017_b04_closeup`

## Recommendations for the next cycle

- Vary the fullbody/cinematic shots to include more active movement (running, jumping, climbing) rather than just balancing.
- Diversify closeup hooks by focusing on different body parts or interactions (e.g., adjusting gear, wiping oil, reacting to sound).
- Ensure hair movement is caused by distinct sources (explosion, water splash, rapid turn) to avoid repetition.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e017_b01_closeup` | closeup | 9.0 | 8.0 | 8.0 | 7.0 | Strong micro-reaction (jaw tightening) with clear cause (rubble). Identity is well-preserved. Animation potential is moderate as the action is very brief. |
| `e017_b01_medium` | medium | 9.0 | 8.0 | 8.0 | 9.0 | Excellent use of specific clothing details (feather sleeves) reacting to motion. Clear cause and active torso movement. |
| `e017_b01_fullbody` | fullbody | 8.0 | 7.0 | 7.0 | 8.0 | Good balance against a force (explosion). However, 'holding sword low' is slightly generic without specifying the sword's role in the immediate threat. |
| `e017_b01_dynamic` | dynamic | 8.0 | 9.0 | 8.0 | 9.0 | High energy. The 'shockwave' lifting hair is a valid physical consequence of the laser shot. Good directional energy. |
| `e017_b01_cinematic` | cinematic | 8.0 | 8.0 | 9.0 | 9.0 | Strong narrative hook (catching gear to swing it back). Clear cause and consequence. Good use of motion blur. |
| `e017_b02_closeup` | closeup | 8.0 | 7.0 | 7.0 | 6.0 | Oil spray is a good specific cause. However, 'holding breath' and 'tilting head back' are somewhat static reactions compared to other closeups. |
| `e017_b02_medium` | medium | 8.0 | 8.0 | 8.0 | 8.0 | Water geyser is a strong environmental interaction. Torso arching provides good visual tension. |
| `e017_b02_fullbody` | fullbody | 8.0 | 7.0 | 7.0 | 7.0 | Similar to e017_b01_fullbody (balancing on tilted surface). The 'arms extended outward' is a standard balance pose that risks feeling static if not animated well. |
| `e017_b02_dynamic` | dynamic | 9.0 | 8.0 | 8.0 | 9.0 | Deflecting a pipe is a strong physical interaction. The spinning motion adds dynamic energy. |
| `e017_b02_cinematic` | cinematic | 8.0 | 8.0 | 7.0 | 8.0 | Landing from a leap is good. 'Eyes fixed ahead' is slightly vague but acceptable for a cinematic shot. |
| `e017_b03_closeup` | closeup | 9.0 | 8.0 | 9.0 | 7.0 | Excellent personality expression (suppressing urge to adjust blindfold). The 'faint flush on neck' is a nice detail for an android. |
| `e017_b03_medium` | medium | 8.0 | 8.0 | 8.0 | 8.0 | Electrical arcing is a good specific cause. The fabric rippling due to static charge is a nice touch. |
| `e017_b03_fullbody` | fullbody | 9.0 | 8.0 | 9.0 | 8.0 | Hauling a crate up a ladder is a strong physical action. It breaks the pattern of just balancing. |
| `e017_b03_dynamic` | dynamic | 9.0 | 9.0 | 8.0 | 9.0 | Low slide under a beam is dynamic and clear. The hair fanning out is a good visual cue for speed. |
| `e017_b03_cinematic` | cinematic | 8.0 | 8.0 | 8.0 | 8.0 | Catching a whipping cable is a good specific interaction. The high-angle shot adds variety. |
| `e017_b04_closeup` | closeup | 9.0 | 8.0 | 8.0 | 7.0 | Tearing glove is a good detail. However, it's very similar to e017_b01_closeup in terms of 'gripping something heavy/dangerous'. |
| `e017_b04_medium` | medium | 8.0 | 9.0 | 8.0 | 8.0 | Updraft from ventilation shaft is a good specific cause. The dress hem lifting reveals stockings, which adds visual appeal. |
| `e017_b04_fullbody` | fullbody | 8.0 | 8.0 | 8.0 | 8.0 | Stepping over a sparking beam is good. The sparks flying near boots adds danger. |
| `e017_b04_dynamic` | dynamic | 8.0 | 8.0 | 8.0 | 9.0 | Sidestep from a slamming door is dynamic. The shockwave causing hair to whip is a good visual effect. |
| `e017_b04_cinematic` | cinematic | 8.0 | 8.0 | 7.0 | 8.0 | Balancing on a rotating gear is good. However, it's similar to e017_b02_fullbody and e017_b01_fullbody in terms of 'balancing on an unstable surface'. |

## Premises

### e017_b01_closeup — closeup

2B's gloved fingers grip the edge of a crumbling stone ledge as a chunk of rubble falls past her face, causing her to squint slightly beneath her blindfold; her expression remains composed but her jaw tightens in suppressed annoyance at the debris's proximity.

### e017_b01_medium — medium

2B twists her torso sharply to avoid a swinging chain from an overhead mechanism, her puffy feather-trimmed sleeves flaring outward with the motion; she holds her breath for stability, her black dress fabric pulling taut across her waist as she braces against the impact zone.

### e017_b01_fullbody — fullbody

2B stabilizes herself on a tilted metal platform after an explosion rocks the floor, her thigh-high boots gripping the slanted surface while she leans into the tilt; one arm is extended for balance and the other holds her sword low, ready to pivot.

### e017_b01_dynamic — dynamic

2B dodges a horizontal laser beam that slices through the air just below her chin, forcing her into a deep crouch; her short white hair lifts slightly from the shockwave of the shot, and her blindfold shifts a fraction as she watches the beam pass.

### e017_b01_cinematic — cinematic

2B catches a falling gear with one hand while stepping onto a rotating platform, her body leaning forward to absorb the weight; the background blurs into motion as she prepares to swing the gear back, her posture tense and precise.

### e017_b02_closeup — closeup

Close-up on 2B's face as a fine mist of oil sprays from a ruptured pipe directly onto her black blindfold; she holds her breath and tilts her head back slightly to avoid the droplets hitting her lips, her jaw clenched in tight control while a single drop clings to the edge of her hair.

### e017_b02_medium — medium

Medium shot from the waist up as 2B braces against a sudden upward geyser of water erupting from a broken grate, her torso arching back to protect her face; her black gloves grip the wet concrete edge firmly for traction, and the fabric of her dress stretches taut across her chest as she leans into the pressure.

### e017_b02_fullbody — fullbody

Full-body view of 2B mid-step, freezing on a fractured metal walkway that is tilting sideways due to a snapped support beam; she shifts her weight aggressively onto one thigh-high boot to counterbalance the slope, while her other leg lifts high and her arms extend outward, fingers splayed, to maintain equilibrium.

### e017_b02_dynamic — dynamic

2B twists sharply to deflect a heavy rusted pipe swinging on a chain with her sword arm; the impact sends her body spinning, her puffy sleeves flaring violently against the motion as she uses the momentum to pull herself away from the wall, her expression focused and unyielding.

### e017_b02_cinematic — cinematic

Cinematic low-angle shot as 2B lands on a raised platform after leaping over a chasm, the impact causing dust to billow around her boots; she drops into a deep defensive stance, one hand gripping her sword hilt while the other extends forward for balance, eyes fixed ahead with calm intensity.

### e017_b03_closeup — closeup

Close-up of 2B's face as a jagged shard of glass from a shattered window frame clips the side of her black blindfold, causing it to twist slightly askew; she does not blink, but her jaw clenches tightly and a faint flush appears on her neck as she suppresses the urge to adjust it, maintaining absolute composure despite the intrusion.

### e017_b03_medium — medium

Medium shot of 2B bracing against a sudden surge of electrical arcing from a damaged console; she leans her torso back to keep her distance while her black-gloved hands push firmly against the humming metal casing for stability, the static charge causing the fabric of her puffy sleeves to ripple and lift slightly away from her arms.

### e017_b03_fullbody — fullbody

Full-body view of 2B navigating a narrow, rusted ladder that is bending under the weight of a heavy crate she is hauling up; her thigh-high boots grip the rungs with precision as she shifts her center of gravity aggressively to keep the load from swinging into her face, her arms straining visibly against the strain while her blindfold remains perfectly aligned.

### e017_b03_dynamic — dynamic

2B executes a sharp low slide underneath a falling steel beam, using the momentum to propel herself forward; her short white hair fans out behind her from the rapid movement, and her hands drag along the dusty ground for friction as she prepares to pop up into a defensive stance before the beam crashes down where she just was.

### e017_b03_cinematic — cinematic

Cinematic high-angle shot looking down as 2B stands on a crumbling balcony edge, balancing on the toes of her boots against the shifting stone; she reaches out with one hand to catch a dangling cable that is whipping dangerously close to her head, her body twisted in tension as she tries to pull it clear before the ledge gives way beneath her.

### e017_b04_closeup — closeup

Close-up on 2B's hands as she catches a falling, heavy iron gear that clips her black glove, causing the fabric to tear slightly; her fingers grip the spinning metal with white-knuckled intensity to stop its rotation before it drops, her knuckles visible and tense.

### e017_b04_medium — medium

Medium shot of 2B leaning forward aggressively into a strong updraft from a ruptured ventilation shaft, her puffy feather-trimmed sleeves ballooning outward as she anchors her upper body against the force; her black dress hem lifts slightly, revealing the top of her thigh-high stockings, while her jaw is set in focused determination to maintain stability.

### e017_b04_fullbody — fullbody

Full-body view of 2B mid-lunge, stepping over a broken metal beam that is sparking and shifting under her weight; she drives her front thigh-high boot into the gap for leverage while extending her rear leg for balance, one hand reaching down to steady herself on the unstable debris as sparks fly near her boots.

### e017_b04_dynamic — dynamic

2B executes a rapid sidestep to avoid a slamming blast door that cracks against the floor inches from her feet; the shockwave sends dust and small shards of concrete flying toward her face, forcing her to tilt her head sharply away while her short white hair whips around her blindfold in the sudden gust.

### e017_b04_cinematic — cinematic

Cinematic wide shot as 2B stands on a precarious, rotating gear mechanism that is tilting sideways; she shifts her weight entirely onto one thigh-high boot to counterbalance the slope while extending her free arm to grip a passing chain for stability, her body twisting in a dynamic arc against the industrial backdrop.
