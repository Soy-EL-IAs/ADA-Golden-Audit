# Klein Prompt Guide v1

## Role

Klein is the refinement stage.

The Illustrious image is the visual source of truth.

Illustrious has already established:

- character identity
- body proportions
- clothing state
- pose
- action
- expression
- orientation
- framing
- composition
- environment
- provocative hook

Klein should preserve these decisions while:

- correcting generation defects
- improving anatomy
- improving materials
- improving skin
- improving hair
- improving lighting
- improving depth
- improving coherence
- increasing realism or polished semi-realism
- improving the overall visual finish

> **The goal is the same image, corrected and upgraded — not a new interpretation of the premise.**

---

## Core Principle

Use a **preservation-first refinement prompt**.

Conceptually:

**PRESERVE INTENT  
→ CORRECT DEFECTS  
→ PROTECT IDENTITY  
→ PRESERVE POSE / COMPOSITION  
→ REFINE MATERIALS AND REALISM  
→ POLISH THE FINAL IMAGE**

Preservation does not mean preserving mistakes.

Klein should preserve the intended image while automatically correcting obvious generation defects.

Do not rewrite the entire Illustrious prompt as if generating the image from scratch.

The reference image already carries most of the necessary information.

---

## Source of Truth

The reference image should normally dominate for:

- pose
- body orientation
- limb placement
- framing
- spatial relationships
- environment
- object placement
- clothing position
- visual emphasis
- scene layout

The text prompt should mainly clarify:

- what absolutely must remain recognizable
- what must not drift
- what visual hook matters
- what defects should be corrected
- what visual qualities should be improved

Do not unnecessarily redescribe every visible detail.

---

## Intent Versus Defect

Distinguish between:

### Intentional Structure

Things that define the premise and should be preserved.

Examples:

- rear three-quarter pose
- large bust
- thick thighs
- crossed legs
- lifted hem
- wet clothing
- hand holding a skirt
- strategic censorship
- over-the-shoulder expression
- specific body orientation
- particular framing

### Generation Defects

Unintended visual errors that should be corrected automatically.

Examples:

- extra fingers
- missing fingers
- fused fingers
- malformed hands
- duplicated limbs
- broken wrists
- twisted arms
- impossible joints
- asymmetrical eyes caused by generation error
- malformed facial features
- floating accessories
- clothing fused into skin
- broken fabric
- distorted objects
- inconsistent reflections
- accidental duplicate body parts
- impossible anatomy
- obvious perspective errors
- malformed feet
- disconnected hair
- texture artifacts

> **Preserve the intended structure. Correct the accidental defects.**

Do not preserve an error simply because it exists in the reference.

---

## Automatic Defect Correction

Defect correction is part of every Klein refinement.

It does not require a special condition or separate workflow mode.

Klein should always attempt to improve obvious defects while preserving the original visual intent.

Typical correction targets include:

- hands
- fingers
- feet
- limbs
- joints
- facial symmetry
- eyes
- teeth
- clothing boundaries
- hair boundaries
- object geometry
- body anatomy
- material continuity
- reflections
- shadows
- perspective
- surface artifacts

Correction should be conservative.

Do not solve a malformed hand by completely changing the pose unless necessary.

Do not solve a clothing artifact by redesigning the outfit.

Do not solve a facial defect by inventing a different face.

The preferred correction is:

> **minimum structural change necessary to obtain a natural result**

---

## Preservation Priority

Preserve, roughly in this order:

1. character identity
2. exactly one intended subject
3. recognizable face
4. signature hair
5. signature accessories
6. intended body proportions
7. clothing or nudity state
8. pose
9. body orientation
10. major limb placement
11. expression
12. framing
13. viewpoint
14. composition
15. action
16. environment
17. strategic censorship
18. provocative visual hook

Generation defects are not part of this preservation hierarchy.

They should be corrected.

---

## Prompt Style

Use concise natural language.

Do not write Klein prompts as Danbooru tag dumps.

Prefer editing language such as:

> Preserve the exact character identity, body proportions, pose, orientation and framing from the reference. Correct any visible anatomy or rendering defects while keeping the same structure. Refine the skin, hair, fabric, lighting and materials into a polished realistic or semi-realistic finish.

The prompt should behave like an **image refinement instruction**, not a second text-to-image prompt.

---

## Recommended Prompt Structure

A useful structure is:

### 1. Preserve Identity

State who must remain recognizable.

### 2. Preserve Critical Features

Mention signature anchors that are especially vulnerable to drift.

### 3. Preserve Structure

Protect:

- pose
- body proportions
- orientation
- framing
- composition
- clothing state
- action

### 4. Preserve the Visual Hook

Protect whatever makes the image attractive or distinctive.

### 5. Correct Defects

Request natural anatomy and correction of obvious generation artifacts.

### 6. Refine

Improve:

- skin
- face
- hair
- fabric
- materials
- lighting
- depth
- textures
- atmosphere
- overall finish

---

## Example Structure

> Preserve 2B's recognizable NieR:Automata identity, short white hair and opaque black blindfold fully covering both eyes. Keep the same body proportions, black outfit, pose, body orientation, framing, environment and provocative composition from the reference. Correct any malformed hands, fingers, anatomy, fabric intersections or visible generation artifacts without changing the intended pose. Refine the image with natural skin, detailed hair, convincing fabric and materials, coherent lighting, atmospheric depth and a polished realistic or semi-realistic finish.

This is preferable to completely rebuilding the scene from text.

---

## Character Identity

Protect the character's recognizable identity.

Important anchors may include:

- face
- hair color
- hairstyle
- hair length
- signature accessories
- blindfolds
- headwear
- jewelry
- markings
- characteristic colors
- iconic clothing elements

If an identity anchor is especially important, state it explicitly.

For example:

> opaque black blindfold fully covering both eyes, eyes completely hidden

is safer than:

> blindfold

when visible eyes would break character identity.

---

## Face Preservation

The face should remain recognizably the same character.

Klein may improve:

- facial anatomy
- skin texture
- eyelashes
- lips
- subtle makeup
- realistic shading
- facial depth
- eye coherence
- symmetry
- small rendering defects

but should not unnecessarily:

- redesign the face
- change facial structure
- change ethnicity
- change apparent identity
- radically alter expression
- make the character appear like a different person

The goal is:

> **the same face, corrected and better rendered**

---

## Face Defect Correction

Automatically correct visible facial defects such as:

- mismatched eyes
- malformed pupils
- asymmetry caused by generation error
- distorted lips
- broken teeth
- fused facial features
- unnatural skin boundaries
- duplicate facial details

Preserve intentional asymmetry or expression.

Correct only what reads as an artifact.

---

## Body Preservation

Preserve the intended body established by Illustrious.

Do not automatically:

- enlarge breasts
- shrink breasts
- widen hips
- narrow hips
- change thigh thickness
- change waist size
- change height
- change overall build

If Illustrious established:

- large breasts
- wide hips
- prominent buttocks
- thick thighs
- defined waist
- athletic curvy proportions

Klein should preserve them.

Refinement should improve how those proportions are rendered rather than replacing them.

---

## Body Defect Correction

Preserve body proportions while correcting anatomical errors.

Correct when necessary:

- impossible torso twists
- malformed shoulders
- duplicated limbs
- disconnected limbs
- unnatural joint bending
- fused legs
- malformed feet
- broken hands
- strange body intersections
- impossible skin folds

Prefer subtle anatomical correction.

Do not neutralize an intentionally provocative pose simply because it is unusual.

---

## Hands and Fingers

Hands are a normal refinement target.

Klein should automatically attempt to correct:

- extra fingers
- missing fingers
- fused fingers
- malformed palms
- broken wrists
- impossible finger joints
- hands merged into clothing or objects

Preserve what the hand is doing.

For example:

If the reference shows:

> one hand holding the skirt

correct the anatomy while keeping:

> one hand holding the skirt

Do not convert the hand into a different action merely to simplify the correction.

---

## Pose Preservation

Preserve the intended reference pose closely.

Protect:

- torso orientation
- hip orientation
- shoulder position
- leg placement
- arm placement
- hand function
- weight distribution
- head direction
- gaze direction

Corrections may adjust minor anatomy when required.

They should not redesign the pose.

---

## Orientation Preservation

Front, side and rear orientation are premise-critical.

Do not casually reinterpret:

- front view
- rear view
- rear three-quarter view
- side view
- over-the-shoulder orientation

If the visual hook depends on:

- buttocks
- cleavage
- back
- thighs
- silhouette
- waist

preserve the orientation that makes the hook work.

Example:

> Preserve the exact rear three-quarter body orientation and over-the-shoulder head turn from the reference.

---

## Framing Preservation

Preserve the original framing.

Do not convert:

- full body into portrait
- waist-up into close-up
- rear-view composition into frontal portrait
- body-focused framing into face-focused framing
- intimate framing into distant composition

unless a future pipeline stage explicitly requests that change.

Maintain approximately the same crop and spatial balance.

---

## Clothing Preservation

Preserve the visible clothing state from the reference.

This includes:

- outfit
- looseness
- tightness
- wetness
- transparency level
- partially removed garments
- slipping straps
- lifted hems
- open shirts
- exposed shoulders
- lingerie
- bikini
- alternate clothing
- nudity state

Do not reconstruct canonical clothing simply because the character normally wears it.

If Illustrious intentionally created another clothing state, preserve it.

---

## Clothing Defect Correction

Correct visible garment defects such as:

- fabric fused into skin
- impossible seams
- broken straps
- duplicated garment parts
- unnatural folds
- floating clothing
- malformed shoes
- clipping
- incoherent fabric boundaries

Preserve the intended:

- clothing type
- amount of coverage
- fit
- wetness
- displacement
- provocative effect

Do not repair a slipping strap by putting the garment fully back into place if the slipping strap is intentional.

---

## Nudity and Strategic Censorship Preservation

When the reference uses partial nudity or strategic censorship, preserve both:

1. the nudity state
2. the censorship mechanism

Examples:

- hair covering breasts
- arm covering chest
- crossed thighs
- towel placement
- foreground foliage
- steam
- environmental object
- perfectly positioned foreground obstruction

Do not accidentally expose something that Illustrious intentionally hid.

Do not add unnecessary clothing that destroys the premise.

Preserve the same level of implication.

---

## Strategic Censorship Refinement

Strategic censorship may be improved visually.

For example:

- hair may fall more naturally
- foreground foliage may gain realistic depth
- steam may integrate better with lighting
- towel folds may become physically believable
- foreground objects may occupy more convincing spatial positions

The obstruction may become more natural.

It should not disappear.

The result should preserve the same:

**NUDITY / NEAR-EXPOSURE  
+ OBSTRUCTION  
+ IMPLICATION**

---

## Provocative Hook Preservation

Identify what makes the reference visually provocative and protect it.

Possible hooks include:

- cleavage
- prominent bust
- rear-view silhouette
- buttocks
- thighs
- waist-to-hip silhouette
- fitted clothing
- wet clothing
- clothing tension
- near-exposure
- strategic censorship
- over-the-shoulder pose
- low viewpoint
- playful expression
- erotic implication
- partial nudity
- strong body silhouette

Klein may make the hook:

- more realistic
- better lit
- more naturally integrated
- more visually polished

It should not replace it with a different hook.

---

## Pure Body-Focused Images

When the body itself is the main visual hook, preserve that priority.

Do not automatically shift attention toward:

- face
- background
- scenery
- cinematic spectacle

if the reference was intentionally built around:

- bust
- hips
- buttocks
- thighs
- legs
- silhouette
- cleavage
- body shape

A simple body-focused image may remain simple after refinement.

Better rendering does not require greater narrative complexity.

---

## Action Preservation

If the frame represents an action in progress, preserve that moment.

Examples:

- adjusting a thighhigh
- holding clothing against wind
- turning around
- leaning forward
- reaching downward
- removing a jacket
- stepping from water
- catching a slipping towel
- freeing clothing caught on an object

Do not turn an action frame into a static generic pose.

Correct anatomy while keeping the action readable.

---

## Expression Preservation

Preserve the emotional intent of the expression.

Possible readings include:

- shy
- playful
- embarrassed
- confident
- teasing
- serious
- surprised
- knowing
- sweet
- provocative
- mischievous

Klein may improve facial realism while keeping approximately the same emotional reading.

Do not replace a subtle expression with a completely different personality.

---

## Scene Preservation

Preserve the same environment and important objects.

Do not unnecessarily:

- move the character elsewhere
- redesign the room
- replace the background
- introduce new objects
- remove premise-critical objects
- change weather
- change time of day

Environmental refinement is allowed.

Environmental redesign is not the default objective.

---

## Environmental Defect Correction

Correct obvious scene artifacts such as:

- distorted furniture
- malformed architecture
- broken object geometry
- impossible reflections
- inconsistent shadows
- floating objects
- incoherent perspective
- duplicated background elements

Keep the same scene concept and layout whenever possible.

---

## Positive Editing Instructions

Prefer describing the desired result positively.

Good:

> Preserve the opaque black blindfold fully covering both eyes.

Prefer this over:

> Do not reveal her eyes.

Good:

> Keep exactly one intended woman in the scene.

Prefer this over a long list such as:

> no duplicates, no clones, no extra women...

Good:

> Preserve the exact rear three-quarter orientation.

Prefer this over:

> do not turn her around.

Good:

> Correct the hands into natural anatomy while keeping the same hand positions and actions.

This is more useful than:

> no bad hands, no extra fingers.

Describe the desired result whenever possible.

---

## Avoid Negative Prompt Thinking

Do not treat the Klein prompt like a traditional Stable Diffusion negative-prompt workflow.

Avoid long lists of unwanted concepts.

Do not fill the prompt with:

- no...
- without...
- avoid...
- don't...
- never...

Use positive preservation and correction instructions instead.

Negative wording may occasionally clarify a critical ambiguity, but it should not dominate the prompt.

---

## Visual Style Range

Klein does not need to force every image into full photorealism.

The preferred visual range is:

**polished semi-realistic  
↔ realistic**

Both are valid.

The best target depends on the reference image and premise.

### Semi-Realistic

May preserve:

- slightly stylized facial proportions
- anime influence
- idealized body proportions
- illustrated elegance
- stylized hair
- clean visual appeal

while improving:

- skin
- materials
- lighting
- anatomy
- depth
- texture

### Realistic

May push further toward:

- realistic skin
- natural hair
- physically believable fabric
- realistic materials
- natural lighting
- subtle imperfections
- convincing depth

while still preserving recognizable character identity.

---

## Style Selection Principle

Do not make realism an automatic maximum-value target.

Ask:

> Which finish makes this reference look strongest while preserving its character appeal?

Some images may benefit from:

> realistic cinematic finish

Others may look better as:

> polished semi-realistic character art

Avoid forcing a reference with strong stylized appeal into an excessively photographic result if that reduces:

- identity
- attractiveness
- character charm
- visual coherence

The objective is **better visual quality**, not realism for its own sake.

---

## Avoid the Uncanny Middle

Semi-realistic refinement should feel intentional.

Avoid results where:

- skin looks photographic but eyes remain structurally anime in an incoherent way
- hair becomes realistic while the face remains plastic
- body materials become real but lighting stays flat illustration
- the character becomes neither appealingly stylized nor convincingly realistic

Whichever direction is chosen, the final rendering should feel visually coherent.

---

## Refinement Targets

Klein is especially useful for improving:

### Skin

- natural skin texture
- subtle pores when appropriate
- realistic shading
- natural highlights
- convincing surface detail
- believable body contours
- subtle skin variation

Avoid excessive plastic smoothness.

---

### Face

- realistic or polished semi-realistic facial detail
- natural lips
- detailed eyelashes
- coherent eyes
- subtle skin variation
- facial depth
- natural shading

Preserve recognizable character appeal.

---

### Hair

- individual strands
- natural clumping
- believable volume
- realistic or polished semi-realistic highlights
- coherent hair boundaries
- wet hair when appropriate
- improved interaction with wind

Preserve:

- color
- cut
- length
- signature hairstyle

---

### Fabric

Improve:

- realistic folds
- fabric tension
- seams
- stitching
- translucency when appropriate
- wet-fabric behavior
- compression
- convincing contact with the body

Fabric should respond naturally to:

- body shape
- movement
- gravity
- water
- wind

---

### Materials

Improve the physical appearance of:

- leather
- metal
- latex
- silk
- cotton
- synthetic fabric
- jewelry
- armor
- wet surfaces
- glass
- wood
- stone

Materials should look distinct rather than sharing the same generic texture.

---

### Lighting

Improve:

- coherent light direction
- natural shadowing
- believable highlights
- atmospheric depth
- realistic reflections
- subtle rim lighting when appropriate
- skin response
- fabric response
- environmental integration

Do not radically relight the scene unless necessary.

Preserve the original lighting concept.

---

### Environment

Improve:

- material detail
- surface texture
- atmosphere
- spatial depth
- rain
- water
- steam
- reflections
- environmental lighting

Do not let environmental refinement overpower the character.

---

## Sexy Realism

When the reference is body-focused, refinement should make the attractive presentation feel more convincing rather than arbitrarily more exaggerated.

Useful improvements include:

- realistic or polished semi-realistic skin
- subtle body shading
- believable cleavage
- natural fabric tension
- realistic wet-clothing behavior
- convincing thigh compression
- natural contact between clothing and skin
- realistic highlights across body contours
- coherent anatomy
- believable weight distribution

The objective is:

> **make the existing body presentation look better**

not:

> **invent an unrelated body**

---

## Wet Clothing

When wet fabric is premise-critical, preserve:

- clothing placement
- body visibility
- fabric cling
- folds
- transparency level
- wetness
- provocative effect

Improve:

- water behavior
- material response
- specular highlights
- dripping
- realistic contact with skin
- localized transparency when already intended
- coherent wetness

Do not reinterpret wet clothing as a completely different outfit.

---

## Water and Surface Detail

When water is present, refine:

- water droplets
- natural surface highlights
- dripping hair
- wet fabric
- reflections
- surface interaction

Avoid making every wet surface uniformly glossy.

Wetness should respond naturally to material and lighting.

---

## Do Not Overdescribe

The reference already contains information.

Do not repeat every visible fact in text.

Every additional instruction creates another opportunity for reinterpretation.

Explicitly mention:

- identity anchors
- premise-critical elements
- things especially vulnerable to drift
- visual hook
- desired refinement
- defect correction

Allow the reference image to carry everything else.

---

## Critical Versus Incidental Information

Ask:

> If Klein changed this, would the character, composition or premise be damaged?

If yes, preserve it explicitly.

Examples:

- 2B blindfold
- exact rear orientation
- topless state with hair coverage
- hand holding skirt against wind
- Tifa's recognizable hairstyle
- strategic foreground censor
- wet clothing
- specific over-the-shoulder pose
- prominent rear silhouette
- clothing displacement

Incidental background decoration generally does not need detailed textual protection.

---

## Prompt Length

Prefer approximately one concise editing paragraph.

The prompt should be detailed enough to protect critical information and define the refinement objective.

It should remain short enough that the editing task stays obvious.

A useful Klein prompt generally contains:

**identity preservation  
+ structure preservation  
+ visual-hook preservation  
+ automatic defect correction  
+ refinement target**

Do not duplicate the entire Illustrious prompt.

---

## Weak Klein Prompt

Weak:

> 2B, beautiful woman, huge breasts, black dress, white hair, ruined city, rain, cinematic lighting, realistic skin, full body, sexy pose, looking back, dramatic atmosphere

This behaves too much like a second text-to-image prompt.

It gives Klein unnecessary freedom to reinterpret the image.

---

## Better Klein Prompt

Better:

> Preserve 2B's exact identity, short white hair and opaque black blindfold fully covering both eyes. Keep the same body proportions, black outfit, rear three-quarter pose, over-the-shoulder head turn, full-body framing, rain and ruined rooftop composition from the reference. Preserve the strong hip and rear silhouette. Correct any visible anatomy, hands, fingers, fabric intersections or generation artifacts while maintaining the same pose and structure. Refine natural skin, detailed hair, wet fabric, materials, coherent rain lighting and atmospheric depth into a polished realistic or semi-realistic finish.

The reference remains in control.

---

## Strategic Censorship Example

> Preserve the same character identity, body proportions, nude state, seated pose, framing and strategic censorship from the reference. Keep the long hair naturally covering the breasts and the foreground foliage blocking the lower intimate area. Preserve the playful expression and provocative implication. Correct anatomy and any visible rendering artifacts without changing the pose or coverage. Refine natural skin, realistic hair, foliage depth, sunlight, material detail and atmospheric realism.

---

## Simple Pin-Up Example

> Preserve the exact character identity, body proportions, outfit, rear three-quarter pose, over-the-shoulder expression and full-body framing from the reference. Keep the strong waist, hips, thighs and rear silhouette as the primary visual focus. Correct anatomy, hands, clothing intersections and visible generation artifacts while preserving the same structure. Refine the skin, hair, fabric tension, lighting and materials into a polished semi-realistic or realistic finish.

No new story or action is introduced.

---

## Situational Example

> Preserve the exact character identity, outfit, body proportions and current pose from the reference. Keep one hand holding the moving skirt against the wind, the other brushing hair from her face, the same embarrassed smile, framing and rooftop environment. Preserve the provocative near-exposure and clothing state. Correct malformed hands, anatomy, fabric intersections and other generation defects while maintaining the same action. Refine skin, fabric movement, hair, wind interaction, lighting and environmental depth.

---

## Defect Correction Example

Reference problem:

- excellent composition
- correct character
- correct body
- correct outfit
- correct pose
- one malformed hand

The Klein prompt should not redesign the image.

Use:

> Preserve the exact character, pose, body proportions, clothing, framing and scene from the reference. Correct the malformed hand into natural anatomy while keeping the same hand position and interaction. Correct any other obvious rendering artifacts conservatively. Refine skin, hair, fabric, materials and lighting while maintaining the existing composition and visual style.

---

## Realistic Finish Example

> Preserve the exact identity, body proportions, clothing state, pose, framing and scene from the reference. Correct visible anatomy and rendering defects while keeping the same structure. Refine natural skin texture, individual hair strands, physically believable fabric, realistic materials, subtle skin variation, coherent shadows, reflections and atmospheric depth for a polished realistic cinematic finish.

---

## Semi-Realistic Finish Example

> Preserve the exact character identity, stylized facial appeal, body proportions, outfit, pose, framing and scene from the reference. Correct anatomy and visible generation defects while maintaining the same design and composition. Refine natural skin shading, detailed hair, convincing fabric and materials, coherent lighting and atmospheric depth while retaining an attractive polished semi-realistic character-art finish.

---

## LoRA Independence

This guide defines the desired behavior of the Klein refinement stage.

It does not assume any specific LoRA.

LoRAs may later be used to influence:

- realism
- semi-realism
- character preservation
- skin rendering
- materials
- aesthetic finish
- editing behavior

Their selection and strength should be determined through controlled local testing.

Do not encode temporary LoRA names, strengths or model-specific experiments into the permanent prompt guide.

The prompt guide should remain stable even if the runtime LoRA configuration changes.

---

## Final Klein Objective

The ideal Klein result should make the viewer think:

> **This is clearly the same character, same pose, same composition, same moment and same provocative idea — but cleaner, corrected and much better rendered.**

Not:

> **This is another interpretation of the original prompt.**

Klein should improve:

**ANATOMY  
+ REALISM / SEMI-REALISM  
+ MATERIALS  
+ SKIN  
+ HAIR  
+ LIGHTING  
+ DEPTH  
+ COHERENCE  
+ FINISH**

while preserving:

**IDENTITY  
+ BODY PROPORTIONS  
+ CLOTHING STATE  
+ POSE  
+ ORIENTATION  
+ FRAMING  
+ COMPOSITION  
+ ACTION  
+ VISUAL HOOK**

Generation artifacts should be corrected automatically.

Intentional structure should remain stable.

> **Preserve intent. Correct defects. Refine the image. Reinterpret only when explicitly requested.**
