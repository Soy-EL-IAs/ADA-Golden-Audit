# Ada Viral Guide Evolution — Cycle 015

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

Strong batch with high identity fidelity and animation potential. The primary weakness is the repetition of the 'sleeve tension' hook in medium shots, which slightly undermines the diversity score. Minor adjustments to vary the causal agents would elevate this set further.

## Strengths

- Consistent adherence to the 'Causal Premise Requirement' with visible triggers for most actions.
- Strong integration of clothing elements (blindfold, sleeves, stockings) as active participants in the narrative rather than just aesthetic details.
- High animation potential across dynamic and fullbody shots due to clear directional energy and physical consequences.
- Effective use of 2B's personality guardrails, maintaining composure while showing brief cracks through physical strain or tactile reactions.

## Failures

- Repetition of the 'Sleeve Snag/Tension' hook family in three separate medium shots (b01_med, b02_med, b03_med), violating the batch diversity limit.
- Several closeup premises rely on subtle fluid interactions (condensation, steam, oil) that may be difficult to render distinctly without high-resolution detail, risking visual ambiguity.
- Cinematic shots occasionally drift towards 'character in environment' rather than 'character interacting with specific distant element,' particularly b01_cin and b03_cin.

## Desired patterns

- Specific physical interactions with distinct objects (gears, chains, glass shards) that create clear visual tension.
- Use of clothing as a causal agent to add texture and specificity to the micro-story.
- Clear cause-and-effect chains where the viewer can infer the next second's action.

## Undesired patterns

- Repeated use of 'sleeve snagging' or 'fabric tension' as the primary hook for multiple medium shots.
- Passive contemplation or atmospheric mood pieces lacking a specific physical trigger (e.g., b03_closeup with steam).
- Generic locomotion or balancing acts without a clear narrative consequence beyond maintaining position.

## Repetition clusters

- **Sleeve Snag/Tension**: `e015_b01_medium`, `e015_b02_medium`, `e015_b03_medium`
- **Fluid Drop on Blindfold/Face**: `e015_b01_closeup`, `e015_b04_closeup`

## Recommendations for the next cycle

- Limit 'Sleeve/Clothing Snag' hooks to a maximum of 2 per batch and vary the specific clothing item (e.g., blindfold strap, glove finger, boot heel) to maintain diversity.
- For closeup shots, prioritize tactile interactions with solid objects over fluid drops to ensure clearer visual storytelling at lower resolutions.
- Ensure cinematic shots always include a specific, identifiable distant object or event that the character is actively engaging with, not just observing.

## Per-premise audit

| ID | Category | Identity | Appeal | Micro-story | Animation | Notes |
|---|---|---:|---:|---:|---:|---|
| `e015_b01_closeup` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Strong causal link (condensation drop). The 'slipping blindfold' is a recurring motif. Visual appeal relies on the tension of the fingers and the break in composure. |
| `e015_b01_medium` | medium | 9.0 | 8.0 | 8.0 | 7.0 | Good use of clothing as a causal agent (sleeves tightening). The action is specific (prying a grate) rather than generic. Good balance of strain and composure. |
| `e015_b01_fullbody` | fullbody | 9.0 | 7.0 | 6.0 | 8.0 | The 'tilting platform' is a clear cause. However, the focus on stockings stretching feels slightly secondary to the balance act. Good dynamic potential. |
| `e015_b01_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Excellent dynamic shot. Catching a heavy gear is a specific physical interaction with clear consequence (weight/brace). Hair flying adds visual energy. |
| `e015_b01_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | Steadying a beam is active, but 'precarious ledge' is a common trope. The silhouette framing is good, but the narrative hook is weaker than other entries. |
| `e015_b02_closeup` | closeup | 9.0 | 8.0 | 8.0 | 6.0 | Very strong micro-story. Extracting glass from the blindfold is tactile and specific. The 'hairband' detail adds identity fidelity. High tension. |
| `e015_b02_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Sleeve snagging on rebar is a good causal agent. However, it repeats the 'sleeve tension' hook from b01_medium and b03_medium. The stoic expression is well-placed. |
| `e015_b02_fullbody` | fullbody | 8.0 | 7.0 | 6.0 | 7.0 | Balancing on a crumbling pillar is active. The 'falling debris chunk nearby' provides the cause for the tilt. Slightly generic location (stone pillar) but acceptable. |
| `e015_b02_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Deflecting a chain is a strong physical interaction. Sparks add visual flair. Clear direction of movement and force. |
| `e015_b02_cinematic` | cinematic | 8.0 | 7.0 | 7.0 | 6.0 | Grabbing a slipping elevator cable is a specific focal point. The 'vast industrial background' risks becoming wallpaper if not careful, but the action saves it. |
| `e015_b03_closeup` | closeup | 9.0 | 7.0 | 6.0 | 5.0 | Steam on blindfold is a weak cause compared to the drop of condensation or glass shard. 'Verifying heat damage' is an internal thought process rather than a visible physical consequence. Feels passive. |
| `e015_b03_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Another 'sleeve snag' premise. This is the third time this specific hook family appears (b01_med, b02_med). The repetition dilutes the impact of using clothing as a causal agent. |
| `e015_b03_fullbody` | fullbody | 9.0 | 7.0 | 6.0 | 8.0 | Balancing on a girder with wind is similar to b01_fullbody (tilting platform). The 'testing stability' action is good, but the wind cause feels slightly less tangible than the gravity shift. |
| `e015_b03_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Sliding under a beam is excellent dynamic motion. Dust kicking up adds consequence. Clear cause (swinging beam) and reaction (slide). |
| `e015_b03_cinematic` | cinematic | 8.0 | 7.0 | 6.0 | 5.0 | Climbing a slab towards a light is somewhat generic. The 'flickering emergency light' is a good focal point, but the action (climbing) lacks a specific immediate threat or consequence other than reaching the exit. |
| `e015_b04_closeup` | closeup | 9.0 | 8.0 | 7.0 | 6.0 | Catching an oil drop is a strong tactile interaction. Similar to b01_closeup (condensation) but distinct enough in substance (oil vs water). Good tension. |
| `e015_b04_medium` | medium | 9.0 | 8.0 | 7.0 | 6.0 | Retrieving a data chip is a specific goal. The body twist and dress cutout tension are well-integrated. Good use of the 'gap' environment. |
| `e015_b04_fullbody` | fullbody | 9.0 | 8.0 | 8.0 | 7.0 | Resisting a chain pull is a strong physical conflict. The 'dark grate' adds narrative stakes (being dragged). Good use of stockings stretching as a visual cue for force. |
| `e015_b04_dynamic` | dynamic | 9.0 | 8.0 | 7.0 | 9.0 | Side-stepping steam is a clear cause-and-effect. The hair sweeping across the blindfold is a nice identity-specific detail. Good lateral energy. |
| `e015_b04_cinematic` | cinematic | 8.0 | 7.0 | 7.0 | 6.0 | Pressing against a hydraulic piston to save a unit is a strong heroic act. The scale contrast (small character vs large machine) works well. |

## Premises

### e015_b01_closeup — closeup

2B's gloved fingers tense as she pinches the edge of her slipping black blindfold, a single drop of condensation from a ruptured ceiling pipe landing on her forehead to break her composure.

### e015_b01_medium — medium

2B leans forward with controlled urgency, using both gloved hands to pry open a jammed ventilation grate, the strain tightening her puffy sleeves and pulling her dress hem slightly upward.

### e015_b01_fullbody — fullbody

2B crouches low to maintain balance on a tilting metal platform, one hand gripping a rusted pipe for stability as her thigh-high stockings stretch against the sudden shift in gravity.

### e015_b01_dynamic — dynamic

2B twists sharply to catch a falling heavy gear with her forearm, the impact sending her short white hair flying and disrupting the drape of her dress as she braces for the weight.

### e015_b01_cinematic — cinematic

2B stands on a precarious ledge, extending one arm to steady a collapsing beam that is acting as a bridge, her silhouette framed against the chaotic debris of the structure below.

### e015_b02_closeup — closeup

A jagged shard of glass embeds in the fabric of 2B's black blindfold, causing her gloved hand to freeze mid-motion as she carefully extracts it without disturbing the hairband beneath.

### e015_b02_medium — medium

2B twists her torso sharply to release a puffy sleeve that has snagged on a protruding rebar, the pull stretching the fabric taut across her arm while she maintains a stoic expression.

### e015_b02_fullbody — fullbody

Balancing on one leg atop a crumbling stone pillar, 2B reaches out with her free hand to steady herself as the structure tilts under the weight of a falling debris chunk nearby.

### e015_b02_dynamic — dynamic

2B pivots on her heel to deflect a swinging chain with her forearm, the impact driving her into a low crouch and sending sparks scattering from the metal link.

### e015_b02_cinematic — cinematic

From a high vantage point, 2B extends her arm to grab the dangling cable of a suspended elevator car that is slipping below, her silhouette stretching taut against the vast industrial background.

### e015_b03_closeup — closeup

A thin wisp of steam from a ruptured pipe curls against 2B's black blindfold, causing her gloved fingers to tighten on the strap as she leans forward to verify if the heat is damaging the fabric beneath.

### e015_b03_medium — medium

2B turns her torso sharply to pull a puffy sleeve free from a tangle of loose electrical wiring, the sudden tension stretching the dress cutout across her waist as she maintains a focused gaze on the connection point.

### e015_b03_fullbody — fullbody

2B balances precariously on a narrow, rusted girder, extending one leg forward to test its stability before committing her weight, her thigh-high boots gripping the metal as a gust of wind from below threatens to push her off balance.

### e015_b03_dynamic — dynamic

2B ducks low under a swinging steel beam, using her momentum to slide along the ground, the friction of her boots against the concrete kicking up dust while she watches the hazard clear above her head.

### e015_b03_cinematic — cinematic

From a low angle, 2B climbs the jagged edge of a collapsed concrete slab, her silhouette framed against a distant, flickering emergency light that signals the exit path through the darkened industrial corridor.

### e015_b04_closeup — closeup

2B's gloved hand hovers just above her black blindfold, fingers rigidly extended to catch a single heavy drop of oil falling from a leaking overhead pipe before it strikes the fabric, her white hair trembling slightly with the tension of holding still.

### e015_b04_medium — medium

2B leans into a narrow gap between two concrete blocks to retrieve a dropped data chip, her body twisting at the waist so that the cutout of her dress pulls taut against her midsection while her puffy sleeves brush the rough stone surfaces.

### e015_b04_fullbody — fullbody

2B stands with feet planted wide on a wet, moss-covered stone floor, leaning her entire upper body backward against the pull of a heavy chain wrapped around her wrist, her thigh-high stockings stretching as she resists being dragged toward a dark grate.

### e015_b04_dynamic — dynamic

2B executes a rapid side-step to avoid a burst of pressurized steam from a ruptured valve, the sudden lateral force sending her short white hair sweeping across her blindfold and flaring the hem of her black dress outward.

### e015_b04_cinematic — cinematic

From a low angle, 2B presses both palms against a massive, slowly descending hydraulic piston to create enough clearance for a small mechanical unit to pass beneath, her silhouette framed by the towering industrial machinery and the dust cloud kicked up by the impact.
