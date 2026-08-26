# Viral Premise Guide v1.8 (Candidate)

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
- **Invalid Causes:** "Atmosphere," "mood," "standing still," "looking beautiful," "bracing against wind" without a specific source or consequence.

If the cause is not visible in the frame (e.g., off-screen threat), the character’s reaction must be physically active and distinct (dodging, shielding, turning sharply) rather than static (standing, gripping).

**Clothing as Causal Agent:**
Specific clothing items (sleeves, stockings, hem, accessories, blindfold) should frequently participate in the causal chain. A sleeve catching on a pipe, a stocking snagging on debris, or a blindfold slipping due to movement adds specificity and visual texture that generic poses lack.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face (or eye color if obscured)
- Hairstyle and hair behavior
- Iconic accessories (e.g., blindfold, choker, gloves)
- Clothing design and fit
- Silhouette and proportions
- Personality flavor

Do not replace the character with a generic attractive person. The goal is: *"An attractive and interesting version of this specific character,"* not *"A random attractive character using the same aesthetic."*

**Factual Identity Safeguards:**
- Do not invent canonical facts not present in the local profile (e.g., do not give 2B a sword if she isn't holding one in the premise, unless specified as an action).
- Respect physical limitations (e.g., blindfolded characters should react to sound/touch more than sight, unless the blindfold is displaced).

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. It is one of the primary reasons a viewer stops scrolling. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and elegant proportions
- Confident or expressive body language
- Appealing clothing fit (tension, stretch, drape)
- Strong composition and lighting

However: **Visual appeal should create interest, not replace the premise.**

The ideal formula is:
**Attractive Character + Interesting Moment**

Not merely:
**Attractive Character Only**

### Body Appeal & Integration
Body emphasis is desirable when coherent with the character and composition. Prominent breasts, hips, buttocks, thighs, legs, and a defined waist may intentionally contribute to the visual hook. A voluptuous yet athletic silhouette is generally desirable when appropriate.

Useful visual elements include:
- Fitted clothing showing tension or stretch during action
- Torso twists, weight shifts, leaning, stretching, crouching, bending naturally as part of an action
- Over-the-shoulder presentations that imply intimacy or focus
- Strategic reveals caused by movement (e.g., skirt lifting from a jump, top straining from a lift)

Body language should feel intentional. A pose should communicate: confidence, curiosity, playfulness, elegance, shyness, attitude, or emotion. **Avoid reducing every idea to cleavage or rear view without another visual idea.** The purpose is to make sensuality more memorable by attaching it to character, emotion, context, movement, and story.

---

## Category Rules & Shot Types

To ensure variety in the dataset, premises must be assigned to one of five shot types. Each type has specific structural requirements:

### 1. Closeup
- **Focus:** Face, eyes (or blindfold), hands, or immediate upper body.
- **Requirement:** Must show a micro-expression or tactile interaction. The cause should be visible in the detail (e.g., a tear track, a trembling finger, a specific object being held).
- **Avoid:** Generic "looking at viewer" shots unless there is a distinct emotional trigger visible on the face.

### 2. Medium
- **Focus:** Waist-up or knee-up.
- **Requirement:** Must show body language interacting with a nearby prop or environment. The causal chain should be clear (e.g., adjusting a strap, wiping dust from a lens, reacting to a sound).
- **Avoid:** Standing poses without hand interaction.

### 3. Fullbody
- **Focus:** Entire silhouette in context.
- **Requirement:** Must show the relationship between the character and their immediate space. The pose must imply weight distribution and balance affected by an event (e.g., bracing against a door, stepping over a specific hazard with purpose).
- **Avoid:** Locomotion filler (walking/stepping) without narrative consequence.

### 4. Dynamic
- **Focus:** Action in progress, motion blur, or high-energy pose.
- **Requirement:** Must show a specific physical interaction with force (impact, throw, pull, twist). The direction of movement must be clear.
- **Avoid:** Generic "combat stance" or repetitive dodging without a specific object/force being evaded.

### 5. Cinematic
- **Focus:** Wide angle, environmental context, scale.
- **Requirement:** Must show the character as an active agent within the environment, not just a subject in it. There must be a clear line of sight or interaction path between the character and a specific distant element (e.g., reaching for a distant light, observing a specific machine failure).
- **Avoid:** "Character standing in ruins" without a specific focal point of interest other than the scenery.

---

## Batch-Level Diversity Enforcement

To prevent repetition within a single generation batch (typically 20 premises), apply these hard limits:

1.  **Hook Family Limit:** No more than **2** premises may share the same primary hook family (e.g., "Wind/Outfit Disruption," "Object Catching," "Combat Evasion").
    *   *Example:* If two premises involve wind blowing hair/clothes, a third must use a different mechanic (e.g., gravity/falling, heat/shimmer, sound/reaction).
2.  **Location Limit:** No more than **3** premises may share the same specific location type (e.g., "Ruined Cathedral," "Industrial Factory"). Locations should be varied across batches.
3.  **Emotional Register Limit:** The batch must include at least **4 distinct emotional registers** (e.g., Stoic, Playful, Fierce, Vulnerable, Curious). Do not let one emotion dominate more than 5 premises.
4.  **Action Verb Limit:** Avoid using the same primary action verb (e.g., "dodging," "looking") for more than **3** premises in a batch. Vary verbs: *catching, pulling, pushing, climbing, turning, shielding, reaching, slipping.*

---

## Hard Anti-Pattern Rules

The following patterns are considered failures if they appear without strong mitigating context:

1.  **Atmospheric Mood Pieces:** Rain, fog, or sunset used as the primary hook without a specific physical interaction (e.g., "2B standing in rain" is weak; "2B shaking water from her blindfold" is strong).
2.  **Generic Evasion/Dodging:** Dynamic shots that simply show the character moving sideways/away without specifying *what* they are dodging or *why*.
3.  **Locomotion Filler:** Fullbody shots of walking, stepping over cracks, or jumping barriers where the only purpose is to show legs/movement, not narrative progression (escape/pursuit).
4.  **Passive Contemplation:** Characters standing still, looking at scenery, with no visible cause for their pause.
5.  **Repetitive Sensual Hooks:** Using "outfit adjustment" or "over-the-shoulder look" as the default hook for every Medium/Closeup shot without varying the prop or context.

---

## Micro-Story & Causality Checklist

Before accepting a premise, verify the causal chain:
1.  **Cause:** What specific event triggered this moment? (Must be visible or inferable from physical cues).
2.  **Action/Reaction:** How is the character physically responding? (Active verb required).
3.  **Consequence/Implication:** What does this imply for the next second? (Animation potential).

*Example Check:*
- *Premise:* "2B reaching out to catch a fluttering mechanical butterfly."
- *Cause:* Butterfly is about to land/fall.
- *Action:* Reaching, focusing.
- *Consequence:* Catch or miss.
- *Verdict:* Acceptable, but ensure it doesn't repeat in the batch.

---

## Final Premise Checklist

Before generating prompts, verify:

### Character & Identity
- [ ] Is the character recognizable (face/hair/accessories)?
- [ ] Does the premise respect their specific identity and personality?
- [ ] Are there any factual inventions not supported by the local profile?

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
