# Viral Premise Guide v2.4 (Candidate) — Cycle 021

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip, or a direct hit.
- **Invalid Causes:** "Mood," "atmosphere," "standing still," "waiting."

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face (or lack thereof, e.g., blindfold)
- Hairstyle and hair behavior under force
- Iconic accessories (gloves, choker, weapon hilt)
- Clothing design (dress cut, stockings, boots)
- Silhouette and posture

Do not replace the character with a generic attractive person. The goal is: **"an attractive and interesting version of this character,"** not "a random attractive character using the same aesthetic."

### Factual Identity Safeguards
1. **No Invented Canon:** Do not add items or features not present in the local character profile (e.g., no wings, no different eye color unless specified).
2. **Silhouette Integrity:** The unique silhouette of the character must be readable even at a small scale. If the pose obscures the iconic shape, adjust the angle.
3. **Personality Consistency:** Reactions must align with the established temperament (e.g., 2B’s stoicism vs. hidden vulnerability). Do not force a "cute" reaction if the character is currently in a "combat-ready" state unless the cause justifies it.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and proportions
- Elegant body language and confident poses
- Expressive reactions (even if subtle)
- Appealing clothing design and fit
- Strong composition and lighting

However, **visual appeal should create interest, not replace the premise.** The ideal formula is: `attractive character + interesting moment`. Not just: `attractive character only`.

### Body As A Hook, Not The Entire Premise
Body emphasis is desirable but must be contextualized. Prominent breasts, hips, buttocks, thighs, and a defined waist may contribute to the visual hook when coherent with the character and composition.

Useful visual elements include:
- Torso twist or weight shift onto one leg
- Clothing tension (fabric stretching over muscle)
- Dynamic poses (crouching, bending, reaching) that naturally highlight anatomy
- Over-the-shoulder presentations that imply depth

**Anti-Pattern:** Do not reduce the image to a "rear view" or "cleavage shot" without an accompanying action or narrative reason. The body is the vehicle for the story, not the destination.

---

## Category Rules & Diversity Enforcement

To prevent template fatigue, each batch of 20 premises must strictly adhere to the following category definitions and diversity limits.

### Batch-Level Diversity Enforcement
1. **Max 2 per Hook Family:** No more than two premises in a batch can share the same primary visual hook (e.g., "adjusting blindfold," "dodging debris," "gripping weapon"). If you have two, the third must use a completely different interaction type.
2. **Location Rotation:** Consecutive premises should not be in the exact same location unless the narrative demands continuity. Vary between industrial, organic, architectural, and abstract spaces.
3. **Emotional Tone Spread:** Ensure at least 4 distinct emotional tones across the batch (e.g., Tense, Playful, Focused, Vulnerable, Defiant). Do not have more than 5 premises with the same dominant emotion.

### Category Definitions
- **Closeup (4 shots):** Focus on face, hands, or specific prop interaction. Must show micro-expressions or fine motor skills. *Avoid:* Generic "gripping hilt" unless the grip is reacting to a specific force (e.g., slipping hand).
- **Medium (4 shots):** Waist-up or knee-up. Focus on upper body dynamics and clothing behavior. *Avoid:* Static standing poses. Must show torso twist, lean, or arm movement.
- **Fullbody (4 shots):** Entire character visible. Focus on silhouette, stance, and full-body balance. *Avoid:* Locomotion filler. The pose must imply a specific physical constraint or action (e.g., balancing on a beam, crouching under cover).
- **Dynamic (4 shots):** Motion blur or high-energy action. Focus on speed, impact, or trajectory. *Avoid:* Generic "running." Must show interaction with an object or force (e.g., sliding across floor, deflecting blast).
- **Cinematic (4 shots):** Wide shot establishing scale and environment. Focus on the character’s relationship to their surroundings. *Avoid:* Static "dangling" or "looking into abyss." The environment must be actively interacting with the character (collapsing, tilting, raining debris).

---

## Micro-Story & Animation Potential

Every premise is a frame from a larger moment. It must imply a **Before** and an **After**.

### Causal Chain Requirement
The prompt must describe:
1. **The Cause:** What is happening to the character? (e.g., "a hydraulic piston slams down")
2. **The Reaction:** How does the character physically respond? (e.g., "she twists her torso sharply")
3. **The Consequence/Result:** What is the immediate visual result? (e.g., "her dress hem flares out, revealing her stockings")

### Animation Potential Test
Can this image become a 5–10 second video clip without adding new elements?
- **Yes:** The motion is implied and continuous. (e.g., She is mid-dodge; the next frame shows her landing.)
- **No:** The pose is static and requires a cut or fade to make sense. (e.g., She is standing still looking at a wall; what happens next? Unclear.)

**Fix for Weak Animation Potential:** Add directional energy. Instead of "standing," use "bracing against." Instead of "looking," use "tracking with her eyes."

---

## Hard Anti-Pattern Rules

If a premise contains any of the following, it must be rewritten:

1. **The Atmospheric Filler Trap:** Using mist, rain, or dust as the *only* reason for the character's pose. If you remove the weather, does the action still make sense?
2. **The "Gripping" Repetition:** More than one closeup in a batch featuring "gripping sword/hilt." The second must be a different hand interaction (e.g., adjusting glove, wiping sweat, holding a broken part).
3. **The "Dangling" Static Pose:** Cinematic shots where the character is simply hanging from something without active movement or threat progression. They must be *sliding*, *shifting weight*, or *reaching*.
4. **The Industrial Hazard Clone:** Multiple medium shots involving "dodging sparks/rebar." Vary the hazard: one dodges a projectile, one adjusts to heat, one balances on unstable ground.
5. **Generic Beauty Shot:** Any premise that can be summarized as "Character standing somewhere looking beautiful" without a specific physical interaction.

---

## Cycle 021 Specific Corrections

Based on Cycle 020 failures (Repetition in Closeup/Medium, Weak Cinematic Poses):

1. **Differentiate Closeups:**
   - One closeup must focus on **facial micro-expression** reacting to an off-screen sound or sight.
   - One closeup must focus on a **non-weapon hand interaction** (e.g., adjusting blindfold strap, wiping dirt from cheek, gripping a broken cable).
   - Avoid "gripping sword hilt during vibration" as the default closeup.

2. **Diversify Medium Shots:**
   - Do not use "dodging industrial hazard causing sleeve flare" more than once.
   - Use varied interactions: *twisting away from a blast*, *reaching for a falling object*, *bracing against a sudden gust*.
   - Ensure the clothing behavior (sleeves, hem) is caused by a specific vector of force.

3. **Strengthen Cinematic Motion:**
   - Replace "clinging to edge" with active interactions: *sliding across a tilting platform*, *crouching as debris rains down*, *running along a collapsing beam*.
   - The environment must be *changing* or *threatening*, not just existing.

4. **Enforce Causal Visibility:**
   - In every prompt, explicitly state the cause of the movement. (e.g., "as a sudden gust from [source] forces...")

---

## Acceptance Checklist

Before accepting a premise for the final batch, verify:

### Character & Identity
- [ ] Is the character recognizable via silhouette and key accessories?
- [ ] Does the personality match the situation (stoic vs. reactive)?
- [ ] Are there any factual errors in clothing or anatomy?

### Visual Appeal & Composition
- [ ] Is the composition dynamic (diagonal lines, leading eyes, negative space used effectively)?
- [ ] Is body appeal integrated naturally into the pose (not just added on)?
- [ ] Does the lighting highlight the character’s features and mood?

### Hook & Story
- [ ] Is there a **visible cause** for the action?
- [ ] Is there a clear **reaction**?
- [ ] Would the viewer ask "What happens next?"
- [ ] Is the hook specific to this character, not generic?

### Diversity & Repetition Control
- [ ] Does this premise violate the "Max 2 per Hook Family" rule?
- [ ] Is the location distinct from the previous premise in the sequence?
- [ ] Is the emotional tone different from the last 3 premises?
- [ ] Is the action verb unique or sufficiently varied?

### Animation Potential
- [ ] Can this become a short video clip (5–10s) without adding new elements?
- [ ] Is there implied directional energy or momentum?

### Quality Gate
A strong premise should feel like:
**Character + Appeal + Personality + Moment + Future Motion**

Not merely:
**Character + Pretty Image.**
