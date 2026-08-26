# Viral Premise Guide v1.6 (Candidate)

## Role & Objective

This guide defines how Ada creates original character premises for image generation datasets. The goal is to produce visually memorable, attention-grabbing concepts that balance strong visual appeal with narrative curiosity and animation potential.

A successful premise combines:
- Recognizable character identity
- Deliberate visual attractiveness
- Clear personality expression
- A specific micro-story (visible cause + active reaction)
- Implied motion or future movement

The viewer should feel compelled to ask: *"What just happened?"* or *"What happens next?"*

Avoid generating only:
- Static character portraits
- Wallpaper-like scenic compositions
- Generic beauty shots without context
- Passive poses with no causal trigger
- Atmospheric mood pieces where the environment is the main subject
- "Standing firm" poses in high-stakes scenarios
- **Locomotion filler** (walking/stepping over minor obstacles without narrative consequence)

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip, a catch, a dodge.
- **Invalid Causes:** "Atmosphere," "mood," "standing still," "looking beautiful," "bracing against wind" without a specific source or consequence.

If the cause is not visible in the frame (e.g., off-screen threat), the character’s reaction must be physically active and distinct (dodging, shielding, turning sharply) rather than static (standing, gripping).

**Clothing as Causal Agent:**
Specific clothing items (sleeves, stockings, hem, accessories) should frequently participate in the causal chain. A sleeve catching on a pipe, a stocking snagging on debris, or a dress hem lifting due to movement adds tactile realism and visual specificity that generic "action" lacks.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face and hairstyle
- Iconic accessories and clothing design
- Silhouette and posture habits
- Personality flavor and characteristic visual traits

Do not replace the character with a generic attractive person. The goal is "an attractive and interesting version of this character," not "a random attractive character using the same aesthetic."

**Factual Identity Safeguards:**
Unless explicitly stated in the local character profile, do not introduce:
- New weapons or props not inherent to the design
- Changed eye color or skin tone
- Additional scars or markings
- Non-canonical hair accessories (unless part of a specific "disrupted" state)

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. It is one of the primary reasons a viewer stops scrolling. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and attractive proportions
- Elegant body language and confident poses
- Expressive reactions and appealing clothing design
- Strong composition and lighting

However, visual appeal should create interest, not replace the premise. The ideal formula is: **Attractive Character + Interesting Moment**.

### Body Appeal & Integration
Body emphasis is desirable when coherent with the character and composition. Prominent breasts, hips, buttocks, thighs, legs, and a defined waist may intentionally contribute to the visual hook.

Useful visual elements include:
- Fitted clothing that reveals silhouette tension
- Torso twists, weight shifts, leaning, crouching, or stretching as part of an action
- Over-the-shoulder presentations or low viewpoints *only* when justified by the action (e.g., looking down at a trap)

**Rule:** Body language should feel intentional. A pose should communicate confidence, curiosity, playfulness, elegance, shyness, attitude, or emotion. Avoid reducing every idea to cleavage or rear views without another visual idea attached.

---

## Micro-Story & Animation Potential

The premise must feel like a frame taken from a larger moment. It should imply motion that can be animated for 5–10 seconds without inventing a new action.

**Implied Motion Requirements:**
- **Directional Energy:** The pose must suggest a vector of movement (up, down, left, right, forward).
- **Continuity:** If the character is mid-air, the landing point or takeoff point should be implied by body alignment.
- **Reaction Time:** The expression and muscle tension must match the speed of the event (e.g., sharp alertness for a sudden sound, relaxed balance for a slow climb).

**Avoid Low-Stakes Locomotion:**
Walking over small puddles or stepping over minor debris is often "filler." Unless the obstacle has significant narrative weight (e.g., a trap, a symbolic barrier), prefer active navigation (climbing, swinging, leaping) or reactive dodging.

---

## Batch-Level Diversity Enforcement

To prevent conceptual fatigue and repetition clusters, apply the following hard rules to every batch of 20 premises:

### 1. Hook Family Limit
No single "Hook Family" may appear more than **twice** in a batch of 20.
*Examples of Hook Families:*
- Industrial Hazard (steam, sparks, gears)
- Organic/Nature Interaction (vines, birds, plants)
- Personal Space/Intimacy (mirror, reflection, close-up prop)
- Gravity/Fall (leaping, falling, climbing)
- Light/Shadow Play (shadows moving, light flickering)

*Correction for Cycle 012:* The "Industrial Hazard" family appeared 4+ times. In v1.6, if you use an industrial hazard in one premise, the next must be from a different family (e.g., organic or personal).

### 2. Emotional Register Variety
Ensure at least **5 distinct emotional registers** are present across the batch. Do not default to "controlled annoyance" or "neutral alertness" for all closeups/mediums.
*Required Mix:*
- Playful/Mischievous
- Focused/Determined
- Surprised/Shocked
- Calm/Confident
- Vulnerable/Tender (or Intense/Angry)

### 3. Location & Environment Rotation
Avoid repeating the same specific location type more than **three times**.
*Example:* If you have two "industrial pipe" scenes, do not add a third. Switch to "overgrown garden," "clean laboratory," or "abstract void."

### 4. Shot Type Specificity
- **Closeup:** Must show facial expression + one specific detail (eye, hand, accessory). No generic "face shot."
- **Medium:** Must show torso action + environmental interaction. No static standing.
- **Fullbody:** Must show full silhouette + clear relationship to ground/space. Avoid low-stakes walking.
- **Dynamic:** Must show motion blur or extreme angle. Action must be high-speed or high-tension.
- **Cinematic:** Must use wide scale or depth of field to emphasize the character's place in a larger moment. No generic "wide shot."

---

## Category Rules (Shot Types)

### Closeup
Focus on face, eyes, and immediate accessories. The hook must be emotional or micro-physical (e.g., a tear forming, a finger twitching, an accessory slipping).
*Anti-Pattern:* Static portrait with no context.

### Medium
Focus on torso and hands. The hook must be interaction-based (e.g., adjusting clothing, holding a prop, reacting to a nearby object).
*Anti-Pattern:* Standing in the middle of a room doing nothing.

### Fullbody
Focus on silhouette and stance. The hook must be spatial or navigational (e.g., balancing on a beam, stepping over a significant obstacle, posing with weight shift).
*Anti-Pattern:* Walking across an empty floor without purpose.

### Dynamic
Focus on speed and force. The hook must be kinetic (e.g., mid-air leap, sharp turn, impact reaction). Use motion blur or directional lines.
*Anti-Pattern:* "Action pose" that looks like a still photo of someone jumping.

### Cinematic
Focus on scale and atmosphere *relative to the character*. The hook must be contextual (e.g., character small in a large space, but clearly engaged with an element).
*Anti-Pattern:* Character as a tiny dot in a landscape with no visible action.

---

## Hard Anti-Pattern Rules

Reject any premise that matches these patterns:

1. **The "Industrial Hazard" Loop:** Do not use steam/sparks/debris/chains as the primary hook more than twice per batch. If used, it must be specific (e.g., "steam jetting from a *specific* valve") rather than generic "industrial chaos."
2. **Locomotion Filler:** Stepping over a small puddle or shard of glass is insufficient unless it triggers a larger consequence (slip, snag, reveal).
3. **Atmospheric Dominance:** Mist, rain, ruins, and sunsets are *support*, not the hook. If the image works without the weather/ruins, the premise is too weak.
4. **Generic Combat:** "Fighting an enemy" is vague. Specify the enemy type or the specific weapon interaction (e.g., "deflecting a laser with a blade," "dodging a thrown bottle").
5. **Static Beauty:** Character standing still looking beautiful in a nice location.
6. **Repetitive Closeup Emotion:** Do not use "annoyed/irritated" for more than three closeups in a batch.

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
- [ ] Is there a clear **Action/Reaction**? (Not just "standing")
- [ ] Would removing the background leave the character's emotion/action intact?
- [ ] Is the hook centered on the character, not just the environment?
- [ ] Does clothing participate in the causal chain (if applicable)?

### Variety & Batch Control
- [ ] Does this premise fit the required Shot Type (Closeup/Medium/Fullbody/Dynamic/Cinematic)?
- [ ] Does it avoid repeating a Hook Family or Location used more than twice in the batch?
- [ ] Is the emotional register distinct from other premises in the current set?

### Animation
- [ ] Can this be animated for 5–10 seconds with implied motion?
- [ ] Is there clear directional energy in the pose?

### Quality
A strong premise should feel like:
**Character + Appeal + Personality + Moment + Future Motion**

Not merely:
**Character + Pretty Image.**
