# Ada Viral Guide Evolution — Cycle 012

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.68/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.20 |
| Visual Appeal | 8.40 |
| Diversity | 7.50 |
| Repetition Control | 6.50 |
| Micro Story | 7.20 |
| Animation Potential | 7.30 |

## Verdict

Strong set with high identity fidelity and good causal logic, but suffers from conceptual repetition in the 'industrial hazard' family and lower-stakes fullbody navigation shots that dilute the overall narrative tension.

## Strengths

- Consistent adherence to the local identity profile (blindfold, hair, dress details) across all premises.
- Strong use of specific causal triggers (snagged sleeve, swinging pipe, falling chain) that justify character reactions.
- Good variety in shot types and emotional registers, avoiding a monotonous 'tension' loop.
- Dynamic shots effectively utilize motion blur and directional vectors.

## Failures

- Repetition of the 'industrial hazard reaction' family (steam, sparks, debris, chains) across multiple batches, leading to conceptual fatigue despite different specific objects.
- Fullbody shots in b03 and b04 (stepping over puddle/glass) are lower stakes and less narratively rich than the untangling/climbing shots, feeling like filler locomotion.
- Closeup shots rely heavily on 'controlled annoyance/irritation' as the primary emotional beat, which is consistent but slightly repetitive in register.

## Desired patterns

- Integration of specific clothing items (sleeves, stockings) into the causal chain of events.
- Clear distinction between active navigation (climbing, swinging) and passive observation.
- Use of off-screen causes that have immediate, visible physical consequences on the character's body or outfit.

## Undesired patterns

- Generic 'dodging debris' without a specific source or unique interaction.
- Locomotion shots (stepping over small obstacles) that lack narrative tension or consequence.
- Atmospheric elements (mist, rain, ruins) serving as the primary hook rather than the character's reaction to them.

## Repetition clusters

- **Industrial Hazard Reaction**: `e012_b01_dynamic`, `e012_b02_medium`, `e012_b03_medium`, `e012_b04_medium`
- **Locomotion/Obstacle Navigation (Low Stakes)**: `e012_b01_fullbody`, `e012_b03_fullbody`, `e012_b04_fullbody`
- **Closeup Environmental Irritation**: `e012_b01_closeup`, `e012_b02_closeup`, `e012_b03_closeup`

## Recommendations for the next cycle

- Introduce at least one premise per batch that involves interaction with a non-industrial element (e.g., organic growth, water mechanics, light refraction) to break the 'rust and steam' monotony.
- Elevate the stakes of fullbody locomotion shots; instead of stepping over small debris, involve balance on a crumbling edge or navigating a shifting floor.
- Vary the emotional register in closeups more aggressively; include moments of surprise, focus, or even brief vulnerability rather than just 'controlled annoyance.'
- Ensure dynamic shots have unique vectors (e.g., vertical drop vs. horizontal slide) to avoid visual similarity.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e012_b01_closeup` | closeup | 9.5 | 8.0 | 7.5 | 6.0 | Strong identity with blindfold/hair interaction. 'Controlled annoyance' fits personality well. Cause (ventilation shaft) is specific enough for a closeup. |
| `e012_b01_medium` | medium | 9.5 | 8.5 | 8.5 | 7.0 | Excellent dual-action (pushing gate + adjusting snagged sleeve). The snag provides a clear causal link to the outfit adjustment. Good use of specific clothing details. |
| `e012_b01_fullbody` | fullbody | 9.0 | 8.5 | 6.5 | 7.5 | 'Testing stability' is a good micro-story element that avoids pure static posing. However, 'unstable beam' is a somewhat generic industrial hazard. |
| `e012_b01_dynamic` | dynamic | 8.5 | 9.0 | 7.0 | 9.0 | High energy. 'Steam jets' are a bit generic but the specific action of leaping over them with minimized air resistance is distinct. Good motion blur potential. |
| `e012_b01_cinematic` | cinematic | 9.0 | 8.5 | 7.5 | 6.5 | 'Climbing out' is active, avoiding the 'standing on ledge' trap. Cathedral ruin is a valid location but borders on atmospheric if not careful; here the action saves it. |
| `e012_b02_closeup` | closeup | 9.5 | 7.5 | 6.0 | 4.5 | Heat/flare cause is specific. However, 'sweat beads' and 'damp hair' are subtle changes that may be hard to animate distinctly in a short clip without looking like a static portrait with slight movement. |
| `e012_b02_medium` | medium | 9.5 | 8.0 | 7.5 | 6.5 | Inspecting a panel is good interaction. 'Sparks popping near sleeve' adds consequence to the proximity. Slightly passive compared to b01_medium but acceptable. |
| `e012_b02_fullbody` | fullbody | 9.5 | 8.5 | 8.5 | 7.5 | Untangling stocking from rebar is a strong micro-story with clear cause and physical consequence (tension in posture). Excellent use of specific clothing item. |
| `e012_b02_dynamic` | dynamic | 8.5 | 9.0 | 7.5 | 9.0 | Sliding to evade falling panel is distinct from leaping (b01). Sparks trailing boots add visual flair and consequence of the slide. |
| `e012_b02_cinematic` | cinematic | 8.5 | 9.0 | 7.0 | 8.5 | Swinging on a cable is high motion potential. 'Frayed cable' adds tension/risk. Distinct from climbing (b01) and leaping (b04). |
| `e012_b03_closeup` | closeup | 9.5 | 7.5 | 6.5 | 5.0 | Cold mist jet is a specific cause. Tilting head to shield ear is a good reactive motion. Similar emotional register (controlled reaction) to b01 and b02 closeups. |
| `e012_b03_medium` | medium | 9.5 | 8.0 | 7.5 | 6.5 | Ducking under a swinging pipe is good active navigation. 'Bracing against metal' provides physical contact and consequence. |
| `e012_b03_fullbody` | fullbody | 9.0 | 8.5 | 6.0 | 7.0 | Stepping over a puddle is low-stakes. While it shows locomotion, the 'distorted silhouette' reflection is more atmospheric than causal. Less tension than other fullbody shots. |
| `e012_b03_dynamic` | dynamic | 8.5 | 8.5 | 7.0 | 9.0 | Dodging falling debris is a standard dynamic action. 'Twisting torso' and 'hands extended for balance' are good technical details. |
| `e012_b03_cinematic` | cinematic | 9.0 | 8.5 | 7.0 | 6.0 | Climbing a moss-covered wall in a forest ruin. Distinct location from industrial/cathedral. Active climbing avoids passive scenic pose. |
| `e012_b04_closeup` | closeup | 9.5 | 8.0 | 7.0 | 5.5 | Condensation drop is a very specific, quiet cause. 'Holding breath' and 'eyes wide' are good micro-expressions. High anticipation. |
| `e012_b04_medium` | medium | 9.5 | 8.0 | 7.5 | 6.5 | Chain slamming behind her is a strong off-screen cause with immediate physical consequence (gust of air flaring sleeve). Good reactive action. |
| `e012_b04_fullbody` | fullbody | 9.0 | 8.5 | 6.5 | 7.5 | Stepping over broken glass is similar in function to stepping over a puddle (b03) or beam (b01). It's locomotion but lacks the 'testing' or 'untangling' narrative depth of other fullbody shots. |
| `e012_b04_dynamic` | dynamic | 8.5 | 9.0 | 7.5 | 9.0 | Side-stepping a swinging mace is distinct from leaping/sliding/dodging debris. 'Tucked hands' shows tactical awareness. |
| `e012_b04_cinematic` | cinematic | 8.5 | 9.0 | 7.0 | 8.5 | Leaping across a gap is high stakes. 'Widening gap' adds urgency. Distinct from climbing and swinging. |

## Premises

### e012_b01_closeup — closeup

A tight close-up on 2B's face as a sudden, sharp gust of wind from an off-screen ventilation shaft pushes loose strands of her short white hair across her black blindfold; she squints slightly behind the fabric and tenses her jaw in controlled annoyance rather than surprise, with one gloved hand rising to brush the hair away.

### e012_b01_medium — medium

Waist-up shot of 2B standing in a narrow corridor where a heavy metal gate is slowly closing behind her; she uses one gloved hand to push the sliding panel back open while simultaneously adjusting the puffy feather-trimmed sleeve on her other arm, which has snagged slightly on the gate's edge, maintaining a composed expression despite the effort.

### e012_b01_fullbody — fullbody

Full-body view of 2B stepping carefully across a narrow, unstable beam in a rusted industrial structure; her weight is shifted to one leg as she extends the other foot to test its stability before fully committing, her black dress and thigh-high boots highlighting her balanced posture against the chaotic background.

### e012_b01_dynamic — dynamic

Mid-air dynamic shot of 2B leaping over a sudden burst of steam jets erupting from the floor; her body is arched low, hair trailing behind her with motion blur, and her gloved hands are held tight against her sides to minimize air resistance as she clears the hazard.

### e012_b01_cinematic — cinematic

Wide cinematic angle showing 2B climbing out of a deep, dark shaft in a massive cathedral-like ruin; she grips the stone edge with both hands to pull herself up, her silhouette backlit by a single beam of light from above, emphasizing the scale of the environment against her determined effort.

### e012_b02_closeup — closeup

Extreme close-up on 2B's eyes and the lower half of her black blindfold as a sudden, localized burst of heat from an off-screen flare causes her to blink rapidly; sweat beads form on her temple while her jaw tightens in controlled irritation, with the white hair strands framing her face appearing slightly damp from the humidity.

### e012_b02_medium — medium

Waist-up shot of 2B leaning forward to inspect a cracked, glowing control panel on a wall; her gloved right hand hovers just inches from the surface while she tilts her head sharply to the side, her expression shifting from neutral curiosity to sharp focus as sparks pop and sizzle near her puffy feather-trimmed sleeve.

### e012_b02_fullbody — fullbody

Full-body view of 2B twisting her torso to untangle her left thigh-high stocking from a jagged piece of protruding rebar; she balances on one leg with her weight shifted back, her black dress cutout revealing the tension in her posture as she pulls the fabric free with a sharp yank.

### e012_b02_dynamic — dynamic

High-speed dynamic shot of 2B sliding horizontally across a polished metal floor to evade a falling ceiling panel; her body is low and parallel to the ground, her black boots trailing sparks against the surface, while her hair fans out behind her in a stark white contrast against the dark industrial backdrop.

### e012_b02_cinematic — cinematic

Wide cinematic angle from below showing 2B swinging across a vast, open chasm on a frayed cable; her body is extended in a straight line, defying gravity as she arcs through the air, with the massive scale of the surrounding ruins emphasizing the precariousness and momentum of her movement.

### e012_b03_closeup — closeup

A tight close-up on 2B's face as a sudden, localized jet of cold mist from an off-screen pipe hits the right side of her black blindfold; she tilts her head sharply to the left to shield her ear, her short white hair whipping across her cheek in response to the force, while her jaw sets with focused determination rather than surprise.

### e012_b03_medium — medium

Waist-up shot of 2B crouching slightly as a low-hanging, rusted pipe swings into her path; she ducks under it with precise timing, one gloved hand bracing against the metal to steady herself while her puffy feather-trimmed sleeve brushes the surface, maintaining a composed expression despite the tight clearance.

### e012_b03_fullbody — fullbody

Full-body view of 2B stepping over a shallow puddle that reflects her distorted silhouette; her left boot lifts high to avoid the water, while her right leg remains grounded on the uneven stone surface, her black dress hem lifting slightly with the motion to reveal the thigh-high stockings as she navigates the wet patch.

### e012_b03_dynamic — dynamic

Mid-action dynamic shot of 2B twisting her torso sideways to dodge a falling chunk of debris; her body is angled sharply, hair trailing behind with motion blur, and her gloved hands are extended forward for balance as she clears the obstacle, capturing the peak moment of evasion.

### e012_b03_cinematic — cinematic

Wide cinematic angle showing 2B climbing up a steep, moss-covered wall in a dense forest ruin; she grips the rough stone with both hands to pull herself upward, her silhouette backlit by dappled sunlight filtering through the canopy above, emphasizing the verticality of her ascent against the lush, overgrown environment.

### e012_b04_closeup — closeup

A tight close-up on 2B's face as a single, heavy drop of condensation from a high ceiling pipe falls directly onto the center of her black blindfold; she holds her breath with her eyes wide open behind the fabric, her short white hair falling still in the sudden silence, capturing a moment of hyper-focused anticipation before she blinks.

### e012_b04_medium — medium

Waist-up shot of 2B turning her head sharply to the left as a heavy, rusted chain slams against the wall behind her; she uses one gloved hand to steady herself on a nearby ledge while her puffy feather-trimmed sleeve flares out from the sudden gust of air displaced by the impact, her expression shifting from neutral observation to sharp alertness.

### e012_b04_fullbody — fullbody

Full-body view of 2B mid-stride as she steps over a jagged shard of broken glass on the floor; her left leg is extended high to clear the obstacle, while her right foot pushes off firmly against the stone ground, her black dress hem swinging with the momentum and her thigh-high stockings catching the light as she navigates the debris field.

### e012_b04_dynamic — dynamic

High-speed dynamic shot of 2B executing a rapid side-step to avoid a swinging, spiked mace; her body is twisted tightly to the right, hair whipping across her face with motion blur, and her gloved hands are tucked close to her ribs for compactness as she clears the arc of the weapon.

### e012_b04_cinematic — cinematic

Wide cinematic angle showing 2B leaping across a widening gap between two crumbling stone platforms; her body is extended in mid-air, arms out for balance, with the dark chasm below fading into mist and the distant ruins providing scale to her decisive, airborne maneuver.
