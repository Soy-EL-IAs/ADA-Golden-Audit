# Ada Viral Guide Evolution — Cycle 031

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 6.83/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.00 |
| Visual Appeal | 8.00 |
| Diversity | 6.00 |
| Repetition Control | 5.00 |
| Micro Story | 7.00 |
| Animation Potential | 6.00 |

## Verdict

The set is strong on identity and visual appeal but suffers from moderate repetition in mechanical actions (bracing, sliding, balancing). The causal logic is generally sound. To improve, the next cycle should focus on diversifying the *type* of physical interaction rather than just changing the environment or object.

## Strengths

- Consistent character identity with specific references to blindfold, hair, and outfit details.
- Strong visual appeal in dynamic and cinematic categories, particularly with light effects and motion blur.
- Most premises have a clear visible cause (steam, chain, laser, debris) driving the action.

## Failures

- Significant repetition of 'bracing/leaning against wall' mechanics across multiple medium shots (b01, b02, b04).
- Repetition of 'tilting/sliding platform' fullbody concepts (b02 and b04 are nearly identical in setup).
- Two dynamic premises involve sliding on a floor (b01 metal, b03 oil), reducing verb diversity.
- Cinematic shots rely heavily on silhouette against large machinery/light sources, creating a repetitive visual family.

## Desired patterns

- Clear causal triggers visible in the frame.
- Integration of body appeal through fabric tension and weight shifts rather than static poses.
- Distinct motion verbs for dynamic categories (slide, spin, dive, roll are all present, which is good).

## Undesired patterns

- Generic industrial environments without specific narrative context beyond 'danger'.
- Passive bracing that lacks a secondary active movement or consequence.
- Atmospheric elements (mist, dust) used as primary hooks rather than consequences of action.

## Repetition clusters

- **Bracing/Leaning against structure to counteract force**: `e031_b01_medium`, `e031_b02_medium`, `e031_b04_medium`
- **Balancing on unstable/tilting platform**: `e031_b02_fullbody`, `e031_b04_fullbody`
- **Sliding low across floor to evade hazard**: `e031_b01_dynamic`, `e031_b03_dynamic`
- **Silhouette against large light source/machinery with push-off action**: `e031_b01_cinematic`, `e031_b02_cinematic`, `e031_b04_cinematic`

## Recommendations for the next cycle

- Vary the medium shot mechanics: instead of bracing against walls, use active dodging or interacting with objects (catching a falling tool, stepping over debris).
- Differentiate fullbody balance shots: one could be on ice/water, another on a narrow beam, another climbing a vertical surface.
- Introduce more varied dynamic verbs: consider jumping, crawling, or swinging rather than just sliding and spinning.
- For cinematic shots, vary the character's relationship to the scale: instead of always pushing off/launching, try interacting with the machinery (gripping a moving part, hiding behind a gear) or being dwarfed by it in a moment of stillness that implies tension.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e031_b01_closeup` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Strong identity with specific gear interaction. The 'sparking electrical contact' provides a clear cause for the heat/lean. Good closeup focus. |
| `e031_b01_medium` | medium | 9.0 | 8.0 | 7.0 | 7.0 | Clear cause (steam jet) and reaction (twist/brace). Sleeves flaring adds visual interest. Slightly generic industrial setting but effective. |
| `e031_b01_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 6.0 | Good balance challenge. 'Wind updraft' is a bit vague but acceptable as a consequence of the chasm depth. Hem lift adds appeal. |
| `e031_b01_dynamic` | dynamic | 8.0 | 9.0 | 6.0 | 8.0 | High energy. 'Friction sparks' from stockings is a strong visual hook. Clear cause (laser grid). Distinct verb (slide). |
| `e031_b01_cinematic` | cinematic | 8.0 | 9.0 | 6.0 | 7.0 | Strong scale contrast. Active push-off prevents static statue feel. Silhouette works well with the gear background. |
| `e031_b02_closeup` | closeup | 9.0 | 7.0 | 6.0 | 5.0 | Repetition of steam cause from b01_medium. 'Gripping vibrating grate' is a bit passive compared to the active heat interaction in b01_closeup. |
| `e031_b02_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Chain swing is a good near-miss cause. Similar 'twist/brace' mechanic to b01_medium but distinct object (chain vs steam). |
| `e031_b02_fullbody` | fullbody | 9.0 | 7.0 | 6.0 | 5.0 | Tilting platform is a common trope. 'Dress hem flares from air displacement' feels weakly causal compared to the wind in b01_fullbody. |
| `e031_b02_dynamic` | dynamic | 8.0 | 8.0 | 6.0 | 7.0 | Spin to evade mechanical arm. Good motion blur description. Distinct from slide (b01) and dive (b03). |
| `e031_b02_cinematic` | cinematic | 8.0 | 9.0 | 6.0 | 7.0 | Fractured window/light shafts. Push-off action is good. Similar scale contrast to b01_cinematic but different light source. |
| `e031_b03_closeup` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Chain anchor dropping is a strong specific cause. Reflexive shield pose is dynamic for a closeup. |
| `e031_b03_medium` | medium | 9.0 | 7.0 | 6.0 | 5.0 | Piston slam is a good cause. However, 'static legs' contradicts the active bracing described earlier in the sentence. Slightly confusing phrasing. |
| `e031_b03_fullbody` | fullbody | 8.0 | 9.0 | 6.0 | 7.0 | High arcing leap. 'Swirling mist' is atmospheric but the leap itself has clear momentum. Hem flare is well-integrated. |
| `e031_b03_dynamic` | dynamic | 8.0 | 9.0 | 7.0 | 8.0 | Slide on oil floor. Very similar to b01_dynamic (slide on metal). 'Black droplets' spray is a nice detail but the core action repeats. |
| `e031_b03_cinematic` | cinematic | 8.0 | 8.0 | 6.0 | 5.0 | Gripping ladder rung. 'Vibrating' is a weak cause for a cinematic scale shot; feels more like a medium action. Less impactful than the push-offs in previous cinematics. |
| `e031_b04_closeup` | closeup | 9.0 | 7.0 | 5.0 | 4.0 | Collapsing shelf/dust. 'Brushing debris' is a low-stakes action. Feels more like a cleanup moment than a high-tension micro-story. |
| `e031_b04_medium` | medium | 9.0 | 7.0 | 6.0 | 5.0 | Lateral shaking floor. Bracing against bulkhead. Similar 'brace/twist' mechanic to b01_medium and b02_medium. |
| `e031_b04_fullbody` | fullbody | 9.0 | 8.0 | 6.0 | 6.0 | Tilting/rotating platform. Very similar to b02_fullbody (tilting/sliding platform). Repetition of the 'balance on unstable surface' hook. |
| `e031_b04_dynamic` | dynamic | 8.0 | 8.0 | 6.0 | 7.0 | Backward roll. Distinct verb from slide/spin/dive. Falling beam is a clear cause. |
| `e031_b04_cinematic` | cinematic | 8.0 | 9.0 | 6.0 | 7.0 | Fractured skylight. Pulling up to stand/reach for cable. Similar light shaft aesthetic to b02_cinematic. |

## Premises

### e031_b01_closeup — closeup

2B's gloved hand firmly grips a frayed wire hanging from an exposed conduit, her blindfold slightly askew as she leans into the heat of a sparking electrical contact, short white hair catching the orange glow while she maintains a focused, stoic expression.

### e031_b01_medium — medium

2B twists her torso sharply to evade a sudden jet of steam erupting from a broken pipe, her puffy feather-trimmed sleeves flaring outward with the force, one arm braced against a rusted wall for balance while her hair whips across her face.

### e031_b01_fullbody — fullbody

2B balances on a narrow, crumbling concrete beam over a chasm, knees bent deep to lower her center of gravity as debris crumbles from under her thigh-high boots, one hand extended forward to catch the next stable ledge while her dress hem lifts with the wind updraft.

### e031_b01_dynamic — dynamic

2B slides low across a polished metal floor, her thigh-high stockings creating friction sparks against the surface as she dodges a sweeping laser grid, body parallel to the ground with one leg extended and arms tucked tight for speed.

### e031_b01_cinematic — cinematic

2B stands silhouetted against a massive, rotating industrial gear in the background, her small figure contrasting with the colossal machinery as she actively pushes off a protruding bolt to launch herself upward, blindfold catching a sliver of ambient light.

### e031_b02_closeup — closeup

Close-up on 2B's face and gloved hand as she firmly grips a vibrating metal grate to steady herself, her black blindfold tight against her forehead while short white hair is sharply displaced by the sudden upward surge of pressurized steam escaping from below.

### e031_b02_medium — medium

2B twists her upper body sharply to the left, bracing against a rusted wall as a heavy industrial chain swings violently through the air just inches from her hair; her puffy feather-trimmed sleeves stretch with the motion and her expression remains stoically controlled despite the near miss.

### e031_b02_fullbody — fullbody

Full-body shot of 2B crouching low on a tilted, sliding metal platform, her thigh-high boots digging into the surface for friction as she lowers her center of gravity to counterbalance the incline; one arm extends forward to grasp a fixed railing while her dress hem flares slightly from the air displacement.

### e031_b02_dynamic — dynamic

2B performs a rapid, low-profile spin to evade a sweeping mechanical arm, her body angled sharply with motion blur trailing from her black gloves and the hem of her dress; debris kicks up around her feet as she initiates the turn, eyes focused on the next gap in the machinery.

### e031_b02_cinematic — cinematic

2B is silhouetted against a massive, fractured window letting in harsh shafts of light; she actively pushes off a crumbling ledge with one leg to propel herself upward, her short white hair catching the backlight and creating a halo effect as she launches into the open space.

### e031_b03_closeup — closeup

Close-up on 2B's face and shoulder as she tilts her head sharply to the left, short white hair whipping across her blindfold from the sudden recoil of a heavy chain anchor dropping beside her; her gloved hand is raised near her temple in a reflexive shield against flying dust, eyes narrowed with focused alarm behind the fabric.

### e031_b03_medium — medium

2B leans backward against a crumbling stone archway to brace her weight as a massive piston slams into the ground just inches from her boots, her puffy feather-trimmed sleeves stretching taut with the strain of holding her balance; her torso twists slightly to keep her center of gravity stable while debris rains down around her static legs.

### e031_b03_fullbody — fullbody

2B is captured mid-air in a high, arcing leap over a chasm of swirling mist, her body fully extended with one leg trailing back and the other driving forward to propel herself; her black dress hem flares dramatically behind her due to air resistance, while her arms are tucked tight against her sides for aerodynamic speed.

### e031_b03_dynamic — dynamic

2B dives low and slides horizontally across a slick oil-covered floor to dodge a vertical laser beam, her thigh-high stockings creating a spray of black droplets as they screech against the surface; motion blur trails behind her body while she twists her upper torso at the last second to bring her blindfolded face away from the burning light.

### e031_b03_cinematic — cinematic

2B is silhouetted against a colossal, rotating turbine wheel in a dark industrial cavern, actively gripping a vibrating maintenance ladder rung with both hands to steady herself as the massive machinery vibrates through the metal; her short white hair glows faintly from the ambient light of the spinning blades behind her.

### e031_b04_closeup — closeup

Close-up on 2B's face and upper chest as she sharply inhales through her nose, her black blindfold tight against her forehead while fine dust particles from a nearby collapsing shelf settle onto her short white hair; her gloved hand is raised to brush the debris away, eyes narrowed with focused composure despite the sudden intrusion.

### e031_b04_medium — medium

2B leans heavily against a vibrating metal bulkhead to counteract the intense lateral shaking of the floor, her puffy feather-trimmed sleeves compressing as she braces her arms; her torso twists slightly to maintain stability while her hairband shifts under the stress, keeping her gaze locked on the swaying structure ahead.

### e031_b04_fullbody — fullbody

2B stands on a tilting, rotating platform, her thigh-high boots planted wide against the sliding surface to prevent slipping; she extends one arm high to grip an overhead support beam while her legs bend deep, her dress hem flaring outward from the centrifugal force as she actively stabilizes her center of gravity.

### e031_b04_dynamic — dynamic

2B performs a rapid backward roll to evade a falling metal beam, her body rotating in mid-air with motion blur trailing from her black gloves; debris scatters around her feet as she lands low and crouched, eyes fixed on the next hazard while dust clouds obscure the immediate foreground.

### e031_b04_cinematic — cinematic

2B is silhouetted against a massive, fractured skylight letting in harsh shafts of light; she actively pulls herself up from a low crouch to stand tall, her short white hair catching the backlight and creating a halo effect as she reaches for a dangling cable to swing across the gap.
