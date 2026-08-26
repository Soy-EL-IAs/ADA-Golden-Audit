# Ada Viral Guide Evolution — Cycle 011

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 6.83/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 8.50 |
| Visual Appeal | 7.50 |
| Diversity | 6.00 |
| Repetition Control | 5.50 |
| Micro Story | 7.00 |
| Animation Potential | 6.50 |

## Verdict

The set demonstrates strong character identity and visual appeal, particularly in the dynamic and closeup categories. However, it fails on diversity and repetition control due to a heavy reliance on passive 'standing/bracing' poses in cinematic and medium shots, and repetitive generic industrial hazards. The cinematic category is the weakest link, with 4 out of 5 premises being nearly identical in composition (low-angle, standing still).

## Strengths

- Strong adherence to character identity markers (blindfold, dress, sleeves) across all premises.
- Dynamic shots (b01_dyn, b04_dyn) effectively combine motion with specific hazards and visual hooks.
- Closeups generally succeed in showing physical strain or immediate threat rather than just 'pretty face'.
- Most premises have a visible cause for the character's state.

## Failures

- Cinematic shots are heavily repetitive: three out of five involve 2B standing passively on a platform/ledge while machinery moves in the background.
- Medium and Fullbody shots suffer from 'bracing/gripping/balancing' repetition, lacking distinct narrative actions.
- Several premises rely on generic industrial hazards (steam, sparks, gears) without unique lore-specific context or interaction.
- Passive poses (arms crossed, standing firm) are used in high-stakes cinematic moments where active reaction is expected.

## Desired patterns

- Active engagement with the environment (pushing, pulling, dodging, climbing) rather than just reacting to it.
- Unique interaction with specific props or machinery that implies a larger story context.
- Variety in emotional registers beyond 'tension/composure' (e.g., frustration, determination, quick wit).

## Undesired patterns

- 'Standing firm' as the primary action in cinematic shots.
- Generic industrial hazards (steam/sparks) used without specific source or consequence.
- Repetitive 'gripping/balancing' poses that look like static character sheets with a background added.

## Repetition clusters

- **Passive Standing on Platform/Ledge**: `e011_b01_cinematic`, `e011_b02_cinematic`, `e011_b03_cinematic`, `e011_b04_cinematic`
- **Bracing/Gripping/Balancing (Static Stability)**: `e011_b01_fullbody`, `e011_b02_medium`, `e011_b03_medium`, `e011_b04_medium`
- **Stepping/Navigating Hazard (Glass/Rebar)**: `e011_b03_fullbody`, `e011_b04_fullbody`

## Recommendations for the next cycle

- For Cinematic shots, require the character to be *in motion* or interacting with the scale (e.g., climbing a gear, pushing against a door) rather than standing still.
- Differentiate Medium/Fullbody shots by focusing on specific object interactions (opening a hatch, pulling a lever) rather than just 'holding on' to static structures.
- Introduce more variety in hazards: use biological, technological, or environmental elements beyond standard industrial steam/sparks/gears.
- Ensure every premise has an active verb that implies forward momentum or change of state, not just maintenance of position.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e011_b01_closeup` | closeup | 9.0 | 8.0 | 9.0 | 7.0 | Strong tension. The 'mechanical arm' is a situational prop (valid). Sweat adds physical strain. Good cause-and-effect. |
| `e011_b01_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Specific source for wind (ventilation shaft) satisfies the guide. However, 'tracking the source' is a passive reaction compared to active dodging. |
| `e011_b01_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 5.0 | Balancing on a beam is a classic trope. The 'groaning metal' provides cause, but the action is static balance rather than dynamic movement. |
| `e011_b01_dynamic` | dynamic | 9.0 | 9.0 | 8.0 | 9.0 | Excellent. Specific hazard (sparking cable), clear motion (dodge), and visual hook (dress flare). Strong directional energy. |
| `e011_b01_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | 'Standing' on a platform is passive. The crane swinging is the action; she is just observing it. Violates 'Passive Cinematic Poses' anti-pattern slightly. |
| `e011_b02_closeup` | closeup | 9.0 | 8.0 | 8.0 | 7.0 | Steam jet is a strong visual and sensory hook. Holding breath implies immediate threat. Good tension. |
| `e011_b02_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Gripping a railing is a common pose. The 'power surge' cause is abstract; the physical action of keeping fingers from being crushed is good but visually similar to bracing. |
| `e011_b02_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 5.0 | Leaning against a crate is static. The floor sliding is the cause, but her reaction (shifting weight) is subtle and hard to animate distinctly from standing. |
| `e011_b02_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 8.0 | Controlled descent is good. 'Falling debris field' is a bit generic as a cause, but the landing precision adds story. |
| `e011_b02_cinematic` | cinematic | 7.0 | 6.0 | 4.0 | 3.0 | Major failure. 'Arms crossed in defiance' is explicitly listed as a passive pose anti-pattern. She is standing still while the skylight cracks. |
| `e011_b03_closeup` | closeup | 9.0 | 7.0 | 6.0 | 4.0 | 'Pupils dilating' is a micro-reaction. Tracking light is passive. Lacks the physical strain or active defense seen in other closeups. |
| `e011_b03_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Bracing against a console is similar to b02_medium. The 'explosion' cause is strong, but the action (leaning/steadying) is repetitive. |
| `e011_b03_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 5.0 | Stepping over glass is a navigation hazard. It's functional but lacks the high-stakes tension of the dynamic shots. |
| `e011_b03_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 8.0 | Mid-spin dodge is good. 'Grinding industrial wheel' is a specific hazard. Slightly repetitive with b01_dynamic in terms of 'dodging sparks/electrical hazards'. |
| `e011_b03_cinematic` | cinematic | 7.0 | 6.0 | 4.0 | 3.0 | Another passive 'standing firm' shot. The gears rotating behind her are the action; she is just a silhouette. Weak narrative agency. |
| `e011_b04_closeup` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Steam fogging the blindfold is a great visual detail. However, it repeats the 'steam' hazard from b02_closeup. |
| `e011_b04_medium` | medium | 8.0 | 7.0 | 5.0 | 5.0 | 'Gripping the edge' and 'counterbalancing' is very similar to b02_medium (gripping railing) and b01_fullbody (balancing). High repetition of 'holding on/bracing' concepts. |
| `e011_b04_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 5.0 | Stepping over rebar is similar to b03_fullbody (stepping over glass). Both are 'careful navigation' hazards. Low distinctiveness. |
| `e011_b04_dynamic` | dynamic | 9.0 | 9.0 | 8.0 | 9.0 | Lunging past a hydraulic press is excellent. High stakes, clear motion, strong visual hook (dress stretching). Best of the set. |
| `e011_b04_cinematic` | cinematic | 7.0 | 6.0 | 4.0 | 3.0 | Third passive 'standing on a platform/ledge' shot. The mechanism descending is the threat, but she remains static. Fails to show her *reacting* actively. |

## Premises

### e011_b01_closeup — closeup

2B's face framed tightly, a single bead of sweat tracing her jaw as she grits her teeth to maintain composure while a heavy mechanical arm hovers inches from her blindfold.

### e011_b01_medium — medium

Waist-up shot of 2B bracing against a sudden gust of wind escaping a fractured ventilation shaft, her puffy sleeves billowing violently as she tilts her head to track the source.

### e011_b01_fullbody — fullbody

Full silhouette of 2B balancing precariously on a narrow, rusted maintenance beam, shifting her weight to keep from slipping as the metal groans under her boots.

### e011_b01_dynamic — dynamic

2B mid-dodge in a low crouch, her black dress flaring from the rapid movement as she evades a sparking cable snapping sideways from an overloaded power junction.

### e011_b01_cinematic — cinematic

Low-angle cinematic shot looking up at 2B standing on a cracked platform, dwarfed by the looming shadow of a massive industrial crane swinging toward her.

### e011_b02_closeup — closeup

Extreme close-up on 2B's jawline and neck, skin tightening as she holds her breath while a high-pressure steam jet from a ruptured pipe hisses directly at the edge of her blindfold.

### e011_b02_medium — medium

Waist-up shot of 2B gripping a vibrating metal railing, her puffy sleeves distorting as she strains to keep the door from slamming shut on her fingers amidst a sudden power surge.

### e011_b02_fullbody — fullbody

Full body view of 2B leaning back against a tilting cargo crate, shifting her weight to the balls of her feet as the floor beneath her slides toward a drainage grate.

### e011_b02_dynamic — dynamic

2B mid-air in a controlled descent, knees bent and dress hem flaring upward from gravity as she lands precisely on a narrow ledge to avoid the impact of a falling debris field.

### e011_b02_cinematic — cinematic

Low-angle cinematic shot looking up at 2B from below, her silhouette framed against a massive, cracking skylight as she stands firm on the floor, arms crossed in defiance of the impending collapse above.

### e011_b03_closeup — closeup

Tight crop on 2B's eyes and blindfold, her pupils dilating as she tracks a sudden flash of light from a ruptured coolant line directly above her head.

### e011_b03_medium — medium

Waist-up shot of 2B leaning forward to steady herself against a violently shaking metal console, her puffy sleeves compressing as she braces for impact from a nearby explosion.

### e011_b03_fullbody — fullbody

Full body view of 2B stepping carefully across a floor covered in shattered glass, her thigh-high boots pressing down to maintain grip while debris slides beneath her feet.

### e011_b03_dynamic — dynamic

2B twisting her torso sharply to the side in a mid-spin, her dress hem flaring outward as she dodges a horizontal sweep of sparks from a grinding industrial wheel.

### e011_b03_cinematic — cinematic

Wide low-angle shot showing 2B standing firm on a crumbling ledge, her silhouette small against the massive, rotating gears of a collapsing machinery structure behind her.

### e011_b04_closeup — closeup

Tight crop on 2B's face as a sudden burst of superheated steam from a ruptured valve engulfs the frame, her blindfold fogging up rapidly while she holds her breath to keep her composure intact.

### e011_b04_medium — medium

Waist-up shot of 2B gripping the edge of a swaying industrial gantry, her torso twisting to counterbalance the violent oscillation as she steadies herself against the shifting metal.

### e011_b04_fullbody — fullbody

Full body view of 2B stepping over a jagged, sparking rebar protruding from a broken floor panel, her thigh-high boots carefully navigating the hazard while maintaining forward momentum.

### e011_b04_dynamic — dynamic

2B lunging sideways in a blur of motion, her black dress stretching taut across her hips as she sweeps past a swinging hydraulic press to avoid being crushed.

### e011_b04_cinematic — cinematic

Dramatic low-angle shot looking up at 2B standing on a tilting platform, her silhouette framed against the massive, grinding gears of an overhead mechanism that is slowly descending toward her.
