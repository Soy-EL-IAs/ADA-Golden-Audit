# MiniMax Video Prompt Guide v1

## Role

This guide defines how Ada should write MiniMax H3 video prompts for two workflows only:

1. F2V — First Frame to Video
2. Ref2V — Full Reference to Video

Do not use this guide for T2V, FL2V, L2V, video editing or video continuation.

The purpose is to transform an approved image / premise into a temporally coherent MiniMax H3 video prompt with:

- correct reference syntax
- subject preservation
- clear shot structure
- explicit timing
- controlled camera direction
- physical motion
- identity continuity
- dialogue when required
- synchronized sound
- optional music

---

# 1. Workflow Selection

## F2V

Use F2V when the supplied image is the literal first frame of the generated video.

The reference image represents exactly what exists at:

**00:00.000**

The video must evolve forward from that state.

Internally this corresponds to MiniMax H3 I2VA.

Conceptually:

**REFERENCE IMAGE  
= ACTUAL FRAME AT 0.00s**

then:

**FRAME  
→ ACTION BEGINS  
→ MOTION DEVELOPS  
→ REACTION / RESULT**

---

## Ref2V

Use Ref2V when one or more supplied assets define reusable:

- characters
- identity
- face
- body
- clothing
- objects
- environments
- poses
- actions
- styles
- movement
- composition
- audio characteristics

without necessarily being literal first frames.

Conceptually:

**REFERENCE ASSETS  
→ SUBJECT DEFINITIONS  
→ RETENTION RULES  
→ NEW VIDEO TIMELINE**

Ref2V allows the video to create new:

- shots
- poses
- actions
- viewpoints
- environments
- interactions

while preserving the reference attributes that matter.

---

# 2. F2V Prompt Structure

Every F2V prompt begins with exactly this first-frame relationship:

For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

Then use the three MiniMax H3 core fields:

integrated_multimodal_description:

overall_soundscape:

non_diegetic_music:

Conceptual template:

For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] ...

[Shot 2] At 00:XX.XXX, ...

[Shot 3] At 00:XX.XXX, ...

overall_soundscape: ...

non_diegetic_music: ...

---

# 3. F2V First-Frame Rule

<Picture 1> is not merely an identity reference.

It is the actual first frame.

At 0.00 seconds preserve what is visibly established by the image:

- character identity
- face
- hairstyle
- body proportions
- clothing state
- pose
- limb position
- expression
- framing
- viewpoint
- objects
- environment
- lighting
- spatial relationships

Do not begin by inventing a different pose or composition.

The first visible movement should develop naturally from the supplied frame.

---

# 4. F2V Action Development

A useful progression is:

**FIRST-FRAME ANCHOR  
→ ACTION ONSET  
→ CONTINUOUS DEVELOPMENT  
→ RESULT / REACTION**

Example:

The image shows the character holding her skirt against strong wind.

Do not begin with:

> She suddenly sits on a chair.

Prefer:

> The wind strengthens. Her hair sweeps sideways and the loose fabric lifts further. She tightens her grip on the skirt, shifts her weight and looks toward the viewer with an embarrassed smile.

The generated movement should feel like the next moment after the image.

---

# 5. F2V Identity Preservation

When the seed already establishes a recognizable character, preserve:

- face
- hair
- signature accessories
- body proportions
- clothing
- clothing state
- characteristic colors

Do not unnecessarily redescribe every identity detail.

Explicitly reinforce only important or vulnerable anchors.

Example:

> Preserve her short white hair, opaque black blindfold, recognizable face, body proportions and existing black outfit throughout the sequence.

The image remains the primary visual anchor.

---

# 6. F2V Clothing and Provocative State

Preserve the opening clothing state exactly.

If the seed contains:

- wet clothing
- lingerie
- bikini
- partially removed clothing
- slipping strap
- lifted hem
- topless state
- strategic censorship
- near-exposure

the video should begin with that same state.

Movement may evolve the situation when that is the intended action.

Do not arbitrarily:

- restore canonical clothing
- add new garments
- remove garments without narrative cause
- change censorship mechanisms
- change body proportions

---

# 7. Ref2V Prompt Structure

Ref2V uses six sections in this exact order:

subject_definitions:

summary:

retention_analysis:

detailed_description:

overall_soundscape:

non_diegetic_music:

---

# 8. Ref2V Subject Definitions

`subject_definitions` establishes reusable reference content.

Use:

<Subject 1>
<Subject 2>
<Subject 3>

etc.

A Subject represents reusable visible content, not merely the source file.

Subjects may represent:

- character
- person
- object
- environment
- clothing
- prop
- effect
- style
- pose
- expression
- action

Example:

<Subject 1> is 2B as defined by <Picture 1>, preserving her recognizable facial identity, short white hair, opaque black blindfold, body proportions and visible black outfit.

From then on, refer to:

<Subject 1>

rather than repeatedly rebuilding the character description.

---

# 9. Subject Identity Anchors

Character Subject definitions should describe the important reusable visual information.

Prioritize:

- recognizable face
- hairstyle
- hair color
- signature accessories
- body proportions
- distinctive clothing
- characteristic colors
- iconic visual traits

Do not convert the Subject definition into an exhaustive character biography.

Describe what MiniMax needs to preserve visually.

---

# 10. One Picture May Define Several Subjects

One image may contain several reusable elements.

For example:

<Picture 1>

may provide:

<Subject 1> = character

<Subject 2> = outfit

<Subject 3> = environment

Only separate them when the target video needs to manipulate or reference them independently.

Do not create unnecessary Subject labels.

---

# 11. One Subject May Use Multiple References

A Subject may inherit different attributes from different references.

Example:

<Subject 1> is the woman whose visual identity and body appearance come from <Picture 1>, while her walking motion is referenced from <Video 1>.

Use this when multiple sources genuinely provide different useful attributes.

---

# 12. Picture Labels

Use standalone:

<Picture N>

when the image itself has a structural role such as:

- first frame
- keyframe
- final frame
- composition anchor
- storyboard reference
- shot-planning reference

Example:

<Picture 2> is the composition reference for [Shot 3], defining the rear three-quarter viewpoint and subject placement.

If an image only defines a character, clothing, environment or style, normally cite it inside the corresponding Subject definition instead.

Example:

<Subject 1> is the woman in <Picture 1>...

Do not create a redundant standalone Picture definition unless the image itself matters later.

---

# 13. Ref2V Summary

`summary` is a short English paragraph describing:

- target video
- principal subjects
- main reference relationships
- overall task

For our normal Ada Ref2V generation workflow, begin with:

[reference generation]

Example:

summary:
[reference generation] The target video follows <Subject 1> through a short provocative cinematic sequence in which strong wind disrupts her clothing while her identity, body proportions and outfit remain consistent with the supplied reference.

Keep this short.

Do not describe every shot here.

The actual timeline belongs in `detailed_description`.

---

# 14. Retention Analysis

`retention_analysis` explains what must be preserved from each reference.

For visible content use the official relationship markers:

- fully_preserved
- partially_preserved
- attribute_transfer
- weak_reference

Typical Ada character generation should usually use:

**fully_preserved**

for character identity.

Example:

<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - facial identity, short white hair, black blindfold, body proportions and recognizable character appearance remain consistent throughout the sequence.

If clothing changes intentionally:

<Subject 2> (appears in [Shot 1], [Shot 2]): partially_preserved - the original clothing design remains recognizable while its physical state changes naturally during the action.

Retention describes reference fidelity.

It should not prevent the video from introducing new actions or viewpoints.

---

# 15. Ref2V Detailed Description

`detailed_description` is the actual video.

Before `[Shot 1]`, establish the general target-video style in one or two sentences.

Then write the sequence in playback order.

Conceptual structure:

detailed_description:
The target video uses a polished realistic cinematic style with natural skin, coherent lighting and restrained handheld physicality.

[Shot 1] ...

[Shot 2] At 00:XX.XXX, ...

[Shot 3] At 00:XX.XXX, ...

Each shot should establish as needed:

- composition
- subjects
- subject position
- body state
- environment
- lighting
- action
- reaction
- camera motion
- physical secondary motion
- sound events
- dialogue
- relevant reference labels

Do not reduce `detailed_description` to a plot summary.

Describe what actually happens visually and temporally.

---

# 16. Subject Labels Inside Shots

When a referenced subject appears, use its label.

Example:

[Shot 1] A medium full-body composition frames <Subject 1> standing beside the pool...

Later:

[Shot 2] At 00:03.000, the shot cuts to a rear three-quarter view of <Subject 1>...

This reinforces continuity.

Do not rename the same character differently across shots.

---

# 17. Shot Timing

[Shot 1] has no timestamp.

It begins automatically at:

00:00.000

Every later shot uses:

[Shot N] At MM:SS.mmm, ...

Example:

[Shot 1] ...

[Shot 2] At 00:02.500, ...

[Shot 3] At 00:05.500, ...

[Shot 4] At 00:08.000, ...

Timestamps represent the exact moment of the cut.

They must:

- increase strictly
- remain inside the requested duration
- leave enough time for the described action

Do not assign two shots the same timestamp.

---

# 18. Plan Time Before Writing

Before writing the prompt, silently plan:

1. total duration
2. number of shots
3. cut times
4. purpose of each shot
5. action progression
6. final state

Example internal plan for 10 seconds:

Shot 1:
0.0 → 2.5

Shot 2:
2.5 → 5.5

Shot 3:
5.5 → 8.0

Shot 4:
8.0 → 10.0

The exact distribution depends on the premise.

Do not mechanically split every video into equal intervals.

---

# 19. Shot Count

More shots are not automatically better.

Use the minimum number of shots necessary to communicate the idea clearly.

A cut should preferably reveal new information about:

- subject
- body
- action
- reaction
- space
- viewpoint
- state
- time

If only a small framing change is required, prefer camera motion inside the current shot.

Do not cut simply to make the prompt look cinematic.

---

# 20. Ada Shot Heuristic

As a practical starting point:

### 5-second video

Usually:

- 1 to 3 shots

### 10-second video

Usually:

- 2 to 4 shots

### 15-second video

Usually:

- 3 to 5 shots

These are project heuristics, not hard MiniMax rules.

A single continuous shot may be better when:

- identity preservation is critical
- the movement itself is the hook
- the scene is intimate
- continuity matters more than coverage

Use more shots when different viewpoints genuinely add value.

---

# 21. Shot Purpose

Each shot should have a reason.

Useful shot roles include:

### Establish

Show:

- character
- pose
- environment
- starting state

### Reveal

Show a previously hidden visual element.

Examples:

- rear silhouette
- body detail
- object
- reaction

### Action

Show the principal physical event.

### Reaction

Show face or body response.

### Payoff

Deliver the final visual joke, provocative implication or dramatic beat.

A short video does not need every role.

---

# 22. Camera Direction

Unlike Illustrious prompting, MiniMax video prompts should explicitly describe camera behavior.

Useful movement types include:

- Zoom In
- Zoom Out
- Push In
- Pull Out
- Pan Left
- Pan Right
- Truck Left
- Truck Right
- Tilt Up
- Tilt Down
- Pedestal Up
- Pedestal Down
- Arc Shot
- Tracking Shot
- Static Shot
- slight camera shake
- strong camera shake
- POV
- Roll Clockwise
- Roll Counterclockwise

Write them as natural English actions.

Good:

> The camera pushes in with small amplitude at slow speed toward her expression.

Good:

> The camera tracks alongside her as she steps forward.

Avoid:

> Push In, slow, cinematic, small amplitude.

---

# 23. Camera Amplitude and Speed

Use when useful:

### Amplitude

- with small amplitude
- with large amplitude

### Speed

- at slow speed
- at fast speed

Medium amplitude and normal speed generally do not need explicit labels.

Do not over-specify every camera movement.

---

# 24. Framing Vocabulary

Useful framing includes:

- extreme close-up
- close-up
- chest-up
- medium shot
- medium-wide shot
- three-quarter body
- full-body shot
- wide shot
- rear three-quarter shot
- over-the-shoulder shot
- POV shot
- detail shot

Framing should serve the current shot's purpose.

---

# 25. Camera and Provocative Composition

Camera direction may deliberately emphasize the visual hook.

Examples:

### Bust / Cleavage

- close-up
- chest-up
- slow Push In
- slight high or eye-level perspective

### Waist / Hips

- medium shot
- three-quarter framing
- Arc Shot
- side or three-quarter composition

### Buttocks / Rear Silhouette

- rear three-quarter shot
- tracking from behind
- controlled low viewpoint
- slow Arc Shot

### Legs / Thighs

- three-quarter body
- full-body
- lateral tracking
- low or neutral viewpoint

Do not sacrifice subject identity purely to exaggerate the body.

---

# 26. Motion Hierarchy

Each shot should have:

**PRIMARY ACTION**

and optionally:

**SECONDARY MOTION**

Example:

Primary action:

> She turns toward the viewer.

Secondary motion:

> Her hair and loose clothing respond naturally to the turn.

Good secondary motion includes:

- breathing
- blinking
- hair movement
- fabric movement
- straps
- accessories
- water
- rain
- wind
- steam
- body-weight shifts

Do not make every visible element move aggressively at once.

---

# 27. Physical Continuity

Movement should obey physical continuity.

Objects and body parts should demonstrate:

- weight
- inertia
- contact
- acceleration
- deceleration
- gravity
- believable follow-through

Examples:

A heavy weapon should move with weight.

Wet hair should respond differently from dry hair.

Loose fabric should lag slightly behind rapid body movement.

A towel held by one hand must remain spatially connected to that hand.

---

# 28. Character Continuity

Across all shots preserve:

- face
- hair
- body proportions
- signature accessories
- clothing identity
- clothing state unless intentionally changed
- recognizable character features

Avoid:

- face drift
- unexplained hairstyle changes
- body-proportion drift
- clothing morphing
- unexplained accessory changes
- anatomy drift

When necessary, explicitly reinforce continuity at the end of the prompt.

---

# 29. Body Continuity

Intentional body characteristics should remain stable across the sequence.

If the reference establishes:

- large breasts
- defined waist
- wide hips
- prominent buttocks
- thick thighs
- athletic curvy proportions

do not allow those proportions to fluctuate between shots.

Camera perspective may change their apparent prominence.

The underlying body identity should remain consistent.

---

# 30. Clothing Continuity

Clothing state should change only through visible physical action.

For example:

Good:

strap starts on shoulder
→ slips gradually
→ character catches it

Bad:

full outfit
→ unexplained bikini after cut

Good:

dry shirt
→ character enters water
→ wet shirt clings naturally

State transitions should have an observable cause.

---

# 31. Strategic Censorship in Video

When strategic censorship is part of the premise, treat the censor as a physical moving element.

Examples:

- hair
- towel
- steam
- foliage
- foreground object
- furniture
- clothing
- environmental prop

Preserve the intended coverage while allowing believable movement.

Example:

> Strong wind moves her long hair across her shoulders while several strands continue to cover her chest naturally.

Or:

> Steam drifts across the foreground, repeatedly obscuring the intimate areas as she moves.

The censorship mechanism may itself become part of the visual tension.

---

# 32. Provocative Action

Provocative motion should remain physically understandable.

Useful patterns include:

- clothing adjustment
- over-the-shoulder turn
- leaning closer
- sitting or standing
- stretching
- stepping from water
- towel adjustment
- strap movement
- skirt reacting to wind
- wet clothing reacting to movement
- body-weight shift
- playful gaze change
- shy reaction becoming teasing

Avoid meaningless random movement simply because the seed is provocative.

---

# 33. Expressions Over Time

Expression may evolve during the video.

Useful transitions include:

- neutral → surprised
- surprised → embarrassed
- embarrassed → playful
- innocent → knowing smile
- serious → subtle teasing
- confident → amused
- shy → confident

Keep transitions readable and gradual when possible.

Do not radically change personality every second.

---

# 34. Dialogue Speaker IDs

A visual Subject and a speaker ID are different concepts.

Example:

<Subject 1>

identifies the reusable visual character.

(S1)

identifies the vocal source.

If <Subject 1> speaks:

<Subject 1> (S1)

The same speaker must keep the same speaker ID across all shots.

Characters who never speak or vocalize do not need speaker IDs.

---

# 35. Dialogue Syntax

Dialogue uses:

<d>[Language] exact dialogue</d>

Example:

<Subject 1> (S1) looks toward the viewer and says with a soft Russian accent, <d>[Spanish] Señorita Belén.</d>

Keep outside `<d>`:

- speaker identity
- action
- emotion
- tone
- accent
- vocal description

Keep inside `<d>`:

- language tag
- exact spoken words

Do not translate user-supplied dialogue.

---

# 36. Voice Description

When no audio reference exists, describe useful vocal traits when important:

- gender presentation
- pitch
- timbre
- pace
- accent
- emotional delivery
- volume

Example:

> <Subject 1> (S1) speaks in a soft feminine voice with a noticeable Russian accent, restrained volume and deliberately slow delivery.

Do not repeatedly redefine the voice in every shot.

---

# 37. Dialogue Timing

Dialogue must fit inside the available shot duration.

Do not write long speeches into a 1-second shot.

When planning dialogue:

**available seconds  
→ realistic spoken duration  
→ action around dialogue**

Dialogue should not force impossible pacing.

---

# 38. Dialogue Across Cuts

When dialogue naturally continues across a cut, preserve audio continuity.

Do not restart the voice merely because the viewpoint changed.

If necessary, use MiniMax dialogue continuity syntax such as:

<scenetrans>

for dialogue spanning a scene transition.

Use:

<cutoff>

when speech is intentionally truncated by the end of the video.

Use these only when actually needed.

---

# 39. Diegetic Sound

Physical sounds occurring inside the scene belong in the shot description when timing matters.

Examples:

- footsteps
- fabric movement
- water splash
- door closing
- glass impact
- breathing
- wind gust
- chair scrape
- weapon impact
- rain
- laughter

Synchronize sound with visible action.

Example:

> Her boot lands on the wet floor with a soft splash as water sprays outward.

---

# 40. overall_soundscape

After the detailed timeline, summarize the complete ambient and physical sound environment.

Use one short paragraph.

Examples of content:

- room ambience
- rain
- wind
- footsteps
- fabric
- breathing
- water
- environmental sounds
- impacts

Do not repeat full dialogue here.

Example:

overall_soundscape: Continuous rain falls around the rooftop while strong wind moves loose fabric and hair. Wet footsteps, subtle breathing and clothing friction remain naturally synchronized with her movements.

---

# 41. non_diegetic_music

This describes music heard only by the audience.

Describe:

- instrumentation
- tempo
- rhythm
- dynamic evolution

Example:

non_diegetic_music: Sparse electronic pulses at a slow tempo with low sustained strings, gradually increasing in intensity before fading during the final shot.

If there should be no background score:

non_diegetic_music: N/A

Do not confuse environmental music audible by the character with non-diegetic music.

---

# 42. F2V Example

For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] Preserve the exact woman, facial identity, body proportions, clothing state, rooftop composition and strong rear three-quarter pose shown in <Picture 1>. Strong wind continues moving her hair and loose fabric. She tightens one hand around the hem of her outfit while turning her head farther over her shoulder toward the viewer. The camera slowly arcs around her with small amplitude while maintaining the strong hip and rear silhouette.

[Shot 2] At 00:03.000, the shot cuts to a medium upper-body view as another gust pushes her hair across her face. She brushes it aside with her free hand, briefly looking embarrassed before developing a subtle playful smile. Her clothing and hair continue reacting naturally to the wind.

[Shot 3] At 00:06.500, the shot cuts back to a three-quarter full-body composition. She releases some of the tension in her stance, shifts her weight onto one leg and takes a slow step forward while maintaining eye contact. The camera tracks backward at slow speed, preserving her recognizable identity and body proportions through the end of the sequence.

overall_soundscape: Strong rooftop wind moves continuously around the character, accompanied by fabric flutter, hair movement, soft footsteps and subtle breathing. Distant city ambience remains low beneath the wind.

non_diegetic_music: Low electronic pulses with sparse sustained synth tones at a slow tempo, gradually decreasing in volume during the final shot.

---

# 43. Ref2V Example

subject_definitions:
<Subject 1> is 2B as defined by <Picture 1>, preserving her recognizable facial identity, short white hair, opaque black blindfold, curvy athletic body proportions and signature visual appearance.
<Subject 2> is the black outfit shown on <Subject 1> in <Picture 1>, including its fitted silhouette and recognizable dark YoRHa-inspired design.

summary:
[reference generation] The target video follows <Subject 1> through a short provocative rooftop sequence while preserving her identity and <Subject 2>. Strong wind creates ongoing clothing and hair movement as the camera reveals different views of the character.

retention_analysis:
<Subject 1> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - facial identity, short white hair, opaque black blindfold, body proportions and recognizable character appearance remain consistent throughout the sequence.
<Subject 2> (appears in [Shot 1], [Shot 2], [Shot 3]): fully_preserved - the recognizable black outfit, fit and visual design remain consistent while the fabric responds naturally to wind and body movement.

detailed_description:
The target video uses a polished realistic cinematic style with natural skin, detailed fabric, coherent lighting and restrained atmospheric motion.

[Shot 1] A three-quarter full-body composition frames <Subject 1> on a high ruined rooftop wearing <Subject 2>. Strong wind blows across the scene, moving her short white hair and loose fabric. She stands with her weight on one leg and gradually turns her torso away while looking back over her shoulder. The camera begins a slow Arc Shot with small amplitude, preserving her recognizable body proportions and strong silhouette.

[Shot 2] At 00:03.000, the shot cuts to a closer side view of <Subject 1>. A stronger gust catches part of <Subject 2>, and she immediately reaches downward with one hand to control the moving fabric. Her initial surprise develops into a slight embarrassed smile. Hair, fabric and body motion remain physically coherent.

[Shot 3] At 00:06.500, the shot cuts to a rear three-quarter full-body view. <Subject 1> finishes adjusting <Subject 2>, turns her head toward the viewer and develops a subtle knowing smile. The camera pushes in with small amplitude at slow speed while wind continues moving her hair and clothing. Her facial identity, blindfold, body proportions and outfit remain stable through the end of the video.

overall_soundscape: Continuous rooftop wind moves through the scene with natural fabric flutter and hair movement. Soft footsteps, clothing friction and restrained breathing remain synchronized with <Subject 1>'s movement while distant city ambience remains subtle.

non_diegetic_music: Sparse low strings and restrained electronic percussion at a slow tempo, gradually building during the final Push In before fading.

---

# 44. F2V Versus Ref2V Mental Model

Use this distinction:

## F2V

**THIS IMAGE IS FRAME ZERO.**

Ask:

> What happens next?

Structure:

**Picture 1  
→ motion  
→ shots  
→ result**

---

## Ref2V

**THESE ASSETS DEFINE THINGS I MAY REUSE.**

Ask:

> What must remain recognizable while I create a new video?

Structure:

**References  
→ Subjects  
→ Retention  
→ new timeline  
→ shots**

---

# 45. Final Rule

For F2V:

> **Respect frame zero and evolve forward from it.**

For Ref2V:

> **Define subjects once, preserve what matters, then direct the new video using those stable references.**

For both:

> **Plan the timeline before writing the prose. Every shot needs a purpose, every cut needs a time, every movement needs physical continuity, and the character must remain recognizable from beginning to end.**