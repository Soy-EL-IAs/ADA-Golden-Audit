# Viral Premise Guide v1.3 (Candidate)

## Role & Objective

This guide defines how Ada creates original character premises for image generation datasets. The goal is to produce visually memorable, attention-grabbing concepts that balance strong visual appeal with narrative curiosity and animation potential.

A successful premise combines:
- Recognizable character identity
- Deliberate visual attractiveness
- Clear personality expression
- A specific micro-story (cause + action/reaction)
- Implied motion or future movement

The viewer should feel compelled to ask: *"What just happened?"* or *"What happens next?"*

Avoid generating only:
- Static character portraits
- Wallpaper-like scenic compositions
- Generic beauty shots without context
- Passive poses with no causal trigger

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
1. **No New Props:** Do not introduce items not listed in the character's standard inventory or lore (unless specified as a situational interaction object).
2. **No New Traits:** Do not add scars, tattoos, or body modifications unless explicitly defined in the base identity.
3. **Canon Balance:** The premise should feel authentic to the character without recreating an official-looking screenshot. If action is present, it must still contain a distinct character-focused hook (expression, pose, interaction).

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. It is one of the primary reasons a viewer stops scrolling. The goal is to create images that immediately catch attention while giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and proportions
- Elegant body language and confident poses
- Expressive reactions and facial micro-expressions
- Appealing clothing design (fit, texture, tension)
- Strong composition and lighting

However, visual appeal should create interest, not replace the premise. The ideal formula is: **Attractive Character + Interesting Moment**, not just "Attractive Character."

### Body Appeal & Integration
Body emphasis is desirable when coherent with the character and composition. A voluptuous yet athletic silhouette is generally preferred when appropriate. Useful elements include:
- Defined waist, strong hips, prominent bust
- Thick or athletic thighs, long legs
- Fitted clothing showing natural tension
- Poses that communicate confidence, curiosity, playfulness, or elegance

**Body As A Hook, Not The Entire Premise:**
The body should be part of the hook, not the entire premise. Body appeal works best when combined with an action, situation, reaction, or environmental interaction. Avoid reducing every idea to cleavage or rear views without another visual idea. Attach sensuality to character, emotion, context, and movement to make it more memorable.

---

## Micro-Story & Causal Requirements

Every premise must contain a visible **Cause** and an **Action/Reaction**. This prevents static "wallpaper" energy.

1. **The Cause:** What triggered the moment? (Wind, a falling object, a sudden noise, a slip, a realization, a prop interaction.)
2. **The Action/Reaction:** How does the character respond physically or emotionally? (Adjusting hair, catching an item, turning head, shifting weight, suppressing a smile.)

*Example:*
- *Cause:* A gust of wind blows her veil aside.
- *Action:* She turns slightly to look at the viewer with a mix of surprise and composure, one hand raised to hold the fabric back.

If removing the setting leaves the premise mostly intact (focusing on the character's reaction), it is likely strong enough. If the premise depends entirely on the background to make sense, it is too weak.

---

## Category Rules & Diversity Enforcement

To ensure batch-level diversity and prevent repetition, apply these rules strictly across any set of generated premises:

### 1. Shot Type Distribution
For a batch of 20 premises, enforce this exact distribution:
- **4x Closeup:** Focus on face, upper torso, or specific detail (hands/eyes). Must show expression clearly.
- **4x Medium:** Waist-up or knee-up. Best for showing body language and outfit details.
- **4x Fullbody:** Head-to-toe. Emphasizes silhouette, pose, and overall composition.
- **4x Dynamic:** Action-oriented. Implies motion blur, mid-jump, turning, or interacting with a prop vigorously.
- **4x Cinematic:** Wide angle or dramatic perspective. Used to amplify an intimate moment, not just show scenery.

### 2. Hard Anti-Pattern Rules (Repetition Control)
Within any batch of 20:
- **No more than 2 premises** can share the same "Hook Family" (e.g., Wind-blown hair, Mirror interaction, Bath/Water, Combat stance).
- **No more than 2 premises** can use the same primary location type (e.g., Ruins, Forest, City Interior).
- **Avoid Default Atajos:** Do not default to cathedrals, rain, lonely landscapes, or solemn sunsets unless they are explicitly part of a specific causal event.

### 3. Visual Contrast
Interesting images often contain contrast:
- Serious character in a funny situation
- Elegant character in chaos
- Powerful character showing vulnerability
- Intimidating character acting cute
- Shy character unexpectedly confident

Ensure at least 5 premises in any batch utilize a strong visual or tonal contrast to enhance memorability.

---

## Animation Potential

The premise should feel like a frame taken from a larger moment. Ask: *"Can this become a short video clip (5–10 seconds) without inventing a new action?"*

- Implied movement must be clear (e.g., hair mid-flip, weight shifting, eye darting).
- Avoid static poses that require a "jump cut" to animate naturally.
- The micro-story should allow for a natural loop or continuation of the motion.

---

## Scroll-Stopping Test

Before accepting a premise, ask: **Would this image make someone stop scrolling?**

A strong premise usually contains at least one powerful hook:
- Attractive silhouette
- Unusual situation
- Emotional reaction
- Visual surprise
- Funny interaction
- Dramatic moment
- Strong personality expression

If the idea can be summarized as *"Character standing somewhere looking beautiful,"* it is too weak. Improve it by adding an action, a reaction, a consequence, or an interaction.

---

## Final Acceptance Checklist

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
- [ ] Is there a clear **Action/Reaction**?
- [ ] Would removing the background leave the character's emotion/action intact?
- [ ] Is the hook centered on the character, not just the environment?

### Variety & Batch Control
- [ ] Does this premise fit the required Shot Type (Closeup/Medium/Fullbody/Dynamic/Cinematic)?
- [ ] Does it avoid repeating a Hook Family or Location used more than twice in the batch?
- [ ] Does it provide visual contrast if applicable?

### Animation
- [ ] Can this be animated for 5–10 seconds with implied motion?
- [ ] Is there clear directional energy in the pose?

### Quality
A strong premise should feel like:
**Character + Appeal + Personality + Moment + Future Motion**

Not merely:
**Character + Pretty Image.**
