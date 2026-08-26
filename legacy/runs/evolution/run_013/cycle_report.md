# Ada Viral Guide Evolution — Cycle 013

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 6.58/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 8.50 |
| Visual Appeal | 7.50 |
| Diversity | 6.00 |
| Repetition Control | 5.00 |
| Micro Story | 6.50 |
| Animation Potential | 6.00 |

## Verdict

The set demonstrates strong identity preservation and some excellent micro-stories, but fails on diversity due to an over-reliance on industrial hazards and static atmospheric cinematics. The 'Industrial Hazard' family appears 4 times, violating the batch limit.

## Strengths

- Strong adherence to character identity markers (blindfold, dress, sleeves) across all premises.
- Several excellent examples of 'Clothing as Causal Agent' (e013_b02_02, e013_b04_02).
- Good variety in shot types and some effective dynamic actions.

## Failures

- Heavy reliance on 'Industrial Hazard' hook family (pipes, steam, debris, gears) which violates the limit of twice per batch.
- Multiple Cinematic premises suffer from 'Atmospheric Dominance' where the character is static and the environment provides all the interest.
- Repetition of 'balancing/standing on a ledge' poses in Fullbody categories without distinct narrative consequences.

## Desired patterns

- Specific, tangible interactions with props or clothing that drive the action.
- Clear cause-and-effect chains where the character's reaction is physically active and distinct.
- Use of organic/nature elements to break up industrial themes.

## Undesired patterns

- Static poses in high-stakes or atmospheric environments (e.g., standing on a rooftop in rain).
- Generic industrial hazards (steam, sparks) used as the primary hook without specific narrative weight.
- Low-stakes locomotion or balancing that lacks a clear 'what happens next' implication.

## Repetition clusters

- **Industrial Hazard**: `e013_b01_02`, `e013_b01_03`, `e013_b02_04`, `e013_b03_02`
- **Static Atmospheric Cinematic**: `e013_b01_05`, `e013_b02_05`, `e013_b04_05`

## Recommendations for the next cycle

- Reduce Industrial Hazard hooks to max 2 per batch; replace others with Personal Space or Organic interactions.
- For Cinematic shots, ensure the character is actively engaging with an element (e.g., catching a falling object from above) rather than just standing in scale.
- Avoid 'balancing on a ledge' as a default Fullbody pose; use it only if there is a specific narrative reason (e.g., escaping a collapsing structure).

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e013_b01_01` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Strong identity focus. The 'unseen sound' cause is slightly weak but the physical reaction (head turn/blindfold slip) provides a visible trigger. Good micro-story. |
| `e013_b01_02` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Wind as a cause is borderline 'atmosphere' unless the source (vent shaft) is clearly active. The reaction (twist/grip) is good. Identity markers are well-used. |
| `e013_b01_03` | fullbody | 8.0 | 7.0 | 6.0 | 5.0 | 'Falling gear mechanism' is a generic industrial prop. Balancing on a tank rim is a standard trope. Lacks specific narrative weight beyond 'catch thing'. |
| `e013_b01_04` | dynamic | 8.0 | 7.0 | 6.0 | 8.0 | Good dynamic energy. 'Shard of glass' is a bit generic but the dodge action is clear. Motion blur usage is appropriate for the category. |
| `e013_b01_05` | cinematic | 7.0 | 8.0 | 4.0 | 3.0 | Classic 'Atmospheric Dominance' failure. Standing on a rooftop in rain with hand on hip is a static pose. The storm is the main subject, not her action. |
| `e013_b02_01` | closeup | 9.0 | 8.0 | 6.0 | 5.0 | Raindrop on blindfold is a nice micro-detail. However, 'rain' as the sole cause feels atmospheric again. The reaction (narrowing eye) is subtle. |
| `e013_b02_02` | medium | 9.0 | 8.0 | 8.0 | 7.0 | Excellent use of clothing as a causal agent (sleeve snag). Clear tension and specific interaction with the environment. Strong micro-story. |
| `e013_b02_03` | fullbody | 8.0 | 7.0 | 5.0 | 4.0 | 'Testing stability' is a low-stakes action. Balancing on a ledge is repetitive with e013_b01_03. Lacks a strong narrative consequence. |
| `e013_b02_04` | dynamic | 8.0 | 7.0 | 6.0 | 8.0 | Swinging pipe is a classic industrial hazard. Good dynamic action, but contributes to the 'Industrial Hazard' repetition cluster. |
| `e013_b02_05` | cinematic | 7.0 | 8.0 | 4.0 | 3.0 | Another 'Atmospheric Dominance' failure. Standing on a precipice with arms crossed is static. The fog/lightning are the hook, not her action. |
| `e013_b03_01` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Hair blocking vision is a specific, physical cause. The reaction (tilting head to calculate angle) shows intelligence and composure. Good micro-story. |
| `e013_b03_02` | medium | 8.0 | 7.0 | 6.0 | 7.0 | Steam from a pipe is another Industrial Hazard. The flinch/recoil is reactive but somewhat generic. Adds to the repetition cluster. |
| `e013_b03_03` | fullbody | 8.0 | 7.0 | 6.0 | 5.0 | 'Root system' suggests an organic environment, which is good for diversity. However, 'mid-fall crouch' is a common pose. The cause (falling) is clear but the consequence is vague. |
| `e013_b03_04` | dynamic | 8.0 | 7.0 | 6.0 | 8.0 | Low slide is a good dynamic action. 'Falling debris chunk' is generic but the motion is clear. Good use of friction/water spray for visual interest. |
| `e013_b03_05` | cinematic | 7.0 | 8.0 | 5.0 | 4.0 | Glass floor cracking is a strong visual hook. However, 'looking up with calm determination' while standing still is borderline static. The scale is impressive but the character's agency is low. |
| `e013_b04_01` | closeup | 9.0 | 8.0 | 6.0 | 5.0 | Dust settling is a subtle cause. The 'startled reflex' fits the personality guardrails (brief crack in restraint). Good micro-detail. |
| `e013_b04_02` | medium | 9.0 | 8.0 | 8.0 | 7.0 | Elevator door snag is a specific, modern-industrial interaction. Clear tension and cause-and-effect. Strong micro-story. |
| `e013_b04_03` | fullbody | 8.0 | 7.0 | 6.0 | 5.0 | Plucking a rose is a nice contrast to the industrial themes. However, 'balancing on an archway' while reaching down is a bit contrived. The narrative weight of the rose is unclear. |
| `e013_b04_04` | dynamic | 8.0 | 7.0 | 6.0 | 8.0 | Snapping vine is an Organic/Nature interaction. Good dynamic spin action. Provides necessary diversity against the industrial themes. |
| `e013_b04_05` | cinematic | 7.0 | 8.0 | 4.0 | 3.0 | Cathedral altar is a strong setting. However, 'looking up with calm determination' while standing alone is static. The light shafts are the main visual hook. |

## Premises

### e013_b01_01 — closeup

2B's face is framed by a sudden, sharp intake of breath as her black blindfold slips slightly down the bridge of her nose due to a rapid head turn; her left hand rises instinctively to steady it while her visible eye widens with focused alertness at an unseen sound.

### e013_b01_02 — medium

A strong gust of wind from a broken ventilation shaft catches the hem of 2B's black dress, lifting it to reveal her thigh-high stockings; she twists her torso sharply to maintain balance, one hand gripping the edge of a metal console for stability while her expression remains composed but tense.

### e013_b01_03 — fullbody

2B balances on the narrow, rusted rim of an industrial water tank in a flooded courtyard; her weight shifts precariously to one leg as she extends a gloved hand to catch a falling gear mechanism before it hits the water below, her silhouette emphasizing tension and precision.

### e013_b01_04 — dynamic

Mid-leap over a jagged crack in the floor, 2B's puffy sleeves billow with motion blur as she twists her hips to dodge an incoming shard of glass; her legs are extended dynamically forward, and her hair whips behind her, capturing the peak moment of evasive action.

### e013_b01_05 — cinematic

From a low angle looking up through a broken skylight, 2B stands on the edge of a crumbling rooftop against a vast, stormy sky; rain streaks her face and darkens her dress as she looks down at the city below, one hand resting on her hip in a posture of weary command amidst the chaos.

### e013_b02_01 — closeup

A macro view of 2B's face as a single, heavy raindrop strikes the center of her black blindfold with audible force; her visible eye narrows in sharp, focused determination while her jaw tightens, and the water beads on the fabric begin to slide toward the edge, threatening to obscure her vision.

### e013_b02_02 — medium

2B's right puffy feather-trimmed sleeve has snagged on a jagged piece of rebar protruding from the wall; she leans her torso back to create tension, pulling with her left hand while her black dress stretches taut across her waist, revealing the strain in her posture as she tries to free herself without tearing the fabric.

### e013_b02_03 — fullbody

Perched on the high ledge of a shattered balcony, 2B balances with one leg extended forward to test the stability of a cracked tile; her body weight is shifted back into her heels for counterbalance, and her hand hovers near her thigh-high boot, ready to push off or correct her stance as dust motes swirl around her feet.

### e013_b02_04 — dynamic

In a sharp, low-angle twist, 2B ducks beneath a swinging pipe that has just missed her head; motion blur streaks across her short white hair and the hem of her dress flares upward from the rapid rotation, while her gaze locks onto the next obstacle in the sequence with intense, predictive focus.

### e013_b02_05 — cinematic

From a wide, deep-focus perspective, 2B stands alone on a precipice overlooking an abyss of fog; the wind whips her dress and stockings against her legs, creating a sense of isolation, but she remains grounded with arms crossed, exuding calm confidence as distant lightning illuminates her silhouette in stark contrast to the dark void.

### e013_b03_01 — closeup

2B's visible eye snaps wide in sudden, sharp shock as a loose strand of her short white hair blows across the black blindfold, momentarily blocking her vision; her brow furrows with intense focus as she tilts her head slightly to calculate the precise angle needed to clear it without using her hands.

### e013_b03_02 — medium

A sudden, violent hiss of escaping steam from a ruptured pipe directly above causes 2B to flinch, pulling her torso back sharply; the force of her recoil twists her upper body, causing the fabric of her black dress to ripple and the puffy feather-trimmed sleeves to billow outward as she shields her face with one gloved hand.

### e013_b03_03 — fullbody

2B is caught mid-fall, suspended in a precarious crouch above a chasm; her right leg extends downward to test the stability of a crumbling ledge while her left arm reaches out desperately for a protruding root system, her body twisted in a tight coil that emphasizes the tension in her thighs and the strain on her gloves.

### e013_b03_04 — dynamic

In a blur of rapid motion, 2B executes a low slide across a slick, wet floor to evade a falling debris chunk; her left leg extends forward with kinetic force while her right hand scrapes against the ground for friction, sending up a spray of water droplets and dust that highlights the speed and urgency of her escape.

### e013_b03_05 — cinematic

From an extreme low angle, 2B stands at the center of a vast, circular glass floor that is beginning to crack beneath her weight; the spiderweb fractures radiate outward from her boots as she looks up with calm, confident determination, her silhouette framed against the towering, spiraling architecture of the building above.

### e013_b04_01 — closeup

A macro view of 2B's face as a fine layer of white dust settles onto her black blindfold; her visible eye blinks rapidly in a sharp, startled reflex to the tactile surprise, while her fingers twitch slightly at her temple, ready to brush the intrusion away without disturbing her composure.

### e013_b04_02 — medium

2B's left puffy feather-trimmed sleeve is caught in the narrow gap of a closing elevator door; she leans her torso forward with controlled tension to pull it free, her black dress stretching taut across her waist as she holds her breath, focusing intensely on the precise moment the mechanism reverses.

### e013_b04_03 — fullbody

2B stands poised on a crumbling stone archway in an overgrown garden, her weight shifted back to maintain balance as she reaches down with one gloved hand to pluck a single red rose from the weeds below; her silhouette is elegant and tense against the chaotic greenery, emphasizing the contrast between her precision and the wild environment.

### e013_b04_04 — dynamic

In a high-speed spin to evade a snapping vine, 2B's short white hair whips in a circular motion blur while her black dress flares outward like a dark umbrella; her legs are bent in a low, athletic tuck, and her gaze locks onto the next threat with predictive speed, capturing the kinetic energy of the turn.

### e013_b04_05 — cinematic

From a wide, low angle in a vast, abandoned cathedral, 2B stands alone on the raised altar as shafts of dusty light pierce through broken stained glass; she looks up at the fractured ceiling with calm determination, her small figure anchored by confidence against the immense scale of the decaying architecture.
