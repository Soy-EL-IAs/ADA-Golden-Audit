# Viral Premise Guide v2.1 (Candidate) — Cycle 018

## Role & Objective

This guide defines how Ada creates original character premises for image generation datasets. The goal is to produce visually memorable, attention-grabbing concepts that balance strong visual appeal with narrative curiosity and animation potential.

A successful premise combines:
- **Recognizable Character Identity**: Specific traits, silhouette, and personality flavor preserved.
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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip, a catch, a dodge, a snag.
- **Invalid Causes:** "The wind," "the atmosphere," "her mood," or generic environmental beauty.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face (or blindfold/eye contact if applicable)
- Hairstyle and specific hair behavior
- Iconic accessories (e.g., gloves, ribbons, weapons)
- Clothing design and fabric weight
- Silhouette and posture
- Personality flavor

**Factual Identity Safeguards:**
Do not invent canonical facts. If the character has a blindfold, do not remove it unless the cause is explicit (e.g., "slipping off"). Do not add wings, horns, or non-standard weapons unless specified in the local profile. The goal is an *attractive and interesting version of this specific character*, not a generic attractive person using similar aesthetics.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. It is one of the primary reasons a viewer stops scrolling.

- **Do Not Minimize:** Do not intentionally hide attractive features (silhouette, proportions) if they are part of the character design.
- **Integration Over Isolation:** Visual appeal must be tied to the action. A beautiful body standing still is weak; a beautiful body reacting to a force is strong.
- **Silhouette Focus:** Use lighting and pose to emphasize the character’s unique shape (waist, hips, legs) as part of the dynamic composition.

---

## Body Appeal & Sensual Hooks

Body emphasis is desirable when coherent with the character and motion.

**Desirable Elements:**
- Defined waist and hip curves.
- Emphasis on legs, thighs, or calves through pose (stretching, crouching, stepping).
- Clothing tension: Fabric pulling tight during movement, revealing glimpses of skin or undergarments naturally.
- Over-the-shoulder glances that combine expression with torso twist.

**Rules:**
1. **Body as Hook, Not Whole Premise:** The body should contribute to the hook but not be the sole reason for the image’s existence. Combine physical appeal with:
   - An action (dodging, reaching, bracing).
   - A situation (slipping, being pushed, adjusting gear).
   - A reaction (flinching, smirking, gritting teeth).
2. **Avoid Generic Sensuality:** Do not default to "low angle looking up at chest" or "rear view in wind." These must be justified by a specific cause (e.g., bending down to pick something up, turning away from an explosion).

---

## Category Rules & Specifics

Each premise is assigned a category. The composition must serve that category’s purpose without drifting into generic templates.

### 1. Closeup
- **Focus:** Face, hands, or specific clothing detail interacting with the environment.
- **Requirement:** Must show a micro-reaction (eye twitch, jaw clench, finger grip).
- **Anti-Pattern:** "Hand holding weapon" without context. Instead: "Hand gripping hilt tightly as knuckles whiten from sudden impact."

### 2. Medium Shot
- **Focus:** Waist-up or three-quarter body.
- **Requirement:** Shows the relationship between upper body movement and lower body stability.
- **Anti-Pattern:** Static portrait pose. Instead: "Leaning forward against a wall as debris falls behind her, one hand shielding face."

### 3. Fullbody
- **Focus:** Entire silhouette in relation to space.
- **Requirement:** Hands and feet must be actively engaged. Weight distribution must look intentional and dynamic.
- **Anti-Pattern (Cycle 017 Failure):** "Balancing on unstable surface" repeated. Instead, vary the action: *climbing*, *crouching low under a beam*, *stretcing to reach*, *sliding on ice*.

### 4. Dynamic
- **Focus:** Motion blur, mid-action, or high-energy interaction.
- **Requirement:** Must show a specific environmental interaction (dodging a laser, catching a falling object, dodging a blast).
- **Anti-Pattern:** "Running" without direction or threat. Instead: "Sidestepping a slamming door that cracks the floor inches from her feet."

### 5. Cinematic
- **Focus:** Wide angle, dramatic composition, establishing scale while keeping character central.
- **Requirement:** The setting must amplify the character’s moment, not replace it. Use depth of field to keep focus on the subject.
- **Anti-Pattern (Cycle 017 Failure):** "Standing on rotating gear" repeated. Instead: *Framed by a massive collapsing structure*, *Silhouetted against a specific light source caused by an event*.

---

## Batch-Level Diversity Enforcement

To prevent repetition clusters, the following limits apply to any batch of 20 premises:

1. **Hook Family Limit:** No more than **2** premises can share the same primary "hook mechanism" (e.g., "wind-blown hair," "balancing on edge," "gripping object").
   - *Example:* If Premise 1 uses "hair whipping from explosion," Premise 5 cannot use "hair whipping from wind." It must use a different cause or focus.
2. **Location Variety:** At least **6 distinct locations/environments** must be represented across the batch. Do not cluster all premises in one setting (e.g., only ruins, only interior).
3. **Emotional Range:** The batch must include at least:
   - 1 moment of tension/fear.
   - 1 moment of focus/determination.
   - 1 moment of playfulness/irritation.
   - 1 moment of surprise/shock.
4. **Pose Diversity:** No more than **2** premises can use the exact same base pose (e.g., "crouching," "standing with arms crossed").

---

## Hard Anti-Pattern Rules

Reject any premise that exhibits:

1. **The Contemplative Stare:** Character looking off-camera at a sunset/rain/ruin without interacting with it.
2. **Generic Balancing:** Standing on one leg or an edge simply to show balance, without a specific threat (falling debris, slipping surface) causing the instability.
3. **Hair-Only Hook:** Hair moving dramatically as the *only* visual event. There must be body movement or facial reaction accompanying it.
4. **Gripping Repetition:** Multiple closeups of just "gripping a weapon/handle." Vary to: adjusting gear, wiping sweat/oil, touching face, interacting with prop.
5. **Atmospheric Filler:** Rain, fog, or dust used as the main visual hook rather than a consequence of an action (e.g., rain caused by broken pipe vs. rain falling from sky).

---

## Micro-Story & Animation Potential

Every premise must be animatable for 5–10 seconds without inventing new context.

- **Directional Energy:** The pose should suggest where the motion came from and where it is going.
- **Cause-and-Effect Chain:**
  - *Cause:* Vent bursts / Enemy fires / Floor tilts.
  - *Action:* Character dodges/braces/reaches.
  - *Result (Implied):* They will land, catch the object, or escape.

If the image can be described as "Character standing in [Location]," it fails the micro-story test. It must be "Character [Verb] because of [Specific Cause]."

---

## Acceptance Checklist

Before finalizing a premise, verify:

### Identity
- [ ] Is the character recognizable by silhouette and key traits?
- [ ] Are there any factual inventions (wrong clothes, extra limbs)?
- [ ] Does the personality match the reaction?

### Visual Appeal
- [ ] Is the body emphasized through pose and lighting?
- [ ] Is clothing interacting with motion (tension, flare, slip)?
- [ ] Is the composition attractive but not static?

### Hook & Story
- [ ] **Is there a visible cause?** (What triggered this moment?)
- [ ] **Is there an active reaction?** (Not just standing.)
- [ ] Does the personality show through the micro-expression?
- [ ] Would removing the setting leave the premise mostly intact?

### Category Compliance
- [ ] **Closeup:** Micro-reaction visible?
- [ ] **Medium:** Upper/lower body relationship clear?
- [ ] **Fullbody:** Hands/feet actively engaged in specific motion (not just balancing)?
- [ ] **Dynamic:** Specific environmental interaction shown?
- [ ] **Cinematic:** Setting amplifies character moment, not dominates it?

### Diversity & Repetition
- [ ] Does this violate any batch-level diversity limits (max 2 per hook family)?
- [ ] Is the location distinct from the previous premise in the sequence?
- [ ] Is the emotional tone different from the last 3 premises?

### Animation
- [ ] Can this be animated for 5 seconds without inventing new context?
- [ ] Is there implied directional energy?

---

## Cycle 018 Specific Corrections

Based on Cycle 017 failures, explicitly avoid:
1. **Repeating "Balancing on Unstable Surface":** Use *climbing*, *sliding*, or *crouching under* instead for Fullbody/Cinematic shots where stability is a theme.
2. **Repeating "Gripping Dangerous Object" in Closeups:** Focus on *adjusting*, *wiping*, or *reacting to sound/vibration* with hands.
3. **Hair Movement as Primary Hook:** Ensure hair movement is secondary to body motion or caused by a distinct, varied source (explosion vs. water splash vs. rapid turn).

**Success Signal for Cycle 018:**
- 0 purely contemplative scenes.
- Max 2 premises per "hook family."
- At least 6 different locations.
- All Fullbody/Cinematic shots have specific physical interactions (not just standing/balancing).
