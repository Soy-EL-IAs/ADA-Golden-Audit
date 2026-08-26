# Ada Viral Guide Evolution — Cycle 016

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.48/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 8.50 |
| Visual Appeal | 8.20 |
| Diversity | 7.00 |
| Repetition Control | 6.50 |
| Micro Story | 7.50 |
| Animation Potential | 7.20 |

## Verdict

Solid batch with strong identity and dynamic action in most categories. However, the Fullbody and Cinematic sections suffer from static 'waiting' poses that lack narrative consequence and animation potential. Needs more active engagement in these shot types to avoid repetition of passive stances.

## Strengths

- Strong adherence to character identity facts (blindfold, hair, outfit details) across all premises.
- Dynamic and Closeup categories are particularly strong with clear cause-and-effect interactions.
- Good use of fabric tension and hair movement as visual consequences of action.

## Failures

- Several Fullbody and Cinematic premises rely on static 'waiting' or 'balancing' poses that lack active narrative consequence (e016_b01_3, e016_b02_5, e016_b03_3, e016_b03_5, e016_b04_3, e016_b04_5).
- Repetition of 'arms at sides' or 'arms crossed' as a substitute for active engagement in multiple premises.
- Some Cinematic shots risk becoming atmospheric mood pieces if the interaction with the environment is too passive.

## Desired patterns

- Active physical reactions to immediate threats (dodging, catching, prying).
- Specific micro-expressions that reflect personality cracks (holding breath, squinting, annoyance).
- Clear causal triggers visible in the frame (falling debris, swinging chains, cracking glass).

## Undesired patterns

- Static balancing or waiting poses without immediate motion potential.
- 'Arms at sides' or 'arms crossed' used as a default stance rather than an active brace.
- Environmental framing that dominates over the character's specific interaction.

## Repetition clusters

- **Static Balancing/Waiting**: `e016_b01_3`, `e016_b02_5`, `e016_b03_3`, `e016_b03_5`, `e016_b04_3`, `e016_b04_5`
- **Wind/Hair Disruption**: `e016_b01_2`, `e016_b01_4`, `e016_b03_4`, `e016_b04_4`

## Recommendations for the next cycle

- Replace static 'balancing' or 'waiting' fullbody/cinematic premises with active interactions (e.g., stepping over a gap, pushing against a closing door).
- Reduce reliance on 'arms at sides' or 'arms crossed'; use hands for gripping, shielding, or reaching.
- Ensure every Cinematic premise has a specific physical interaction with the environment, not just framing.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e016_b01_1` | closeup | 9.0 | 8.0 | 7.0 | 8.0 | Strong tactile interaction. The 'pulling free' action provides clear cause and effect. Identity is preserved through the specific sleeve detail. |
| `e016_b01_2` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Classic wind interaction. The 'broken vent' provides a visible cause for the gust, avoiding pure atmosphere. Good tension between composure and physical disruption. |
| `e016_b01_3` | fullbody | 8.0 | 7.0 | 6.0 | 5.0 | Balancing is a static state rather than an active event. 'Looking down' is passive. Lacks the immediate threat or consequence that would drive a short animation loop effectively. |
| `e016_b01_4` | dynamic | 8.0 | 9.0 | 8.0 | 9.0 | Excellent dynamic energy. The hairband flying loose is a specific consequence of the dodge, adding narrative weight to the motion. |
| `e016_b01_5` | cinematic | 8.0 | 7.0 | 6.0 | 4.0 | Shielding from light is a valid reaction, but 'pressing back against wall' feels static. The cinematic framing risks becoming a wallpaper shot if the light interaction isn't intense enough. |
| `e016_b02_1` | closeup | 9.0 | 8.0 | 7.0 | 8.0 | The hanging oil drop creates high tension. The 'holding breath' micro-expression fits the personality guardrails perfectly. |
| `e016_b02_2` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Adjusting a slipped strap is a specific causal action. The fabric tension on the waist adds visual appeal without replacing the story. |
| `e016_b02_3` | fullbody | 9.0 | 8.0 | 7.0 | 7.0 | The 'sudden slip' provides the cause. The crouch and hand placement show active recovery rather than just posing on a slick floor. |
| `e016_b02_4` | dynamic | 8.0 | 9.0 | 8.0 | 9.0 | Kicking a gear is a strong physical interaction. The off-balance momentum suggests immediate follow-through motion. |
| `e016_b02_5` | cinematic | 7.0 | 8.0 | 6.0 | 5.0 | 'Arms at sides' and 'waits without flinching' border on the Passive Stare/Gameplay Idle anti-pattern. The turbine is a threat, but her reaction is too static. |
| `e016_b03_1` | closeup | 9.0 | 8.0 | 7.0 | 8.0 | Pinching a frayed thread is a subtle but clear micro-story. The 'annoyance' crack in composure fits the character profile well. |
| `e016_b03_2` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Prying open a hatch is a strong physical exertion. The sleeve compression adds visual detail and consequence to the action. |
| `e016_b03_3` | fullbody | 8.0 | 7.0 | 6.0 | 5.0 | Bracing against tremors is a reaction, but 'arms crossed' and 'wide stance' are very static poses. It lacks the dynamic energy of other fullbody entries. |
| `e016_b03_4` | dynamic | 8.0 | 9.0 | 8.0 | 9.0 | Tracking a projectile is high-energy. The hair whipping provides visual motion cues that support the animation potential. |
| `e016_b03_5` | cinematic | 7.0 | 8.0 | 6.0 | 4.0 | Similar to e016_b02_5. 'Arms at sides' and 'stands perfectly still' are weak reactions to a closing press. It feels like waiting rather than acting. |
| `e016_b04_1` | closeup | 9.0 | 8.0 | 7.0 | 8.0 | Pressing against cracking glass is a strong tactile and visual hook. The hair falling forward adds to the sense of urgency. |
| `e016_b04_2` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Leaning back from a chain is a clear dodge. The fabric tension and sleeve flare are good visual consequences of the motion. |
| `e016_b04_3` | fullbody | 8.0 | 7.0 | 5.0 | 4.0 | 'Testing stability' is a vague action. Balancing on a pillar edge is similar to e016_b01_3 in its static nature. Lacks a specific immediate threat or consequence. |
| `e016_b04_4` | dynamic | 8.0 | 9.0 | 8.0 | 9.0 | Mid-air twist is highly dynamic. The laser beam provides a clear cause for the contortion. Excellent motion potential. |
| `e016_b04_5` | cinematic | 7.0 | 8.0 | 6.0 | 5.0 | 'Back to viewer' and 'arms crossed' are passive. Watching a piston lower is less engaging than interacting with it. Feels like a setup shot rather than a peak moment. |

## Premises

### e016_b01_1 — closeup

2B's gloved hand firmly grips a jagged shard of glass protruding from her puffy sleeve, her expression remaining stoic despite the visible strain on the fabric as she pulls free.

### e016_b01_2 — medium

A sudden gust of wind from a broken vent whips up her black dress hem, revealing thigh-high stockings, while she tilts her head to keep her blindfold secure against the force.

### e016_b01_3 — fullbody

2B balances on one leg atop a narrow rusted beam, arms out for stability as she looks down at a crumbling floor far below, her dress skirt flaring slightly with the tension.

### e016_b01_4 — dynamic

Mid-dodge from a falling debris chunk, 2B twists her torso sharply to avoid impact, her hairband flying loose and short white hair scattering across her blindfold.

### e016_b01_5 — cinematic

Framed by the dark arch of a collapsed structure, 2B presses her back against the concrete wall to shield her blindfold from intense light streaming through a nearby shattered window.

### e016_b02_1 — closeup

A close-up on 2B's face as she holds her breath, lips pressed tight in restrained composure, while a thick drip of viscous industrial oil hangs from a rusted pipe directly above her blindfold, threatening to break.

### e016_b02_2 — medium

2B's torso twists sharply as she reaches behind her back to adjust a slipped strap on her shoulder armor, the movement causing her puffy feather-trimmed sleeves to bunch up and her black dress fabric to pull taut across her waist.

### e016_b02_3 — fullbody

Full-body view of 2B crouching low on a slick, oil-stained metal floor, her thigh-high boots gripping for traction as she carefully places one hand flat against the ground to steady herself after a sudden slip.

### e016_b02_4 — dynamic

2B lunges forward with her left leg extended, using it to kick away a rolling heavy gear just inches from her foot, her short white hair whipping back violently as the momentum of the dodge carries her off-balance.

### e016_b02_5 — cinematic

Framed by a massive, rotating industrial turbine blade in the foreground, 2B stands poised on a narrow maintenance catwalk, her back straight and arms at her sides as she waits for the heavy metal to swing past without flinching.

### e016_b03_1 — closeup

2B's gloved fingers are shown tightly pinching a frayed thread hanging from her black blindfold, pulling it taut with a subtle micro-expression of annoyance as she tries to maintain her composed expression.

### e016_b03_2 — medium

Waist-up view of 2B leaning forward slightly, using both hands to pry open a jammed rusted hatch cover, her puffy feather-trimmed sleeves compressing against the metal frame as she exerts force.

### e016_b03_3 — fullbody

2B stands with legs apart in a wide, stable stance on a cracked stone slab, her arms crossed over her chest to brace herself against the tremors of the shaking ground beneath her boots.

### e016_b03_4 — dynamic

2B snaps her head sharply to the left, tracking a high-speed projectile whizzing past her ear, causing her short white hair to whip violently while her body remains anchored in a defensive crouch.

### e016_b03_5 — cinematic

Framed by the massive, slowly closing jaws of an industrial press machine, 2B stands perfectly still in the center, her posture rigid and arms at her sides as she waits for the precise moment to step aside.

### e016_b04_1 — closeup

2B's gloved hand presses firmly against a vertical glass pane to steady herself as the surface cracks from an external impact, her short white hair falling forward to obscure part of her blindfold while she holds her breath in restrained composure.

### e016_b04_2 — medium

Waist-up view of 2B leaning sharply back to avoid a swinging chain, the motion pulling her black dress fabric taut across her torso and causing her puffy feather-trimmed sleeves to flare outward as she maintains an unblinking stare.

### e016_b04_3 — fullbody

Full-body view of 2B balancing on the edge of a crumbling concrete pillar, one leg extended forward to test stability while her arms are held slightly out, her thigh-high boots gripping the rough surface as dust settles around her feet.

### e016_b04_4 — dynamic

2B twists mid-air to evade a horizontal laser beam, her body contorting so that the light passes just millimeters from her nose, causing her short white hair to blur with motion and her black dress hem to ripple violently behind her.

### e016_b04_5 — cinematic

Framed by a towering, slowly descending mechanical piston in the background, 2B stands with her back to the viewer on a grated platform, arms crossed over her chest as she watches the massive metal component lower toward the gap beside her.
