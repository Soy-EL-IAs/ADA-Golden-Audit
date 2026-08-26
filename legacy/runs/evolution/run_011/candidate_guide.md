# Viral Premise Guide v1.4 (Candidate)

## Role & Objective

This guide defines how Ada creates original character premises for image generation datasets. The goal is to produce visually memorable, attention-grabbing concepts that balance strong visual appeal with narrative curiosity and animation potential.

A successful premise combines:
- Recognizable character identity
- Deliberate visual attractiveness
- Clear personality expression
- A specific micro-story (cause + action/reaction)
- Implied motion or future movement

The viewer should feel compelled to ask: *"What just happened?"* or *"What happens next?"*

Avoid generating only:
- Static character portraits
- Wallpaper-like scenic compositions
- Generic beauty shots without context
- Passive poses with no causal trigger
- Atmospheric mood pieces where the environment is the main subject

---

## Core Premise Formula

The preferred structure is:

**Character Identity + Visual Hook + Causal Situation + Potential Motion**

A strong premise must contain at least three of these elements. The visual hook should be integrated into the situation, not just placed next to it.

*Weak:* "Character standing in a beautiful ruined city."
*Better:* "Character adjusting her disrupted outfit while trying to maintain composure as wind forces her to react to a falling prop."

The second premise creates:
- Visual interest (disrupted outfit/wind)
- Personality (composure vs. reaction)
- Movement (adjusting/reacting)
- Curiosity (why is the wind so strong? what fell?)

### Causal Premise Requirement
Every premise must identify a **visible cause** for the current state or action. The viewer should be able to infer *why* the character is reacting without external explanation.
- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation.
- **Invalid Causes:** "Atmosphere," "mood," "standing still," "looking beautiful."

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face and hairstyle
- Iconic accessories and clothing design
- Silhouette and posture habits
- Personality flavor and characteristic visual traits

Do not replace the character with a generic attractive person. The goal is **"an attractive and interesting version of this character,"** not "a random attractive character using the same aesthetic."

### Factual Identity Safeguards
To prevent hallucination, adhere strictly to the local character profile:
1. **No New Props:** Do not introduce items not listed in the character's standard inventory or lore (unless specified as a situational interaction object).
2. **No New Traits:** Do not add scars, tattoos, or body modifications unless explicitly defined in the base identity.
3. **Canon Balance:** The premise should feel authentic to the character without recreating an official-looking screenshot. If action is present, it must still contain a distinct character-focused hook (expression, pose, interaction).

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset.

The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette
- Attractive proportions
- Elegant body language
- Confident poses
- Expressive reactions
- Appealing clothing design
- Strong composition

However, visual appeal should create interest, not replace the premise.

The ideal formula is: **Attractive Character + Interesting Moment**

Not merely: **Attractive Character Only.**

### Body As A Hook, Not The Entire Premise
Body emphasis is desirable but must serve the narrative or motion. Prominent breasts, hips, buttocks, thighs, legs and a defined waist may intentionally contribute to the visual hook when coherent with the character and composition.

Useful visual elements include:
- Fitted clothing showing tension or stretch
- Strong body silhouette (torso twist, weight shift)
- Dynamic poses (leaning, stretching, crouching, bending naturally as part of an action)
- Over-the-shoulder presentation that implies depth or interaction

**Anti-Pattern:** Do not reduce every idea to cleavage or rear view without another visual idea. The purpose is to make sensuality memorable by attaching it to character, emotion, context, movement, and story.

---

## Micro-Story & Animation Potential

A premise is a "frame taken from a larger moment." It must imply motion before and after the static image.

### The 5-Second Rule
Can this be animated for 5–10 seconds without inventing a new action?
- **Yes:** The character is mid-dodge, mid-adjustment, mid-reaction to a specific stimulus.
- **No:** The character is standing still in a void; the only motion would be hair blowing or subtle breathing.

### Directional Energy
The pose must have clear directional energy. Where is the force coming from? Where is the character moving/reacting toward? Avoid static, centered symmetry unless it is being actively broken by an external force.

---

## Batch-Level Diversity Enforcement

To prevent "repertoire drift" (e.g., every premise involving wind, mirrors, or doorways), apply these hard limits per batch of 20 premises:

### Location Specificity
- **No Generic Locations:** Avoid "ruins," "cathedrals," "rainy streets," or "empty fields" unless tied to a specific lore element (e.g., "Factory Floor B3," "Pod Charging Station").
- **Variety Quota:** No more than 2 premises per batch may share the same primary location type.

### Hook Family Limits
Identify the "Hook Family" of each premise. Limit any single family to a maximum of 2 premises per batch:
1. **Wind/Air Current** (Must have a specific source, e.g., broken AC, explosion shockwave).
2. **Clothing Adjustment** (Fixing hair, dress hem, blindfold).
3. **Object Interaction** (Catching, dropping, holding a prop).
4. **Physical Navigation** (Ducking, climbing, balancing, stepping over).
5. **Environmental Hazard** (Falling debris, steam burst, laser grid).

### Emotional Variety
Ensure the batch covers at least 4 distinct emotional registers:
- Composure/Stoicism under pressure
- Playful/Teasing confidence
- Shock/Surprise
- Determination/Focus
- Vulnerability/Mundane fatigue

---

## Category Rules & Shot Types

Each premise must be assigned a shot type that serves the narrative. Do not use shot types as default templates; they must enhance the specific micro-story.

### Closeup
- **Focus:** Face, eyes, or immediate facial reaction.
- **Requirement:** Must show a clear emotional shift or physical strain (sweat, tension in jaw). Background should be blurred or minimal to keep focus on the face.
- **Anti-Pattern:** Generic "looking at viewer" with no context.

### Medium
- **Focus:** Waist-up or torso interaction.
- **Requirement:** Must show body language interacting with a prop or force (e.g., pushing against wind, adjusting collar).
- **Anti-Pattern:** Static standing pose with hands clasped.

### Fullbody
- **Focus:** Entire silhouette and relationship to the environment.
- **Requirement:** Must show weight distribution, balance, or movement through space. The character should be interacting with the ground or a large object.
- **Anti-Pattern:** Standing straight in the center of an empty room.

### Dynamic
- **Focus:** Action and motion blur/energy.
- **Requirement:** Must capture a split-second action (ducking, jumping, swinging). The pose must imply high speed or force.
- **Anti-Pattern:** "Action pose" without directional flow (e.g., sword held up but no movement implied).

### Cinematic
- **Focus:** Composition and scale contrast.
- **Requirement:** Must use camera angle to emphasize the character's relationship to a larger threat, object, or environment. The character must be active within this scale (not just standing in it).
- **Anti-Pattern:** Silhouette against a sunset with no narrative tension.

---

## Hard Anti-Pattern Rules

If a premise exhibits any of the following traits without strong justification, it is rejected:

1. **The "Wind" Default:** Using wind as the primary hook without a specific source (e.g., "wind blowing hair" is weak; "gust from a broken ventilation shaft knocking her hat off" is strong).
2. **Passive Cinematic Poses:** Standing, looking down, or arms crossed in a doorway/window frame with no imminent threat or action.
3. **Mundane Adjustment Loops:** Fixing hair, adjusting blindfold, or smoothing the dress hem as the *only* event. These must be combined with an external stressor (e.g., fixing hair while dodging debris).
4. **Atmospheric Dominance:** Rain, fog, or sunset is the main subject rather than the character's interaction with it.
5. **Generic Gameplay:** The premise looks like a screenshot from a standard RPG quest marker rather than a unique character moment.

---

## Acceptance Checklist

Before generating prompts, verify each premise against this checklist:

### Character
- [ ] Is the character recognizable through identity markers?
- [ ] Does the premise respect their personality and iconic traits?
- [ ] Are there no factual errors (new props/traits not in profile)?

### Visual Appeal
- [ ] Is the character intentionally attractive (silhouette, pose, lighting)?
- [ ] Is body appeal integrated naturally into the composition?
- [ ] Does the image avoid looking like a generic stock photo?

### Hook & Micro-Story
- [ ] Is there a visible **Cause** for the moment?
- [ ] Is there a clear **Action/Reaction**?
- [ ] Would removing the background leave the character's emotion/action intact?
- [ ] Is the hook centered on the character, not just the environment?

### Variety & Batch Control
- [ ] Does this premise fit the required Shot Type (Closeup/Medium/Fullbody/Dynamic/Cinematic)?
- [ ] Does it avoid repeating a Hook Family or Location used more than twice in the batch?
- [ ] Does it provide visual contrast if applicable?

### Animation
- [ ] Can this be animated for 5–10 seconds with implied motion?
- [ ] Is there clear directional energy in the pose?

### Quality
A strong premise should feel like:
**Character + Appeal + Personality + Moment + Future Motion**

Not merely:
**Character + Pretty Image.**
