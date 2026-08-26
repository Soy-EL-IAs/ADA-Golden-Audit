# Viral Premise Guide v2.7 (Candidate) — Cycle 024

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip, or a deliberate character decision that disrupts equilibrium.
- **Invalid Causes:** "Mystery energy," generic wind without a source, ambient atmosphere, or unexplained tension.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face (or blindfold/eye contact)
- Hairstyle and hair physics
- Iconic accessories (blindfold, gloves, boots, weapon)
- Clothing design (dress cut, sleeves, stockings)
- Silhouette and posture
- Personality flavor

Do not replace the character with a generic attractive person. The goal is:
*"An attractive and interesting version of this specific character."*

### Factual Identity Safeguards
To prevent hallucination in image generation:
1. **No New Scars/Tattoos:** Unless specified in the local profile, do not add visible injuries or markings.
2. **Clothing Consistency:** The outfit must match the canonical design (e.g., 2B’s black dress with white accents). Do not invent new layers unless physically justified by the action (e.g., a torn hem from a specific snag).
3. **Accessories:** Keep iconic items (blindfold, Pod) consistent. If removed, it must be part of the micro-story (e.g., holding it in hand), not just missing.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. It is one of the primary reasons a viewer stops scrolling. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and proportions
- Elegant body language and confident poses
- Expressive reactions (micro-expressions)
- Appealing clothing fit and tension
- Strong composition

However, visual appeal should create interest, not replace the premise. The ideal formula is:

**Attractive Character + Interesting Moment**

Not just: **Attractive Character Only.**

### Body Appeal & Integration
Body emphasis is desirable but must be integrated into the action. Prominent breasts, hips, buttocks, thighs, and a defined waist may contribute to the visual hook when coherent with the character and composition.

Useful visual elements include:
- Clothing tension (fabric stretching over muscles)
- Torso twists and weight shifts
- Dynamic limb placement (crossed legs, extended arms)
- Over-the-shoulder or low-angle presentations that highlight silhouette

**Rule:** Body language should communicate confidence, curiosity, playfulness, elegance, shyness, attitude, or emotion. A pose must not exist solely to show off a body part; it must be the *result* of an action or reaction.

---

## Micro-Story & Causality

A micro-story is a 3-beat narrative compressed into one frame:
1. **Trigger (Cause):** Something happens (object falls, door sticks, light flickers).
2. **Action/Reaction:** The character responds physically and emotionally.
3. **Consequence/State:** The immediate result visible in the image (clothing shift, object position, facial expression).

### Causal Specificity Rule
Avoid generic triggers like "wind" or "danger." Be specific:
- *Generic:* "Wind blows her hair."
- *Specific:* "A burst of steam from a cracked pipe pushes her hair back and lifts her dress hem slightly as she shields her eyes with one gloved hand."

### Personality-Driven Reactions
The reaction must fit the character’s core personality.
- **Stoic Character:** Minimal facial movement, tight jaw, controlled breathing, precise physical adjustment.
- **Playful Character:** Raised eyebrow, smirk, relaxed shoulders despite danger, teasing glance at viewer/off-screen entity.
- **Fierce Character:** Tensed muscles, narrowed eyes, aggressive grip on weapon/prop.

---

## Batch-Level Diversity Enforcement

To prevent "batch fatigue" and repetitive patterns (a key failure in Cycle 023), apply the following hard constraints across any set of 10–20 premises:

### 1. The Hook Family Limit
Define a "Hook Family" as the primary type of interaction or visual trope. Examples: *Mechanical Jam, Fluid Exposure, Climbing/Balancing, Combat Stance, Mirror/Reflection, Prop Interaction.*
- **Rule:** No more than **2 premises** per batch may share the same Hook Family.
- *Cycle 023 Failure:* 4 premises involved mechanical jamming/prying. This is a violation.

### 2. The Verb Repetition Cap
Count the primary action verbs used in the batch (e.g., "prying," "pulling," "balancing," "dodging").
- **Rule:** No single verb may appear as the primary action more than **3 times**.
- *Cycle 023 Failure:* "Prying" and "Pulling" were overused.

### 3. Environmental Context Rotation
Ensure locations are not clustered in one aesthetic category (e.g., all industrial, all gothic ruins).
- **Rule:** In a batch of 20, no more than **4 premises** should share the same broad environmental type (e.g., "Industrial/Factory," "Gothic/Ruins," "Domestic/Interior").
- *Cycle 023 Failure:* Heavy skew toward industrial/mechanical settings.

### 4. Emotional Variance
The batch must display a range of emotional states.
- **Rule:** Include at least one premise for each of the following distinct emotional tones: *Composure, Surprise/Fear, Playful/Teasing, Effort/Strain, Focus/Determination.*

---

## Category Rules & Shot Types

Each premise is assigned to a category. The category dictates the framing and focus but does not excuse weak causality.

### 1. Closeup
- **Focus:** Face, hands, or specific prop interaction.
- **Requirement:** Must show a micro-expression or detailed physical interaction (e.g., fingers gripping a fraying rope). Background should be blurred or minimal to keep attention on the character’s reaction.
- **Anti-Pattern:** "Face in rain" without cause.

### 2. Medium
- **Focus:** Waist-up or knee-up.
- **Requirement:** Clear body language and torso movement. Clothing physics (sleeves, dress hem) must be active due to motion.
- **Anti-Pattern:** Static standing pose with arms at sides.

### 3. Fullbody
- **Focus:** Entire silhouette from head to toe.
- **Requirement:** Emphasize proportions, stance, and relationship to the ground/environment. Must show weight distribution (e.g., leaning on one leg, mid-stride).
- **Anti-Pattern:** "Model pose" where the character is just standing still in a nice outfit.

### 4. Dynamic
- **Focus:** Action-in-progress.
- **Requirement:** Implies high speed or force. Hair and clothing should be streaming or flaring. The angle should suggest motion (diagonal lines, motion blur hints).
- **Anti-Pattern:** "Action pose" that looks like a statue (e.g., holding a sword up but with no directional force).

### 5. Cinematic
- **Focus:** Wide shot with environmental context, but character remains the focal point.
- **Requirement:** The environment must be *secondary* to the event. Use depth of field or lighting to isolate the character’s action within the space.
- **Anti-Pattern:** "Wallpaper" where the landscape is beautiful but the character is small and passive.

---

## Hard Anti-Pattern Rules (The "No-Go" List)

If a premise matches any of the following, it must be rewritten:

1. **The Atmospheric Wallflower:** Character is standing still in rain/snow/fog with no specific physical interaction or causal trigger.
2. **The Mechanical Repetition:** The 3rd+ instance in a batch where the character is prying, pulling cables, or twisting valves.
3. **The Generic Dodge:** Character is "dodging" or "balancing" without showing *what* they are dodging/balancing on specifically (e.g., not just "a beam," but "a rusted I-beam with a loose bolt dropping below").
4. **The Passive Beauty Shot:** Character is looking at the viewer with a neutral expression, standing in a nice location, doing nothing.
5. **The Unexplained Injury:** Visible blood or tears without a visible cause (e.g., no cut, no falling object).

---

## Animation Potential Check

Every premise must be "animatable" for 5–10 seconds without inventing new major actions. Ask:
- Can I animate the hair and clothing moving based on the implied force?
- Can I animate the character’s facial expression shifting slightly (e.g., from focus to realization)?
- Is there a clear direction of motion or force vector in the composition?

If the image is static in a way that requires inventing a new object or action to make it move, it fails.

---

## Acceptance Checklist

Before accepting a premise for the batch, verify:

### Identity & Factual Integrity
- [ ] Is the character recognizable (face/hair/outfit)?
- [ ] Are there any unexplained scars, tattoos, or costume changes?
- [ ] Does the personality match the reaction?

### Visual Appeal & Composition
- [ ] Is body appeal integrated into the pose naturally (not just added on)?
- [ ] Is the composition dynamic (diagonal lines, leading eyes, effective negative space)?
- [ ] Does lighting highlight the character’s features and mood?

### Hook & Story (Causality)
- [ ] **Cause:** What specific event triggered this moment? (Must be visible or inferable).
- [ ] **Reaction:** How is the character physically/emotionally responding?
- [ ] **Consequence:** Is there a secondary effect (clothing shift, object movement)?
- [ ] Would the viewer ask "What happens next?"

### Diversity & Repetition Control (Batch Level)
- [ ] Does this premise violate the **"Max 2 per Hook Family"** rule?
- [ ] **Verb Check:** Have I repeated the primary action verb more than 3 times in this batch?
- [ ] Is the location distinct from the previous premise in the sequence?
- [ ] **Environmental Rotation:** Am I exceeding 4 premises of the same environmental type?

### Animation & Motion
- [ ] Can this become a short video clip without inventing new actions?
- [ ] Is there implied movement (hair, cloth, debris)?
- [ ] Does the pose suggest a clear direction of force or motion?
