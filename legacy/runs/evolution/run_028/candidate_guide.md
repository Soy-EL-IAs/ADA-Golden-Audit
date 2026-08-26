# Viral Premise Guide v3.0 (Candidate) — Cycle 028

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip, or a deliberate adjustment.
- **Invalid Causes:** "Vibes," "atmosphere," generic tension, or unexplained stillness.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face (or specific occlusion style)
- Hairstyle and hair texture
- Iconic accessories (blindfold, gloves, headpiece)
- Clothing design and fabric behavior
- Silhouette and proportions
- Personality flavor

**Factual Identity Safeguards:**
1. **No Canon Drift**: Do not invent new scars, tattoos, or eye colors unless specified in the character profile. If the character wears a blindfold, do not show eyes looking through it unless the premise explicitly states the blindfold is removed or transparent (rare).
2. **Silhouette Integrity**: The iconic silhouette must remain readable even in dynamic poses. Do not distort proportions for pure aesthetic exaggeration unless consistent with the character’s established design language.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. It is one of the primary reasons a viewer stops scrolling.

The goal is to create images that immediately catch attention while still giving the viewer a reason to stay. Do not intentionally minimize attractive character features when they are part of the character design.

Characters may intentionally emphasize:
- Feminine silhouette and elegant body language
- Attractive proportions (waist-to-hip ratio, leg length)
- Confident poses and expressive reactions
- Appealing clothing design and fabric tension
- Strong composition leading to the face or key action point

However: **Visual appeal should create interest, not replace the premise.**

The ideal formula is: **Attractive Character + Interesting Moment**

Not merely: **Attractive Character Only.**

### Body As A Hook, Not The Entire Premise
Body emphasis is desirable but must be contextual. Prominent features (bust, hips, thighs) contribute to the visual hook when coherent with the character and composition.

Avoid reducing every idea to:
- Cleavage or rear view without action
- Low viewpoint solely for perspective distortion
- Generic "sexy pose" without a physical reason

The purpose is to make sensuality more memorable by attaching it to **character, emotion, context, movement, and story.**

---

## Category Rules & Distribution

For every batch of 20 premises, enforce the following distribution:
- **4 Closeup**: Focus on face, upper body, or specific detail. Must have strong emotional causality.
- **4 Medium**: Waist-up or three-quarter view. Balanced focus on expression and upper-body action.
- **4 Fullbody**: Entire character visible. Focus on silhouette, pose dynamics, and full-body interaction with environment.
- **4 Dynamic**: High kinetic energy, motion blur, mid-action. Must imply rapid movement.
- **4 Cinematic**: Wide or dramatic angle. Strong composition, depth, and environmental context while keeping the character as the focal point.

**Category-Specific Constraints:**
- **Closeup**: Avoid generic "looking at viewer." Require a specific trigger (e.g., dust in eye, sudden noise, adjusting accessory).
- **Cinematic**: Avoid "standing in ruins" or "contemplating landscape." The environment must interact with the character (wind, debris, light shift) or reflect their immediate action.

---

## Batch-Level Diversity Enforcement

To prevent mechanical repetition across a batch of 20 premises, apply these hard limits:

### 1. Hook Family Limit
- **Max 2 per Hook Family**: No more than two premises in a single batch can share the same primary interaction type (e.g., "climbing/pulling up," "wind-blown hair adjustment," "catching falling object").
- *Example*: If `b01_cinematic` uses "pulling up on ledge," no other cinematic or medium shot may use "pulling up." Use "hanging," "swinging," or "descending" instead.

### 2. Environmental Force Limit
- **Max 3 per Batch for Passive Forces**: No more than three premises can rely solely on passive environmental forces (wind, rain, snow) as the primary causal agent without a secondary physical prop interaction.
- *Correction*: If using wind, pair it with a specific object (e.g., "wind pushes a loose sheet against her face" rather than just "hair blowing in wind").

### 3. Location Diversity
- **Max 2 per Location Type**: No more than two premises can share the same broad location type (e.g., "Industrial Interior," "Forest," "Rooftop").
- *Requirement*: Ensure at least 5 distinct location types across the batch of 20.

### 4. Action Verb Limit
- **Max 4 per Primary Verb**: No more than four premises in a batch should use the same primary action verb (e.g., "standing," "running," "looking"). Vary with synonyms or different mechanics (e.g., "bracing" instead of "standing," "vaulting" instead of "jumping").

### 5. Emotional Register Diversity
- **Max 3 per Emotion**: No more than three premises should share the same primary emotional register (e.g., "Stoic/Determined," "Playful/Teasing," "Strained/Painful"). Ensure a mix of at least 4 distinct emotional tones across the batch.

---

## Hard Anti-Pattern Rules

Reject any premise that matches these patterns:

1. **The Contemplative Statue**: Character standing still, looking into distance or at camera, with no visible cause for their pose.
2. **The Atmospheric Mood Piece**: Rain, fog, or sunset is the main subject; character is a passive silhouette in the background.
3. **The Generic Combat Pose**: Sword raised, ready to strike, with no specific enemy or threat visible/inferable.
4. **The Industrial Loop**: Repeated use of pipes, gears, and turbines without distinct narrative function. If using industrial settings, ensure each has a unique mechanical failure or interaction.
5. **The Climbing Repetition**: More than one premise in the batch featuring "pulling oneself up" or "climbing vertical structure."
6. **The Wind-Only Hook**: Hair and clothes blowing due to wind without any other physical consequence (e.g., revealing an item, disrupting balance).

---

## Micro-Story & Animation Potential

Every premise must function as a frame from a larger moment. It should suggest:
1. **Before**: What triggered this? (Visible cause)
2. **Now**: What is the character doing/reacting? (Active verb + physical detail)
3. **After**: What happens next? (Implied consequence or continuation)

**Animation Potential Check:**
- Can this become a 5–10 second video clip without inventing new actions?
- Is there implied secondary motion (hair, fabric, debris, dust)?
- Does the pose suggest a clear direction of force or momentum?

If the answer is no, rewrite to add a specific physical interaction or consequence.

---

## Final Premise Checklist

Before accepting a premise, verify:

### Character & Identity
- [ ] Is the character recognizable through silhouette and key traits?
- [ ] Does the premise respect their identity without factual drift (e.g., blindfold consistency)?
- [ ] Does the personality feel appropriate to the situation?

### Visual Appeal & Composition
- [ ] Is the silhouette strong and readable?
- [ ] Is body appeal integrated into the pose/action (not just static)?
- [ ] Does the composition lead the eye to the character’s face or key action point?
- [ ] Is the visual hook specific, not generic?

### Causality & Story
- [ ] **Cause:** What specific event triggered this moment? (Must be visible/inferable).
- [ ] **Reaction:** How is the character physically responding?
- [ ] **Consequence:** Is there a secondary visual effect (clothing shift, object movement)?
- [ ] Would the viewer ask "What happens next?"

### Diversity & Repetition Control
- [ ] Does this premise violate the **"Max 2 per Hook Family"** rule in the current batch?
- [ ] Have I repeated the primary action verb more than **4** times in this batch?
- [ ] Is the location distinct from previous premises (max 2 per type)?
- [ ] If using "balancing," "dodging," or "standing," have I hit the limit for that specific mechanic/category?

### Animation & Motion
- [ ] Can this become a short video clip without inventing new actions?
- [ ] Is there implied movement (hair, cloth, debris)?
- [ ] Does the pose suggest a clear direction of force or motion?

---

## Quality Standard

A strong premise should feel like:

**Character + Appeal + Personality + Moment + Future Motion**

Not merely:

**Character + Pretty Image.**
