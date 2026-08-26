# Viral Premise Guide v2.0 (Candidate)

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
- **Invalid Causes:** "Vibes," general atmosphere, "preparing for battle" without visible preparation, standing still because it looks cool.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face (or blindfold/glasses if applicable)
- Hairstyle and hair behavior under motion
- Iconic accessories
- Clothing design and fabric physics
- Silhouette
- Personality flavor
- Characteristic visual traits

Do not replace the character with a generic attractive person. The goal is: **"an attractive and interesting version of this character,"** not "a random attractive character using the same aesthetic."

### Factual Identity Safeguards
1. **No Canon Invention:** Do not add items, scars, or features not present in the provided character profile unless explicitly stated as a variant.
2. **Consistent Silhouette:** The body type and proportions must match the reference. A slender character should not suddenly appear muscular; an athletic character should not appear frail.
3. **Outfit Integrity:** Clothing must behave according to its material (e.g., leather doesn't flow like silk). Do not mix outfits from different sources unless specified.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette (or masculine equivalent, depending on character)
- Attractive proportions
- Elegant body language
- Confident poses
- Expressive reactions
- Appealing clothing design
- Strong composition

However: **Visual appeal should create interest, not replace the premise.**

The ideal formula is: `attractive character + interesting moment`
Not: `attractive character only.`

---

## Body Appeal & Integration

Body emphasis is desirable when coherent with the character and composition. A voluptuous yet athletic silhouette (or appropriately toned/muscular build) is generally desirable when appropriate.

Useful visual elements include:
- Defined waist and hips
- Prominent bust or chest definition
- Strong legs and thighs
- Fitted clothing that shows tension
- Torso twist
- Weight shifted onto one leg
- Leaning, stretching, crouching, bending naturally as part of an action

**Crucial Rule:** Body language should feel intentional. A pose should communicate confidence, curiosity, playfulness, elegance, shyness, attitude, or emotion. It must not be a static display of anatomy.

### Body As A Hook, Not The Entire Premise
The body should be part of the hook, not necessarily the entire premise. Avoid reducing every idea to:
- Cleavage
- Rear view
- Low viewpoint
- Large breasts/buttocks

...without another visual idea. Attach sensuality to:
- Character emotion
- Context
- Movement
- Story

---

## Category Rules & Shot Diversity

To ensure batch-level diversity, premises must be distributed across four distinct shot categories. Each category has specific constraints to prevent homogeneity.

### 1. Closeup (4 premises)
**Focus:** Face, hands, or specific prop interaction.
**Goal:** Intimacy and micro-expression.
**Requirements:**
- Must show a **micro-reaction** (squinting, biting lip, gripping tight).
- Background should be blurred or abstract to keep focus on the character's immediate state.
- Avoid generic "looking at viewer." The gaze must have intent (suspicion, fear, amusement).

### 2. Medium (4 premises)
**Focus:** Waist-up or knee-up.
**Goal:** Personality and upper-body dynamics.
**Requirements:**
- Must show **torso movement** (twist, lean, recoil).
- Hands must be active (holding, pushing, shielding), not resting at sides.
- Clothing tension should be visible due to the action.

### 3. Fullbody (4 premises)
**Focus:** Entire silhouette and stance.
**Goal:** Balance, weight distribution, and spatial awareness.
**Requirements:**
- **No Static Balancing:** The character cannot just "stand on a ledge." They must be actively stabilizing against a force or preparing to move.
- Feet must show grip or slip risk.
- Arms must be engaged in the balance (out for stability, holding an object, shielding).

### 4. Dynamic/Cinematic (4 premises)
**Focus:** Action peak and environmental interaction.
**Goal:** High energy and scale.
**Requirements:**
- **Specific Physical Interaction:** The character must touch, dodge, or react to a specific environmental element (falling debris, swinging chain, laser, door closing).
- **No Atmospheric Dominance:** The environment supports the action; it does not replace it. Avoid "standing in rain" as the primary hook.

---

## Batch-Level Diversity Enforcement

To prevent repetition clusters (a key failure in Cycle 016), the following limits apply to any batch of 20 premises:

| Element | Max Occurrences per Batch | Notes |
| :--- | :---: | :--- |
| **Wind/Hair Disruption** | 3 | Must be caused by a specific source (vent, explosion, movement), not generic breeze. |
| **Arms at Sides/Crossed** | 2 | Only allowed if actively bracing against force or holding breath for tension. Otherwise, hands must move. |
| **Looking Directly at Viewer** | 3 | Gaze must have clear intent (defiance, curiosity). No passive "model stare." |
| **Rain/Weather as Main Hook** | 1 | Weather is a modifier, not the premise. The character's interaction with it matters more. |
| **Cathedral/Ruins/Lonely Landscape** | 2 | If used, there must be an immediate physical threat or object interaction in frame. |
| **Mirror/Reflection** | 1 | Must involve a change (cracking, smudging) or dual action. |

---

## Hard Anti-Pattern Rules

Reject any premise that fits the following descriptions:

1. **The Passive Stare:** Character looking directly at the viewer with no action, reaction, or environmental context.
2. **The Locomotion Filler:** Walking, running, or jumping without a clear narrative consequence (escape, pursuit, discovery, evasion).
3. **The Static Balance:** Standing on an edge or pillar with arms slightly out, looking "cool" but doing nothing. There is no visible force trying to knock them over.
4. **The Atmospheric Mood Piece:** Rain, fog, or sunset where the character is merely present. The weather is not interacting with the character's body or outfit in a specific way.
5. **The Gameplay Idle:** Poses that look like idle animations from a video game (arms at sides, neutral face, no weight shift).
6. **The Repetitive Hook Cluster:** Using "sleeve snag," "wind-blown hair," or "fluid drop" more than the batch limits allow without varying the cause.

---

## Micro-Story & Causality

Every premise must tell a 5-second story within the frame.

**Structure:**
1. **Cause (Visible):** What is happening *right now* that affects the character? (e.g., A chain swings, a floor cracks, a light flickers).
2. **Action/Reaction (Visible):** How does the character respond physically? (e.g., Leans back, grips rail, flinches).
3. **Personality Filter:** How does their temperament modify this response? (e.g., Stoic: holds breath; Playful: smirks despite danger).

**Example of Weak Causality:**
"2B stands in a dark room." -> *Why is she there? What is she doing?*

**Example of Strong Causality:**
"The floor beneath 2B's left foot cracks and tilts, causing her to lunge forward with one hand on the wall for support. Her blindfold slips slightly as she grits her teeth in suppressed annoyance at the instability." -> *Cause: Floor crack. Action: Lunge/support. Personality: Suppressed annoyance.*

---

## Animation Potential

Every premise must have high potential for 5–10 second animation:
- **Directional Energy:** The pose should suggest where the movement is coming from and going to.
- **Continuity:** It should be easy to imagine the previous frame (cause) and next frame (effect).
- **No New Invention Needed:** The animation should not require inventing a new object or action that isn't implied by the static image.

*Test:* Can you animate this character for 5 seconds without adding new props or changing the location? If yes, it passes. If the character is just "standing," they will likely start walking or turning around, requiring new context. Avoid this.

---

## Final Premise Checklist

Before generating prompts, verify each premise against this checklist:

### Character & Identity
- [ ] Is the character recognizable (face/hair/outfit)?
- [ ] Are there any factual errors in identity?
- [ ] Does the pose fit their physical build?

### Visual Appeal
- [ ] Is the composition attractive and scroll-stopping?
- [ ] Is body appeal integrated naturally into the action?
- [ ] Is the lighting enhancing, not just illuminating?

### Hook & Story
- [ ] **Is there a visible cause?** (What triggered this moment?)
- [ ] **Is there an active reaction?** (Not just standing.)
- [ ] Does the personality show through the reaction?
- [ ] Would removing the setting leave the premise mostly intact? (If no, the setting is too dominant.)

### Category Compliance
- [ ] Does it meet the specific requirements for its assigned category (Closeup/Medium/Fullbody/Dynamic)?
- [ ] For Fullbody: Are hands and feet actively engaged in balance/motion?
- [ ] For Dynamic: Is there a specific environmental interaction?

### Diversity & Repetition
- [ ] Does this violate any batch-level diversity limits?
- [ ] Is it distinct from the previous 4 premises in tone, pose, and hook?

### Animation
- [ ] Can this be animated for 5 seconds without inventing new context?
- [ ] Is there implied directional energy?

---

## Acceptance Criteria for Cycle 017

A premise is **accepted** only if:
1. It passes all checklist items above.
2. It avoids the "Static Balancing" and "Passive Stare" anti-patterns.
3. It contributes to batch diversity (does not exceed hook limits).
4. The visual appeal is tied to a specific action or reaction, not just static beauty.

A premise is **rejected** if:
1. It relies on atmosphere (rain
