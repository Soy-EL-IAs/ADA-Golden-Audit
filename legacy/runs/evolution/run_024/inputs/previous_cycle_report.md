# Ada Viral Guide Evolution — Cycle 023

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.08/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 8.50 |
| Visual Appeal | 7.80 |
| Diversity | 6.50 |
| Repetition Control | 6.00 |
| Micro Story | 6.50 |
| Animation Potential | 7.20 |

## Verdict

Solid batch with strong identity and visual appeal, but suffers from moderate repetition in mechanical interaction themes and some generic causal triggers. Needs more variety in environmental contexts and specific narrative hooks to elevate micro-story scores.

## Strengths

- Strong preservation of character identity across all premises.
- Good use of dynamic poses in the 'Dynamic' category shots.
- Effective integration of clothing physics (dress hem, sleeves) into actions.

## Failures

- Repetition of mechanical interaction themes (prying, pulling cables, twisting valves).
- Several premises rely on generic causes (falling debris, steam blasts) without unique narrative hooks.
- Some 'Cinematic' shots risk becoming atmospheric wallpaper due to lack of specific event focus.

## Desired patterns

- More varied environmental interactions beyond mechanical/industrial settings.
- Stronger causal links between the trigger and the character's specific reaction.
- Greater emphasis on personality-driven micro-expressions in close-ups.

## Undesired patterns

- Repeated use of 'prying' or 'pulling' as primary actions.
- Generic 'dodging' or 'balancing' without specific narrative context.
- Atmospheric elements (sparks, steam) acting as the main hook rather than secondary effects.

## Repetition clusters

- **Mechanical Jam/Prying**: `e023_b01_medium`, `e023_b03_medium`
- **Fluid/Steam Exposure**: `e023_b02_dynamic`, `e023_b04_medium`
- **Climbing/Balancing on Precarious Structures**: `e023_b01_fullbody`, `e023_b02_cinematic`, `e023_b04_cinematic`

## Recommendations for the next cycle

- Introduce more non-mechanical interactions (e.g., biological, environmental hazards).
- Vary the 'cause' of action to include more character-driven decisions rather than external forces.
- Ensure each 'Cinematic' shot has a distinct narrative event that prevents it from being just a scenic view.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e023_b01_closeup` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Strong identity with blindfold interaction. The spark is a visible cause, but the reaction (pushing blindfold back) feels slightly disconnected from the immediate threat of the spark on her cheek. |
| `e023_b01_medium` | medium | 8.0 | 7.0 | 6.0 | 5.0 | Lifting a grate is active but generic. The 'holding steady' aspect makes it feel static rather than dynamic. Identity is preserved well. |
| `e023_b01_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 7.0 | Balancing on a ledge is a classic trope. The 'sliding slab' provides cause, but the reaction (weight shift) is passive. Good silhouette. |
| `e023_b01_dynamic` | dynamic | 8.0 | 9.0 | 7.0 | 9.0 | Excellent dynamic shot. Dodging a chain is specific and high-energy. Hair and dress physics are well-described. |
| `e023_b01_cinematic` | cinematic | 8.0 | 7.0 | 5.0 | 6.0 | Catching falling debris is a bit generic. The 'moonlight' atmosphere risks becoming wallpaper if the catch isn't emphasized enough. |
| `e023_b02_closeup` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Bracing against a beam is good. The detail about the blindfold strap snapping taut adds nice micro-story tension. |
| `e023_b02_medium` | medium | 8.0 | 7.0 | 6.0 | 5.0 | Pulling a cable is active. However, 'sparks popping nearby' is atmospheric filler unless they directly threaten her. |
| `e023_b02_fullbody` | fullbody | 8.0 | 8.0 | 7.0 | 8.0 | Sliding under a press is high-stakes and specific. Good use of body compression for visual appeal. |
| `e023_b02_dynamic` | dynamic | 8.0 | 9.0 | 7.0 | 9.0 | Leaping over steam is dynamic. The 'split jump' pose is visually strong and implies clear velocity. |
| `e023_b02_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 7.0 | Swinging on a chain is a common action. The 'precarious girder' adds context but the action itself is somewhat standard. |
| `e023_b03_closeup` | closeup | 9.0 | 8.0 | 6.0 | 5.0 | Tracking electricity is reactive. The 'sharp focus' expression is good for personality, but the action (turning head) is low-energy. |
| `e023_b03_medium` | medium | 8.0 | 7.0 | 6.0 | 5.0 | Prying a vent cover. This falls into the 'Prying' cluster limit (max 2). It is active but repetitive in concept with other mechanical interactions. |
| `e023_b03_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 6.0 | Catching a falling beam is active. The 'deep lunge' pose is good for silhouette but the cause (falling beam) is generic. |
| `e023_b03_dynamic` | dynamic | 8.0 | 9.0 | 7.0 | 9.0 | Vaulting over a pit with a chain. Very dynamic and visually interesting. Good use of negative space. |
| `e023_b03_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 6.0 | Grabbing a cargo crate is specific. The 'fighting for balance against wind' adds a secondary layer of difficulty. |
| `e023_b04_closeup` | closeup | 9.0 | 8.0 | 7.0 | 5.0 | Using glass to reflect light is a clever micro-story. It shows intelligence and resourcefulness, fitting her personality. |
| `e023_b04_medium` | medium | 8.0 | 7.0 | 6.0 | 5.0 | Twisting a valve is active. The 'sliding gloves' detail adds realism but the overall action is somewhat mundane. |
| `e023_b04_fullbody` | fullbody | 8.0 | 8.0 | 7.0 | 7.0 | Hanging from a beam and reaching for a bolt is a good combination of balance and precision. Visually strong silhouette. |
| `e023_b04_dynamic` | dynamic | 8.0 | 9.0 | 7.0 | 9.0 | Kicking a door while sliding is high-energy and specific. The 'parallel to ground' pose is visually striking. |
| `e023_b04_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 6.0 | Pulling a rope on a tilting platform is good. The 'tangled rope' adds a specific obstacle to overcome. |

## Premises

### e023_b01_closeup — closeup

Close-up on 2B's face as she forcibly pushes her black blindfold back to reveal her eyes, her jaw tight with controlled strain while a sudden, sharp electrical spark from a nearby broken conduit snaps against her cheek, illuminating the tension in her expression.

### e023_b01_medium — medium

Medium shot of 2B waist-up, actively twisting her torso to lift a heavy, rusted metal grate over her head; her black gloves grip the edge firmly as her puffy sleeves flare with the motion, and her dress cutout reveals the tension in her core muscles as she holds the weight steady.

### e023_b01_fullbody — fullbody

Full-body view of 2B balancing on a narrow, crumbling stone ledge; one foot planted firmly while the other hovers over a gap, her weight shifted back to counterbalance a loose slab sliding off the edge beside her, highlighting the line of her thigh-high boots and stockings against the dark ruins.

### e023_b01_dynamic — dynamic

Dynamic low-angle shot capturing 2B mid-dodge as she leans sharply backward to avoid a swinging chain, her short white hair whipping forward and the hem of her black dress flaring upward from the rapid turn, revealing the movement of her legs in motion.

### e023_b01_cinematic — cinematic

Cinematic wide shot showing 2B standing silhouetted against a massive, cracked window where moonlight floods in; she is actively reaching up to catch a falling debris piece before it hits the ground behind her, her figure framed by the dramatic contrast of light and shadow.

### e023_b02_closeup — closeup

Close-up on 2B's upper chest and neck as she actively braces her left arm against a vibrating, loose structural beam to stop it from swinging into her face; the vibration causes her black blindfold strap to snap taut against her cheekbone while her hairband digs slightly into her short white hair under the physical stress.

### e023_b02_medium — medium

Medium shot of 2B waist-up, leaning forward to pull a frayed electrical cable free from a jammed socket; her black gloves grip the insulated wire firmly as sparks pop nearby, and the sudden jerk causes the cutout in her black dress to stretch tight across her ribs, revealing the strain in her posture.

### e023_b02_fullbody — fullbody

Full-body view of 2B crouching low on a slick, oil-stained metal floor to slide under a descending hydraulic press; her body is compressed flat against the ground with knees tucked and boots splayed for traction, highlighting the length of her legs in thigh-high stockings as she evades the crushing weight above.

### e023_b02_dynamic — dynamic

Dynamic high-angle shot capturing 2B mid-air as she leaps over a burst of steam venting from a broken pipe; her legs are extended forward in a split jump, and the upward force of the blast pushes the hem of her black dress and puffy sleeves backward, creating a sense of rapid vertical velocity.

### e023_b02_cinematic — cinematic

Cinematic wide shot from below looking up at 2B standing on a precarious, broken girder high above a chasm; she is actively reaching out to grab a dangling, rusted chain to swing across the gap, her silhouette framed against the bright sky as her boots grip the narrow edge for purchase.

### e023_b03_closeup — closeup

Close-up on 2B's face as she sharply turns her head to the left, tracking a sudden crackle of electricity from a nearby power line; her short white hair whips sideways with the rapid motion, and the black blindfold strap pulls taut against her cheekbone, revealing a micro-expression of sharp focus amidst the controlled tension.

### e023_b03_medium — medium

Medium shot of 2B waist-up as she leans heavily against a crumbling brick wall, using her black-gloved hands to pry open a jammed metal vent cover; the puffy feather-trimmed sleeves bunch up at her elbows with the strain, and the cutout in her dress pulls tight across her torso as she exerts force to dislodge the rusted latch.

### e023_b03_fullbody — fullbody

Full-body view of 2B in a deep lunge on a slippery, moss-covered stone floor; her back foot is planted firmly while her front leg extends forward to catch a falling, heavy iron beam before it hits the ground, highlighting the length of her thigh-high stockings and the tension in her posture as she stabilizes the weight.

### e023_b03_dynamic — dynamic

Dynamic low-angle shot capturing 2B mid-swing as she uses a broken chain to vault over a pit of jagged debris; her body is arched backward in the air, short white hair flying upward against gravity, and the hem of her black dress lifts dramatically from the momentum, revealing the line of her legs in motion.

### e023_b03_cinematic — cinematic

Cinematic wide shot showing 2B standing on a high, exposed balcony railing; she is actively reaching out to grab the edge of a passing cargo crate that has slipped from its mooring, her figure silhouetted against a bright, overcast sky as she fights for balance against the wind.

### e023_b04_closeup — closeup

Close-up on 2B's face as she holds a broken shard of glass before her eyes to reflect the glow of a distant explosion; the jagged edge trembles slightly in her black-gloved hand, and the fractured light catches the taut line of her jaw and the slight displacement of her blindfold strap against her cheekbone.

### e023_b04_medium — medium

Medium shot of 2B waist-up as she forcefully twists a large, corroded valve wheel to stop a leaking pipe; her black gloves slide against the wet metal surface, causing her puffy sleeves to bunch and strain at the cuffs while the sudden release of pressure forces her torso to twist sharply, stretching the fabric across her chest.

### e023_b04_fullbody — fullbody

Full-body view of 2B hanging by one arm from a high, rusted I-beam; her body is suspended vertically with legs crossed at the ankles for balance, highlighting the length of her thigh-high stockings and boots against the dark background as she reaches with her free hand to grab a loose bolt dropping below her.

### e023_b04_dynamic — dynamic

Dynamic side-angle shot capturing 2B mid-slide across a polished metal floor as she uses her booted foot to kick open a stuck maintenance door; her body is parallel to the ground, short white hair streaming back from the velocity, and the hem of her dress flares out behind her due to the drag against the surface.

### e023_b04_cinematic — cinematic

Cinematic wide shot showing 2B standing on a precarious, tilted platform suspended over a deep shaft; she is actively pulling down a heavy, tangled rope to secure it against the railing as the platform begins to tilt further, her silhouette framed by the dramatic depth of the shaft and the tension in her posture.
