# Ada Viral Guide Evolution — Cycle 010

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 6.83/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 8.50 |
| Visual Appeal | 7.00 |
| Diversity | 6.00 |
| Repetition Control | 5.50 |
| Micro Story | 6.50 |
| Animation Potential | 7.50 |

## Verdict

The set demonstrates strong identity preservation and good animation potential, particularly in dynamic shots. However, it suffers from significant repetition in causal hooks (wind) and passive cinematic framing. The micro-stories are often low-stakes or generic, lacking the specific narrative flavor of the source material. Needs tighter control on hook diversity and location specificity.

## Strengths

- Consistent adherence to 2B's visual identity (blindfold, hair, dress details).
- Strong animation potential in dynamic shots with clear directional energy.
- Several premises successfully integrate environmental causes (wind, debris, water) into character reactions.

## Failures

- Heavy reliance on 'Wind/Draft' as a causal hook across multiple batches (b01 closeup/fullbody, b03 medium).
- Repetitive location types: Corridors, Precipices/Edges, and Doorways appear frequently without distinct narrative variation.
- Several cinematic shots rely on passive poses ('looking down', 'standing still') rather than active engagement with the environment.
- Hair adjustment actions (b02 medium, b04 medium) are nearly identical in concept and low-stakes.

## Desired patterns

- Unique environmental interactions specific to NieR:Automata lore (e.g., Pod interaction, Yoctopede debris, specific machine types).
- Clearer cause-and-effect chains where the environment actively challenges the character's composure.
- More varied shot compositions that avoid default low-angle silhouettes.

## Undesired patterns

- Generic 'wind blowing hair' as a primary hook without specific context.
- Passive poses in cinematic shots (standing, looking) that lack immediate narrative tension.
- Repetitive mundane actions like fixing hair/clothing without higher stakes.

## Repetition clusters

- **Wind/Draft Interaction**: `e010_b01_closeup`, `e010_b01_fullbody`, `e010_b03_medium`
- **Hair/Clothing Adjustment (Mundane)**: `e010_b02_medium`, `e010_b04_medium`
- **Passive Cinematic Pose (Silhouette/Doorway)**: `e010_b01_cinematic`, `e010_b02_cinematic`, `e010_b03_cinematic`

## Recommendations for the next cycle

- Limit 'Wind' to one premise per batch and ensure it has a specific source (e.g., broken AC unit, explosion shockwave).
- Replace generic locations with specific NieR:Automata set pieces (e.g., Bunker interior, specific machine ruins, Pod docking bay).
- For cinematic shots, require an active interaction or imminent threat rather than just a dramatic angle on a static pose.
- Differentiate hair/clothing adjustments by adding stakes (e.g., fixing blindfold before battle vs. casual adjustment).

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e010_b01_closeup` | closeup | 9.0 | 7.0 | 6.0 | 8.0 | Strong identity markers (blindfold, hair). The 'wind' cause is generic but the reaction (tightening jaw) fits personality. Good animation potential. |
| `e010_b01_medium` | medium | 8.0 | 6.0 | 7.0 | 5.0 | 'Minor stumble' is a weak cause for such a composed character. Adjusting collar is a good micro-story but feels slightly mundane without stronger context. |
| `e010_b01_fullbody` | fullbody | 9.0 | 8.0 | 6.0 | 7.0 | Precipice is a generic location. The wind cause repeats the closeup's hook family. Visual appeal is high due to silhouette and sleeve flare. |
| `e010_b01_dynamic` | dynamic | 8.0 | 7.0 | 6.0 | 9.0 | 'Sudden sound' is vague but acceptable for dynamic action. The pivot motion is clear and animatable. Lacks specific environmental interaction. |
| `e010_b01_cinematic` | cinematic | 8.0 | 7.0 | 5.0 | 6.0 | Doorway is a very common trope. 'Caught in the act of stepping out' is passive; it's a pose rather than an event. Backlighting is effective but cliché. |
| `e010_b02_closeup` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Gripping a crumbling ledge is a strong micro-story (cause: drop/instability). Focus on hands/gloves adds texture detail. Good tension. |
| `e010_b02_medium` | medium | 9.0 | 6.0 | 5.0 | 4.0 | Adjusting hairband is a very low-stakes action. 'Rigid and formal' posture contradicts the casual nature of fixing hair slightly. Weak causal trigger. |
| `e010_b02_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 5.0 | Pushing aside a curtain is a good interaction. However, 'narrow corridor' is a repetitive location type seen in other premises. Action is somewhat static. |
| `e010_b02_dynamic` | dynamic | 8.0 | 7.0 | 6.0 | 9.0 | Stepping over debris is clear and dynamic. The dress hem lifting adds visual interest. Good kinetic energy. |
| `e010_b02_cinematic` | cinematic | 8.0 | 7.0 | 5.0 | 4.0 | 'Unseen threat' is an atmosphere substitute for an event. Looking over shoulder is a pure pose. The 'dark void' background is generic. |
| `e010_b03_closeup` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Dust mote interaction is unique and intimate. 'Holding breath' is a subtle but clear micro-story. Excellent use of close-up framing. |
| `e010_b03_medium` | medium | 8.0 | 6.0 | 5.0 | 4.0 | Wind/draft cause repeats the b01 family. 'Perfectly still' contradicts the 'flaps violently' description slightly. Feels like a static pose against wind. |
| `e010_b03_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 5.0 | Moss-covered stone is a specific detail, but 'narrow gap' location is repetitive. Balancing act is clear but lacks narrative weight. |
| `e010_b03_dynamic` | dynamic | 8.0 | 7.0 | 6.0 | 9.0 | Leaping over a crate is standard dynamic action. 'Minimizing air resistance' is a nice technical detail for an android. Good motion. |
| `e010_b03_cinematic` | cinematic | 8.0 | 7.0 | 5.0 | 4.0 | 'Lowering gaze to observe' is passive. The 'recessed alcove' location adds little narrative value. Feels like a portrait with dramatic lighting. |
| `e010_b04_closeup` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Broken pipe spray is a strong environmental cause. 'Unexpected cleansing' adds personality nuance. Good sensory detail. |
| `e010_b04_medium` | medium | 9.0 | 6.0 | 5.0 | 4.0 | Re-threading hair is very similar to b02_medium (adjusting hairband). Repetitive hook family. Low stakes action. |
| `e010_b04_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 5.0 | Balancing on a pipe is visually interesting but physically precarious for a dress. 'Industrial sector' location is generic. Static balance pose. |
| `e010_b04_dynamic` | dynamic | 8.0 | 7.0 | 6.0 | 9.0 | Ducking under a beam is clear and dynamic. Good use of motion blur description. Standard obstacle navigation. |
| `e010_b04_cinematic` | cinematic | 8.0 | 8.0 | 7.0 | 6.0 | Cracking window is a strong visual hook. 'Arms crossed' is a static pose within a dynamic event, which creates tension but limits animation flow. |

## Premises

### e010_b01_closeup — closeup

Close-up on 2B's face and upper shoulders as a sudden gust of wind ruffles her short white hair against the black blindfold; she maintains a stoic expression but tightens her jaw slightly, with one gloved hand raised mid-motion to smooth down a stray lock.

### e010_b01_medium — medium

Medium shot from the waist up showing 2B adjusting the high collar of her black dress after a minor stumble; her posture remains upright and composed, but the tension in her shoulders reveals a brief crack in her composure as she straightens the fabric.

### e010_b01_fullbody — fullbody

Full-body shot of 2B standing on a precipice edge, her weight shifted back to maintain balance against a strong crosswind that flares out the puffy feather-trimmed sleeves; she looks forward with calm confidence while her thigh-high boots grip the uneven surface.

### e010_b01_dynamic — dynamic

Dynamic action shot of 2B mid-turn, her black dress and stockings swirling with the motion as she reacts to a sudden sound; her gloved hands are positioned for balance rather than combat, capturing the fluidity of her quick pivot.

### e010_b01_cinematic — cinematic

Low-angle cinematic shot looking up at 2B as she pauses in a doorway, backlit by harsh light that silhouettes her hair and blindfold; she is caught in the act of stepping out, one leg forward, creating a dramatic contrast between her dark figure and the bright void behind her.

### e010_b02_closeup — closeup

Extreme close-up on 2B's gloved hand as it grips the edge of a crumbling stone ledge, her knuckles white with tension; the black fabric of her glove stretches taut against the rough texture, while the blurred background hints at a sudden drop she is bracing for.

### e010_b02_medium — medium

Medium shot capturing 2B from the waist up as she reaches behind her back to adjust a loose hairband, her posture rigid and formal despite the casual action; the puffy feather-trimmed sleeves flare slightly with the movement, emphasizing the contrast between her elegant attire and the mundane task.

### e010_b02_fullbody — fullbody

Full-body view of 2B standing in a narrow corridor, using one gloved hand to push aside a heavy curtain that is drifting back into the frame; her thigh-high boots are planted firmly for stability, and her gaze remains fixed forward with disciplined focus as she navigates the obstruction.

### e010_b02_dynamic — dynamic

Dynamic shot of 2B mid-step over a low debris barrier, her black dress hem lifting to reveal the top of her thigh-high stockings; her body leans forward with kinetic energy, arms swinging for balance, capturing the split second before she clears the obstacle.

### e010_b02_cinematic — cinematic

Cinematic wide-angle shot from a low perspective looking up at 2B as she looks down over her shoulder, the harsh overhead lighting casting deep shadows across her blindfold and face; the composition isolates her silhouette against a dark void, emphasizing her stoic detachment while implying an unseen threat approaching from behind.

### e010_b03_closeup — closeup

Extreme close-up on 2B's face as a single, persistent dust mote hovers directly in front of her blindfold; her eyes dart slightly behind the fabric while she holds her breath to avoid disturbing it, capturing a moment of intense, silent focus and the subtle tension in her cheeks.

### e010_b03_medium — medium

Medium shot from the waist up showing 2B standing in a drafty corridor where a loose hem of her black dress flaps violently against her legs; she remains perfectly still and composed, using only subtle weight shifts to counterbalance the pull, highlighting her disciplined control amidst the chaotic fabric movement.

### e010_b03_fullbody — fullbody

Full-body shot of 2B stepping cautiously onto a slippery, moss-covered stone slab in a narrow gap; her thigh-high boots find purchase with precision as she extends one arm to touch the wall for stability, her posture elongated and graceful despite the precarious footing.

### e010_b03_dynamic — dynamic

Dynamic action shot of 2B mid-leap over a low, unstable wooden crate; her puffy feather-trimmed sleeves trail behind her with the momentum, and her black dress lifts to reveal the full length of her thigh-high stockings as she tucks her knees tightly to minimize air resistance.

### e010_b03_cinematic — cinematic

Low-angle cinematic shot looking up at 2B from a recessed alcove as she pauses on the upper landing, her silhouette framed by the dark doorway; she is caught in the act of lowering her gaze to observe something below, creating a dramatic vertical composition that emphasizes her height and detached authority.

### e010_b04_closeup — closeup

Extreme close-up on 2B's face and the black blindfold as a fine mist of water droplets from a broken pipe sprays directly into her path; she tilts her chin up slightly to let the spray wash over the fabric, her expression remaining serene but with a subtle tension in her jaw as she holds still for the unexpected cleansing.

### e010_b04_medium — medium

Medium shot from the waist up showing 2B using both gloved hands to carefully re-thread a loose strand of her short white hair back under her hairband; her posture is rigid and focused, with the puffy feather-trimmed sleeves bunching at the elbows as she concentrates on the precise task, revealing a rare moment of mundane vulnerability amidst her usual stoicism.

### e010_b04_fullbody — fullbody

Full-body shot of 2B balancing on one leg atop a narrow, unstable pipe in an industrial sector, her free arm extended to the side for counterbalance; her black dress and thigh-high stockings are taut against her silhouette as she adjusts her center of gravity with microscopic precision, showcasing her athletic control and elegant posture under precarious conditions.

### e010_b04_dynamic — dynamic

Dynamic action shot of 2B ducking sharply underneath a low-hanging rusted beam, her black dress hem flaring out behind her as she tucks her head down; the motion blurs the edges of her puffy sleeves while her eyes remain sharp and focused on the gap ahead, capturing the split-second agility required to navigate the tight obstacle.

### e010_b04_cinematic — cinematic

Cinematic over-the-shoulder shot from a low angle looking up at 2B as she stands silhouetted against a massive, circular industrial window that is slowly cracking; shards of glass begin to rain down around her, but she remains perfectly still with arms crossed, the contrast between the chaotic destruction and her composed stance creating a dramatic tension about whether she will move.
