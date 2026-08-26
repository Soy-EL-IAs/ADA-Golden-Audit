# Viral Premise Guide v2.3 (Candidate) — Cycle 020

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip, or a deliberate action with immediate consequence.
- **Invalid Causes:** "Mood," "thinking," "waiting," "standing guard" without a visible threat or event.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face (or blindfold/eyes if applicable)
- Hairstyle and hair physics
- Iconic accessories (e.g., blindfold, gloves, boots)
- Clothing design and fit
- Silhouette and posture habits
- Personality flavor

Do not replace the character with a generic attractive person. The goal is: **"an attractive and interesting version of this character"**, not "a random attractive character using the same aesthetic."

**Factual Identity Safeguards:**
- Do not introduce canon-inaccurate accessories unless specified in the local profile.
- Do not alter hair color or length significantly without cause (e.g., wet hair, tied up for action).
- Respect the character's typical combat stance and elegance level.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. It is one of the primary reasons a viewer stops scrolling. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and proportions
- Elegant body language and confident poses
- Expressive reactions and facial micro-expressions
- Appealing clothing design (fitted, flowing, or torn)
- Strong composition and lighting

However: **visual appeal should create interest, not replace the premise.**

The ideal formula is: **attractive character + interesting moment**, not just "attractive character only."

---

## Body Appeal & Sensual Hooks

Body emphasis is desirable when coherent with the action. Prominent breasts, hips, buttocks, thighs, legs, and a defined waist may intentionally contribute to the visual hook. A voluptuous yet athletic silhouette is generally desirable when appropriate.

Useful visual elements include:
- **Clothing Tension:** Fabric stretching across curves during movement (e.g., dress hem lifting, sleeves tightening).
- **Silhouette Emphasis:** Poses that highlight waist-to-hip ratio or leg length (crouching, arching back, high kick).
- **Strategic Reveals:** Natural exposure caused by action (e.g., skirt flaring from wind, top unzipping during exertion) rather than static posing.

**Body As A Hook, Not The Entire Premise:**
The body should be part of the hook, not necessarily the entire premise. Body appeal works best when combined with:
- An action or reaction
- A visual joke or contrast
- Environmental interaction (wind, water, debris)
- Cause and effect

Avoid reducing every idea to cleavage or rear views without another visual idea. The purpose is to make sensuality memorable by attaching it to character, emotion, context, and movement.

---

## Category Rules & Specificity

To ensure variety and prevent template fatigue, each premise must be assigned a specific category with distinct requirements:

### 1. Closeup
- **Focus:** Face, hands, or upper torso detail.
- **Requirement:** Must show a micro-reaction (flinch, squint, grip tightening) caused by an immediate threat or sensation.
- **Anti-Pattern:** Hand shielding face as a default; generic "looking at camera."

### 2. Medium
- **Focus:** Waist-up to full torso.
- **Requirement:** Must show the character interacting with a prop, weapon, or environmental force that affects their posture or clothing.
- **Anti-Pattern:** Standing still with hands on hips; static combat stance without motion blur or impact.

### 3. Fullbody
- **Focus:** Entire silhouette from head to toe.
- **Requirement:** Must demonstrate full-body weight distribution and movement (running, jumping, sliding, crouching). The pose must imply momentum or balance correction.
- **Anti-Pattern:** "Model walk" stance; standing on one leg without a reason (like balancing on a beam); generic hero pose with sword raised but no target.

### 4. Dynamic
- **Focus:** High-energy action moment.
- **Requirement:** Must capture mid-action (mid-air, mid-swing, mid-dodge). Motion blur or particle effects are encouraged to convey speed.
- **Anti-Pattern:** "Action pose" that looks like a statue; jumping but not showing the trajectory of movement.

### 5. Cinematic
- **Focus:** Wide shot establishing context and character presence.
- **Requirement:** Must show the relationship between the character and their environment. The character must be small in frame but visually dominant due to lighting or action.
- **Anti-Pattern:** Character standing alone in a vast empty landscape (wallpaper energy); no visible interaction with the surroundings.

---

## Batch-Level Diversity Enforcement

To prevent repetition across a batch of 20 premises, enforce the following hard limits:

1. **Hook Family Limit:** No more than **2** premises may share the same primary visual hook type (e.g., "wind-blown hair," "steam burst," "blade reflection").
2. **Emotional Tone Variety:** At least **4 distinct emotional tones** must be present in any batch of 10 (e.g., focused, surprised, angry, playful, exhausted).
3. **Location Rotation:** No more than **3** premises may share the same specific location type (e.g., "rooftop," "industrial interior"). Locations should vary between indoor/outdoor, natural/artificial, and clean/dirty.
4. **Action Verb Diversity:** Use at least **8 different primary action verbs** across a batch of 20 (e.g., dodging, gripping, sliding, spinning, bracing, reaching, falling, climbing).
5. **Viewpoint Variation:** Ensure a mix of low-angle, high-angle, eye-level, and over-the-shoulder shots. No more than **4** premises from the same camera angle type in a batch of 20.

---

## Hard Anti-Pattern Rules

Reject any premise that falls into these categories:

1. **The "Contemplative Statue":** Character standing still, looking into distance or at camera, with no visible cause for their presence or posture.
2. **The "Generic Hazard":** Using steam, sparks, or debris as a filler without a specific source (e.g., "steam from nowhere" vs. "steam jet from cracked pipe").
3. **The "Locomotion Filler":** Walking or running across an empty space without a destination or threat.
4. **The "Atmospheric Mood Piece":** Rain, fog, or sunset used as the main subject rather than the character's interaction with them.
5. **The "Repetitive Shield":** Hand near face/head to shield from light/debris in more than 2 closeups per batch.
6. **The "Hero Pose":** Sword raised high, chest out, standing on a rock/ruin without an immediate enemy or consequence.

---

## Micro-Story & Animation Potential

Every premise must function as a "frame from a larger moment." It should answer: *What is happening right now?* and imply: *What happens in the next 5 seconds?*

**Animation Test:**
Can this image be animated into a 5–10 second clip without inventing new objects or characters?
- **Yes:** Character dodges a falling beam (clip shows the dodge).
- **No:** Character standing on a cliff looking at mountains (clip requires them to start moving for no reason).

**Causal Chain Requirement:**
The premise must contain:
1. **Trigger:** A visible event or force.
2. **Reaction:** The character's physical response.
3. **Consequence/State Change:** Visible effect on clothing, hair, or position.

---

## Acceptance Checklist

Before accepting a premise, verify all boxes are checked:

### Identity & Factual Accuracy
- [ ] Is the character recognizable via silhouette and accessories?
- [ ] Are there no factual errors (wrong hair color, non-existent item)?
- [ ] Does the personality match the reaction (e.g., 2B remains composed even when flustered)?

### Visual Appeal & Hook
- [ ] Is the visual appeal integrated into the action (not just a static pose)?
- [ ] Is there a clear "scroll-stopping" element (tension, contrast, surprise)?
- [ ] Does the body language communicate emotion or intent?

### Micro-Story & Causality
- [ ] Is there a visible cause for the character's action?
- [ ] Is the reaction active rather than passive?
- [ ] Can the viewer infer what happened 1 second before this frame?

### Category Compliance
- [ ] Does it fit the assigned category (Closeup, Medium, Fullbody, Dynamic, Cinematic) rules?
- [ ] For **Fullbody**: Is there clear weight distribution and momentum?
- [ ] For **Cinematic**: Is the environment interacting with the character?

### Diversity & Repetition
- [ ] Does this violate any batch-level diversity limits (max 2 per hook family)?
- [ ] Is the location distinct from the previous premise in the sequence?
- [ ] Is the emotional tone different from the last 3 premises?
- [ ] Is the action verb unique or sufficiently varied?

### Animation Potential
- [ ] Can this become a short video clip (5–10s) without adding new elements?
- [ ] Is there implied directional energy or momentum?

---

## Cycle 020 Specific Corrections

Based on Cycle 019 failures, explicitly avoid:

1. **Static Cinematic Stances:** Replace "peering down/looking into abyss" with active interactions like *clinging to a crumbling edge*, *sliding across a wet surface*, or *bracing against a sudden impact*.
2. **Medium Shot Bracing Repetition:** Avoid generic "shielding from wind/debris." Instead, use actions like *gripping a moving cable*, *twisting away from a projectile*, or *adjusting equipment under pressure*.
3. **Fullbody Locomotion Filler:** Ensure every full-body movement has a narrative purpose (escape, pursuit, discovery). "Stepping over a slab" is weak; "sprinting past a collapsing pillar to reach a door" is strong.
4. **Closeup Variety:** Ensure at least 2 closeups involve interactions with *weapons
