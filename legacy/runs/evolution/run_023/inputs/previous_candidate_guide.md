# Viral Premise Guide v2.5 (Candidate) — Cycle 022

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip hazard.
- **Invalid Causes:** "Mood," "contemplation," "standing there," generic wind without a source, vague danger.

**The Causal Chain:** `Trigger Event` → `Physical/Emotional Reaction` → `Secondary Consequence (e.g., clothing shift, object displacement)`.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face and hairstyle (including specific hair physics).
- Iconic accessories (blindfold, gloves, jewelry).
- Clothing design (fabric type, silhouette, hem length).
- Silhouette and posture habits.
- Personality flavor in reaction.

**Factual Identity Safeguards:**
1.  **No Factual Drift:** Do not invent new scars, tattoos, or clothing items not present in the character profile.
2.  **Anatomical Consistency:** Maintain correct limb count and joint articulation unless specified as stylized distortion.
3.  **Costume Integrity:** If a garment is torn, it must be logically consistent with the cause (e.g., a tear from a sharp edge, not just "damage").

The goal is: *"An attractive and interesting version of this character."*
Not: *"A random attractive character using the same aesthetic."*

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. It is one of the primary reasons a viewer stops scrolling. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and proportions.
- Elegant body language and confident poses.
- Expressive reactions (micro-expressions).
- Appealing clothing design and fit.
- Strong composition using negative space and leading lines.

However, **visual appeal should create interest, not replace the premise.**

The ideal formula is:
`Attractive Character + Interesting Moment`
Not: `Attractive Character Only.`

### Body Appeal Integration
Body emphasis is desirable when coherent with the character and composition. Useful visual elements include:
- Defined waist and strong hips.
- Prominent bust or buttocks where appropriate to silhouette.
- Thick or athletic thighs/legs.
- Fitted clothing creating tension lines.
- Torso twists, weight shifts, leaning, stretching, crouching.

**Rule:** Body language must feel intentional. A pose should communicate confidence, curiosity, playfulness, elegance, shyness, attitude, or emotion. Do not let body appeal become the *only* hook; it must be attached to a story beat.

---

## Hard Anti-Pattern Rules (Cycle 022 Corrections)

Based on Cycle 021 analysis, the following patterns are **strictly limited** or **prohibited**:

### 1. The "Balancing Cluster" Limit
- **Weakness in v2.4:** Overuse of "balancing on unstable surface" (e.g., rebar, chimney edge, glass sheet).
- **Rule:** Maximum **2 premises per batch** may use "balancing/counterweighting" as the primary physical constraint.
- **Alternative Physical Constraints:** Use climbing, hanging from a hook, crawling under low clearance, pushing against a closing door, pulling a lever, or catching a falling object.

### 2. The "Static Cinematic" Trap
- **Weakness in v2.4:** Wide shots (Cinematic) often featured static poses ("standing beneath," "crouched defensive") with atmospheric dust/sparks as the only interest.
- **Rule:** Cinematic shots must contain an **active environmental interaction**. The character must be doing something *to* or *with* the environment, not just existing in it.
    - *Bad:* Standing under a falling beam.
    - *Good:* Pushing against a heavy steel door to keep it open while sparks fly from the hinges.

### 3. The "Twist/Lean" Verb Monotony
- **Weakness in v2.4:** Medium shots relied heavily on "twist" and "lean."
- **Rule:** Vary upper-body dynamics. Include verbs such as: *reaching, pushing, pulling, catching, bracing, gripping, adjusting, shielding, striking.*

### 4. Atmospheric Filler
- **Rule:** Dust, rain, fog, or sparks are **supporting elements**, not the main hook. If you remove the atmosphere, the premise must still stand on its own physical action and character reaction.

---

## Batch-Level Diversity Enforcement

To prevent repetition within a single generation run (e.g., 20 premises), apply these hard limits:

1.  **Hook Family Cap:** No more than **2 premises** may share the same primary "hook family" (e.g., "outfit disruption," "balancing act," "combat strike").
2.  **Location Distinctness:** No two consecutive premises should take place in the exact same location type (e.g., do not follow a "ruined cathedral interior" with another "ruined cathedral interior").
3.  **Emotional Tone Variation:** The emotional tone must shift across the batch. Do not have more than 3 consecutive premises sharing the same dominant emotion (e.g., all "stoic determination"). Alternate between: *Determination, Playfulness, Surprise, Tension, Relief.*
4.  **Camera Angle Rotation:** Ensure a mix of Closeup, Medium, Fullbody, Dynamic, and Cinematic shots as per dataset requirements, but avoid repeating the same specific camera angle (e.g., low-angle looking up) in more than 25% of the batch without significant context change.

---

## Category Specifics & Rules

### Closeup
- **Focus:** Face, hands, or specific accessory interaction.
- **Requirement:** Must show a micro-expression or hand action that implies a larger body movement off-screen.
- **Avoid:** Generic "looking at viewer" without context.
- **Example:** 2B’s fingers tightening on the strap of her blindfold as sweat rolls down her temple, eyes narrowed in concentration against a bright glare.

### Medium
- **Focus:** Waist-up or torso-focused action.
- **Requirement:** Must show upper-body dynamics beyond simple leaning/twisting. Use pushing, pulling, reaching, or bracing.
- **Avoid:** Static "twist and look."
- **Example:** 2B bracing her shoulder against a sliding metal panel to stop it from crushing a small object she is holding, her face showing strained focus.

### Fullbody
- **Focus:** Entire silhouette and environment interaction.
- **Requirement:** Must show how the character moves through space. Avoid static balancing unless within the "Balancing Cluster" limit.
- **Avoid:** Standing still in a wide shot.
- **Example:** 2B crawling under a low, sparking ventilation duct, her dress dragging slightly on the grate, one hand reaching forward to grab a handle for leverage.

### Dynamic
- **Focus:** High-energy motion blur or rapid movement.
- **Requirement:** Must show directional momentum. The character is in transit or reacting to immediate force.
- **Avoid:** Generic "fighting pose."
- **Example:** 2B mid-dodge, her body twisted sharply as a projectile grazes her shoulder, her hair whipping forward and her dress hem flaring from the sudden stop of her momentum.

### Cinematic
- **Focus:** Wide angle, environmental scale, dramatic composition.
- **Requirement:** Must show active interaction with the environment (pushing, pulling, climbing, interacting with machinery). The character is an agent, not a statue.
- **Avoid:** "Standing in ruins" or "Crouching under threat."
- **Example:** 2B pulling on a massive rusted lever to release hydraulic pressure, her entire body weight thrown back against the resistance, boots digging into the concrete floor as dust plumes erupt from the mechanism.

---

## Visual Contrast & Personality

Interesting images often contain contrast. Examples:
- Serious character in a funny situation.
- Elegant character in chaos.
- Powerful character showing vulnerability.
- Intimidating character acting cute.
- Shy character unexpectedly confident.

**Personality Filter:** The reaction must match the character’s core personality. If the character is stoic, their "reaction" might be a subtle tightening of the jaw or a controlled breath, not a wide scream. If playful, it might be a smirk or a deliberate tease.

---

## Scroll-Stopping Test

Before accepting a premise, ask:
1.  **Would this image make someone stop scrolling?**
2.  **Is there a visible cause for the action?** (If no, reject.)
3.  **Is the character the subject, not the background?** (If the environment is more interesting than the character, reject.)
4.  **Can this become a 5–10 second video clip without inventing new actions?**

A strong premise usually contains at least one powerful hook:
- Attractive silhouette in motion.
- Unusual situation with clear cause.
- Emotional reaction to a specific trigger.
- Visual surprise (e.g., unexpected clothing interaction).
- Funny or tense interaction.
- Dramatic moment with personality expression.

If the idea can be summarized as: *"Character standing somewhere looking beautiful,"* it is probably too weak. Improve it by adding an action, a reaction, a consequence, or an interaction.

---

## Final Premise Checklist

Before generating prompts, verify each premise against this checklist:

### Character & Identity
- [ ] Is the character recognizable via silhouette and key accessories?
- [ ] Does the personality match the situation (stoic vs. reactive)?
- [ ] Are there any factual errors in clothing or anatomy?
- [ ] **Identity Safeguard:** No invented scars, tattoos, or costume changes not supported by the profile.

### Visual Appeal & Composition
- [ ] Is the composition dynamic (diagonal lines, leading eyes, negative space used effectively)?
- [ ] Is body appeal integrated naturally into the pose (not just added on)?
- [ ] Does the lighting highlight the character’s features and mood?

### Hook & Story (Causality)
- [ ] **Cause:** What specific event triggered this moment? (Must be visible or inferable).
- [ ] **Reaction:** How is the character physically/emotionally responding?
- [ ] **Consequence:** Is there a secondary effect (clothing shift, object movement)?
- [ ] Would the viewer ask "What happens next?"
- [ ] Is the hook specific to this character, not generic?

### Diversity & Repetition Control
- [ ] Does this premise violate the **"Max 2 per Hook Family"** rule?
- [ ] **Balancing Check:** If using balancing/counterweighting, have we already used it twice in this batch?
- [ ] Is the location distinct from the previous premise in the sequence?
