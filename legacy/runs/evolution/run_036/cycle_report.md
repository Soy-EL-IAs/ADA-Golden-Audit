# Ada Viral Guide Evolution — Cycle 036

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.50/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.00 |
| Visual Appeal | 8.00 |
| Diversity | 7.00 |
| Repetition Control | 6.00 |
| Micro Story | 7.00 |
| Animation Potential | 8.00 |

## Verdict

Strong batch with high identity fidelity and animation potential. Main weakness is repetitive hook families in cinematic and mechanical categories.

## Strengths

- Strong adherence to the 'Causal Premise' rule; almost every premise has a visible physical trigger.
- Consistent preservation of 2B's identity markers (blindfold, gloves, dress cut) across all shots.
- High animation potential due to clear motion vectors and implied next steps.

## Failures

- Repetition of 'hanging/dangling' motifs in cinematic categories (b01_cinematic, b02_cinematic).
- Several premises rely on similar 'industrial machinery failure' hooks (piston, valve, fan, silo) without enough variation in the type of threat.
- Some dynamic shots (e.g., b01_dynamic) lack sufficient narrative context for the action (why vault?).

## Desired patterns

- Integration of body appeal with specific physical strain or tension.
- Use of unique, specific props that interact directly with the character's clothing or body.
- Clear emotional micro-expressions tied to the physical cause.

## Undesired patterns

- Generic 'industrial ruin' settings without specific interacting elements.
- Repetition of the same causal force (e.g., multiple steam/pressure events).
- Passive poses where the environment is just a backdrop rather than an active threat.

## Repetition clusters

- **Hanging/Dangling from above in shafts/fans**: `e036_b01_cinematic`, `e036_b02_cinematic`
- **Industrial machinery failure/impact**: `e036_b01_medium`, `e036_b02_fullbody`, `e036_b04_cinematic`

## Recommendations for the next cycle

- Vary the 'Cinematic' category to include more horizontal scale or environmental interaction rather than just vertical hanging.
- Introduce non-mechanical causes (e.g., biological, elemental, social) to break the industrial monotony.
- Ensure dynamic shots have a clearer 'why' for the movement beyond just obstacle avoidance.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e036_b01_closeup` | closeup | 9.0 | 7.0 | 8.0 | 7.0 | Strong causal link (sparking wire) and clear physical reaction. Identity is preserved via glove and blindfold edge. |
| `e036_b01_medium` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Good use of recoil as a cause. The 'rusted piston' is specific enough to avoid generic ruin. |
| `e036_b01_fullbody` | fullbody | 9.0 | 7.0 | 8.0 | 9.0 | Excellent balance challenge. The falling gear striking the boot provides a clear consequence and motion vector. |
| `e036_b01_dynamic` | dynamic | 8.0 | 7.0 | 5.0 | 9.0 | High energy but weak narrative cause. Why is she vaulting? 'Jagged shard' is a minor obstacle without clear threat context (Locomotion Filler risk). |
| `e036_b01_cinematic` | cinematic | 8.0 | 9.0 | 7.0 | 8.0 | Strong scale contrast. Hanging from a fan blade is active interaction with the environment. |
| `e036_b02_closeup` | closeup | 9.0 | 7.0 | 8.0 | 6.0 | Steam jet provides clear cause. The 'stoic endurance' fits personality well. |
| `e036_b02_medium` | medium | 9.0 | 7.0 | 7.0 | 7.0 | Mechanical torque is a good cause. The gate sliding open implies a larger event. |
| `e036_b02_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 8.0 | Oil-slicked platform adds texture and risk. Stabilizing the valve wheel is a clear action. |
| `e036_b02_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Catching debris mid-spin is dynamic. The 'redirect' hint adds narrative depth. |
| `e036_b02_cinematic` | cinematic | 8.0 | 9.0 | 7.0 | 8.0 | Similar to b01_cinematic (hanging/dangling in shaft). Repetition of 'dangling from above' motif. |
| `e036_b03_closeup` | closeup | 9.0 | 7.0 | 8.0 | 6.0 | Worn glove reveals skin (consistent with 'black gloves' profile if damaged). Good tactile detail. |
| `e036_b03_medium` | medium | 9.0 | 7.0 | 7.0 | 7.0 | Prying a hatch is active. The 'corroded' detail adds specificity. |
| `e036_b03_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 8.0 | Balancing on a cable is good. 'Wind shear' from snapping cable is a valid cause. |
| `e036_b03_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Sliding to evade chandelier fragment is clear. Good use of friction/surface interaction. |
| `e036_b03_cinematic` | cinematic | 8.0 | 8.0 | 6.0 | 7.0 | Climbing a crumbling staircase is active. However, 'vast open sky' risks becoming atmospheric if the crumbling isn't emphasized enough. |
| `e036_b04_closeup` | closeup | 9.0 | 7.0 | 8.0 | 6.0 | Static electricity arc is a strong visual hook. 'Suppressed shock' fits personality. |
| `e036_b04_medium` | medium | 9.0 | 7.0 | 7.0 | 7.0 | Hoisting up from a drop is clear. The 'slick wet stone' adds texture. |
| `e036_b04_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 7.0 | Glass shard walkway is specific. Holding an artifact adds a 'why' to the movement. |
| `e036_b04_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Backflip from steam vent is high energy. Clear cause and consequence. |
| `e036_b04_cinematic` | cinematic | 8.0 | 9.0 | 7.0 | 8.0 | Centrifugal force in a silo is a strong physics-based hook. Active interaction with the wall. |

## Premises

### e036_b01_closeup — closeup

A tight closeup on 2B's black-gloved hand as it firmly grips a fraying, sparking copper wire protruding from a cracked wall panel; her fingers are tensed white-knuckle style against the heat and voltage, with a single bead of sweat rolling down her temple just above the edge of her blindfold, highlighting a micro-expression of strained focus.

### e036_b01_medium — medium

A waist-up shot showing 2B's torso twisted sharply to the left as she braces against the recoil of a massive, rusted piston slamming into her shoulder; the impact causes her black dress's cutout and puffy sleeves to ripple violently outward, revealing the tension in her core muscles while her hairband strains under the sudden lateral force.

### e036_b01_fullbody — fullbody

Full-body view of 2B balancing precariously on a narrow, fractured beam of metal suspended over a deep pit; her center of gravity is shifted heavily to one leg as she reaches out with both black-gloved hands to catch a falling gear that is currently striking the heel of her thigh-high boot, her body arched backward in reaction to the impact.

### e036_b01_dynamic — dynamic

2B mid-vault over a jagged shard of broken glass on the floor; her legs are extended behind her in a high kick, clearing the obstacle by inches, while her hair and dress hem trail back with significant motion blur, capturing the peak velocity of her jump as she lands on a lower platform just out of frame.

### e036_b01_cinematic — cinematic

Low-angle cinematic shot looking up at 2B as she hangs from the edge of a massive, rotating industrial fan blade; her weight is pulling on her black gloves which are wrapped around the metal rim, while her body dangles horizontally against the scale of the machinery, with dust and debris swirling upward toward her face in the turbulent air current.

### e036_b02_closeup — closeup

Extreme closeup on the side of 2B's face where her black blindfold is being forcibly pulled taut by a sudden, high-pressure jet of steam erupting from a fractured pipe; the fabric stretches thin over her cheekbone while a single drop of condensation rolls down her jawline, capturing the micro-expression of stoic endurance as she holds her breath to prevent the moisture from reaching her skin.

### e036_b02_medium — medium

Waist-up shot of 2B leaning back heavily against a heavy, rusted iron gate that is slowly sliding open on its hinges; her core muscles are visibly engaged to counteract the torque, causing the cutout in her dress to widen slightly as she twists her torso to maintain leverage, while her hairband digs into her short white hair under the strain of the sudden mechanical movement.

### e036_b02_fullbody — fullbody

Full-body view of 2B in a deep lunge on a slippery, oil-slicked metal platform, her front thigh-high boot bracing against the edge to prevent slipping as she reaches down with both black-gloved hands to stabilize a large, rolling industrial valve wheel that is currently spinning out of control toward her feet.

### e036_b02_dynamic — dynamic

2B mid-spin with her hair whipping in a tight blur around her head as she catches a falling, jagged piece of metal debris with one black-gloved hand; the momentum of the catch forces her hips to flare outward and her dress hem to lift sharply, revealing the tension in her thigh-high stockings as she prepares to redirect the object.

### e036_b02_cinematic — cinematic

High-angle cinematic shot looking down into a deep, circular shaft where 2B is dangling from a fraying rope attached to her wrist; below her, a massive, rotating fan blade sweeps through the air just inches from her boots, and she must twist her body sharply against the pull of gravity to avoid being clipped by the machinery.

### e036_b03_closeup — closeup

Extreme closeup of 2B's black-gloved hand gripping a jagged, rusted gear that is grinding against her palm; the friction has worn through the glove material at the knuckles, revealing raw skin beneath as she forces the mechanism to stop rotating, with a single drop of hydraulic fluid beading on the metal edge just before it drips onto her wrist.

### e036_b03_medium — medium

Waist-up shot of 2B leaning forward aggressively, using both black-gloved hands to pry open a sealed, corroded hatch on a curved metallic wall; her torso is compressed and twisted as she applies leverage, causing the puffy sleeves to bunch up at her elbows while the cutout in her dress strains against the tension in her core muscles.

### e036_b03_fullbody — fullbody

Full-body view of 2B mid-stride across a wide, broken suspension bridge cable; one thigh-high boot is planted firmly on the swaying wire while her other leg kicks out to push off from a nearby support beam, shifting her center of gravity dangerously high as she balances against the wind shear created by the snapping cable.

### e036_b03_dynamic — dynamic

2B executing a sharp, low slide across a polished marble floor to evade a falling chandelier fragment; her body is compressed close to the ground with motion blur trailing behind her dress hem and hair, while one hand skims the surface of the floor, sending up a spray of dust and debris in the wake of her rapid deceleration.

### e036_b03_cinematic — cinematic

Low-angle cinematic shot looking up at 2B as she stands atop a crumbling, spiraling staircase of stone; she is actively climbing upward against the pull of gravity, her boots digging into the loose steps as chunks of rock crumble away behind her, with dust swirling around her silhouette against the vast, open sky above.

### e036_b04_closeup — closeup

Tight closeup on 2B's jawline and the edge of her black blindfold as a sudden, sharp crack of static electricity arcs from a nearby conduit to her hair; her skin flinches minutely, pulling the fabric taut against her cheekbone, while a single strand of white hair stands on end, highlighting the micro-expression of suppressed shock rather than full panic.

### e036_b04_medium — medium

Waist-up shot of 2B leaning forward over a slick, wet stone ledge, her black-gloved hands gripping the edge to hoist herself up from a sudden drop in elevation; the effort causes her puffy sleeves to compress tightly at the elbows and the cutout of her dress to stretch visibly across her lower back, emphasizing the strain in her core as she resists sliding backward.

### e036_b04_fullbody — fullbody

Full-body view of 2B crouching low on a narrow, suspended walkway made of broken glass shards; she is carefully shifting her weight onto one thigh-high boot to avoid shattering the fragile surface beneath her other foot, while holding a small, glowing artifact in one gloved hand, her body compressed and tense against the risk of falling.

### e036_b04_dynamic — dynamic

2B executing a rapid backflip away from a bursting steam vent on the floor; her legs are tucked tightly to minimize air resistance, and her dress hem flares upward due to the explosive force pushing up from below, capturing the peak of her rotation as debris spins around her in a chaotic vortex.

### e036_b04_cinematic — cinematic

High-angle cinematic shot looking down at 2B as she is pinned against the interior wall of a massive, rotating cylindrical silo by centrifugal force; her boots dig into the curved metal surface to prevent sliding toward the bottom opening, while sparks fly from her gloves as they scrape against the rough texture of the machinery.
