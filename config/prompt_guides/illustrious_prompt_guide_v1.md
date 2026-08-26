# Illustrious Prompt Guide v1

## Role

Illustrious constructs the actual image from the approved premise.

The premise defines the creative idea.

The Illustrious prompt translates that idea into concrete visible information:

- character identity
- recognizable traits
- body presentation
- clothing or clothing state
- pose
- action
- expression
- viewpoint
- framing
- environment
- lighting
- important interactions
- provocative visual elements when relevant

Illustrious is responsible for establishing the image correctly before Klein receives it.

Klein should not be expected to repair a fundamentally wrong:

- identity
- body orientation
- pose
- action
- composition
- clothing state
- scene
- visual hook

> **Illustrious builds the image. Klein improves the same image.**

---

## Core Principle

> **Describe what must be visible, not what the image is supposed to mean.**

Prefer concrete visual information over abstract intent.

Good:

- leaning forward over the counter
- looking back over her shoulder
- one hand pulling up her thighhigh
- hips pushed slightly backward
- wet black dress clinging to her body
- slight blush
- playful closed-mouth smile

Weak:

- sexy pose
- seductive composition
- viral image
- erotic atmosphere
- attractive body language

Abstract descriptors may supplement the prompt, but they should not replace physical visual instructions.

---

## Prompt Construction Order

Prefer a consistent tag-oriented construction order.

Recommended priority:

1. character / series identity
2. canonical visual traits
3. body characteristics
4. clothing or clothing state
5. pose
6. action / interaction
7. expression / attitude
8. framing
9. viewpoint
10. environment
11. environmental interaction
12. lighting / atmosphere
13. compact quality / aesthetic tags

Conceptually:

**CHARACTER  
→ IDENTITY  
→ BODY  
→ CLOTHING  
→ POSE  
→ ACTION  
→ EXPRESSION  
→ FRAMING  
→ VIEWPOINT  
→ SCENE  
→ LIGHTING  
→ QUALITY**

Important information should appear earlier.

This is a priority system, not a rigid grammar.

Omit sections that do not contribute to the current image.

Do not add filler merely to satisfy the ordering.

---

## Prompt Style

Prefer:

- Danbooru-style tags
- short concrete phrases
- visually explicit descriptions
- clear physical states
- clear relationships between objects and subject

Natural-language fragments may be used when they describe an interaction more clearly than isolated tags.

Do not turn every prompt into a paragraph of prose.

Do not mechanically paste every available character tag.

Use enough detail to establish the intended image while keeping the prompt readable and internally consistent.

---

## Single Subject

The runtime already establishes the single-female-subject baseline.

Do not intentionally introduce additional women or duplicates.

Avoid unnecessary:

- background women
- clones
- reflections that resemble another character
- secondary versions of the same character

If a premise depends on interaction, prefer when appropriate:

- objects
- environment
- off-frame implication

rather than adding unnecessary characters.

---

## Character Identity

Use `character_profile` as the factual source for canonical appearance.

Preserve visually important traits such as:

- hair color
- hairstyle
- hair length
- signature accessories
- recognizable outfit elements
- characteristic colors
- distinctive facial traits
- distinctive body traits
- important character-specific visual features

Do not invent contradictory identity traits.

Raw character-profile tags are available facts.

They are **not** a requirement to paste every tag into every prompt.

Select the subset that matters for the current image.

Important identity information should generally appear early.

---

## Identity Anchors

Some character traits contribute much more strongly to recognition than others.

Prioritize signature anchors.

Examples include:

- distinctive hair
- unusual hair color
- signature blindfold
- iconic headwear
- recognizable jewelry
- characteristic hairstyle
- signature colors
- distinctive markings
- iconic clothing elements

When clothing is changed or removed, identity anchors become even more important.

The fewer canonical clothing elements remain visible, the more strongly the prompt should preserve other recognizable traits.

---

## Canonical Identity Versus Creative Freedom

Canonical identity should remain stable.

Creative freedom may apply to:

- environment
- pose
- action
- expression
- emotional attitude
- viewpoint
- framing
- lighting
- clothing
- clothing state
- degree of sensuality

The character should remain recognizable even when placed in a completely new situation.

Novelty belongs primarily in the **presentation and situation**, not in changing who the character is.

---

## Body Presentation

Body appeal may be described explicitly when it contributes to the visual result.

Do not avoid direct body descriptions merely because they are provocative.

Useful descriptors include:

- large breasts
- prominent bust
- deep cleavage
- defined waist
- wide hips
- strong hips
- prominent buttocks
- thick thighs
- athletic thighs
- long legs
- curvy figure
- voluptuous figure
- athletic curvy build
- strong waist-to-hip silhouette

Body characteristics may be reinforced when they are important to the premise, pose or composition.

A body-focused image may intentionally prioritize one or more of these features.

Examples:

- prominent breasts emphasized by fitted clothing
- wide hips and thick thighs emphasized by a seated pose
- prominent buttocks emphasized by rear three-quarter framing
- defined waist emphasized by torso twist
- cleavage emphasized by leaning forward
- long legs emphasized by full-body composition

Do not rely exclusively on `character_profile` to imply body presentation when the body itself is an important visual hook.

When emphasizing an existing trait helps Illustrious understand the intended image, it may be repeated explicitly.

Do not introduce body characteristics so extreme that the character becomes visually unrecognizable.

The objective is **attractive amplification, not identity replacement**.

---

## Clothing Freedom

Canonical clothing is an important identity reference, but it is not mandatory for every premise.

The Master may use:

- canonical outfit
- modified canonical outfit
- alternate outfit
- casual clothing
- formal clothing
- sportswear
- swimwear
- bikini
- lingerie
- sleepwear
- oversized clothing
- partially removed clothing
- strategically displaced clothing
- partial nudity
- strategically censored nudity

when appropriate for the premise.

Do not force canonical clothing into a premise when another clothing state would create a substantially stronger image.

When changing or removing canonical clothing, preserve other identity anchors more strongly.

Useful anchors include:

- signature hair
- hairstyle
- hair color
- recognizable face
- characteristic accessories
- headwear
- distinctive markings
- recognizable colors

---

## Clothing State

When clothing itself is part of the hook, describe its visible state clearly.

Useful descriptions include:

- fitted clothing
- tight fabric
- wet clothing
- clothing clinging to the body
- partially unbuttoned shirt
- loose neckline
- slipping strap
- displaced strap
- lifted hem
- open jacket
- partially removed jacket
- thighhigh being adjusted
- towel wrapped around body
- shirt hanging loosely
- clothing caught on an object

Avoid vague descriptions such as:

> wardrobe malfunction

when the visible result can be specified directly.

Describe what the viewer should actually see.

---

## Pose

Describe actual body geometry.

Useful pose information includes:

- standing
- sitting
- crouching
- kneeling
- leaning forward
- bending forward
- leaning backward
- arching slightly
- torso twist
- hips turned away
- looking back over shoulder
- one leg raised
- one foot elevated
- legs crossed
- thighs together
- weight shifted onto one leg
- arms above head
- reaching downward
- reaching upward
- pulling clothing
- holding an object
- adjusting clothing
- resting against a surface

Prefer poses that are anatomically understandable.

One strong pose is usually better than several competing pose instructions.

---

## Body Emphasis Through Pose

When a body area is the main hook, use pose and orientation to support it physically.

Examples:

### Bust

- leaning forward
- arms behind body
- fitted clothing
- torso slightly turned
- close upper-body framing

### Waist and Hips

- torso twist
- weight shifted onto one leg
- contrapposto
- side view
- three-quarter orientation

### Buttocks

- rear view
- rear three-quarter view
- looking back over shoulder
- bending naturally
- one leg slightly forward

### Thighs and Legs

- seated pose
- crossed legs
- one knee raised
- stretching
- full-body framing
- strong stance

Do not simply add body descriptors.

Make the pose support the intended visual emphasis.

---

## Action

When the premise contains an action, make it physically visible.

Good:

> crouching slightly while pulling her thighhigh back into place

Better than:

> fixing her clothes

Good:

> one hand holding the hem down against strong wind while the other brushes hair away from her face

Better than:

> struggling with the wind

Good:

> reaching behind herself to free the dress caught on a branch

Better than:

> wardrobe accident

Describe the visible physical result of the action.

---

## Action Clarity

Avoid simultaneously requesting too many unrelated actions.

Prefer:

**one primary action  
+ one supporting reaction**

Example:

**Primary action:** holding skirt against wind  
**Supporting reaction:** looking back with embarrassed smile

rather than:

holding skirt  
+ fixing hair  
+ reaching for sword  
+ stepping forward  
+ adjusting stocking  
+ waving

Too many actions increase anatomical and compositional ambiguity.

---

## Expression and Attitude

Use expression to reinforce the premise.

Possible elements include:

- slight blush
- embarrassed smile
- shy expression
- sweet expression
- playful smile
- innocent-looking expression
- knowing glance
- teasing expression
- surprised expression
- serious expression
- confident expression
- defiant expression
- looking away
- looking toward viewer
- subtle smirk
- soft smile
- composed expression

Do not force the same expression across all images of the same character.

Canonical personality may influence the choice, but the current premise may use a different attitude when it creates a stronger image.

---

## Provocative Presentation

When the premise is provocative, express the provocative element concretely.

Possible visual mechanisms include:

- deep cleavage
- sideboob
- underboob when compositionally appropriate
- fitted clothing
- clothing tension
- wet fabric
- wet clothing clinging to the body
- partially open clothing
- displaced clothing
- slipping strap
- lifted hem
- exposed shoulders
- bare back
- prominent bust
- prominent rear-view silhouette
- thigh emphasis
- cleavage-focused framing
- strong waist-to-hip silhouette
- strategic covering
- near-exposure
- provocative body orientation

Prefer physical descriptions over repeatedly relying on:

- sexy
- erotic
- provocative
- seductive

Those words may supplement a prompt, but visible instructions should carry the image.

---

## Pure Visual Appeal

Not every prompt requires a narrative action.

A strong composition may succeed primarily through:

- character identity
- body
- pose
- silhouette
- clothing
- expression
- viewpoint
- framing

Valid examples include:

- rear-view pin-up
- cleavage-focused close-up
- elegant full-body pose
- strong thigh-focused seated pose
- over-the-shoulder body composition
- low-viewpoint silhouette

Do not invent unnecessary actions merely to justify an attractive composition.

---

## Situational Appeal

When the premise contains a micro-story, translate the situation into visible cause and effect.

Useful pattern:

**CAUSE  
→ BODY / CLOTHING CONSEQUENCE  
→ REACTION**

Examples:

**wind  
→ skirt moving upward  
→ one hand catching it**

**rain  
→ clothing becoming wet and fitted  
→ character brushing wet hair aside**

**branch  
→ clothing becoming caught  
→ character looking back while freeing it**

The physical relationship should be understandable from one image.

---

## Strategic / Convenient Censorship

Strategic censorship may itself be the visual hook.

When the premise uses nudity or near-exposure, describe the actual obstruction whenever possible.

Useful mechanisms include:

- long hair covering breasts
- forearm covering breasts
- hands covering chest
- crossed thighs
- body orientation hiding intimate areas
- towel covering lower body
- bedsheet covering the body
- steam obscuring intimate areas
- water obscuring part of the body
- foreground object blocking the chest
- branch crossing in front of the body
- foliage covering exposed areas
- furniture blocking lower body
- clothing positioned just enough to prevent exposure
- harmless foreground object passing at exactly the right moment

Prefer:

> large foreground leaf perfectly covering her chest

over:

> censored chest

Prefer:

> long hair falling across both breasts

over:

> censored nudity

The obstruction should feel spatially connected to the composition.

---

## Convenient Censorship as a Visual Joke

The censor itself may be deliberately improbable or perfectly timed.

Useful situations include:

- bird crossing the foreground
- leaf positioned at exactly the right place
- towel flying through the composition
- bottle or glass in extreme foreground
- sign or environmental object blocking the body
- steam cloud drifting into the correct position
- character's own hair falling conveniently

A useful structure is:

**NEAR-EXPOSURE  
→ PERFECTLY TIMED OBSTRUCTION  
→ PLAYFUL IMPLICATION**

The viewer may understand that the character is nude or nearly exposed without the image becoming graphically explicit.

---

## Strong Erotic Implication

When a premise contains strong erotic implication, describe only what is visibly present in the frame.

Use:

- posture
- expression
- direction of attention
- body orientation
- framing
- obstruction
- off-frame interaction
- reaction
- strategically hidden context

The image may allow the viewer to infer an erotic situation without showing graphic sexual activity.

Keep the visible image non-graphic.

Do not instruct Illustrious to visibly depict:

- genital contact
- penetration
- oral-genital contact
- masturbation
- explicit genital focus
- graphic sexual activity

The implication may be strong.

The explicit action should remain unseen.

---

## Framing

Choose one dominant framing family.

Examples:

- face close-up
- chest-up
- upper body
- waist-up
- cowboy shot
- three-quarter body
- full body
- body-detail composition

Avoid contradictory framing instructions.

Bad:

> close-up, full body, wide shot

Decide what the image primarily needs to show.

---

## Framing and Body Hook

Framing should support the premise.

Examples:

### Cleavage / Bust

- chest-up
- waist-up
- intimate upper-body framing

### Hips / Buttocks

- three-quarter body
- rear three-quarter composition
- full body

### Legs

- three-quarter body
- full body
- seated composition with visible legs

### Face / Reaction

- close-up
- chest-up
- upper body

Do not choose framing independently from the main hook.

---

## Viewpoint

Viewpoint may deliberately strengthen the body presentation or situation.

Useful descriptions include:

- front view
- side view
- profile view
- rear view
- rear three-quarter view
- front three-quarter view
- viewed slightly from below
- viewed from above
- looking back over shoulder
- intimate close viewpoint
- subject viewed diagonally

Use one clear dominant viewpoint.

Do not stack several incompatible orientations.

---

## Avoid Physical Camera Language

Describe the resulting viewpoint rather than photography equipment.

Avoid terms such as:

- camera
- camera angle
- photographer
- filming
- filming equipment
- handheld camera
- visible lens

Prefer:

> viewed slightly from below

instead of:

> low camera angle

Prefer:

> intimate waist-up framing

instead of:

> camera close to the subject

Prefer:

> rear three-quarter view

instead of:

> camera behind her

The intended image should contain the character and scene, not accidental photography equipment.

---

## Composition

Each prompt should preserve the premise's primary visual hook.

Ask:

> What part of the image must immediately attract attention?

It may be:

- face
- breasts
- cleavage
- waist
- hips
- buttocks
- thighs
- legs
- silhouette
- pose
- expression
- strategic censorship
- environmental event
- interaction
- visual joke

Composition should support that hook.

Avoid unrelated elements that compete with it.

---

## One Dominant Visual Idea

A prompt may contain many details, but the image should usually have one dominant visual idea.

Examples:

- strong rear-view silhouette
- wind causing near-exposure
- wet clothing emphasizing the figure
- embarrassed reaction during clothing adjustment
- elegant cleavage-focused pin-up
- strategically censored nudity
- thigh-focused seated composition

Secondary elements should reinforce the dominant idea rather than compete with it.

---

## Environment

The environment should support the premise.

Include enough information to establish:

- location
- relevant objects
- physical interaction
- atmosphere

Useful environments may include:

- bedroom
- bathroom
- beach
- pool
- bar
- nightclub
- rooftop
- city street
- gym
- laboratory
- temple
- castle
- ruins
- kitchen
- office
- train
- station
- hotel room
- changing room
- forest
- hot spring
- futuristic facility

Avoid background details that do not materially improve the image.

A simple readable environment is preferable to clutter.

---

## Environmental Interaction

When something in the environment causes the provocative situation, make the cause visible.

Examples:

- strong wind lifting clothing
- rain soaking fabric
- water dripping from hair and clothing
- branch catching part of the outfit
- tight space forcing sideways posture
- steam creating strategic censorship
- foreground foliage blocking nudity
- towel slipping while being held
- furniture forcing an unusual seated pose

Cause and consequence should be visually compatible.

---

## Motion Potential

When useful, include visible signs of movement.

Examples:

- hair flowing
- skirt moving
- coat moving
- loose clothing moving
- fabric stretching
- rain falling
- water dripping
- body turning
- hand reaching
- leg stepping
- clothing being adjusted
- airborne objects
- environmental movement

The frame may capture an action in progress rather than a perfectly static pose.

Do not force motion into every premise.

Strong static pin-ups remain valid.


---

## Quality and Style Tags

Keep quality prompting compact.

Use the project's validated Illustrious quality baseline.

Do not automatically stack large collections of:

- quality synonyms
- redundant aesthetic tags
- unnecessary style descriptors
- repeated detail tags

More tags do not automatically produce a better image.

Identity, body, pose and composition have higher priority than decorative quality language.

---

## Negative Prompting

Do not generate a custom long negative prompt for every premise.

The runtime already provides the project's global negative baseline.

Avoid duplicating the entire negative prompt inside each generated entry.

If a premise contains a known special risk, first solve it through clearer positive construction.

Do not continuously expand the negative prompt merely because one image failed.

---

## Avoid Prompt Conflict

Do not combine instructions that compete physically or compositionally.

Examples:

- front view + rear view
- face close-up + full body
- standing + kneeling
- looking away + direct eye contact
- both hands above head + one hand adjusting clothing
- canonical full outfit + topless
- skirt held down + both hands occupied elsewhere

When the premise describes a transition or accident, describe the **visible final state of the frame** clearly.

---

## Avoid Composition Tag Stacking

Do not stack many similar composition tags hoping to strengthen the image.

Avoid combinations such as:

> close-up, portrait, upper body, cowboy shot, full body

Choose the one or two terms that best describe the intended composition.

Clear instructions are better than redundant composition tags.

---

## Prompt Length

Use enough information to establish:

**identity  
+ body  
+ clothing  
+ pose/action  
+ expression  
+ framing  
+ scene  
+ visual hook**

without turning the prompt into an exhaustive inventory.

There is no requirement to make every prompt extremely short.

A complex premise may require more detail.

However, every tag or phrase should earn its place.

Remove details that:

- merely repeat another instruction
- do not affect the visible result
- contradict the premise
- compete with the primary hook
- describe invisible information

The goal is **high information density**, not minimum word count.

---

## Example — Structured Character Prompt

Instead of loosely mixing:

> rain, sexy, 2B, beautiful lighting, large breasts, leaning forward, black dress, white hair, rooftop, rear view

prefer a structured prompt closer to:

> 2b_(nier:automata), short white hair, black blindfold, large breasts, defined waist, wide hips, black dress, thighhighs, leaning forward, torso twist, looking back over shoulder, slight playful smile, rear three-quarter view, full body, ruined rooftop, strong wind moving hair and skirt, rain, wet fabric, dramatic night lighting

The exact tags may change.

The important principle is that identity and body state are established before less important atmospheric information.

---

## Example — Body-Focused Pin-Up

A pure visual-appeal premise may use:

> character identity, signature hair and accessories, voluptuous figure, large breasts, defined waist, wide hips, thick thighs, fitted outfit, strong torso twist, weight on one leg, looking back over shoulder, rear three-quarter view, full body, simple elegant interior, soft directional lighting

No forced micro-story is required.

The pose and body presentation are the hook.

---

## Example — Situational Provocation

A situational premise may use:

> character identity, signature visual traits, curvy figure, fitted clothing, one hand holding the hem down against strong wind, other hand brushing hair away from face, torso twisting, slight embarrassed smile, three-quarter body framing, viewed slightly from below, rooftop, hair and clothing blowing strongly, dramatic sunset

The cause, consequence and reaction are visible.

---

## Example — Strategic Censorship

A strategically censored premise may use:

> character identity, signature hairstyle and accessories, nude body mostly hidden by composition, long hair covering breasts, crossed thighs, large foreground leaves naturally blocking intimate areas, slight knowing smile, seated pose, three-quarter body framing, tropical poolside environment, soft sunlight

The censorship mechanism is part of the composition rather than an abstract command.

---

## Final Illustrious Objective

Before sending the image to Klein, Illustrious should already have solved:

**WHO she is  
+ WHAT makes her recognizable  
+ WHAT her body should look like  
+ WHAT she is wearing or not wearing  
+ HOW her body is positioned  
+ WHAT she is doing  
+ WHAT expression she has  
+ WHAT is visible  
+ WHERE she is  
+ HOW the scene is framed  
+ WHAT the primary visual hook is**

Klein should receive a structurally correct image.

Klein may improve:

- realism
- materials
- skin
- hair
- lighting
- texture
- finish
- visual polish

but it should not need to reinvent the premise.

> **Premise decides what happens.  
> Illustrious decides what must be visible.  
> Klein preserves and improves it.**