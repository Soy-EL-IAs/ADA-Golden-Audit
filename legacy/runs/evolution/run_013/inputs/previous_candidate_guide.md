# Viral Premise Guide v1.5 (Candidate)

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

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face and hairstyle
- Iconic accessories and clothing design
- Silhouette and posture habits
- Personality flavor and characteristic visual traits

Do not replace the character with a generic attractive person. The goal is **"an attractive and interesting version of this character,"** not "a random attractive character using the same aesthetic."

### Factual Identity Safeguards
To prevent hallucination, adhere strictly to the local character profile:
1. **No New Props:** Do not introduce weapons, tools, or items unless explicitly listed in the character profile.
2. **Clothing Consistency:** Maintain canonical clothing cuts and colors. If clothing is damaged/disrupted, it must be consistent with the cause (e.g., steam burns, tear from snagging).
3. **Accessory Integrity:** Iconic accessories (blindfolds, gloves, ribbons) should remain present unless a specific narrative reason explains their absence or displacement.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and attractive proportions
- Elegant body language and confident poses
- Expressive reactions and appealing clothing design
- Strong composition and lighting

However, **visual appeal should create interest, not replace the premise.** The ideal formula is:
**Attractive Character + Interesting Moment**

Not merely: **Attractive Character Only.**

### Body As A Hook, Not The Entire Premise
Body emphasis is desirable when coherent with the character and composition. Prominent bust, hips, thighs, legs, and a defined waist may intentionally contribute to the visual hook. Use body language to communicate confidence, curiosity, playfulness, elegance, or emotion.

Avoid reducing every idea to:
- Cleavage
- Rear view
- Low viewpoint
- Large breasts/buttocks

...without another visual idea (action, reaction, prop interaction). The purpose is to make sensuality more memorable by attaching it to character, emotion, context, and movement.

---

## Hard Anti-Pattern Rules

These patterns have shown high repetition rates in previous cycles. They are **prohibited** as primary hooks unless heavily modified:

1.  **"Standing Firm" on a Platform/Ledge:** The character standing still on a high vantage point with machinery/background moving behind them is considered *passive*. If used, the character must be actively interacting (climbing, slipping, catching something).
2.  **Generic Industrial Hazards:** Steam, sparks, and gears are valid only if they have a specific source and consequence for the character (e.g., "steam jet pushing her hair into her face," "spark singeing her sleeve"). Do not use them as generic background noise.
3.  **Bracing/Gripping/Balancing:** Using "gripping the edge" or "balancing on one leg" as the sole action is too static. These must be part of a larger motion (e.g., "gripping while swinging," "balancing to avoid falling into specific hazard").
4.  **Cathedral/Ruin/Rain Contemplation:** Avoid solemn, lonely landscapes unless the character is actively navigating them. No passive scenic poses.
5.  **Direct Smirk at Viewer:** While effective, using a direct eye-contact smirk as the primary hook in more than 2 premises per batch is repetitive. Vary with sidelong glances, profile views, or eyes closed/focused on action.

---

## Batch-Level Diversity Enforcement

To prevent the model from falling into narrow local optima (e.g., all cinematic shots being low-angle standing poses), apply these quantitative limits to any batch of 20 premises:

1.  **Hook Family Limit:** No more than **2** premises may share the same primary hook family (e.g., "outfit adjustment," "mirror interaction," "slip/fall").
2.  **Location Limit:** No more than **3** premises should take place in the same general location type (e.g., "industrial interior," "forest exterior").
3.  **Emotional Register Variety:** The batch must include at least **4 distinct emotional registers**. Examples: Tension, Playfulness, Determination, Frustration, Surprise, Serenity. Do not rely solely on "Tension/Composure."
4.  **Action Verb Variety:** Ensure no single action verb (e.g., "standing," "gripping") is the primary descriptor for more than 3 premises in the batch.

---

## Category Rules & Shot Types

Each shot type has a specific narrative function. Do not use them interchangeably.

### Closeup
- **Focus:** Face, eyes, or upper chest.
- **Purpose:** Intimacy, immediate reaction, detail of emotion.
- **Requirement:** Must show a micro-expression change (squint, breath catch, eye widen) caused by an immediate stimulus. Avoid generic "pretty face" shots.

### Medium
- **Focus:** Waist-up or three-quarter body.
- **Purpose:** Interaction with props, mid-range action, social dynamics.
- **Requirement:** Must show the character’s hands interacting with something (holding a tool, pushing an object, adjusting clothing) or engaging in a specific gesture. Avoid static "standing" poses.

### Fullbody
- **Focus:** Entire body and immediate surroundings.
- **Purpose:** Silhouette, posture, spatial relationship to environment.
- **Requirement:** Must show weight distribution, balance, or locomotion (stepping, crouching, stretching). The pose must imply directionality or effort. Avoid "fashion model" standing poses unless interacting with the environment.

### Dynamic
- **Focus:** Motion blur, speed lines, or extreme angles.
- **Purpose:** High energy, combat, evasion, rapid movement.
- **Requirement:** Must show a clear vector of motion (dodging left, leaping up). The character should be mid-action, not starting or ending the action.

### Cinematic
- **Focus:** Wide angle, environmental scale, dramatic lighting.
- **Purpose:** Establishing stakes, epic moments, contrast between small character and large world.
- **Requirement:** Despite being wide, the character must be **active**. Avoid "standing on a ledge watching gears turn." Instead: "climbing out of a pit," "sliding down a wall to avoid debris," or "struggling against a massive force." The environment should threaten or support the action, not just decorate it.

---

## Micro-Story & Animation Potential

A strong premise is a frame from a larger moment. It must be animatable into a 5–10 second clip without inventing new actions.

### Causal Chain
The image must answer:
1.  **What happened?** (Cause)
2.  **What is happening now?** (Action/Reaction)
3.  **What will happen next?** (Implied Future Motion)

### Animation Test
If you were to animate this image for 5 seconds, would the movement feel natural and continuous?
-   *Good:* Character slipping → catching ledge → pulling up.
-   *Bad:* Character standing still → wind blows hair → character blinks. (Too low energy for "animation potential" unless specifically a mood piece).

---

## Final Premise Checklist

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
