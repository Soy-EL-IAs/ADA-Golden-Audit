# Ada Viral Guide Evolution — Cycle 021

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.33/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.00 |
| Visual Appeal | 8.00 |
| Diversity | 7.00 |
| Repetition Control | 6.00 |
| Micro Story | 7.00 |
| Animation Potential | 7.00 |

## Verdict

Good batch with strong identity and visual appeal. Main weakness is repetition in the Fullbody category (balancing) and slightly passive Cinematic shots. Needs minor adjustments to break the balancing cluster and add more active environmental interaction in wide shots.

## Strengths

- Strong adherence to character identity facts (blindfold, hair, dress details) across all premises.
- Most dynamic and full-body shots have clear causal triggers (rebar, crate, wind shear).
- Closeups successfully avoid the 'gripping sword' trap with varied hand/face interactions.

## Failures

- Repetition of 'balancing on unstable surface' hook in Fullbody category (b01_3, b03_3, b04_5).
- Cinematic shots (b02_5, b03_5) lean towards static poses ('standing beneath', 'crouched defensive') rather than active environmental interaction.
- Some medium shots rely heavily on 'twist/lean' as the primary verb, reducing variety in upper-body dynamics.

## Desired patterns

- Explicit causal chains (Cause -> Reaction -> Consequence).
- Integration of clothing physics (sleeve flare, hem lift) with specific forces.
- Micro-expressions that reflect stoic personality under stress.

## Undesired patterns

- Static balancing poses without immediate threat progression.
- Atmospheric elements (dust, sparks) serving as the only visual interest in cinematic shots.
- Generic 'looking up' or 'crouching' without specific physical interaction with the environment.

## Repetition clusters

- **Balancing on unstable/tilting surface**: `e021_b01_3`, `e021_b03_3`, `e021_b04_5`
- **Crouching under looming threat (static defensive)**: `e021_b01_5`, `e021_b03_5`

## Recommendations for the next cycle

- Replace one 'balancing' fullbody shot with a different physical constraint (e.g., climbing, hanging from a hook, crawling under low clearance).
- Make cinematic shots more active: instead of standing/crouching, have the character interacting with the environment (pushing against a closing door, pulling a lever to stop a machine).
- Vary medium shot verbs beyond 'twist/lean': include reaching, pushing, pulling, or catching.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e021_b01_1` | closeup | 9.0 | 7.0 | 8.0 | 6.0 | Strong identity via blindfold/hair. Cause (hydraulic hiss) is auditory/off-screen but visual consequence (dust falling) is clear. Good micro-expression. |
| `e021_b01_2` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Clear cause (steam burst). Good use of sleeve flare. Slightly generic 'twist away' but effective. |
| `e021_b01_3` | fullbody | 9.0 | 8.0 | 7.0 | 7.0 | Balancing on tilting beam is a specific physical constraint. Good silhouette focus. |
| `e021_b01_4` | dynamic | 8.0 | 9.0 | 7.0 | 9.0 | High energy. Sliding to evade rebar is a clear action. Hair whip adds motion. |
| `e021_b01_5` | cinematic | 8.0 | 7.0 | 6.0 | 6.0 | Cinematic shot. Crouching under debris is active but slightly passive compared to other dynamic shots. Dust obscuring background risks 'atmospheric filler' if not careful. |
| `e021_b02_1` | closeup | 9.0 | 8.0 | 8.0 | 7.0 | Excellent closeup. Wiping fluid is a specific non-weapon hand interaction. Good tension in knuckles. |
| `e021_b02_2` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Leaning back from glass shard. Good counter-rotation description. Distinct from b01_2 steam twist. |
| `e021_b02_3` | fullbody | 9.0 | 8.0 | 6.0 | 7.0 | Mid-leap. 'Tuck to minimize drag' is a bit technical but works. Hem lift is subtle. |
| `e021_b02_4` | dynamic | 8.0 | 9.0 | 7.0 | 9.0 | Deflecting crate. Strong impact visual. Dust eruption adds consequence. |
| `e021_b02_5` | cinematic | 8.0 | 7.0 | 5.0 | 4.0 | Weak. 'Standing directly beneath' is close to static. Looking up with composed focus is a pose rather than an interaction. Sparks dripping are atmospheric. |
| `e021_b03_1` | closeup | 9.0 | 7.0 | 6.0 | 5.0 | Heat wave/sweat. Cause is off-screen furnace. Reaction (sweat/jaw clench) is subtle but valid micro-story. |
| `e021_b03_2` | medium | 9.0 | 8.0 | 7.0 | 7.0 | Catching data core. Good weight absorption description. Distinct from other medium shots. |
| `e021_b03_3` | fullbody | 9.0 | 8.0 | 7.0 | 6.0 | Sliding platform. Similar to b01_3 (tilting/balancing) but different mechanism (sliding vs balancing). Acceptable variation. |
| `e021_b03_4` | dynamic | 8.0 | 9.0 | 7.0 | 9.0 | Swinging chain. High motion blur potential. Clear cause (debris wave). |
| `e021_b03_5` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | Turbine blade. Crouched defensive stance is similar to b01_5 (crouching under threat). 'Eyes tracking' helps but still feels like a pose. |
| `e021_b04_1` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Cable snap. Good micro-expression of pain/stoicism. Distinct from other closeups. |
| `e021_b04_2` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Pressing control panel. Hair lifting from static is a nice detail. Distinct interaction. |
| `e021_b04_3` | fullbody | 9.0 | 8.0 | 7.0 | 8.0 | Slipping on glass. S-curve twist is dynamic. Good use of stockings reveal. |
| `e021_b04_4` | dynamic | 8.0 | 9.0 | 7.0 | 9.0 | Wind shear skidding. High energy. Similar to b01_2 (wind/steam force) but different body reaction (skid vs twist). |
| `e021_b04_5` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | Chimney edge. Balancing/leaning back is similar to b01_3 and b03_3 (balancing on unstable surface). Repetition of 'balance' hook. |

## Premises

### e021_b01_1 — closeup

A tight close-up on 2B's face as a sudden, sharp hiss from an off-screen hydraulic leak startles her; the vibration causes a fine layer of dust to fall from her short white hair onto her black blindfold, while her fingers twitch slightly at her sides in a micro-expression of suppressed shock.

### e021_b01_2 — medium

Waist-up shot of 2B twisting her torso sharply to the left as a burst of steam erupts from a broken pipe behind her right shoulder; the force pushes her puffy feather-trimmed sleeve outward, creating a dramatic flare that contrasts with her rigid, composed posture.

### e021_b01_3 — fullbody

Full-body view of 2B balancing on a narrow, tilting metal beam as the structure groans and dips under her weight; she extends one gloved hand to steady herself against a rusted wall while her black dress hem flutters in the sudden updraft, highlighting the silhouette of her thigh-high stockings.

### e021_b01_4 — dynamic

High-energy action shot of 2B sliding across a concrete floor to evade a falling rebar, her body low and angled; motion blur trails behind her as her hair whips forward from the momentum, and one boot scrapes sparks against the ground in an effort to stop.

### e021_b01_5 — cinematic

Wide establishing shot of a collapsing industrial catwalk where 2B is crouched low, shielding her head as large chunks of debris rain down around her; the environment is actively breaking apart, with dust clouds rising rapidly to obscure the background, emphasizing her small but determined figure against the chaos.

### e021_b02_1 — closeup

Extreme close-up of 2B's black blindfold as a sudden, high-velocity spray of hydraulic fluid from an off-screen ruptured valve strikes the fabric; her gloved fingers reach up with precise, controlled speed to wipe the dark liquid away before it can seep through and obscure her vision, highlighting the tension in her knuckles.

### e021_b02_2 — medium

Waist-up shot of 2B leaning back sharply to avoid a jagged shard of glass slicing through the air; her torso twists in counter-rotation, causing her puffy feather-trimmed sleeve to compress and stretch against her arm, while her hairband holds her short white hair firmly in place despite the abrupt change in vector.

### e021_b02_3 — fullbody

Full-body view of 2B mid-leap across a widening gap between two crumbling concrete pillars; her legs are extended in a tight tuck to minimize drag, and the black dress hem lifts slightly against her thigh-high stockings due to the upward air displacement from the jump, emphasizing her athletic silhouette.

### e021_b02_4 — dynamic

High-energy action shot of 2B deflecting a heavy metal crate that is slamming down onto her shoulder; she braces with both arms, driving her feet into the dirt ground to absorb the impact, causing dust and small stones to erupt from beneath her boots as the crate bounces off her forearms.

### e021_b02_5 — cinematic

Wide low-angle shot of a massive, rusted gear grinding into its housing above 2B; she stands directly beneath the mechanism, looking up with composed focus as sparks and grease drip down around her, while her dress hem remains still despite the turbulent air currents created by the turning machinery.

### e021_b03_1 — closeup

Extreme close-up of the lower half of 2B's face and neck as a sudden, intense heat wave from an off-screen furnace causes her skin to glisten with fine beads of sweat; she keeps her jaw clenched in rigid control while her black blindfold strap tightens slightly against the tension in her scalp, capturing a micro-expression of suppressed discomfort.

### e021_b03_2 — medium

Waist-up shot of 2B extending both arms forward to catch a heavy, falling data core; the impact drives her shoulders down and twists her torso slightly as she absorbs the weight, causing the fabric of her puffy feather-trimmed sleeves to stretch taut over her biceps while her hairband remains steady against the sudden jolt.

### e021_b03_3 — fullbody

Full-body view of 2B standing on a cracked, tilting platform as it begins to slide down a sloped metal ramp; she plants her boots firmly into the grooves of the surface for traction, leaning back slightly to counterbalance the downward pull, which pulls her black dress hem taut against her thigh-high stockings and highlights the silhouette of her stance.

### e021_b03_4 — dynamic

High-energy action shot of 2B twisting her torso sharply to swing a heavy chain around her, using its momentum to knock aside a rushing wave of debris; motion blur trails the chain's arc as her hair whips outward from the centrifugal force, and one gloved hand grips the handle with visible strain against the kinetic pull.

### e021_b03_5 — cinematic

Wide low-angle shot of a massive, rotating turbine blade slicing through the air inches above 2B; she is crouched low in a defensive stance, her eyes tracking the descending edge with intense focus as dust and grease are sucked into the vortex around her, emphasizing her small but precise figure against the looming mechanical threat.

### e021_b04_1 — closeup

Extreme close-up of the side of 2B's head as a thin, frayed electrical cable snaps taut against her temple; her black blindfold strap shifts millimeters from the sudden tension in her scalp, while her jaw clenches so hard the muscles ripple visibly under the skin, capturing a micro-expression of suppressed pain without breaking her stoic composure.

### e021_b04_2 — medium

Waist-up shot of 2B leaning forward aggressively to press both gloved palms against a sparking, unstable control panel; the static charge causes her short white hair to lift slightly away from her scalp, and the strain in her shoulders stretches the fabric of her puffy feather-trimmed sleeves taut over her arms, emphasizing her focused determination.

### e021_b04_3 — fullbody

Full-body view of 2B caught mid-slip on a sheet of shattered glass covering the floor; she kicks one leg out to the side for traction, her body twisting in an S-curve as she fights gravity, causing her black dress hem to swing wildly and reveal the full length of her thigh-high stockings against the chaotic backdrop.

### e021_b04_4 — dynamic

High-energy action shot of 2B being struck by a lateral wind shear from a ruptured ventilation shaft; her body is forced into a low, skidding posture as she digs her boots into the gravel to maintain footing, motion blur trailing behind her as her hair whips sideways and her dress flares out dramatically against the gale.

### e021_b04_5 — cinematic

Wide shot from a low angle looking up at 2B as she stands on the edge of a crumbling brick chimney, balancing precariously; a massive chunk of masonry is sliding away from beneath her feet, and she leans back sharply to counterbalance the loss of support, her silhouette stark against the overcast sky as dust plumes erupt around her boots.
