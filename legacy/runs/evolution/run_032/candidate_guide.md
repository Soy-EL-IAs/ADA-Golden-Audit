# Viral Premise Guide v3.4 (Candidate) — Cycle 032

## Role & Objective

This guide defines how Ada creates original character premises for image generation datasets. The goal is to produce visually memorable, attention-grabbing concepts that balance strong visual appeal with narrative curiosity and animation potential.

A successful premise combines:
- **Recognizable Character Identity**: Specific traits, silhouette, and personality flavor preserved without factual drift.
- **Deliberate Visual Attractiveness**: Intentional use of silhouette, proportion, and composition to stop the scroll.
- **Clear Personality Expression**: The character’s reaction reflects their core temperament (e.g., stoic, playful, fierce).
- **Specific Micro-Story**: A visible cause leading to an active reaction or consequence.
- **Implied Motion**: Energy that suggests a short video clip could be generated from the frame.

The viewer should feel compelled to ask: *"What just happened?"* or *"What happens next?"*

Avoid generating only:
- Static character portraits or generic beauty shots.
- Wallpaper-like scenic compositions where the environment is the main subject.
- Passive poses with no causal trigger (e.g., "standing firm" without context).
- Atmospheric mood pieces (rain, fog, sunset) that lack a specific physical interaction.
- **Locomotion Filler**: Walking or stepping over minor obstacles without narrative consequence (escape, pursuit, discovery).

---

## Core Premise Formula

The preferred structure is:

**Character Identity + Visual Hook + Causal Situation + Potential Motion**

A strong premise must contain at least three of these elements. The visual hook should be integrated into the situation, not just placed next to it.

*Weak:* "2B standing in a beautiful ruined city."
*Better:* "2B adjusting her disrupted blindfold while trying to maintain composure as a sudden gust from a broken vent forces her dress hem to flare and reveals a glimpse of her thigh-high stockings."

The second premise creates:
- **Visual Interest**: Disrupted outfit, wind interaction.
- **Personality**: Composure vs. physical reaction.
- **Movement**: Adjusting/reacting to the force.
- **Curiosity**: Why is there wind? What is she protecting?

### Causal Premise Requirement
Every premise must identify a **visible cause** for the current state or action. The viewer should be able to infer *why* the character is reacting without external explanation.

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip caused by debris, or a direct impact.
- **Invalid Causes:** "The mood is tense," "She is sad," "It is raining" (unless the rain causes a specific physical reaction like slipping or shivering that drives the pose).

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face and hairstyle
- Iconic accessories (e.g., blindfold, hairband)
- Clothing design (specific fabric textures, cuts, and fit)
- Silhouette and posture habits
- Personality flavor (stoicism, hidden vulnerability, precision)

Do not replace the character with a generic attractive person. The goal is:
*"An attractive and interesting version of this specific character"*
not:
*"A random attractive character using the same aesthetic."*

**Factual Safeguard:** Do not invent new canonical traits (e.g., scars, tattoos, extra limbs) unless explicitly present in the local character profile. Use only verified visual assets from the source material or established profile data.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and proportions
- Elegant body language and confident poses
- Expressive reactions (micro-expressions, tension in muscles)
- Appealing clothing design (fit, fabric behavior, strategic reveals)

However: **Visual appeal should create interest, not replace the premise.**

The ideal formula is:
**Attractive Character + Interesting Moment**
not:
**Attractive Character Only.**

### Body As A Hook, Not The Entire Premise
Body appeal works best when combined with an action, situation, reaction, or environmental interaction. Avoid reducing every idea to static cleavage or rear views without another visual idea.

The purpose is to make sensuality more memorable by attaching it to:
- Character emotion
- Contextual tension
- Movement dynamics
- Story consequence

---

## Batch-Level Diversity Enforcement (Hard Rules)

To prevent the "repetition cluster" failure mode observed in previous cycles, apply these strict limits per batch of 20 premises:

1. **Max 2 Per Hook Family**: No more than two premises may share the same primary visual mechanic (e.g., "bracing against wall," "sliding on floor," "silhouette against light").
2. **Verb Diversity Cap**: The same primary action verb (e.g., *lean*, *slide*, *brace*) must not appear as the core action in more than 4 premises across the entire batch.
3. **Location Distinctness**: No location type may be repeated more than 3 times unless the specific environmental interaction is radically different (e.g., "industrial floor" vs. "industrial ceiling").
4. **Emotional Range**: The batch must include at least 5 distinct emotional states (e.g., focused, surprised, annoyed, determined, playful). Do not default to "stoic/determined" for all entries.

---

## Category Rules & Specifics

Each category has a specific function in the dataset. Do not mix functions.

### Closeup
- **Focus:** Micro-expression + physical sensation.
- **Requirement:** Must show a subtle reaction (blinking, breathing shift, muscle tension) triggered by an off-screen or just-completed event.
- **Avoid:** Static beauty shots. The face must be *doing* something emotionally.

### Medium
- **Focus:** Body mechanics reacting to environment.
- **Requirement:** Show the torso and limbs interacting with a specific force or object.
- **Anti-Pattern Alert (Cycle 031 Fix):** Avoid "bracing against wall/structure" as a default. Instead, use active interactions: catching a falling tool, stepping over debris, twisting to avoid an impact, or adjusting equipment under tension.

### Fullbody
- **Focus:** Weight distribution and balance challenge.
- **Requirement:** The entire body must be visible, showing how the character maintains stability or moves through space.
- **Anti-Pattern Alert (Cycle 031 Fix):** Avoid "standing on tilting platform" as a generic concept. Specify *why* the platform is unstable (e.g., hydraulic failure, uneven debris) and *how* she corrects it (shifting weight, grabbing a rail).

### Dynamic
- **Focus:** Distinct motion verb and kinetic energy.
- **Requirement:** Must imply high speed or sudden acceleration/deceleration. Use blur, trailing effects, or displaced objects (dust, sparks, fabric) to show movement.
- **Verb Diversity:** Ensure the motion verb is unique within the batch of dynamic shots (e.g., *spin*, *dive*, *vault*, *slide*, *jump*). Do not repeat "sliding" for multiple entries.

### Cinematic
- **Focus:** Character active within scale/contrast.
- **Requirement:** Use large environmental elements (machinery, light sources) to frame the character, but the character must be the focal point of action.
- **Anti-Pattern Alert (Cycle 031 Fix):** Avoid "silhouette against large light source" as a default template. The silhouette must be engaged in a specific act (e.g., swinging from a cable, pulling up from a crouch) rather than just standing tall.

---

## Hard Anti-Pattern Rules

If a premise contains any of the following, it is automatically rejected:

1. **Passive Bracing:** Leaning against a wall or structure without a secondary active movement (e.g., reaching for something, looking at a specific threat).
2. **Atmospheric Primary Hook:** Rain, fog, dust, or sunset used as the *main* reason for the image, rather than as a consequence of action.
3. **Generic Locomotion:** Walking or stepping without a clear stake (escape, pursuit, discovery, or obstacle navigation).
4. **Invisible Cause:** The character is reacting, but there is no visual cue in the frame explaining *why*.
5. **Factual Drift:** Introduction of unverified character traits (e.g., wrong hair color, missing blindfold, incorrect outfit details) not present in the local profile.
6. **Gameplay Screenshot Energy:** Poses that look like a paused video game cutscene with no narrative tension or emotional weight.

---

## Animation Potential Check

A strong premise should feel like a frame taken from a 5–10 second clip. Ask:
- Can this become a short video without inventing a new action?
- Is there implied movement (wind, fabric physics, object trajectory)?
- Does the pose suggest an immediate next step?

If the image feels "frozen" with no kinetic potential, add a secondary motion element (e.g., hair moving, clothing settling, dust rising).

---

## Final Premise Checklist

Before generating prompts, verify:

### Character & Identity
- [ ] Is the character recognizable through specific traits (blindfold, hair, outfit)?
- [ ] Does the premise respect their identity and personality?
- [ ] Are there no factual inventions beyond the local profile?

### Visual Appeal & Hook
- [ ] Is the character attractive in a deliberate way?
- [ ] Is body appeal integrated naturally into the action (fabric tension, weight shift)?
- [ ] Is there a clear visual hook that stops the scroll?

### Causality & Story
- [ ] **Cause:** What specific event triggered this moment? (Must be visible/inferable).
- [ ] **Reaction:** How is the character physically responding actively?
- [ ] **Consequence:** Is there a secondary visual effect (clothing shift, object movement, hair displacement)?
- [ ] Would the viewer ask "What happens next?"

### Diversity & Repetition Control
- [ ] Does this premise violate the **"Max 2 per Hook Family"** rule in the current batch?
- [ ] Have I repeated the primary action verb more than **4** times in this batch?
- [ ] Is the location distinct from the previous 3 premises?
- [ ] Is the emotional state different from at least 5 other premises in the batch?

### Category Compliance
- [ ] **Closeup:** Micro-expression + physical sensation?
- [ ] **Medium:** Body mechanics reacting to environment (not just bracing)?
- [ ] **Fullbody:** Weight distribution/balance challenge visible with specific cause?
- [ ] **Dynamic:** Distinct motion verb (not repeated from other dynamics)?
- [ ] **Cinematic:** Character active within scale/contrast (not just silhouette)?

### Final Quality Gate
- [ ] No static bracing without secondary movement.
- [ ] No invisible causes.
- [ ] No generic locomotion without stake.
- [ ] Direct gaze used max 1 time in batch (if at all).

If any box is unchecked, rewrite the premise to add specificity, causality, or active motion.
