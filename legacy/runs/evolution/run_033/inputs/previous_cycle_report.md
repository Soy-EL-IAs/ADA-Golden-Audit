# Ada Viral Guide Evolution — Cycle 032

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.17/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.00 |
| Visual Appeal | 8.00 |
| Diversity | 6.00 |
| Repetition Control | 5.00 |
| Micro Story | 7.00 |
| Animation Potential | 8.00 |

## Verdict

Solid batch with strong identity and animation potential, but penalized for significant repetition in cinematic and medium categories. The 'rotating fan' duplication is a clear failure of diversity enforcement.

## Strengths

- Consistent character identity with accurate outfit details (blindfold, puffy sleeves, stockings).
- Strong causal links in most premises; actions are triggered by visible environmental hazards.
- High animation potential due to clear motion verbs and implied physics (dust, sparks, fabric movement).
- Good use of scale in cinematic shots to frame the character actively.

## Failures

- Major repetition in Cinematic category: e032_b01_cinematic and e032_b02_cinematic both feature clinging to a rotating fan blade.
- Repetition in Medium category: e032_b01_medium (catching gear) and e032_b03_medium (catching bolt) share the same core mechanic of catching a falling heavy object.
- Fullbody premises lean heavily on 'balancing/stepping' which feels repetitive across b01, b02, b03, and b04.
- Some close-ups rely on subtle reactions that may be hard to distinguish in static images without strong lighting cues.

## Desired patterns

- Active interaction with specific objects (wrench, extinguisher) rather than just environmental forces.
- Clear cause-and-effect chains where the character's action directly responds to a visible threat.
- Use of distinct motion verbs for dynamic shots (vault, dive, somersault, swing).
- Integration of fabric physics (sleeves puffing, hem flaring) to enhance visual appeal without replacing the story.

## Undesired patterns

- Reusing the same environmental hazard (rotating fan blade) for multiple cinematic shots.
- Defaulting to 'catching falling object' as a medium shot mechanic.
- Passive balancing/stepping in fullbody shots without a strong secondary action or consequence.
- Abstract causes like 'electrical surge' that are harder to visualize than physical impacts.

## Repetition clusters

- **Clinging to rotating fan blade**: `e032_b01_cinematic`, `e032_b02_cinematic`
- **Catching a falling heavy object**: `e032_b01_medium`, `e032_b03_medium`
- **Balancing/Stepping on narrow/unstable surface**: `e032_b01_fullbody`, `e032_b02_fullbody`, `e032_b03_fullbody`, `e032_b04_fullbody`

## Recommendations for the next cycle

- Differentiate cinematic shots by varying the scale element (e.g., giant gear, collapsing bridge, massive light source) instead of reusing fan blades.
- Vary medium shot mechanics: include pushing, pulling, twisting to avoid, or interacting with machinery controls, not just catching/dodging.
- For fullbody shots, introduce more active consequences: slipping and recovering, jumping a gap, or being pulled by a force, rather than just maintaining balance.
- Ensure close-ups have distinct visual triggers (e.g., water droplet, dust cloud, light flare) that are clearly visible in the frame.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e032_b01_closeup` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Strong causal link (shattering glass). The 'crack in blindfold' is a minor factual risk but acceptable as damage. Good micro-expression. |
| `e032_b01_medium` | medium | 9.0 | 8.0 | 7.0 | 7.0 | Active interaction (catching gear). Good use of fabric physics. Slightly generic 'industrial' setting but the action is specific. |
| `e032_b01_fullbody` | fullbody | 9.0 | 8.0 | 6.0 | 7.0 | Balance challenge is clear. Wind cause is visible/inferable. Good silhouette. |
| `e032_b01_dynamic` | dynamic | 9.0 | 8.0 | 6.0 | 9.0 | High kinetic energy. Vaulting is a distinct verb. Dust trail adds consequence. |
| `e032_b01_cinematic` | cinematic | 8.0 | 9.0 | 7.0 | 8.0 | Strong scale contrast. Active grip on rotating fan blade avoids static silhouette trap. |
| `e032_b02_closeup` | closeup | 9.0 | 7.0 | 8.0 | 5.0 | Excellent micro-story (oil drop on hairband). Very specific cause and reaction. Low animation potential as it's a moment of impact. |
| `e032_b02_medium` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Dodge action is clear. 'Twisting' verb repeats from b01_medium but context differs (avoid vs catch). Acceptable. |
| `e032_b02_fullbody` | fullbody | 9.0 | 7.0 | 6.0 | 8.0 | Vibrating beam is a good cause. Similar to b01_fullbody (balance on narrow surface) but distinct enough due to vibration vs wind. |
| `e032_b02_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Diving low is distinct from vaulting. Clear cause (falling beam). Good motion blur description. |
| `e032_b02_cinematic` | cinematic | 8.0 | 9.0 | 6.0 | 7.0 | REPEATED CONCEPT: Clinging to rotating fan blade. Nearly identical to e032_b01_cinematic (upside down vs side). Major repetition failure. |
| `e032_b03_closeup` | closeup | 9.0 | 7.0 | 6.0 | 5.0 | Electrical surge causing vibration is a bit abstract for a close-up. 'Squeezing eyes shut' is a good reaction but less visually distinct than the oil drop. |
| `e032_b03_medium` | medium | 9.0 | 8.0 | 7.0 | 7.0 | REPEATED CONCEPT: Catching a falling heavy object. Very similar to e032_b01_medium (catching gear). 'Leaning back' vs 'twisting' is not enough differentiation for the core mechanic. |
| `e032_b03_fullbody` | fullbody | 9.0 | 7.0 | 6.0 | 6.0 | Stepping over glass is a form of locomotion. The guide warns against 'generic locomotion' without stake. Reaching for exit provides some stake, but it's weaker than the balance challenges in b01/b02. |
| `e032_b03_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Somersault is a distinct verb. Laser grid is a clear threat. Good variety in dynamic actions. |
| `e032_b03_cinematic` | cinematic | 8.0 | 9.0 | 7.0 | 8.0 | Descending elevator shaft is a strong scale element. Active grip on rivets. Distinct from fan blades. |
| `e032_b04_closeup` | closeup | 9.0 | 7.0 | 6.0 | 5.0 | Ice shard snapping off blindfold is a nice detail. 'Exhale' is subtle. Good micro-story. |
| `e032_b04_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Pulling a fire extinguisher is a specific interaction. 'Steadying' and 'pulling' are active verbs. Good variety from catching/dodging. |
| `e032_b04_fullbody` | fullbody | 9.0 | 7.0 | 6.0 | 7.0 | Stepping over a crack with steam. Similar to b03_fullbody (navigating obstacle). 'Hovering cautiously' is passive compared to the balance struggles in b01/b02. |
| `e032_b04_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Swinging a wrench is a distinct action. 'Twisting' verb repeats (3rd time), but the object and context are unique. |
| `e032_b04_cinematic` | cinematic | 8.0 | 9.0 | 7.0 | 8.0 | Grabbing a descending lift. Good scale and tension. Distinct from fan/elevator shaft. |

## Premises

### e032_b01_closeup — closeup

Close-up on 2B's face as a sudden crack in her blindfold reveals one eye widening in surprise, while a single white hair falls across her cheek from the impact of a nearby shattering glass pane.

### e032_b01_medium — medium

Medium shot of 2B twisting her torso to catch a heavy, falling gear with one gloved hand, the impact causing her puffy sleeves to puff out and her dress cutout to stretch taut against her side.

### e032_b01_fullbody — fullbody

Full body view of 2B maintaining balance on a narrow, cracked ledge as a gust of wind from below lifts her dress hem and thigh-high stockings, forcing her to grip the edge with both hands to prevent slipping.

### e032_b01_dynamic — dynamic

Dynamic action shot of 2B vaulting over a low debris pile in mid-air, her legs extended and boots kicking up a cloud of dust, with her blindfold fluttering violently from the forward momentum.

### e032_b01_cinematic — cinematic

Cinematic low-angle shot of 2B pulling herself up onto a massive, rotating industrial fan blade using only her grip on the metal rim, her body suspended against the scale of the machinery with sparks flying from the friction.

### e032_b02_closeup — closeup

Extreme close-up of 2B's jaw tightening and eyes narrowing in controlled annoyance as a heavy, viscous drop of black oil from a ruptured pipe above lands directly on her hairband, causing the fabric to twitch with the sudden weight.

### e032_b02_medium — medium

Medium shot of 2B twisting sharply to the left to avoid a swinging chain, her puffy feather-trimmed sleeves flaring outward against the wind of its passage while she grips a nearby pipe for stability with her black-gloved hand.

### e032_b02_fullbody — fullbody

Full body view of 2B balancing on a narrow, vibrating metal beam that is shaking violently from a distant explosion, her legs spread wide for stability and her boots gripping the rusted surface as her dress hem flutters in the updraft.

### e032_b02_dynamic — dynamic

Dynamic shot of 2B diving low under a falling steel I-beam, her body parallel to the ground and motion-blurred as she slides across the concrete floor, leaving a trail of dust behind her boots.

### e032_b02_cinematic — cinematic

Cinematic wide shot of 2B clinging to the underside of a massive, rotating ceiling fan blade, her body suspended upside down against the vast industrial dark as sparks shower down from the friction of the metal above.

### e032_b03_closeup — closeup

Extreme close-up of 2B's face as a sudden electrical surge from a nearby conduit causes her black blindfold to vibrate violently, forcing her to squeeze her eyes shut behind the fabric while a single strand of white hair is blown sharply across her cheek.

### e032_b03_medium — medium

Medium shot of 2B leaning back with one arm extended to catch a heavy, loose bolt plummeting from a cracked ceiling pipe, her puffy feather-trimmed sleeves billowing outward against the downdraft while she maintains a steady grip on the metal edge.

### e032_b03_fullbody — fullbody

Full body view of 2B stepping carefully across a field of broken glass shards scattered on a wet floor, her thigh-high boots pressing down to prevent slipping while she extends one gloved hand toward a distant exit, her dress hem swaying with the precise rhythm of her cautious steps.

### e032_b03_dynamic — dynamic

Dynamic shot of 2B executing a rapid backward somersault to evade a sweeping laser grid, her body tucked tight and motion-blurred as sparks shower from the surface she just cleared, leaving a trail of disturbed dust in her wake.

### e032_b03_cinematic — cinematic

Cinematic wide shot of 2B clinging to the side of a massive, descending elevator shaft as it drops rapidly, her body pressed flat against the rusted metal by the G-force while debris tumbles past her in slow motion, emphasizing her grip on the rivets.

### e032_b04_closeup — closeup

Extreme close-up of 2B's lips parting to release a sharp, controlled exhale as a jagged shard of crystallized ice snaps off her black blindfold and skitters across the concrete floor in front of her.

### e032_b04_medium — medium

Medium shot of 2B extending one arm to steady a wobbling, rusted fire extinguisher mounted on a tilted wall bracket, her other hand gripping the metal casing as she pulls it free with visible effort, causing her puffy feather-trimmed sleeve to strain and bulge at the shoulder.

### e032_b04_fullbody — fullbody

Full body view of 2B mid-step over a deep, jagged crack in the floor that is emitting wisps of steam, her left leg planted firmly on the stable side while her right boot hovers cautiously above the gap, her dress hem and thigh-high stockings billowing slightly from the heat vent below.

### e032_b04_dynamic — dynamic

Dynamic shot of 2B twisting her torso sharply to swing a heavy, detached pipe wrench through the air, her body rotating with the momentum and her white hair whipping around her face as she aims for a sparking electrical box.

### e032_b04_cinematic — cinematic

Cinematic low-angle shot of 2B reaching up to grab the handle of a descending, rusted service lift platform as it jolts downward, her arms fully extended and her body suspended in mid-air against the towering concrete pillar behind her.
