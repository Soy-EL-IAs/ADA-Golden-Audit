# Viral Premise Guide v1.7 (Candidate)

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
Specific clothing items (sleeves, stockings, hem, accessories) should frequently participate in the causal chain. A sleeve catching on a pipe, a stocking snagging on debris, or a hem lifting due to sudden movement provides immediate visual tension and narrative logic.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face (if visible)
- Hairstyle
- Iconic accessories
- Clothing design
- Silhouette
- Personality flavor
- Characteristic visual traits

**Factual Identity Safeguards:**
Do not introduce factual elements not present in the local character profile. If the profile does not list a specific weapon, accessory, or color variation, do not invent it unless explicitly part of the "alternate aesthetic" allowed by the batch context. The goal is *"an attractive and interesting version of this character,"* not *"a random attractive character using the same aesthetic."*

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. Visual appeal is one of the primary reasons a viewer stops scrolling. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette
- Attractive proportions
- Elegant body language
- Confident poses
- Expressive reactions
- Appealing clothing design
- Strong composition

However, visual appeal should create interest, not replace the premise. The ideal formula is: **Attractive Character + Interesting Moment.**

### Body Appeal & Integration
Body emphasis is desirable when coherent with the character and composition. Prominent breasts, hips, buttocks, thighs, legs, and a defined waist may intentionally contribute to the visual hook. A voluptuous yet athletic silhouette is generally desirable when appropriate.

Useful visual elements include:
- Defined waist-to-hip ratio
- Strong body silhouette
- Torso twist or weight shift
- Fitted clothing tension
- Natural bending as part of an action (not static posing)

Body language should feel intentional. A pose should communicate confidence, curiosity, playfulness, elegance, shyness, attitude, or emotion. **Crucially:** Body appeal must be integrated into the action. The body is reacting to the cause; it is not just displayed for display’s sake.

---

## Hard Anti-Pattern Rules

To prevent the "conservative drift" (v1.2 failure) and the "narrow repetitive drift" (Extreme test failure), apply these hard constraints:

### 1. The Atmospheric Dominance Ban
In **Cinematic** shots, the environment must not be the main subject. If the character is static in a vast space (cathedral, ruins, rainstorm), they are failing this rule unless they are actively engaging with an element (catching falling debris, interacting with light beams, reacting to sound).
- **Fail:** Standing alone on a rooftop in the rain.
- **Pass:** Reaching up to catch a raindrop that is about to hit her face, or shielding her eyes from a sudden flash of lightning.

### 2. The Industrial Hazard Cap
Generic industrial hazards (steam pipes, gears, sparks, debris) are valid hooks but must not dominate the batch.
- **Limit:** Max 2 premises per batch may use "Industrial Hazard" as the primary causal agent.
- **Requirement:** If used, the hazard must be specific (e.g., a *specific* valve turning red, a *single* gear jamming) rather than generic background noise.

### 3. The Locomotion Filler Ban
Avoid "balancing on a ledge" or "walking across a beam" as a default pose unless there is a distinct narrative consequence (e.g., the ledge is crumbling, she is escaping something). Simple balancing without a "what happens next" implication is weak.

### 4. The Mirror/Bath/Wind Trap
Avoid repeating the same sensual hook family more than twice per batch. Specifically:
- Max 2 premises using mirrors/reflections.
- Max 2 premises involving water/bath/steam as the primary interaction.
- Max 2 premises where wind is the *only* cause for hair/clothing movement (wind must interact with a prop or another force).

---

## Batch-Level Diversity Enforcement

For every batch of 20 premises, enforce the following distribution rules to ensure variety:

### Hook Family Distribution
No single "Hook Family" may appear more than **3 times** in a batch.
*Examples of Hook Families:*
- Industrial/Mechanical Interaction
- Organic/Nature Interaction (plants, animals, weather)
- Personal Space/Prop Interaction (tools, books, food, small objects)
- Combat/Evasion Action
- Emotional/Social Reaction (interaction with off-screen entity or self-reflection)

### Location Variety
No single location type may appear more than **4 times** in a batch.
*Examples:* Industrial interior, Overgrown Garden, Urban Rooftop, Laboratory, Forest, Office/Interior, Ruined Structure.

### Emotional Register
Ensure at least **5 distinct emotional registers** are represented across the batch (e.g., focused determination, playful mischief, startled shock, calm confidence, frustrated effort). Do not let one emotion (e.g., "cool confidence") dominate more than 40% of the set.

---

## Category Rules & Shot Types

Each premise must be assigned a specific shot type that enhances the micro-story:

### Closeup
- **Focus:** Face, eyes, or immediate upper body interaction.
- **Requirement:** Must show a subtle but clear reaction to a cause (e.g., eye widening at a noise, adjusting a blindfold). Background is secondary/blurry.
- **Anti-Pattern:** Generic beauty portrait with no visible trigger for the expression.

### Medium
- **Focus:** Waist-up or knee-up.
- **Requirement:** Shows body language and interaction with props. The causal agent (object, person, force) should be visible in the frame if possible.
- **Anti-Pattern:** Standing pose with arms crossed unless reacting to something specific.

### Fullbody
- **Focus:** Entire silhouette and relationship to the environment.
- **Requirement:** Must show weight distribution and balance related to an action (e.g., leaning, crouching, stretching). Avoid static "model" poses.
- **Anti-Pattern:** Standing straight in a scenic location with no active engagement.

### Dynamic
- **Focus:** Motion blur, mid-action, high energy.
- **Requirement:** Must capture the *peak* of an action (dodging, swinging, catching). There must be implied velocity.
- **Anti-Pattern:** "Action pose" that looks frozen and lacks directional flow.

### Cinematic
- **Focus:** Wide angle, scale, composition.
- **Requirement:** The character must be the anchor of interest despite the wide view. Use lighting or scale to emphasize their isolation *or* dominance in the scene.
- **Anti-Pattern:** Character as a tiny speck with no discernible action or emotion.

---

## Micro-Story & Animation Potential

Every premise must function as a "frame from a larger moment."

### The 5-Second Test
Can this image be animated for 5–10 seconds without inventing new actions?
- **Yes:** If the cause is visible and the reaction is ongoing (e.g., pulling a sleeve free, catching an apple).
- **No:** If the action is complete or static (e.g., standing after having caught it, just posing).

### Causal Chain Clarity
The viewer must understand:
1. **Trigger:** What happened? (Visible cause)
2. **Response:** How is the character reacting? (Active motion/expression)
3. **Consequence:** What will happen next? (Implied future state)

If any part of this chain is missing, revise the premise to add specificity.

---

## Final Acceptance Checklist

Before accepting a premise for the batch, verify all items below:

### Identity & Factual Accuracy
- [ ] Is the character recognizable via silhouette and key traits?
- [ ] Does the premise respect their personality and iconic traits?
- [ ] Are there no factual errors (new props/traits not in profile)?

### Visual Appeal
- [ ] Is the character intentionally attractive (silhouette, pose, lighting)?
- [ ] Is body appeal integrated naturally into the composition/action?
- [ ] Does the image avoid looking like a generic stock photo or wallpaper?

### Hook & Micro-Story
- [ ] Is there a visible **Cause** for the moment?
- [ ] Is there a clear **Action/Reaction**? (Not just "standing")
- [ ] Would removing the background leave the character's emotion/action intact?
- [ ] Is the hook centered on the character, not just the environment?
- [ ] Does clothing participate in the causal chain (if applicable)?

### Variety & Batch Control
- [ ] Does this premise fit the required Shot Type (Closeup/Medium/Fullbody/Dynamic/Cinematic)?
- [ ] Does it avoid repeating a Hook Family or Location used more than twice/three times in the batch?
- [ ] Is the emotional register distinct from other premises in the current set?
- [ ] If Industrial Hazard is used, is it within the max 2/batch limit?

### Animation Potential
- [ ] Can this be animated for 5–10 seconds with implied motion?
- [ ] Is there clear directional energy in the pose?
- [ ] Does it pass the "What happens next?" test?

### Quality Summary
A strong premise should feel like:
**Character + Appeal + Personality + Moment + Future Motion**

Not merely:
**Character + Pretty Image.**
