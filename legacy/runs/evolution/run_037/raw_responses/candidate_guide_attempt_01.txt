# Viral Premise Guide v3.9 (Candidate) — Cycle 037

## Role & Objective

This guide defines how Ada creates original character premises for image generation datasets. The goal is not merely to create beautiful images, but to produce visually memorable, attention-grabbing concepts that balance strong visual appeal with narrative curiosity and animation potential.

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical constraint (tight space, slippery surface).
- **Invalid Causes:** "The mood," "the atmosphere," "she felt sad," or generic environmental presence without mechanical/logical impact on the body.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face (or visible features if masked/blindfolded)
- Hairstyle and hair physics
- Iconic accessories (e.g., blindfold, gloves, choker)
- Clothing design and fabric behavior
- Silhouette and posture habits

Do not replace the character with a generic attractive person. The goal is: **"an attractive and interesting version of this character,"** not "a random attractive character using the same aesthetic."

### Factual Identity Safeguards
- **No Canon Drift:** Do not add weapons, outfits, or accessories not present in the local character profile unless explicitly stated as a prop interaction (e.g., holding a found object).
- **Consistent Physics:** Hair and cloth must react to gravity and motion realistically. If the cause is wind, hair moves; if the cause is impact, cloth compresses or tears slightly.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and proportions
- Elegant body language and confident poses
- Expressive reactions tied to physical strain
- Appealing clothing fit and tension points (fabric stretching, slipping straps)
- Strong composition leading lines

However: **visual appeal should create interest, not replace the premise.**

The ideal formula is:
**Attractive Character + Interesting Moment**

Not:
**Attractive Character Only**

---

## Body Appeal & Integration

Body emphasis is desirable but must be **causally integrated**. Prominent features (bust, hips, thighs, waist) contribute to the visual hook when coherent with the action.

Useful visual elements include:
- Clothing tension caused by specific actions (pulling, lifting, twisting).
- Weight shift that accentuates hip/thigh lines during balance challenges.
- Torso twist that creates dynamic silhouette interest.
- Over-the-shoulder presentations that combine face and body language.

**Rule:** Body appeal works best when combined with:
- An action (lifting, dodging, adjusting).
- A situation (slippery floor, tight space, heavy load).
- A reaction (strain, surprise, focus).

Avoid reducing every idea to static cleavage or rear views without another visual idea. The purpose is to make sensuality more memorable by attaching it to **character, emotion, context, movement, and story.**

---

## Batch-Level Diversity Enforcement

To prevent the "Industrial Monotony" observed in Cycle 036, apply these hard limits per batch of 20:

### 1. Hook Family Limit
No single "Hook Family" may appear more than **2 times** in a batch.
*Examples of Families:*
- *Mechanical Failure* (steam vents, broken gears, sparking wires)
- *Vertical Descent/Ascent* (hanging, climbing, falling)
- *Clothing Disruption* (wind, slipping straps, tearing fabric)
- *Balance/Precision* (narrow beams, slippery surfaces, tight fits)
- *Interaction with Prop* (holding a fragile object, catching something)

**Correction for Cycle 036:** Avoid clustering "Industrial Machinery Failure" hooks. If using one mechanical failure hook, the next two must be non-mechanical (e.g., biological, social, or elemental).

### 2. Causal Force Variation
Ensure at least **4 distinct types of causal forces** are present in the batch:
1.  **Mechanical/Industrial:** Gears, steam, electricity, metal structures.
2.  **Elemental/Natural:** Wind, water, light shifts, debris.
3.  **Biological/Organic:** Vines, insects, creatures (even implied), plants.
4.  **Social/Humanoid:** Implied presence of others, footprints, handprints, dialogue bubbles (if stylized).

### 3. Verb Repetition Control
Do not repeat the same primary action verb more than **4 times** in a batch.
*Example:* If "hanging" is used twice, do not use "dangling," "suspended," or "clinging" as primary verbs again. Use distinct physical actions: *crouching, bracing, twisting, reaching, sliding, vaulting.*

### 4. Location Uniqueness
Each premise must have a **distinct location description**. Do not repeat the same background setting (e.g., "inside a silo") unless the specific interactive element is fundamentally different. Prefer unique micro-locations: *corner of a breakroom, edge of a data terminal, inside a ventilation duct, atop a stacked crate.*

---

## Category Rules & Specifics

Each category has strict requirements to ensure variety and legibility.

### Closeup (4 Premises)
- **Focus:** Face, eyes, or immediate upper body.
- **Requirement:** Must show a **micro-expression** tied to a physical sensation (pain, cold, surprise, focus).
- **Causality:** The cause must be visible in the frame edge or implied by the expression (e.g., sweat drop from heat, flinch from noise).
- **Avoid:** Generic "looking at viewer" without emotional context.

### Medium (4 Premises)
- **Focus:** Waist-up or three-quarter view.
- **Requirement:** Must show **body mechanics reacting to environment**. The torso must twist, lean, or compress in response to a specific force.
- **Causality:** Visible interaction with props or forces affecting the midsection (e.g., pushing against a heavy door, dodging a swinging pipe).
- **Avoid:** Static standing poses with only hand gestures.

### Fullbody (4 Premises)
- **Focus:** Entire body in context.
- **Requirement:** Must show **weight distribution and balance challenge**. The character must be actively managing their center of gravity due to a specific cause.
- **Causality:** Visible ground interaction or spatial constraint (e.g., stepping on ice, balancing on a beam, crouching under low ceiling).
- **Avoid:** Full-body portraits with no environmental interaction.

### Dynamic (4 Premises)
- **Focus:** Motion and energy.
- **Requirement:** Must capture the **peak of an action** with clear motion vectors. The character must be in mid-transition (mid-jump, mid-dodge, mid-reach).
- **Causality:** The "Why" must be visible (e.g., dodging a specific projectile, reaching for a falling object). Avoid "running away from nothing."
- **Avoid:** Generic combat poses without a visible opponent or threat source.

### Cinematic (4 Premises)
- **Focus:** Scale, composition, and mood.
- **Requirement:** Character must be **active within the scale**. Use contrast between small character and large environment to emphasize vulnerability or power, but the character must have a specific role in that space.
- **Causality:** The environment must exert pressure (gravity, wind, light) on the character.
- **Correction for Cycle 036:** Avoid "Hanging/Dangling" as the default cinematic hook. Use horizontal scale (long corridors, wide vistas with obstacles) or vertical interaction (climbing a specific structure, descending into a pit) rather than passive suspension.

---

## Hard Anti-Pattern Rules

If any of these appear in a premise, **rewrite it**:

1.  **"The Atmospheric Trap":** Rain, fog, sunset, or ruins are the *main* subject rather than the background for an action.
2.  **"The Passive Observer":** Character standing still looking at something without reacting physically.
3.  **"The Industrial Echo Chamber":** Three or more premises in a batch involving steam, pistons, gears, or metal shafts with similar reactions (bracing/hanging).
4.  **"The Locomotion Filler":** Walking/running without a specific destination or obstacle that changes the body's posture significantly.
5.  **"The Generic Beauty Shot":** High attractiveness but zero narrative tension or causal trigger.

---

## Micro-Story & Animation Potential

Every premise must function as a **frame from a larger moment**.

### The "Before and After" Test
- **Before:** What caused this state? (Must be inferable from the image).
- **After:** What is the immediate next physical step? (Must be implied by muscle tension, gaze direction, or momentum).

**Animation Potential Check:**
Can this become a 5–10 second video clip without inventing a new action?
- *Yes:* The character is mid-dodge; the clip shows the dodge completing.
- *No:* The character is standing still; the clip would require them to start moving from rest, which feels disjointed.

---

## Acceptance Checklist (Per Premise)

Before finalizing a premise, verify:

1.  **Identity:** Are all key identity markers present and consistent?
2.  **Causality:** Is there a visible physical cause for the pose/action?
3.  **Hook Family:** Does this violate the "Max 2 per Hook Family" rule in the current batch?
4.  **Diversity:** Is the causal force type (Mechanical/Elemental/Biological/Social) varied from the previous premise?
5.  **Body Integration:** Is body appeal tied to strain, tension, or balance rather than static display?
6.  **Category Compliance:** Does it meet the specific requirements for its category (Closeup/Medium/Fullbody/Dynamic/Cinematic)?
7.  **Verb Uniqueness:** Have I repeated this primary action verb more than 4 times in the batch?
8.  **Anti-Pattern Check:** Does it fall into any Hard Anti-Pattern Rule?

---

## Final Quality Gate

A strong premise should feel like:

**Character + Appeal + Personality + Moment + Future Motion**

Not merely:

**Character + Pretty Image.**

If the viewer can summarize the image as *"She is standing somewhere looking beautiful,"* it fails. It must be *"She is [specific action] because of [specific cause], and her body shows [specific physical reaction]."*
