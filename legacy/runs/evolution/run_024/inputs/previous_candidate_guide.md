# Viral Premise Guide v2.6 (Candidate) — Cycle 023

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip, or a direct impact.
- **Invalid Causes:** "Mood," "atmosphere," "standing there," or generic "danger" without a specific visual trigger.

### Active vs. Passive Action
The character must be **actively manipulating** the environment or their body in response to the cause.
- **Active (Preferred):** Bracing against force, catching an object, pulling a lever, shielding eyes, stepping over debris, twisting to avoid impact.
- **Passive (Avoid):** Holding breath, tilting head slightly, staring, gripping without resistance, standing still while effects happen around them.

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face (if visible) or silhouette profile
- Hairstyle and hair texture
- Iconic accessories (blindfold, gloves, boots, dress details)
- Clothing design and fit
- Personality flavor

**Factual Identity Safeguards:**
1. **No Invented Anatomy:** Do not add scars, tattoos, or body modifications not present in the character profile.
2. **Consistent Costume Physics:** The dress, gloves, and blindfold must react physically to the action (e.g., fabric tension, sliding straps) rather than floating statically.
3. **Personality Consistency:** A stoic character should show restraint; a playful character should show mischief. Do not force a personality mismatch unless it is part of the specific micro-story conflict.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and proportions
- Elegant body language and confident poses
- Expressive reactions and facial micro-expressions
- Appealing clothing design (fit, tension, fabric interaction)
- Strong composition (diagonals, leading lines, negative space)

**Body Appeal Integration:**
Body emphasis is desirable but must be **functional**. Prominent features (bust, hips, thighs, legs, waist) should contribute to the visual hook when coherent with the action.
- **Good:** Thighs compressed against a wall while bracing; dress hem lifting due to motion revealing leg line; torso twisting causing fabric tension across the chest.
- **Bad:** Cleavage or rear view emphasized solely through camera angle without physical context.

The ideal formula is:
**Attractive Character + Interesting Moment = Memorable Image**

---

## Category Rules & Shot Diversity

To ensure batch-level diversity, each premise must be assigned to one of the following categories. The shot type dictates the primary focus but does not excuse weak storytelling.

1. **Closeup**: Focus on face/upper body. Must show specific facial reaction (strain, surprise, determination) caused by a visible trigger. Avoid generic "looking at viewer."
2. **Medium**: Focus on waist-up or knee-up. Best for showing upper-body dynamics (prying, shielding, adjusting). Ensure hands and arms are doing work.
3. **Fullbody**: Focus on the entire silhouette. Must show weight distribution, leg positioning, and how the whole body interacts with space (crawling, jumping, balancing).
4. **Dynamic**: Focus on motion blur or extreme angles. The character must be in mid-action (leaping, swinging, falling). Implied velocity is key.
5. **Cinematic**: Wide shot establishing context. Must include the environment but keep the character as the clear focal point via lighting or composition. Avoid "wallpaper" energy; there must be a specific event happening within the frame.

**Batch Distribution Requirement:**
For any batch of 20 premises, aim for an even distribution: 4 Closeup, 4 Medium, 4 Fullbody, 4 Dynamic, 4 Cinematic. Adjust slightly if necessary to serve diversity, but do not let one category dominate.

---

## Hard Anti-Pattern Rules (Cycle 023 Corrections)

Based on Cycle 022 failures, the following patterns are strictly limited or prohibited in a single batch:

1. **The "Prying" Cluster:**
   - *Problem:* Repeated use of "prying open jammed panels/doors."
   - *Rule:* Max **2** premises per batch may involve prying/opening stuck metal. If used, vary the object (panel vs. hatch) and the physical strain (one-hand pull vs. two-hand lever).

2. **The "Fluid Blast" Cluster:**
   - *Problem:* Repeated use of "steam/fluid blast causing head tilt."
   - *Rule:* Max **2** premises per batch may involve fluid/steam blasts. If used, vary the reaction: one must be **active dodging**, the other **bracing against pressure**. Do not let both be passive tilts.

3. **Atmospheric Filler:**
   - *Problem:* Dust/sparks/rain as the primary hook instead of character action.
   - *Rule:* Particles (dust, sparks) are secondary effects. They must result from a specific physical interaction (e.g., grinding metal, breaking glass). If removing the particles leaves no story, the premise is weak.

4. **Heavy Door/Hatch Repetition:**
   - *Problem:* Multiple premises involving heavy doors/hatches without variation.
   - *Rule:* Max **2** premises per batch may involve large mechanical structures (doors, hatches). Vary the interaction: pushing vs. hanging vs. climbing.

5. **Passive Gripping:**
   - *Problem:* "Gripping a cable/rope" without visible resistance.
   - *Rule:* If gripping, show the result of the grip: knuckles white, fabric tearing, body swinging, or object slipping.

---

## Batch-Level Diversity Enforcement

To prevent homogeneity, apply these constraints across the entire batch:

1. **Hook Family Limit:** No more than **2** premises should share the same core "hook family" (e.g., wind interaction, mechanical failure, combat dodge).
   - *Examples of Hook Families:*
     - Wind/Gust Interaction
     - Mechanical Jam/Prying
     - Fluid/Steam Exposure
     - Combat/Evasion
     - Climbing/Balancing
     - Discovery/Inspection
2. **Location Variation:** No more than **3** premises should take place in the same specific location type (e.g., "inside a cathedral," "on a rooftop"). Ensure at least 5 distinct environmental contexts per batch of 20.
3. **Emotional Range:** The batch must include a mix of:
   - Stoic/Controlled (4-6 premises)
   - Strained/Effortful (4-6 premises)
   - Surprised/Reactive (4-6 premises)
   - Playful/Mischievous (2-4 premises, if character-appropriate)
4. **Verb Variation:** Track the primary action verb for each premise. Avoid repeating the same verb (e.g., "holding," "looking," "standing") more than 3 times in a batch.

---

## Animation Potential

Every premise should feel like a frozen frame from a 5-10 second video clip.
- **Implied Motion:** The pose must suggest direction of movement. Where is the character coming from? Where are they going?
- **Physics Check:** Does hair, clothing, and debris move logically with the action?
- **Continuity:** Can you easily imagine the 2 seconds before and after this frame? If not, the premise lacks causal clarity.

---

## Final Premise Checklist

Before accepting a premise into the batch, verify:

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
- [ ] **Verb Check:** Have I repeated the primary action verb more than 3 times in this batch?

### Animation & Motion
- [ ] Can this become a short video clip without inventing new actions?
- [ ] Is there implied movement (hair, cloth, debris)?
- [ ] Does the pose suggest a clear direction of force or motion?
