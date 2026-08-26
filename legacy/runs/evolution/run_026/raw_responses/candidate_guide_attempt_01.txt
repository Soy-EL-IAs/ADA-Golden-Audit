# Viral Premise Guide v2.8 (Candidate) — Cycle 026

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip, a mechanical failure.
- **Invalid/Vague Causes:** "Wind," "shadow," "mood," "atmosphere," "presence of danger" (unless the source is visible).

---

## Character Identity Priority

Every premise must preserve the identity of the original character based on the local profile provided. The character should remain recognizable through:
- Face structure and expression style.
- Hairstyle and hair texture.
- Iconic accessories (e.g., blindfold, gloves, boots).
- Clothing design details (cuts, fabric, trim).
- Silhouette and proportion.

**Identity Safeguard Rule:** Do not introduce factual elements not present in the local profile (e.g., adding a weapon if the character is unarmed in this context, changing eye color, altering outfit structure) unless explicitly part of the "disruption" caused by the micro-story. The goal is *"an attractive and interesting version of this character,"* not a generic avatar wearing their clothes.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. It is one of the primary reasons a viewer stops scrolling.

- **Silhouette First:** The body shape must be readable from a distance.
- **Clothing as Secondary Skin:** Clothing should emphasize, not hide, the body’s form. Fitted fabrics, strategic cutouts, and tension points are encouraged.
- **Body Language:** Poses must communicate confidence, curiosity, playfulness, or intensity. Avoid neutral "standing" poses.

**The Appeal/Story Balance:**
Visual appeal creates interest; story creates retention. A premise with high appeal but zero story is a wallpaper. A premise with strong story but flat visual design is a screenshot. The ideal combines both: *attractive character + interesting moment.*

---

## Body As A Hook, Not The Entire Premise

Body emphasis is desirable and should be prominent when coherent with the character design (e.g., hips, thighs, waist definition, bust). However, body appeal works best when combined with:
- An action.
- A reaction to a force.
- Environmental interaction.
- Cause and effect.

**Anti-Pattern:** Do not reduce every idea to "cleavage" or "rear view" without another visual idea. The purpose is to make sensuality memorable by attaching it to character, emotion, context, movement, or story.

---

## Micro-Story & Causality

Every premise must contain a **visible causal chain**:
1.  **Trigger:** A specific event occurs (object falls, door closes, machine breaks).
2.  **Reaction:** The character physically responds (dodges, braces, reaches, adjusts).
3.  **Consequence:** A secondary visual effect happens (clothing shifts, debris moves, hair flies).

**Specificity Requirement:**
- Instead of "avoiding danger," use "sliding under a falling beam."
- Instead of "reacting to wind," use "holding her dress down as a vent bursts open."
- Instead of "looking at shadow," use "turning sharply toward a flickering emergency light."

---

## Category Rules & Diversity Enforcement

To prevent repetition, each batch must adhere to the following structural rules:

### 1. Category Definitions
- **Closeup:** Focus on face/upper body. Must show specific facial micro-expressions or accessory interactions (e.g., touching blindfold, hair covering eye).
- **Medium:** Focus on torso/waist-up or waist-down. Must show interaction with objects or clothing tension caused by movement.
- **Fullbody:** Entire character visible. Must show weight distribution, leg extension, or full-body balance dynamics.
- **Dynamic:** High kinetic energy. Implies fast motion (blur, stretch, impact). Must have a clear vector of force.
- **Cinematic:** Wide shot with environmental context. The environment must actively interact with the character (crushing, enclosing, illuminating), not just frame them.

### 2. Batch-Level Diversity Quotas (Hard Limits)
For any batch of 20 premises:
- **Max 2 per Hook Family:** Do not use the same core interaction mechanic more than twice.
    - *Example Families:* Catching/Bracing, Sliding/Dodging, Adjusting Clothing, Prying/Pulling, Reaching/Grabbing.
- **Min 3 Distinct Locations:** At least three different environmental settings must be present in the batch (e.g., industrial interior, outdoor overgrowth, mechanical chamber).
- **Max 1 Atmospheric Dominance:** No single atmospheric element (rain, fog, dust) can be the primary visual hook for more than 2 premises.

### 3. Action Verb Variation
Track the primary action verb across the batch. If a verb like "catch," "dodge," or "stand" appears in >4 premises, rewrite at least half of them to use distinct mechanics (e.g., "slide," "twist," "lean," "brace").

---

## Hard Anti-Pattern Rules

Reject any premise that matches the following:

1.  **The Contemplative Trap:** Character standing still, looking into distance or camera, with no physical interaction with objects or environment.
2.  **Vague Force:** Using "wind," "shadow," or "mood" as the sole cause of action without a visible source (vent, fan, light fixture).
3.  **Generic Combat:** Character in a fighting stance with no specific opponent or impact point visible.
4.  **Repeated Mechanics:** If two premises share the same core physical mechanic (e.g., both involve "mid-air rotation to avoid obstacle"), one must be rewritten.
5.  **Wallpaper Energy:** The environment is more detailed and interesting than the character’s action.

---

## Animation Potential Check

A premise has high animation potential if:
- It implies a clear direction of force (left-to-right, up-down).
- Secondary motion is evident (hair, cloth, debris).
- The pose is unstable or transitional (not a final resting state).
- A 5–10 second clip could be generated by simply resolving the cause and effect.

---

## Acceptance Checklist

Before accepting a premise for inclusion in the dataset, verify:

### Character & Identity
- [ ] Is the character recognizable via local profile traits?
- [ ] Are there no factual errors (wrong accessories, wrong hair)?
- [ ] Does the personality match the reaction?

### Visual Appeal
- [ ] Is the silhouette strong and readable?
- [ ] Is body appeal integrated into the pose/action?
- [ ] Does the composition lead the eye to the character’s face or key action point?

### Causality & Story
- [ ] **Cause:** What specific event triggered this moment? (Must be visible/inferable).
- [ ] **Reaction:** How is the character physically responding?
- [ ] **Consequence:** Is there a secondary visual effect (clothing shift, object movement)?
- [ ] Would the viewer ask "What happens next?"

### Diversity & Repetition Control
- [ ] Does this premise violate the **"Max 2 per Hook Family"** rule in the current batch?
- [ ] Have I repeated the primary action verb more than **4** times in this batch?
- [ ] Is the location distinct from previous premises in the sequence?
- [ ] If using "balancing" or "prying," have I hit the limit for that specific mechanic?

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
