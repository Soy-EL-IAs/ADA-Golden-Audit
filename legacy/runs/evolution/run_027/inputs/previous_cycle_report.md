# Ada Viral Guide Evolution — Cycle 026

- Model: `qwen3.8-27b-uncensored` via local LM Studio
- Premises: 20
- Rendering: not executed
- Overall diagnostic mean: 7.00/10

## Set scores

| Dimension | Score |
|---|---:|
| Identity | 9.00 |
| Visual Appeal | 8.00 |
| Diversity | 6.00 |
| Repetition Control | 5.00 |
| Micro Story | 7.00 |
| Animation Potential | 7.00 |

## Verdict

The set is strong on identity and visual appeal but suffers from mechanical repetition in fullbody and cinematic categories. The closeup premises lack sufficient variety in reaction type. To improve, diversify physical mechanics beyond balancing/dodging and increase the kinetic energy of wide shots.

## Strengths

- Consistent adherence to the local identity profile (blindfold, hair, dress details) across all premises.
- Strong use of secondary motion (hair, sleeves, fabric) in dynamic and medium shots.
- Most closeup and dynamic premises have clear, visible causes for the character's reaction.

## Failures

- Significant repetition in the 'Fullbody' category: three out of four premises involve balancing/weight-shifting on unstable surfaces (beam, ledge, rebar, platform).
- The 'Cinematic' category suffers from low-energy actions ('standing firmly', 'slowly raising hand') that feel more like poses than active interactions.
- Two closeup premises (b02 and b04) are nearly identical in concept: debris near face + hair obscuring blindfold + unblinking focus.
- Invented canon fact in b02_closeup ('crystallized data') which is not present in the local profile.

## Desired patterns

- Clear causal chains where the character's action directly responds to a visible force or object.
- Use of distinct physical mechanics (roll, slide, hang, brace) rather than relying on generic 'balance' or 'dodge'.
- Integration of visual appeal (silhouette, clothing tension) with active motion.

## Undesired patterns

- Passive standing poses in cinematic shots where the environment is more interesting than the character's action.
- Repetition of 'balancing on narrow surface' as a fullbody mechanic.
- Weak micro-reactions like 'flinch slightly' or 'snap head left' that lack physical consequence.

## Repetition clusters

- **Balancing/Weight-Shift on Unstable Surface**: `e026_b01_fullbody`, `e026_b02_fullbody`, `e026_b03_fullbody`, `e026_b04_fullbody`
- **Debris Near Face + Hair Obscuring Blindfold**: `e026_b02_closeup`, `e026_b04_closeup`
- **Low-Energy Catch/Stand in Cinematic Shot**: `e026_b02_cinematic`, `e026_b04_cinematic`

## Recommendations for the next cycle

- Diversify Fullbody mechanics: Move away from 'balancing' to actions like climbing, jumping, or interacting with large objects (pushing a door, pulling a lever).
- Increase energy in Cinematic shots: Instead of standing still, have the character actively navigating the environment (running through debris, sliding under a falling beam) while maintaining wide framing.
- Differentiate Closeup reactions: Avoid 'hair obscuring face' as the primary visual hook for multiple premises. Focus on accessory interaction (adjusting blindfold, gripping weapon/handle) or specific facial micro-expressions triggered by distinct causes (heat, cold, impact).
- Strictly enforce canon facts: Remove invented elements like 'crystallized data' unless explicitly part of the disruption.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e026_b01_closeup` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Strong causal link (spark). Good identity preservation. Slight risk of 'static' if the spark isn't visually prominent enough in a still frame. |
| `e026_b01_medium` | medium | 9.0 | 8.0 | 7.0 | 7.0 | Leaning back is a passive reaction to an active threat. Good use of sleeve flare. 'Falling debris chunk' is generic but acceptable. |
| `e026_b01_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 6.0 | Classic 'crossing the gap' trope. The action of grabbing a bolt to secure footing is specific and good. However, it leans into generic traversal. |
| `e026_b01_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | High kinetic energy. Laser beam is a clear vector. Good use of hair/strap motion. |
| `e026_b01_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | 'Stands grounded but tense' is borderline contemplative. The piston slamming *behind* her makes the current moment a reaction to a past event rather than an active interaction with the present force. |
| `e026_b02_closeup` | closeup | 8.0 | 7.0 | 6.0 | 6.0 | 'Crystallized data' is an invented canon fact not in the profile. 'Snap head slightly left' is a weak physical reaction compared to dodging or bracing. |
| `e026_b02_medium` | medium | 9.0 | 8.0 | 7.0 | 8.0 | Mid-air leap is dynamic. Reaching for a pipe adds consequence. Good balance of appeal and story. |
| `e026_b02_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 6.0 | 'Testing stability' is a specific micro-story. Good use of weight distribution. Slightly static but implies imminent action. |
| `e026_b02_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Rolling is a distinct mechanic from dodging/twisting. Good use of sparks and fabric trail. |
| `e026_b02_cinematic` | cinematic | 8.0 | 7.0 | 5.0 | 4.0 | 'Slowly raises one hand to catch a falling fragment' is very low energy for a cinematic shot. The environment (server room) dominates the visual interest over the character's action. |
| `e026_b03_closeup` | closeup | 9.0 | 7.0 | 8.0 | 8.0 | Steam burst is a strong visible cause. 'Snap head back' is reactive but clear. Good micro-expression detail. |
| `e026_b03_medium` | medium | 9.0 | 8.0 | 7.0 | 7.0 | Hanging from a cable is a distinct mechanic. Swinging away from oil adds secondary motion and danger. |
| `e026_b03_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 6.0 | Balancing on rebar is similar to b01_fullbody (beam) and b04_fullbody (platform). Repetition of 'balance/weight shift' mechanic. |
| `e026_b03_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Chain falling is a good cause. Pivot/spin is distinct from roll (b02) and twist (b01). Good kinetic energy. |
| `e026_b03_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | 'Stands firmly' is passive. Deflecting a panel is active but the overall composition feels like a 'hero shot' rather than an ongoing interaction. |
| `e026_b04_closeup` | closeup | 8.0 | 7.0 | 5.0 | 5.0 | High repetition with b02_closeup. 'Flinch slightly' is a weak reaction. 'Unblinking focus' is generic. |
| `e026_b04_medium` | medium | 9.0 | 8.0 | 7.0 | 7.0 | Bracing against a wall is distinct from leaning (b01). Hydraulic press is a strong cause. Good use of sleeve flare. |
| `e026_b04_fullbody` | fullbody | 9.0 | 8.0 | 7.0 | 6.0 | Tilted platform balance is very similar to b01 and b03 fullbody premises. Repetition of 'weight shift/balance' mechanic. |
| `e026_b04_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 8.0 | Steam burst is repeated from b03_closeup. Ducking/sliding is a distinct mechanic from twist/roll/pivot. |
| `e026_b04_cinematic` | cinematic | 8.0 | 7.0 | 5.0 | 4.0 | Near-identical to b02_cinematic. 'Slowly raises hand to catch falling gear' is low energy. Environment dominates. |

## Premises

### e026_b01_closeup — closeup

2B's gloved fingers tightly grip the edge of her black blindfold as a sudden, sharp electrical spark from a nearby conduit singes the air inches from her face; her short white hair lifts slightly in the static discharge while she holds her breath, maintaining composure despite the visible flicker of light reflecting off her dark lenses.

### e026_b01_medium — medium

2B leans back sharply against a rusted metal railing to avoid a falling debris chunk, her puffy feather-trimmed sleeves flaring outward with the force of the impact; her black dress cutout exposes the tension in her midsection as she braces her weight on one thigh-high boot, eyes fixed on the object that just missed her shoulder.

### e026_b01_fullbody — fullbody

2B steps carefully across a narrow, broken steel beam spanning a chasm, her body low and balanced with arms extended for stability; the movement stretches her black dress fabric taut across her hips, highlighting the silhouette of her thigh-high stockings as she reaches to grab a loose bolt on the far side to secure her footing before crossing.

### e026_b01_dynamic — dynamic

2B twists her upper body violently to dodge a horizontal laser beam that slices through the air where her head was a moment ago, causing her short white hair and blindfold straps to whip forward; her black gloves are outstretched in mid-motion, capturing the fleeting blur of movement as she pivots on one heel.

### e026_b01_cinematic — cinematic

A massive mechanical piston slams down into a concrete floor behind 2B, sending a shockwave of dust and small rocks bouncing off her boots; she stands grounded but tense in the wide shot, one hand raised to shield her blindfold from the debris cloud while the heavy machinery looms ominously over her, creating a stark contrast between her fragile stance and the industrial force.

### e026_b02_closeup — closeup

A jagged shard of crystallized data hurls toward 2B's face, forcing her to snap her head slightly left; the impact of the nearby explosion sends a shockwave that ripples through her short white hair, causing it to brush against her black blindfold and momentarily obscure one side of her calm, unblinking expression as she tracks the debris's trajectory with precise focus.

### e026_b02_medium — medium

2B is suspended in mid-air just after leaping over a sparking electrical cable, her black dress hem flaring upward due to the air displacement from her rapid ascent; the tension in her puffy feather-trimmed sleeves creates sharp folds against her arms as she extends one gloved hand forward to grab a protruding metal pipe for support, her waist twisted slightly to maintain momentum while avoiding the live voltage below.

### e026_b02_fullbody — fullbody

Standing on a precarious ledge of broken concrete, 2B extends one leg forward to test its stability before placing her full weight on it, causing the fabric of her black dress to stretch tight across her hips; her other foot remains on the crumbling edge, toes gripping for balance as she lowers herself slowly into a crouch, highlighting the length of her thigh-high stockings and boots against the jagged ruins below.

### e026_b02_dynamic — dynamic

A heavy mechanical claw swings down from above, forcing 2B to roll forward along the ground in a fluid motion; her short white hair streams backward against the direction of movement as she twists her torso to clear the impact zone, with one black glove scraping sparks off the metal floor while her puffy sleeves catch the air, creating a blurred trail of fabric behind her rapid escape.

### e026_b02_cinematic — cinematic

Inside a vast, dimly lit server room, a single emergency light flickers on, casting long, sharp shadows across the floor; 2B stands at the center of the frame, her silhouette framed by the towering racks of machinery, as she slowly raises one hand to catch a falling fragment of glass that has detached from a nearby monitor, the contrast between her stillness and the chaotic decay around her emphasizing her controlled presence in the industrial void.

### e026_b03_closeup — closeup

A burst of steam from a ruptured valve erupts directly in front of 2B, causing her to snap her head back sharply; the sudden heat and pressure force her black blindfold to shift slightly off-center while her short white hair lifts and clings to her forehead, revealing a micro-expression of sharp intake of breath as she shields her face with one gloved hand.

### e026_b03_medium — medium

2B hangs from a fraying industrial cable, her body suspended in mid-air as the rope creaks under the strain; she twists her torso to swing away from a dripping oil slick below, causing the fabric of her black dress to stretch taut across her waist and expose the tension lines of her puffy feather-trimmed sleeves, while her thigh-high boots dangle precariously close to the viscous liquid.

### e026_b03_fullbody — fullbody

Balancing on a single, narrow rebar protruding from a crumbling wall, 2B extends her arms wide to maintain equilibrium as the structure groans; her weight is shifted entirely onto one thigh-high boot, causing her black dress hem to ride up and reveal the full length of her stockings against the industrial backdrop, while her free hand reaches for a loose brick to anchor herself before the rebar snaps.

### e026_b03_dynamic — dynamic

A heavy chain falls from above, striking the ground inches behind B and sending up a spray of gravel; she pivots on her heel in a rapid spin to avoid the impact zone, causing her short white hair and blindfold straps to whip forward in a blur while her black gloves trail sparks off the metal floor, capturing the fleeting moment of near-miss with high kinetic energy.

### e026_b03_cinematic — cinematic

Inside a collapsing elevator shaft, 2B stands firmly on the descending floor as debris rains down around her; she raises one arm to deflect a falling panel while the other hand grips a rusted railing for stability, her silhouette framed by the jagged edges of the broken walls and the flashing emergency lights casting long, dramatic shadows across her black dress and thigh-high boots.

### e026_b04_closeup — closeup

A jagged shard of broken glass strikes the air just inches from 2B's nose, causing her to flinch slightly; her short white hair whips forward across her face due to the sudden proximity of the debris, momentarily obscuring one side of her black blindfold as she holds her breath and keeps her eyes fixed on the falling fragment with intense, unblinking focus.

### e026_b04_medium — medium

2B braces herself against a vibrating metal wall as a heavy hydraulic press slams into the floor beside her; the shockwave sends a ripple through her puffy feather-trimmed sleeves, causing them to flare outward while she grips the rusted railing with both black gloves, her waist twisted sharply to absorb the impact and keep her balance on the unstable surface.

### e026_b04_fullbody — fullbody

Standing on a tilted platform of broken concrete, 2B shifts her weight onto one thigh-high boot to counterbalance the slope; the movement stretches her black dress taut across her hips as she reaches out with one gloved hand to steady herself against a protruding pipe, her other leg extended for balance while debris continues to crumble from the edge below.

### e026_b04_dynamic — dynamic

A burst of steam erupts from a ruptured pipe directly in front of 2B, forcing her to duck low and slide forward on one knee; the sudden pressure sends her short white hair flying upward while her black gloves scrape against the wet metal floor, creating sparks as she maneuvers around the scalding mist with rapid, controlled motion.

### e026_b04_cinematic — cinematic

Inside a vast, dimly lit industrial chamber, a single overhead light flickers on, casting long shadows across the floor; 2B stands at the center of the frame, her silhouette framed by towering machinery as she slowly raises one hand to catch a falling gear that has detached from a nearby mechanism, the contrast between her stillness and the chaotic decay around her emphasizing her controlled presence in the industrial void.
