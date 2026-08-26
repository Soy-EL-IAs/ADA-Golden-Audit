# Ada Viral Guide Evolution — Cycle 038

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.75/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.50 |
| Visual Appeal | 8.00 |
| Diversity | 7.50 |
| Repetition Control | 6.50 |
| Micro Story | 7.50 |
| Animation Potential | 7.50 |

## Verdict

Strong batch with high identity consistency and good causal logic, but suffers from passive cinematic framing and repetitive medium-shot mechanics. Needs more active environmental engagement in wide shots.

## Strengths

- Consistent and accurate character identity across all 20 premises.
- Strong causal logic in most premises (visible cause -> physical reaction).
- Effective use of clothing physics (dress cutout, sleeves, stockings) to enhance visual appeal without losing narrative focus.
- Good variety in causal forces (mechanical, elemental, biological).

## Failures

- Cinematic category suffers from passive 'standing and looking' poses in 3 out of 4 entries (b01, b02, b03), lacking active interaction.
- Repetition of 'torso twist + fabric tension' as the primary visual hook in multiple medium shots (b01, b03, b04).
- Several dynamic premises rely on similar 'mid-air evasion with hair trailing' mechanics, reducing distinctiveness.

## Desired patterns

- Active environmental interaction where the character changes the state of the environment or is physically altered by it.
- Distinctive body language that reflects personality (restraint, composure) rather than just generic action poses.
- Clear cause-and-effect chains visible in a single frame.

## Undesired patterns

- Passive observation ('staring at', 'looking out') as the primary action.
- Atmospheric mood pieces (backlighting, dust) substituting for specific physical events.
- Repeated use of 'twisting torso to show dress tension' without varying the underlying cause or body mechanics.

## Repetition clusters

- **Passive Cinematic Stance**: `e038_b01_cinematic`, `e038_b02_cinematic`, `e038_b03_cinematic`
- **Torso Twist & Fabric Tension (Medium)**: `e038_b01_medium`, `e038_b03_medium`, `e038_b04_medium`
- **Mid-Air Evasion with Trailing Hair (Dynamic)**: `e038_b01_dynamic`, `e038_b02_dynamic`, `e038_b04_dynamic`

## Recommendations for the next cycle

- For Cinematic shots, require an active physical interaction with the environment (e.g., pushing against a closing door, catching a falling object) rather than just standing in it.
- Vary the body mechanics in Medium shots; avoid defaulting to 'torso twist' for every mechanical cause. Use leg movement, head tilt, or arm extension instead.
- Differentiate Dynamic shots by varying the type of motion (e.g., vertical drop vs horizontal slide vs rotational spin) and the specific clothing element reacting (sleeves vs hem vs hair).

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e038_b01_closeup` | closeup | 9.5 | 7.0 | 8.5 | 6.0 | Strong causal link (condensation drop) to reaction (flinch). Identity markers (blindfold, steam context) are clear. Slightly low animation potential as the action is a micro-flinch. |
| `e038_b01_medium` | medium | 9.5 | 8.5 | 8.0 | 7.5 | Good use of mechanical cause (tilting floor) to create clothing tension (cutout dress). Visual appeal is high due to the torso twist and fabric interaction. |
| `e038_b01_fullbody` | fullbody | 9.5 | 8.0 | 8.5 | 8.0 | Excellent biological/organic cause (vines coiling). Creates immediate threat and physical consequence (balance shift). Strong silhouette. |
| `e038_b01_dynamic` | dynamic | 9.0 | 8.5 | 7.5 | 9.0 | High energy spin with clear cause (shrapnel). Hair and sleeves flaring adds visual noise/interest. Slightly generic 'evasive maneuver' but well-executed. |
| `e038_b01_cinematic` | cinematic | 9.5 | 7.5 | 6.5 | 4.0 | Weak micro-story. 'Staring down at a shadow' is passive observation rather than active interaction. Relies heavily on atmosphere (backlighting/dust) to carry the scene. |
| `e038_b02_closeup` | closeup | 9.5 | 7.0 | 8.0 | 6.5 | Clear cause (glass shard) and reaction (recoil/sting). Good tension in the face. The 'dust motes' detail is atmospheric but supports the stillness after impact. |
| `e038_b02_medium` | medium | 9.5 | 8.0 | 7.5 | 7.0 | Mechanical cause (jammed hatch) leads to physical strain. Good use of gloves and sleeve tension. Slightly static compared to other medium shots but effective. |
| `e038_b02_fullbody` | fullbody | 9.5 | 8.5 | 7.5 | 8.5 | Vertical descent with elemental cause (smoke). Good use of stockings and dress hem interaction. Clear 'escape' narrative. |
| `e038_b02_dynamic` | dynamic | 9.5 | 8.0 | 7.0 | 9.0 | Leap over crack with falling debris cause. Good momentum implied by hair/blindfold trailing. Slightly similar to b01_dynamic in terms of 'mid-air evasion' but distinct enough. |
| `e038_b02_cinematic` | cinematic | 9.5 | 7.0 | 6.0 | 4.5 | Passive standing on sinking ship. 'Looking out' is weak interaction. Relies on the burning deck for visual interest rather than character action. |
| `e038_b03_closeup` | closeup | 9.5 | 7.5 | 8.0 | 6.0 | Elemental cause (cold/coolant) with visible effect (mist/frost). Good physical reaction (pulling collar up). Strong sensory detail. |
| `e038_b03_medium` | medium | 9.5 | 8.5 | 7.5 | 7.5 | Mechanical cause (swinging chain) leads to torso twist and dress tension. Good use of gloves for stability. Clear danger. |
| `e038_b03_fullbody` | fullbody | 9.5 | 7.5 | 7.0 | 6.5 | Debris crash cause. Bracing pose is good but slightly static compared to the vine/beam premise. Hair swept back adds motion. |
| `e038_b03_dynamic` | dynamic | 9.5 | 8.5 | 7.5 | 9.5 | High energy somersault over lava with steam jet cause. Excellent use of heat distortion and fabric whipping. Very strong visual hook. |
| `e038_b03_cinematic` | cinematic | 9.5 | 7.0 | 6.5 | 4.0 | Colossus shadow cause creates wind effect on hair/blindfold. However, the character is still 'standing alone' and observing. Passive stance weakens the cinematic impact. |
| `e038_b04_closeup` | closeup | 9.5 | 7.5 | 8.5 | 6.5 | Biological cause (beetles) leading to restrained reaction (holding breath/stillness). Excellent personality expression (restraint vs instinct). |
| `e038_b04_medium` | medium | 9.5 | 8.0 | 7.5 | 7.0 | Mechanical cause (ladder jolt) leading to balance loss and torso twist. Good use of sleeve tension. Similar structural logic to b01_medium but distinct enough. |
| `e038_b04_fullbody` | fullbody | 9.5 | 7.5 | 7.0 | 6.5 | Crate sliding cause leads to crouch/balance shift. Good use of boot tips and weight distribution. Slightly less dramatic than other fullbody shots. |
| `e038_b04_dynamic` | dynamic | 9.5 | 8.0 | 7.0 | 8.5 | Horizontal slide with kick action. Clear cause (loose stone/debris). Good lateral motion implied by hair trailing. |
| `e038_b04_cinematic` | cinematic | 9.5 | 8.5 | 7.5 | 6.0 | Bird landing cause creates structural shudder/crack. Better than previous cinematic shots because the environment reacts to a specific event (bird) rather than just being present. |

## Premises

### e038_b01_closeup — closeup

2B's composure cracks slightly as a single drop of condensation from an overhead industrial pipe lands on her black blindfold, causing her to flinch and tighten her jaw while steam rises around her neck.

### e038_b01_medium — medium

2B grips the edge of a rusted metal railing as a sudden mechanical lurch causes the floor to tilt, forcing her to twist her torso sharply and pulling the fabric of her cutout dress taut across her waist.

### e038_b01_fullbody — fullbody

2B balances precariously on a narrow, moss-covered beam over a drop, shifting her weight to one leg as thick vines rapidly coil around her thigh-high boots, threatening to pull her off-center.

### e038_b01_dynamic — dynamic

2B is captured mid-spin in a tight evasive maneuver as shrapnel from an exploding machine cuts through the air, her white hair and puffy sleeves flaring outward with the momentum of the rotation.

### e038_b01_cinematic — cinematic

2B stands on a high stone ledge overlooking a vast chasm, backlit by the warm glow of a distant fire that illuminates the dust particles swirling around her, as she stares down at a shadow moving in the depths below.

### e038_b02_closeup — closeup

A cold shock ripples through 2B's features as a shard of shattered glass from a nearby window frame clips the edge of her black blindfold, causing her to recoil sharply and tighten her lips against the sting while dust motes hang suspended in the sudden stillness.

### e038_b02_medium — medium

2B leans forward to pry open a jammed maintenance hatch, her black gloves gripping the rusted metal handle tightly as the strain pulls her puffy sleeves taut and exposes the tension in her shoulders, with sparks flying from the mechanism below.

### e038_b02_fullbody — fullbody

2B slides down a slick vertical support beam to escape rising smoke, her legs extended and thigh-high stockings brushing against the rough metal surface as she controls her descent with one gloved hand, her dress hem fluttering in the updraft.

### e038_b02_dynamic — dynamic

Caught mid-leap over a widening crack in the floor, 2B twists her body to avoid a falling concrete chunk, her white hair and blindfold trailing behind the momentum of the jump as her boots barely clear the edge of the gap.

### e038_b02_cinematic — cinematic

2B stands on the prow of a sinking ship, backlit by the orange glow of flames engulfing the deck behind her as she looks out at the dark water rising around the hull, her silhouette sharp against the chaotic destruction.

### e038_b03_closeup — closeup

A sudden, sharp drop in temperature from a ruptured coolant line causes 2B's breath to mist visibly against her black blindfold, making her flinch and pull her collar up slightly as frost begins to form on the fabric of her puffy sleeves.

### e038_b03_medium — medium

2B leans back sharply to dodge a swinging chain anchor, her black gloves gripping a nearby pipe for stability as the momentum twists her torso and pulls the cutout of her dress taut across her midsection, revealing the tension in her posture.

### e038_b03_fullbody — fullbody

2B braces against a low wooden crate as heavy debris crashes down from above, shifting her weight to one leg and driving her heels into the dirt as her white hair is swept back by the updraft of the impact, highlighting the strain in her legs.

### e038_b03_dynamic — dynamic

Captured mid-somersault over a churning river of lava, 2B twists her hips to clear a rising steam jet, her dress hem and thigh-high stockings whipping violently in the heat distortion as she aims for a narrow stone ledge.

### e038_b03_cinematic — cinematic

2B stands alone at the edge of a collapsing bridge, silhouetted against the massive shadow of an approaching colossus that blocks out the sun, as her hair and blindfold are pulled taut by the intense wind generated by its movement.

### e038_b04_closeup — closeup

A cluster of iridescent beetles lands on the black blindfold, causing 2B to hold her breath and keep perfectly still as she fights the instinct to swat them away, her eyes widening slightly behind the fabric while her jaw tightens with restrained irritation.

### e038_b04_medium — medium

2B grips a descending metal ladder rung with one gloved hand as a sudden jolt from the platform above knocks her off balance, forcing her to twist her torso against the railing and pulling the puffy sleeves of her dress taut across her shoulders.

### e038_b04_fullbody — fullbody

2B crouches low on a slippery stone ledge, balancing on the tips of her thigh-high boots as a heavy wooden crate slides past her feet, her weight shifted back to avoid being knocked into the abyss below.

### e038_b04_dynamic — dynamic

2B is captured mid-air in a horizontal slide across a narrow beam, extending one leg to kick a loose stone away from her path as debris rains down around her, her white hair trailing behind the momentum of the lateral movement.

### e038_b04_cinematic — cinematic

2B stands on a fractured glass floor suspended high above a forest canopy, backlit by the bright sun as a massive bird of prey lands on the edge of the pane beside her, causing the entire structure to shudder and crack further.
