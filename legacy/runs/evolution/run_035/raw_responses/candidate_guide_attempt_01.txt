# Viral Premise Guide v3.7 (Candidate) — Cycle 035

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip, or a deliberate action by the character to secure something.
- **Invalid Causes:** "The wind is blowing," "She looks sad," "It is raining," unless these elements physically interact with the character’s body or equipment in a specific way (e.g., rain soaking her gloves causing her to grip tighter).

---

## Character Identity & Factual Safeguards

Identity is a hard constraint. The character must remain recognizable through:
- Face structure and expression capability.
- Hairstyle and hair physics.
- Iconic accessories (blindfold, gloves, collar, etc.).
- Clothing design and fabric behavior.
- Silhouette and proportions.

**Factual Identity Safeguards:**
1. **No Canon Invention**: Do not introduce props, weapons, or abilities not present in the character's established profile unless explicitly part of a "what-if" scenario clearly marked as such (but for standard datasets, stick to known gear).
2. **Silhouette Integrity**: The character’s unique shape must be readable from 10 feet away. If the pose hides the iconic silhouette (e.g., hugging knees completely), it is weak.
3. **Personality Consistency**: A stoic character should not scream unless the cause justifies extreme shock. A playful character should not look terrified unless the threat is immediate and physical.

---

## Visual Appeal & Body Language

Visual attractiveness is an intentional component of the dataset. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

**Body As A Hook, Not The Entire Premise:**
- **Integrated Sensuality**: Prominent bust, defined waist, strong hips, and legs should be emphasized through *action* (twisting, leaning, stretching) rather than static posing.
- **Clothing Tension**: Use clothing to show body shape. Fitted fabric pulling tight during a reach or twist is more dynamic than loose clothing hanging on a static figure.
- **Weight Distribution**: Show the physics of the body. Weight on one leg creates a natural hip shift and knee bend that adds visual interest and realism.

**Avoid:**
- "Pinup" poses where the character exists only to be looked at, with no interaction with the world.
- Over-emphasis on cleavage or rear view without a narrative reason (e.g., bending over to pick something up is valid; bending over for no reason is not).

---

## Batch-Level Diversity Enforcement

To prevent monotony within a set of 20 premises, apply these hard limits:

1. **Max 2 per Hook Family**:
   - *Hook Families*: Wind/Hair, Rain/Water, Combat/Action, Mechanical/Tech, Environmental Hazard (fire/smoke), Intimate/Personal Space.
   - No more than two premises in a batch can rely on the same primary visual mechanic.

2. **Verb Uniqueness**:
   - The primary action verb must be unique across the batch where possible. If a verb is repeated (e.g., "reach"), the *object* and *consequence* must be significantly different.
   - Avoid repeating verbs like "stand," "look," or "walk" as the primary descriptor.

3. **Location Distinctness**:
   - No two premises in the same batch should share the exact same location type (e.g., "inside a cathedral" vs. "outside a cathedral" are distinct; "ruined city street A" and "ruined city street B" are near-duplicates if the visual props are identical).

4. **Emotional Range**:
   - The batch must cover at least 5 distinct emotional states (e.g., Focus, Surprise, Irritation, Determination, Fear, Playfulness). Do not default to "Neutral/Serious" for more than 3 premises.

---

## Category Rules & Composition Guidelines

Each category has a specific purpose and constraint:

### Closeup
- **Focus**: Micro-expression + physical sensation.
- **Rule**: Must show a reaction to an immediate, tactile cause (e.g., dust in eye, fabric snagging, heat from machine).
- **Avoid**: Generic "smiling at camera" or "looking away thoughtfully."

### Medium
- **Focus**: Body mechanics reacting to environment.
- **Rule**: The torso and limbs must be engaged with an object or force. Show the *effort* of the action.
- **Avoid**: Standing still in a nice outfit. The body must be doing something (reaching, bracing against force, adjusting gear).

### Fullbody
- **Focus**: Weight distribution/balance challenge.
- **Rule**: Must show the full silhouette and how it interacts with space. Is she balancing on one foot? Leaning into wind? Crouching low to avoid debris?
- **Avoid**: "Standing in a field." The pose must imply an imbalance or specific spatial relationship that requires active correction.

### Dynamic
- **Focus**: Distinct motion verb + blur/trail implication.
- **Rule**: Must capture the *peak* of an action (mid-air, mid-turn, mid-slide). Use motion lines or hair/cloth flow to indicate speed.
- **Avoid**: Slow-motion walking. The energy must be high and immediate.

### Cinematic
- **Focus**: Character active within scale/contrast.
- **Rule**: The character is small in the frame but *active* against a large background element (climbing, escaping, signaling). The environment provides context, not just backdrop.
- **Avoid**: Silhouette against sunset with no action. The character must be interacting with the scale of the world.

---

## Hard Anti-Pattern Rules

If a premise violates any of these, it is rejected:

1. **The "Cathedral/Ruin" Default**: Do not use ruined cities, cathedrals, or ancient ruins as the *primary* hook unless there is a specific mechanical hazard (falling brick, steam vent) interacting with the character.
2. **Passive Bracing**: Standing with hands on hips or arms crossed without a visible threat or cause is weak.
3. **Atmospheric Filler**: Rain, fog, snow, or dust must physically affect the character (soaking gloves, obscuring vision, slipping feet). If it can be removed from the prompt without changing the pose’s logic, it is filler.
4. **Direct Gaze Overuse**: Direct eye contact with the viewer should appear max 1 time per batch of 20. It breaks immersion if overused.
5. **Locomotion Without Stake**: Walking or running must have a destination or threat. "Running through a park" is weak; "Sprinting away from a collapsing bridge" is strong.

---

## Micro-Story & Animation Potential

Every premise should feel like a frame from a larger moment.

**The 5-Second Test:**
Can this image be animated into a 5–10 second clip without inventing new actions?
- *Yes*: The cause (wind) is visible, the reaction (holding hair back) is active, and the next step (turning head to look at source) is implied.
- *No*: The character is standing still with no clear trigger. To animate it, you would need to invent a new event from scratch.

**Causality Chain:**
1. **Cause**: Visible object/force/event.
2. **Action**: Character’s physical response.
3. **Consequence**: What changes because of the action (outfit shifts, expression changes, position alters).

---

## Final Premise Checklist

Before accepting a premise into the batch, verify:

### Identity & Facts
- [ ] Is the character recognizable by silhouette and key accessories?
- [ ] Are there any factual errors in gear or appearance?
- [ ] Does the personality match the reaction intensity?

### Visual Appeal
- [ ] Is the body language intentional and attractive (not just neutral)?
- [ ] Is clothing interacting with the body/force to show shape?
- [ ] Is the composition visually balanced but dynamic?

### Hook & Causality
- [ ] Is there a visible cause for the current state?
- [ ] Is the action active (verb-driven) rather than passive (state-driven)?
- [ ] Does the premise answer "Why is she doing this?" without text?

### Diversity & Repetition Control (Batch Level)
- [ ] Does this premise violate the **"Max 2 per Hook Family"** rule in the current batch?
- [ ] Have I repeated the primary action verb more than **4** times in this batch?
- [ ] Is the location distinct from the previous 3 premises and unique within the batch?
- [ ] Is the emotional state different from at least 5 other premises in the batch?
- [ ] Are there any exact duplicates or near-duplicates (same mechanic, same prop)?

### Category Compliance
- [ ] **Closeup**: Micro-expression + physical sensation present?
- [ ] **Medium**: Body mechanics reacting to environment (not just bracing)?
- [ ] **Fullbody**: Weight distribution/balance challenge visible with specific cause?
- [ ] **Dynamic**: Distinct motion verb used (not repeated from other dynamics)?
- [ ] **Cinematic**: Character active within scale/contrast (not just silhouette)?

### Final Quality Gate
- [ ] No static bracing without secondary movement.
- [ ] No invisible causes.
- [ ] No generic locomotion without stake.
- [ ] Direct gaze used max 1 time in batch (if at all).
- [ ] Can this be animated into a 5–10 second clip?

If any box is unchecked, rewrite the premise to add specificity, causality, or active motion.
