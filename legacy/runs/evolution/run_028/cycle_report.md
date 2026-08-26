# Ada Viral Guide Evolution — Cycle 028

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.05/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.50 |
| Visual Appeal | 7.20 |
| Diversity | 6.50 |
| Repetition Control | 5.80 |
| Micro Story | 6.80 |
| Animation Potential | 6.50 |

## Verdict

Solid identity and close-up work, but suffers from static poses and repetitive full-body/cinematic concepts. Needs more active interaction and varied movement mechanics.

## Strengths

- Consistent and accurate character identity across all premises.
- Strong use of specific physical causes (sparks, steam, glass) in close-ups.
- Good integration of clothing details (gloves, sleeves, blindfold) into actions.

## Failures

- Heavy reliance on static poses ('bracing', 'standing', 'suspended') especially in medium and cinematic categories.
- Repetitive full-body concepts: balancing/walking on narrow edges appears multiple times (b01, b04).
- Cinematic shots often feature passive reactions to environmental forces rather than active interaction.
- Generic dynamic actions (vaulting, dodging) lack specific narrative context or unique enemy/threat design.

## Desired patterns

- Active physical interactions with objects or environment (pushing, pulling, catching, breaking).
- Specific mechanical failures or hazards that require a unique solution.
- Dynamic poses that imply immediate consequence or continuation of motion.

## Undesired patterns

- Static bracing/standing poses as the primary action.
- Passive shielding from wind/dust/debris without secondary physical interaction.
- Generic locomotion (walking, balancing) without narrative stakes.
- Repetitive 'narrow path' or 'ledge' full-body concepts.

## Repetition clusters

- **Static Bracing/Standing**: `e028_b01_medium`, `e028_b02_fullbody`, `e028_b03_cinematic`, `e028_b04_medium`, `e028_b04_cinematic`
- **Balancing/Walking on Narrow Edge**: `e028_b01_fullbody`, `e028_b04_fullbody`
- **Passive Shielding from Environmental Force**: `e028_b01_cinematic`, `e028_b03_cinematic`, `e028_b04_cinematic`

## Recommendations for the next cycle

- Replace static 'bracing' poses with active weight-shifting or object manipulation.
- Diversify full-body concepts: avoid multiple 'narrow path' scenarios; use varied terrain (climbing, descending, swimming, crawling).
- Make cinematic shots more interactive: character should be actively moving through the environment, not just standing in it.
- Add specific narrative stakes to dynamic actions: who is she fighting? What is she escaping?

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e028_b01_closeup` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Strong causal trigger (spark) with clear physical reaction. Good identity preservation. |
| `e028_b01_medium` | medium | 9.0 | 7.0 | 7.0 | 6.0 | Decent action, but 'bracing against pillar' is a static pose. The wind detail feels tacked on rather than causal to the main event. |
| `e028_b01_fullbody` | fullbody | 9.0 | 6.0 | 5.0 | 7.0 | Classic 'walking/balancing' filler. Lacks a specific narrative consequence beyond staying on the roof. Generic movement. |
| `e028_b01_dynamic` | dynamic | 9.0 | 8.0 | 6.0 | 9.0 | High kinetic energy. However, 'vaulting over barrier' is a generic combat/movement trope without specific enemy context. |
| `e028_b01_cinematic` | cinematic | 9.0 | 7.0 | 6.0 | 5.0 | Wind pushing metal sheet is a good specific cause. However, 'shielding face' is a passive reaction to an environmental force. |
| `e028_b02_closeup` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Steam burst is a strong visual and physical trigger. Good detail on hair/skin reaction. |
| `e028_b02_medium` | medium | 9.0 | 7.0 | 7.0 | 6.0 | Holding a door open is a static pose. The 'swarm of moths' is visually interesting but the character's action (holding breath) is internal/passive. |
| `e028_b02_fullbody` | fullbody | 9.0 | 7.0 | 6.0 | 5.0 | 'Suspended mid-air' is a static pose. Lacks the dynamic tension of active climbing or falling. |
| `e028_b02_dynamic` | dynamic | 9.0 | 8.0 | 6.0 | 9.0 | Dodge is a good action. 'Pendulum blade' is a specific threat, but the 'perfect balance on one leg' feels like a pose rather than a moment of evasion. |
| `e028_b02_cinematic` | cinematic | 9.0 | 7.0 | 6.0 | 5.0 | 'Standing small in center' is a contemplative statue anti-pattern. The glass falling is atmospheric rather than interactive. |
| `e028_b03_closeup` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Glass fragment is a sharp, specific cause. The blood detail adds stakes and personality (restraint). |
| `e028_b03_medium` | medium | 9.0 | 7.0 | 8.0 | 8.0 | Sliding under rotating rebar is a specific mechanical interaction. Good use of gloves and sleeves. |
| `e028_b03_fullbody` | fullbody | 9.0 | 7.0 | 6.0 | 5.0 | 'Suspended in light' is a static pose. The electrical charge on the puddle is a good cause, but the character is just hovering/preparing. |
| `e028_b03_dynamic` | dynamic | 9.0 | 7.0 | 6.0 | 8.0 | Leaping over sludge is generic. The 'toxic green sludge' is a visual cliché in sci-fi/fantasy. |
| `e028_b03_cinematic` | cinematic | 9.0 | 7.0 | 5.0 | 4.0 | 'Standing on cracked bridge' is a static pose. Shielding from dust is passive. The scale contrast is good but lacks active interaction. |
| `e028_b04_closeup` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Coolant jet is a strong specific cause. Good detail on fogging blindfold and hair. |
| `e028_b04_medium` | medium | 9.0 | 7.0 | 6.0 | 5.0 | 'Bracing against railing' is a static pose. The cargo crate sliding past is a good cause, but the reaction is just gripping. |
| `e028_b04_fullbody` | fullbody | 9.0 | 6.0 | 5.0 | 7.0 | Another 'balancing on narrow path' premise. Very similar to e028_b01_fullbody. Repetitive concept. |
| `e028_b04_dynamic` | dynamic | 9.0 | 7.0 | 6.0 | 8.0 | Sidestep is a good action. 'Snapping cable' is specific. However, the focus on revealing stockings feels like visual appeal overriding story. |
| `e028_b04_cinematic` | cinematic | 9.0 | 7.0 | 5.0 | 4.0 | 'Standing in foreground' is a static pose. Shielding from suction is passive. Similar to e028_b01_cinematic. |

## Premises

### e028_b01_closeup — closeup

Close-up on 2B's face and upper chest as a sudden electrical spark from a damaged nearby console jumps onto her black glove, causing her to flinch and tighten her jaw in composed restraint while the static charge makes the loose strands of her short white hair stand up against her blindfold.

### e028_b01_medium — medium

Medium shot of 2B waist-up, bracing herself against a crumbling stone pillar as a heavy chain-link fence collapses behind her; she tilts her head slightly to avoid the falling debris, her puffy feather-trimmed sleeves catching the wind and revealing the tension in her black dress fabric.

### e028_b01_fullbody — fullbody

Full-body view of 2B mid-stride on a slippery, moss-covered rooftop edge; she is leaning forward to maintain balance as her thigh-high boots grip the surface, her dress hem flapping violently in the updraft while she stares intently at the narrow path ahead.

### e028_b01_dynamic — dynamic

Dynamic action shot of 2B vaulting over a low concrete barrier, her body stretched horizontally with one hand reaching out and the other holding her sword; motion blur trails behind her white hair and black gloves as dust kicks up from her boots landing on the other side.

### e028_b01_cinematic — cinematic

Cinematic low-angle wide shot with 2B standing in the foreground, silhouetted against a massive, broken clock tower in the background; a sudden gust of wind pushes a large sheet of torn metal across her path, forcing her to turn and shield her face with one gloved hand while her blindfold remains steady.

### e028_b02_closeup — closeup

Extreme close-up on 2B's face as a sudden burst of steam from a ruptured valve hits her directly, forcing her to clench her jaw and keep her blindfold steady despite the heat; condensation beads form instantly on her skin and the fine white hairs of her bangs curl slightly away from the impact zone.

### e028_b02_medium — medium

Medium shot of 2B waist-up, leaning back against a heavy steel door to keep it open as a swarm of mechanical moths rushes through the gap; she holds her breath and keeps her eyes forward behind the blindfold while the chaotic fluttering obscures her puffy sleeves in a blur of wings.

### e028_b02_fullbody — fullbody

Full-body view of 2B suspended mid-air, her boots hooked over the edge of a crumbling concrete ledge as she lowers herself down; her body is taut with controlled tension, her dress hem swinging freely in the void below while one hand grips a jagged piece of rebar for support.

### e028_b02_dynamic — dynamic

Dynamic shot of 2B spinning rapidly to dodge a swinging pendulum blade; her body is twisted in motion, with the black fabric of her dress and the trim of her sleeves creating a circular blur around her core as she maintains perfect balance on one leg.

### e028_b02_cinematic — cinematic

Cinematic high-angle shot looking down from a shattered atrium ceiling, with 2B standing small in the center of the frame; massive shards of glass are falling around her like rain, but she has positioned herself perfectly to let them pass by leaning slightly, her silhouette sharp against the bright light flooding from above.

### e028_b03_closeup — closeup

Close-up on 2B's face and neck as a fragment of shattered glass from a nearby window slices through the air toward her, causing her to tilt her head sharply to avoid it; a single drop of blood beads on her cheek while she maintains unblinking composure behind the blindfold, the black hairband tightening slightly against the sudden movement.

### e028_b03_medium — medium

Medium shot of 2B waist-up, crouching low to slide under a horizontal bar of twisted rebar that is slowly rotating; her black gloves grip the wet concrete floor for traction while the puffy feather-trimmed sleeves brush against the metal, creating sparks as she times her movement with the mechanical rhythm.

### e028_b03_fullbody — fullbody

Full-body view of 2B suspended in a vertical shaft of light, her boots hovering just inches above a puddle to avoid the electrical charge crackling on the surface; her dress hem is lifted by the rising heat distortion, revealing the length of her thigh-high stockings as she prepares to step forward with precise balance.

### e028_b03_dynamic — dynamic

Dynamic shot of 2B mid-leap over a spreading patch of toxic green sludge, her body twisted to keep her sword clear of the liquid; motion blur emphasizes the speed as her white hair whips back, and the black fabric of her dress flares dramatically behind her, contrasting with the organic hazard below.

### e028_b03_cinematic — cinematic

Cinematic wide shot from a low angle, capturing 2B standing on a cracked bridge as a massive concrete slab collapses in the background; she remains stationary with one hand raised to shield her blindfold from the dust cloud engulfing her, the sheer scale of the destruction dwarfing her figure while highlighting her stillness against the chaos.

### e028_b04_closeup — closeup

Close-up on 2B's face and neck as a high-pressure jet of icy coolant sprays from a ruptured pipe directly into her blindfold, causing her to wince and tighten her jaw in composed restraint; the mist instantly fogs the black fabric while droplets cling to the fine white hairs of her bangs, contrasting with the sharp tension in her expression.

### e028_b04_medium — medium

Medium shot of 2B waist-up, bracing herself against a vibrating metal railing as a heavy cargo crate slides past on the track below; her black gloves grip the bar tightly to absorb the shockwave, while the puffy feather-trimmed sleeves billow slightly from the displacement of air created by the moving weight.

### e028_b04_fullbody — fullbody

Full-body view of 2B balancing on a narrow, rusted iron catwalk suspended over a chasm; her thigh-high boots grip the wet metal surface as she leans into the wind to keep her center of gravity, her dress hem and stockings whipping violently in the updraft while she stares intently at the next anchor point ahead.

### e028_b04_dynamic — dynamic

Dynamic action shot of 2B executing a rapid sidestep to avoid a snapping cable that whips past her ear; motion blur trails behind her white hair and black gloves as she twists her torso, the black fabric of her dress flaring out to reveal the length of her thigh-high stockings in the instant of evasion.

### e028_b04_cinematic — cinematic

Cinematic low-angle wide shot with 2B standing in the foreground, silhouetted against a massive, rotating turbine fan in the background; she holds her ground as debris is sucked toward the blades behind her, one hand raised to shield her face from the intense suction force while her blindfold remains steady against the chaos.
