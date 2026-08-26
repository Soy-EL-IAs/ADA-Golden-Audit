# Viral Premise Guide v3.6 (Candidate) — Cycle 034

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip event, or a direct impact.
- **Invalid Causes:** "Vibes," general atmosphere, "looking cool," or abstract emotional states without a physical anchor.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face (or lack thereof, e.g., blindfold)
- Hairstyle and hair accessories (e.g., hairband)
- Iconic accessories (gloves, choker, specific jewelry)
- Clothing design (dress cut, sleeve style, stocking length)
- Silhouette and posture

Do not replace the character with a generic attractive person. The goal is: **"an attractive and interesting version of this character"** — not "a random attractive character using the same aesthetic."

### Factual Identity Safeguards
Unless specified in the local profile, do not invent new canonical traits (e.g., tattoos, scars, specific weapon types not listed). If a weapon is present, it must be consistent with the character's known arsenal or a generic prop that does not contradict canon.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and proportions
- Elegant body language
- Confident or expressive poses
- Appealing clothing fit and tension
- Strong composition (rule of thirds, leading lines)

However: **Visual appeal should create interest, not replace the premise.**

The ideal formula is:
**Attractive Character + Interesting Moment**
*Not:*
**Attractive Character Only**

### Body Appeal Integration
Body emphasis is desirable but must be contextual. Prominent features (waist, hips, legs, bust) may contribute to the visual hook when coherent with the action.

Useful visual elements include:
- Torso twist or weight shift onto one leg
- Clothing tension from movement (sleeves flaring, hem lifting)
- Dynamic poses: crouching, stretching, bending naturally as part of an action
- Over-the-shoulder presentations that imply depth and proximity

Body language should communicate confidence, curiosity, playfulness, elegance, shyness, attitude, or emotion. Avoid static "pin-up" posing unless the pose itself is a reaction to a specific cause (e.g., catching balance).

---

## Micro-Story & Animation Potential

A premise must feel like a frame taken from a larger moment. It should imply:
1. **Before**: What triggered this?
2. **Now**: What is happening in this exact second?
3. **After**: What will happen next?

### Animation Seed Test
Can this image be animated into a 5–10 second clip without inventing new actions?
- *Yes:* If the pose implies immediate follow-through (e.g., mid-dive, mid-reach, mid-turn).
- *No:* If the pose is static and requires a cut to change context.

Prefer **active verbs** over passive states:
- *Active:* Vaulting, catching, bracing against impact, adjusting, reaching, pivoting.
- *Passive (Avoid):* Standing, waiting, observing, existing.

---

## Batch-Level Diversity Enforcement

This is the critical correction for Cycle 034. Individual premises may be strong, but the batch must be diverse. The following rules apply to any set of 20 premises:

### 1. The "Unique Core Mechanic" Rule
No two premises in a single batch may share the same **core physical interaction mechanism**.
- *Example:* If Premise A involves "catching a falling object," no other premise in the batch can involve catching a different falling object. It must be a distinct mechanical concept (e.g., "bracing against wind," "slipping on ice," "climbing a wall").

### 2. The "Max 2 per Hook Family" Rule
Categorize hooks into families and limit usage:
- **Family A: Environmental Force** (Wind, water splash, debris impact) — Max 3 premises.
- **Family B: Physical Obstacle Navigation** (Vaulting, climbing, balancing on beam) — Max 4 premises.
- **Family C: Object Interaction** (Catching, throwing, manipulating controls/props) — Max 4 premises.
- **Family D: Social/Entity Interaction** (Looking at another character, reacting to off-screen threat) — Max 3 premises.
- **Family E: Self-Interaction/Grooming** (Adjusting blindfold, fixing hair, checking gear) — Max 2 premises.

*Note:* If a premise fits multiple families, assign it to the primary driver of the visual hook.

### 3. Location Distinction Rule
No two premises may share the same **primary environmental texture**.
- *Invalid Pair:* "Industrial metal corridor" + "Rusted factory floor." (Both are industrial metal).
- *Valid Pair:* "Industrial metal corridor" + "Overgrown grassy field with ruins." (Distinct textures: hard/industrial vs. organic/natural).

Ensure at least 5 distinct environmental contexts in a batch of 20.

### 4. Emotional State Variety
The character’s emotional expression must vary across the batch. Do not default to "serious/stoic" for every premise. Include:
- Focus/Urgency
- Playfulness/Teasing
- Surprise/Shock
- Relief/Satisfaction
- Determination/Fierce

---

## Category Rules

Each premise is assigned a category. The visual execution must match the category's specific requirements to ensure readability and variety.

### Closeup (4 premises)
- **Focus:** Micro-expression + physical sensation.
- **Requirement:** Must show a visible reaction to a stimulus (e.g., flinch from heat, squint from light, tighten jaw from effort). The body is secondary; the face/hands are primary.
- **Anti-Pattern:** Generic "pretty face" with no context.

### Medium (4 premises)
- **Focus:** Body mechanics reacting to environment.
- **Requirement:** Must show torso-level interaction with a prop or force. The pose must imply weight and balance.
- **Anti-Pattern:** Standing still holding an object without tension.

### Fullbody (4 premises)
- **Focus:** Weight distribution/balance challenge.
- **Requirement:** The entire silhouette must be visible, emphasizing how the character maintains stability against a specific cause (e.g., leaning into wind, balancing on one foot).
- **Anti-Pattern:** Static full-body portrait with no implied motion or force.

### Dynamic (4 premises)
- **Focus:** Distinct motion verb and blur/trajectory.
- **Requirement:** Must imply high-speed action. Use motion blur, hair/clothing flow, or mid-air positioning. The verb must be unique within the batch (e.g., "backflip" vs. "dive").
- **Anti-Pattern:** Repeating the same jump/dive mechanic with different props.

### Cinematic (4 premises)
- **Focus:** Character active within scale/contrast.
- **Requirement:** The character must be small in the frame relative to the environment, BUT must have an active role (e.g., emerging from dust, silhouetted against explosion, navigating a vast chasm). They cannot just "stand there."
- **Anti-Pattern:** Passive observation or simple locomotion without narrative stake.

---

## Hard Anti-Pattern Rules

If any of the following are present, the premise is rejected:

1. **The Atmospheric Trap**: Rain, fog, sunset, or snow used as the *primary* hook without a specific physical interaction (e.g., "standing in rain" is weak; "shaking water from hair while dodging a falling beam" is strong).
2. **The Locomotion Filler**: Walking, running, or stepping over debris without a clear reason (escape? pursuit? discovery?). If the character is moving, *why* are they moving this way?
3. **The Passive Balance**: Standing on one leg or balancing on a beam just to show off legs, with no threat of falling or specific cause for the balance challenge.
4. **The Direct Gaze Overload**: Direct eye contact with the viewer is powerful but must be used sparingly (Max 1 per batch). Otherwise, it becomes generic "portrait" energy.
5. **The Canon Drift**: Inventing new scars, tattoos, or clothing changes not supported by the local character profile.

---

## Final Premise Checklist

Before generating prompts, verify:

### Character & Identity
- [ ] Is the character recognizable via silhouette and key accessories?
- [ ] Does the personality match the reaction (e.g., stoic character shows subtle tension, not exaggerated shock)?
- [ ] Are there no factual inventions outside the local profile?

### Visual Appeal & Hook
- [ ] Is the body language intentional and expressive?
- [ ] Is fabric physics used to enhance motion/appeal (sleeves flaring, hem lifting)?
- [ ] Is the hook centered on the character's interaction, not just the setting?
- [ ] Is there a visible cause for the current state?

### Diversity & Repetition Control (Batch Level)
- [ ] Does this premise violate the **"Max 2 per Hook Family"** rule in the current batch?
- [ ] Have I repeated the primary action verb more than **4** times in this batch?
- [ ] Is the location distinct from the previous 3 premises and unique within the batch?
- [ ] Is the emotional state different from at least 5 other premises in the batch?
- [ ] Are there any exact duplicates or near-duplicates (same mechanic, same prop)?

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
- [ ] Can this be animated into a 5–10 second clip?

If any box is unchecked, rewrite the premise to add specificity, causality, or active motion.
