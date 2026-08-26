# Viral Premise Guide v3.5 (Candidate) — Cycle 033

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip hazard, or a direct impact.
- **Invalid Causes:** "Vibes," "atmosphere," generic tension, or unexplained postures.

---

## Character Identity & Factual Safeguards

Every premise must preserve the identity of the original character (e.g., 2B from *NieR:Automata*). The character should remain recognizable through:
- Face structure and blindfold placement.
- Hairstyle (bob cut, long braids if applicable to variant).
- Iconic accessories (choker, gloves, garter straps).
- Clothing design (white dress, black tights/stockings, puffy sleeves).
- Silhouette and posture language (stoic, elegant, precise).

**Factual Identity Safeguards:**
1. **No Canon Inventions**: Do not introduce weapons, gadgets, or clothing items not present in the local character profile unless specified as "prop interaction" (e.g., holding a wrench does not mean she *owns* it canonically; it is a situational prop).
2. **Silhouette Integrity**: The dress length and stocking height must remain consistent with the base model unless the premise explicitly involves tearing or shifting fabric due to force.
3. **Personality Alignment**: Reactions must match the character's core temperament. For 2B, this means maintaining composure even in chaos, showing subtle frustration rather than overt panic, and using precise, controlled movements rather than flailing.

---

## Visual Appeal & Body Language Philosophy

Visual attractiveness is an intentional component of the dataset. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

**Body As A Hook, Not The Entire Premise:**
The body should be part of the hook, not necessarily the entire premise. Body appeal works best when combined with:
- An action (reaching, twisting, bracing).
- A situation (slipping, falling, adjusting).
- A reaction (flinching, focusing, exhaling).

**Desired Visual Elements:**
- **Silhouette Emphasis**: Use lighting and pose to highlight the waist-to-hip ratio, leg length, or torso twist.
- **Fabric Physics**: Use clothing tension, hem flaring, sleeve puffing, or stocking stretching to imply force and motion. This adds visual appeal without replacing the story.
- **Intentional Poses**: Avoid generic "standing" poses. Every pose must communicate:
    - Confidence (weight shifted, chin up).
    - Tension (muscle engagement, tight grip).
    - Surprise (head tilt, eye widening).
    - Effort (strained arms, bent knees).

**Sensual Visual Hook Priority:**
The dataset should intentionally explore the character's visual appeal. Attractive body features, silhouette, and feminine presence are valid parts of the visual hook. Do not make characters visually neutral by default. However, sensuality must be attached to:
- Character emotion.
- Contextual action.
- Movement.

Avoid reducing every idea to "cleavage" or "rear view" without another visual idea (e.g., a falling object threatening her balance).

---

## Batch-Level Diversity Enforcement (Hard Rules)

To prevent the "repetition cluster" failures observed in Cycle 032, the following batch-level rules are **mandatory** for any set of 20 premises:

### 1. The "Max 2 per Hook Family" Rule
No more than **two** premises in a single batch may share the same core mechanical hook or interaction type.
*Examples of Hook Families:*
- *Catching/Falling Object*: Catching a wrench, catching a bolt, catching a tool. (Limit: 2)
- *Balancing/Stepping*: Stepping over crack, balancing on beam, stepping off ledge. (Limit: 2)
- *Wind/Air Disruption*: Hair blowing from vent, dress flaring from fan, debris flying. (Limit: 2)
- *Gripping/Holding On*: Holding a lift handle, gripping a railing, holding an extinguisher. (Limit: 2)

*If you need a third premise in this family, change the mechanic entirely (e.g., instead of catching, she is dodging; instead of balancing, she is vaulting).*

### 2. The "Distinct Verb" Rule for Dynamic Shots
In any batch, no single primary motion verb may be used more than **four times** across all categories.
*Example:* If you use "swing" in two dynamic shots and one full-body shot, the fourth use must be a different verb (e.g., "vault," "dive," "twist").

### 3. The "Location Distinction" Rule
No location type may appear more than **three times** in a batch.
*Example:* If you have three premises set in an industrial factory, the fourth must be in a different environment (e.g., office, rooftop, underground tunnel).

### 4. The "Emotional State" Spread
Across the batch, ensure at least **five distinct emotional states** are represented.
*Examples:* Stoic focus, subtle frustration, surprise, determination, playful smirk, controlled panic. Do not let 15/20 premises be "neutral/stoic."

---

## Category-Specific Rules

### Closeup (4 Premises)
- **Focus:** Micro-expression + physical sensation.
- **Requirement:** Must show a specific facial reaction to an immediate stimulus (e.g., eye twitch from dust, exhale from cold, brow furrow from strain).
- **Prohibition:** No static "looking at camera" shots unless the cause is visible in the reflection or immediate foreground.

### Medium (4 Premises)
- **Focus:** Body mechanics reacting to environment.
- **Requirement:** Must show upper body interaction with a specific object or force (e.g., pulling a lever, bracing against wind, adjusting gear).
- **Prohibition:** No generic "holding a weapon" poses without a visible reason (aiming at something off-screen is okay; posing with it is not).

### Fullbody (4 Premises)
- **Focus:** Weight distribution and balance challenge.
- **Requirement:** Must show the character's stance in response to a physical obstacle or force. The cause of the imbalance must be visible (e.g., a hole, a slope, a push).
- **Prohibition:** No "standing confidently" without a secondary action or consequence. Avoid repeating the same balance mechanic (e.g., one-foot on ledge) more than twice in the batch.

### Dynamic (4 Premises)
- **Focus:** Distinct motion verbs and kinetic energy.
- **Requirement:** Must imply high-speed movement. Use verbs like *vault, dive, somersault, swing, leap, dash*.
- **Prohibition:** No slow-motion "floating" without a clear force (gravity release, jump apex). Each dynamic shot must use a unique motion verb not repeated in other dynamics.

### Cinematic (4 Premises)
- **Focus:** Character active within scale/contrast.
- **Requirement:** Use camera angles (low angle, wide shot) to emphasize the character's agency against the environment. The character must be doing something specific (e.g., reaching for a handle, dodging debris), not just standing in a large space.
- **Prohibition:** No "silhouette against sunset" shots unless there is an active interaction with light/shadow caused by movement.

---

## Hard Anti-Pattern Rules

The following patterns are **banned** from appearing as the primary hook of any premise:

1. **The Contemplative Atmospheric Shot**: Rain, fog, or wind used solely for mood without a physical interaction (e.g., "2B standing in rain" is weak; "2B wiping rain from her blindfold to see a falling debris" is strong).
2. **The Generic Gameplay Pose**: Standing in a combat stance with no visible enemy or threat. The threat must be implied by the environment (sparks, shadows, movement) or the character's focus.
3. **The Passive Balancer**: Stepping over a crack or standing on one foot without a reason (e.g., "to reach something" or "because the other side is broken").
4. **The Duplicate Hazard**: Using the same environmental hazard (e.g., rotating fan, falling pipe) for more than two premises in a batch.
5. **The Abstract Cause**: "Electrical surge," "mystical energy," or "tension" without a visual proxy (sparks, wires, sweat, trembling).

---

## Acceptance Checklist

Before accepting a premise into the final batch, verify:

### Character & Identity
- [ ] Is the character recognizable via silhouette and key accessories?
- [ ] Does the personality match the core temperament (stoic/playful/etc.)?
- [ ] Are there any factual inventions not supported by the local profile?

### Causality & Micro-Story
- [ ] **Cause:** What is the visible trigger for this action/reaction?
- [ ] **Reaction:** How is the character physically responding actively?
- [ ] **Consequence:** Is there a secondary visual effect (clothing shift, object movement)?
- [ ] Would the viewer ask "What happens next?"

### Visual Appeal & Hook
- [ ] Is the body language intentional and expressive?
- [ ] Is fabric physics used to enhance motion/appeal?
- [ ] Is the hook centered on the character's interaction, not just the setting?

### Diversity & Repetition Control (Batch Level)
- [ ] Does this premise violate the **"Max 2 per Hook Family"** rule in the current batch?
- [ ] Have I repeated the primary action verb more than **4** times in this batch?
- [ ] Is the location distinct from the previous 3 premises?
- [ ] Is the emotional state different from at least 5 other premises in the batch?

### Category Compliance
- [ ] **Closeup:** Micro-expression + physical sensation present?
- [ ] **Medium:** Body mechanics reacting to environment (not just bracing)?
- [ ] **Fullbody:** Weight distribution/balance challenge visible with specific cause?
- [ ] **Dynamic:** Distinct motion verb used (not repeated from other dynamics)?
- [ ] **Cinematic:** Character active within scale/contrast (not just silhouette)?

### Final Quality Gate
- [ ] No static bracing without secondary movement.
- [ ] No invisible causes.
- [ ] No generic locomotion without stake.
- [ ] Direct gaze used max 1 time in batch (if at all).

If any box is unchecked, rewrite the premise to add specificity, causality, or active motion.
