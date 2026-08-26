# Viral Premise Guide v3.2 (Candidate) — Cycle 030

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip, or a direct hit from debris.
- **Invalid Causes:** "Mood," "atmosphere," "contemplation," "waiting," or generic "danger."

---

## Character Identity Priority

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face and hairstyle (including iconic elements like blindfolds, buns, or specific hair textures).
- Iconic accessories (gloves, stockings, dress details, weapon design if visible).
- Silhouette and body language consistent with their canonical temperament.

**Factual Identity Safeguards:**
1. **No Invented Traits:** Do not add scars, tattoos, piercings, or clothing items not present in the local character profile unless explicitly stated as a "variant."
2. **Canon Balance:** The premise should feel authentic to the character without recreating an official-looking scene. If action or combat is present, it must contain a distinct character-focused hook (e.g., a specific reaction or pose), not just generic gameplay energy.
3. **Personality Filter:** The reaction must match the character’s core personality. A stoic character does not scream; they tighten their jaw. A playful character does not freeze in terror; they smirk despite the danger.

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset. It is one of the primary reasons a viewer stops scrolling. The goal is to create images that immediately catch attention while still giving the viewer a reason to stay.

Do not intentionally minimize attractive character features when they are part of the character design. Characters may intentionally emphasize:
- Feminine silhouette and attractive proportions.
- Elegant body language and confident poses.
- Expressive reactions and appealing clothing design.
- Strong composition that guides the eye to the face or key action point.

**Body Appeal Integration:**
Body emphasis is desirable but must be contextualized by the action. Prominent curves, fitted clothing tension, and strong silhouettes contribute to the visual hook when coherent with the character and composition.
- **Desirable Elements:** Defined waist, strong hips, emphasized legs/thighs, torso twists, weight shifts, leaning, stretching, crouching, bending naturally as part of an action.
- **Integration Rule:** Body language should feel intentional. A pose should communicate confidence, curiosity, playfulness, elegance, shyness, attitude, or emotion *through* the physical interaction with the environment or object.

**The "Attraction-Forward" Standard:**
At least 60% of premises in a batch must be **attraction-forward**. This means the visual appeal is not just background; it is the primary reason for the stop-scroll effect, integrated with the action. The character’s silhouette and expression are the focal point, supported by the situation.

---

## Hard Anti-Pattern Rules (Cycle 030 Corrections)

Based on Cycle 029 failures, the following patterns are **strictly prohibited** or limited:

1. **Static Bracing/Support:**
   - *Prohibited:* Leaning against a wall/floor solely to "hold" something or "brace" for impact without an active secondary movement (e.g., reaching, dodging, adjusting gear).
   - *Correction:* Replace with active evasion or manipulation of the force. If bracing is necessary, show the character actively shifting weight or preparing to move.

2. **Wind/Air Current Monoculture:**
   - *Limit:* Maximum **2** premises in a batch may use wind/gusts/air currents as the primary causal hook.
   - *Correction:* Introduce varied physical interactions: water splashes, magnetic fields, biological elements (vines, insects), thermal expansion, mechanical failure, or direct object collision.

3. **Debris/Dust Atmosphere:**
   - *Limit:* Maximum **2** premises in a batch may rely primarily on dust/debris clouds for visual interest.
   - *Correction:* Debris must be a specific threat (e.g., "dodging a falling beam") rather than ambient mood ("standing in dusty ruins").

4. **Generic Locomotion:**
   - *Prohibited:* Walking, balancing, or climbing without a clear destination, immediate threat, or narrative stake.
   - *Correction:* Full-body premises must have a specific goal (escaping a fire, reaching a ledge, avoiding a trap) or hazard.

5. **Passive Observation/Inspection:**
   - *Prohibited:* Close-ups of the character looking at an object/dust/mirror without a physical reaction to it.
   - *Correction:* Show the moment of impact, the adjustment, or the sudden realization (e.g., hand flinching away from heat, eyes widening as a reflection shifts).

---

## Batch-Level Diversity Enforcement

To prevent repetition clusters, apply these quantitative limits per 20-premise batch:

1. **Hook Family Limit:** No more than **2** premises may share the same primary hook mechanic (e.g., "wind," "mirror," "water splash," "outfit adjustment").
   - *Examples of Hook Families:*
     - Air/Wind/Gusts
     - Liquid/Splash/Steam
     - Mechanical/Moving Parts
     - Biological/Nature Interaction
     - Optical/Reflection/Light Play
     - Physical Impact/Collision

2. **Location Limit:** No more than **3** premises may share the same specific location type (e.g., "industrial interior," "forest exterior," "urban ruin").
   - *Correction:* If using "industrial," vary it significantly: one in a boiler room, one on a catwalk, one inside a machine housing.

3. **Verb Limit:** No primary action verb (e.g., "dodging," "leaning," "grabbing") may appear as the core action in more than **4** premises across the batch.
   - *Note:* This applies to the *primary* physical action, not incidental verbs.

4. **Emotion/Expression Limit:** No more than **3** premises should share the same primary emotional expression (e.g., "determined," "surprised," "playful"). Ensure a mix of stoic, playful, fierce, vulnerable, and focused expressions.

5. **Category Balance:**
   - **Closeup:** Must show active micro-reactions (blink, flinch, adjust, catch breath) rather than static gaze.
   - **Medium:** Must show interaction with an object or immediate environment (holding, pushing, pulling, ducking).
   - **Fullbody:** Must show dynamic pose with clear weight distribution and directional intent.
   - **Dynamic:** Must capture mid-action momentum (blur, extension, impact).
   - **Cinematic:** Must use scale/composition to amplify a specific character moment, not just scenery.

---

## Causal Premise Requirements

Every premise must answer: **"Why is this happening right now?"**

The cause must be visible or immediately inferable from the frame:
- **Physical Trigger:** A falling object, a breaking cable, a sudden gust, a splash of water, a mechanical arm extending.
- **Environmental Change:** Lighting shift revealing something, temperature change causing condensation/steam, gravity shift.
- **Internal Reaction to External Stimulus:** The character’s pose must be a direct response to the trigger.

**Test:** If you remove the background/environment, does the premise still make sense? If yes, it is likely too abstract or atmospheric. The environment must provide the *cause* for the action.

---

## Category Rules

### Closeup
- **Focus:** Face, eyes, hands, or immediate upper body detail.
- **Requirement:** Must show a micro-reaction to an external stimulus.
  - *Good:* Eyes widening as a drop of water lands on her cheek; fingers tightening around a hilt as a vibration runs through the weapon.
  - *Bad:* Simply looking at the camera with a serious expression.

### Medium
- **Focus:** Waist-up or three-quarter body.
- **Requirement:** Must show interaction with an object or immediate space.
  - *Good:* Adjusting a glove while dodging a spark; leaning forward to catch a falling item.
  - *Bad:* Standing still with hands on hips in a generic pose.

### Fullbody
- **Focus:** Entire body and relationship to the environment.
- **Requirement:** Must show dynamic weight distribution and directional intent.
  - *Good:* Crouching low to slide under a beam; stretching upward to reach a ledge while balancing on one foot.
  - *Bad:* Standing upright in a neutral stance.

### Dynamic
- **Focus:** Motion, speed, impact.
- **Requirement:** Must capture mid-action momentum. Use blur, extended limbs, or debris displacement.
  - *Good:* Mid-leap with dress flaring; spinning to strike; diving for cover.
  - *Bad:* A static pose that *implies* motion but lacks visual evidence of it (e.g., "about to jump").

### Cinematic
- **Focus:** Scale, composition, atmosphere supporting the character.
- **Requirement:** Must use wide angle or unique perspective to amplify a specific character moment. The environment is secondary to the character’s action.
  - *Good:* Low-angle shot looking up at 2B standing on a tilting platform, emphasizing her stability against the chaos.
  - *Bad:* Wide landscape with tiny character in distance (wallpaper energy).

---

## Acceptance Checklist

Before generating prompts for a batch, verify each premise against this checklist:

### Character & Identity
- [ ] Is the character recognizable through specific traits (hair, eyes, outfit)?
- [ ] Does the personality match the reaction? (Stoic = controlled; Playful = expressive).
- [ ] Are there any invented factual elements not in the local profile?

### Visual Appeal
- [ ] Is the composition leading the eye to the character’s face or key action point?
- [ ] Is body appeal integrated into the pose/action (not just static)?
- [ ] Is the visual hook specific and readable at a glance?
- [ ] **Attraction-Forward Check:** Does this premise prioritize the character’s visual presence over the environment?

### Causality & Story
- [ ] **Cause:** What specific event triggered this moment? (Must be visible/inferable).
- [ ] **Reaction:** How is the character physically responding actively?
- [ ] **Consequence:** Is there a secondary visual effect (clothing shift, object movement, hair displacement)?
- [ ] Would the viewer ask "What happens next?"

### Diversity & Repetition Control
- [ ] Does this premise violate the **"Max 2 per Hook Family"** rule in the current batch?
- [ ] Have I repeated the primary action verb more than **4** times in this batch
