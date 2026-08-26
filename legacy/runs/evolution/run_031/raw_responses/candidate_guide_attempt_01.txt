# Viral Premise Guide v3.3 (Candidate) — Cycle 031

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip, or a weight shift.
- **Invalid/Vague Causes:** "The atmosphere," "a feeling of dread," "invisible shockwave" (unless visualized by dust/debris displacement), generic "action."

If the cause is not visible in the frame or immediately inferable from the character's physical reaction, the premise fails.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face and hairstyle (including specific accessories like blindfolds).
- Iconic clothing design and silhouette.
- Personality flavor (e.g., 2B’s stoic composure masking internal tension).
- Characteristic visual traits (proportions, posture habits).

Do not replace the character with a generic attractive person. The goal is:
> "An attractive and interesting version of *this specific* character."

Not:
> "A random attractive character using the same aesthetic."

**Factual Identity Safeguard:**
Unless explicitly stated in the local character profile, do not invent factual elements (e.g., scars, tattoos, non-canonical weapons, specific hair colors) that contradict known canon or the provided profile. If unsure, stick to silhouette and posture rather than adding new visual data.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. It is one of the primary reasons a viewer stops scrolling. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and attractive proportions.
- Elegant body language and confident poses.
- Expressive reactions tied to physical sensation.
- Appealing clothing design (fit, tension, fabric behavior).
- Strong composition that guides the eye to the character’s face or key action point.

However: **Visual appeal should create interest, not replace the premise.**

The ideal formula is:
> Attractive Character + Interesting Moment

Not:
> Attractive Character Only.

### Body Appeal & Integration
Body emphasis is desirable but must be integrated into the physics of the moment. Prominent features (bust, hips, thighs) contribute to the visual hook when coherent with the action.

Useful visual elements include:
- Clothing tension caused by movement (stretching fabric, shifting straps).
- Weight shifts that define waist and hip curves.
- Torso twists or leans that create dynamic silhouettes.
- Strategic coverage reveals caused by motion (e.g., hem lifting during a leap, sleeve flaring on impact).

Body language should feel intentional and reactive. A pose should communicate:
- Confidence under pressure.
- Controlled embarrassment or surprise.
- Physical effort or balance maintenance.
- Playful defiance or elegant struggle.

**Rule:** If the body is emphasized, it must be *doing* something (balancing, stretching, bracing against force). Do not use static "pin-up" poses unless triggered by a specific causal event.

---

## Hard Anti-Pattern Rules (Cycle 031 Corrections)

Based on Cycle 030 failures, the following patterns are **strictly prohibited** or heavily restricted:

### 1. No Static Bracing (Cinematic & Fullbody)
In `cinematic` and `fullbody` categories, "standing still" is a failure unless accompanied by a **secondary active movement**.
- *Bad:* Standing on a ledge, looking calm.
- *Good:* Standing on a ledge, but one hand is actively gripping a crumbling edge while the other arm swings to counterbalance a sudden shift in weight.

### 2. No Generic Locomotion (Dynamic)
Walking or stepping is not enough for `dynamic`. The movement must have **narrative stake**.
- *Bad:* Walking through a hallway.
- *Good:* Sprinting low under a swinging pipe, hair whipping back from the speed, expression focused on the gap ahead.

### 3. No Invisible Causes
Every motion must have a visible trigger or physical consequence.
- *Bad:* Hair blowing in an "invisible wind."
- *Good:* Hair blowing because she is moving rapidly past an open vent, with dust particles visible in the air stream.

### 4. Direct Gaze Limitation
Direct eye contact with the camera lens should be used sparingly (max **1 per batch**) and only if accompanied by a specific physical reaction (e.g., catching her own reflection, reacting to the viewer as an intruder). Do not use "looking at camera" as a substitute for interaction.

### 5. No Atmospheric Contemplation
Avoid using rain, fog, or sunsets as the *primary* hook. If weather is present, it must interact physically with the character (e.g., shaking out water from hair after a dive, shielding eyes from sudden bright light).

---

## Category-Specific Rules

To prevent category drift and repetition, enforce these structural rules:

### Closeup
- **Focus:** Face, upper torso, or hands.
- **Requirement:** Must show a micro-expression tied to a physical sensation (heat, cold, pain, effort) or a small-scale interaction (adjusting gear, wiping sweat).
- **Anti-Pattern:** Generic "pretty face" with no context.

### Medium
- **Focus:** Waist-up or three-quarter shot.
- **Requirement:** Must show body mechanics in reaction to an environment (leaning, twisting, bracing).
- **Anti-Pattern:** Static portrait pose with background blur.

### Fullbody
- **Focus:** Entire silhouette and relationship to space.
- **Requirement:** Must demonstrate weight distribution or balance challenge. The character must be *interacting* with the ground/environment (knees bent, feet planted against force).
- **Anti-Pattern:** Standing straight with arms at sides ("T-pose" variant).

### Dynamic
- **Focus:** Motion blur, speed lines, or extreme angles.
- **Requirement:** Must show a distinct verb of motion (dodging, leaping, spinning, diving) that is *different* from other dynamic premises in the batch.
- **Anti-Pattern:** Repetitive mid-air tucks or generic running poses.

### Cinematic
- **Focus:** Composition, scale, and mood amplified by character action.
- **Requirement:** The environment provides scale/contrast, but the character must be *active* within it (e.g., silhouetted against a gear, but hand is gripping a railing; standing in ruins, but actively scanning with a weapon raised).
- **Anti-Pattern:** Character as a static statue in a beautiful landscape.

---

## Batch-Level Diversity Enforcement

To ensure variety across the 20-premise batch, apply these quantitative limits:

1. **Max 2 per Hook Family:** No more than two premises can share the same primary visual hook (e.g., "wind-blown hair," "outfit adjustment," "mirror reflection").
2. **Verb Diversity:** The primary action verb (grabbing, dodging, adjusting, leaping) must not appear more than 4 times in the entire batch.
3. **Location Rotation:** Ensure at least 5 distinct environmental contexts are represented across the batch (e.g., industrial interior, outdoor ruin, water/bath, high altitude, enclosed space).
4. **Emotional Range:** The batch must include a mix of emotions: at least one stoic/controlled, one surprised/alarm, one playful/mischievous, and one intense/focused.

---

## Micro-Story & Animation Potential

Every premise should function as a "frame from a larger moment."
- **Before:** What triggered this? (Visible cause).
- **Now:** What is the character doing/reacting? (Active pose).
- **Next:** Where does this lead? (Implied momentum).

**Animation Test:** Can this image become a 5–10 second video clip without inventing a new action?
- *Yes:* The steam is rising, she is leaning back from the heat. The video shows her stepping away as the steam clears.
- *No:* She is standing still in the rain. To animate it, you would need to add walking or emotion shifts that aren't implied by the pose.

---

## Acceptance Checklist

Before generating prompts for a batch, verify each premise against this checklist:

### Character & Identity
- [ ] Is the character recognizable through specific traits (hair, eyes, outfit)?
- [ ] Does the personality match the reaction? (Stoic = controlled; Playful = expressive).
- [ ] Are there any invented factual elements not in the local profile?

### Visual Appeal
- [ ] Is the composition leading the eye to the character’s face or key action point?
- [ ] Is body appeal integrated into the pose/action (not just static)?
- [ ] Is the visual hook specific and readable at a glance?
- [ ] **Attraction-Forward Check:** Does this premise prioritize the character’s visual presence over the environment?

### Causality & Story
- [ ] **Cause:** What specific event triggered this moment? (Must be visible/inferable).
- [ ] **Reaction:** How is the character physically responding actively?
- [ ] **Consequence:** Is there a secondary visual effect (clothing shift, object movement, hair displacement)?
- [ ] Would the viewer ask "What happens next?"

### Diversity & Repetition Control
- [ ] Does this premise violate the **"Max 2 per Hook Family"** rule in the current batch?
- [ ] Have I repeated the primary action verb more than **4** times in this batch?
- [ ] Is the location distinct from the previous 3 premises?

### Category Compliance
- [ ] **Closeup:** Micro-expression + physical sensation?
- [ ] **Medium:** Body mechanics reacting to environment?
- [ ] **Fullbody:** Weight distribution/balance challenge visible?
- [ ] **Dynamic:** Distinct motion verb (not repeated from other dynamics)?
- [ ] **Cinematic:** Character active within scale/contrast?

### Final Quality Gate
- [ ] No static bracing without secondary movement.
- [ ] No invisible causes.
- [ ] No generic locomotion without stake.
- [ ] Direct gaze used max 1 time in batch (if at all).

If any box is unchecked, rewrite the premise to add specificity, causality, or active motion.
