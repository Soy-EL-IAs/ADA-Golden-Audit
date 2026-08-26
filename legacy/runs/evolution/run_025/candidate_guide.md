# Viral Premise Guide v2.7 (Candidate) — Cycle 025

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip/trip event, or a deliberate character decision to interact with a prop.
- **Invalid Causes:** "Mysterious energy," "atmospheric tension," "general chaos," or vague environmental vibes that do not physically impact the character’s body or clothing in this specific frame.

**Rule:** If you cannot point to a specific object, force, or action in the prompt that *caused* the current pose/expression, rewrite it.

---

## Character Identity Priority

Every premise must preserve the identity of the original character using only **supported facts** from the local profile.

The character should remain recognizable through:
- Face structure and expression style.
- Hairstyle (including specific details like blindfolds if applicable).
- Iconic accessories (weapons, ribbons, gloves).
- Clothing design and fabric behavior.
- Silhouette and proportions.
- Personality flavor in body language.

**Factual Identity Safeguard:**
Do not introduce scars, tattoos, costume changes, or physical traits not present in the local character profile. If the profile specifies "blindfolded," do not remove it unless the specific cause of the action involves removing/adjusting it. If the profile specifies "white hair," do not change color for artistic effect unless lighting dictates a temporary tint (e.g., neon reflection).

---

## Visual Appeal Philosophy

Visual attractiveness is an intentional component of the dataset, but it must be **integrated**, not isolated.

The goal is to create images that immediately catch attention while giving the viewer a reason to stay. Do not intentionally minimize attractive character features when they are part of the design, but do not let them replace the narrative hook.

**Integration Rule:**
Body appeal should serve the action. For example:
- *Bad:* "She poses with hands on hips." (Static)
- *Good:* "She leans back to avoid a swinging pipe, her torso twisting and emphasizing her waistline while her dress hem lifts due to the momentum." (Action-driven)

Characters may intentionally emphasize:
- Feminine silhouette and proportions.
- Elegant body language and confident poses.
- Expressive reactions that highlight facial features.
- Appealing clothing design under tension or movement.

**The Ideal Formula:**
Attractive Character + Interesting Moment = **Scroll Stopper**.
Attractive Character Alone = **Wallpaper Risk**.

---

## Body Appeal & Composition

Body emphasis is desirable when coherent with the character and composition. A voluptuous yet athletic silhouette is generally effective for stopping the scroll.

**Useful Visual Elements:**
- Prominent bust, defined waist, strong hips, prominent buttocks, thick/athletic thighs.
- Long or emphasized legs (especially in dynamic angles).
- Fitted clothing showing tension or strain during movement.
- Torso twists, weight shifts, leaning, stretching, crouching, bending naturally as part of an action.

**Body Language Intent:**
A pose should communicate confidence, curiosity, playfulness, elegance, shyness, attitude, or emotion. Avoid generic "power posing" that lacks context. The body must be *doing* something or *reacting* to something.

---

## Body As A Hook, Not The Entire Premise

The body is a vehicle for the story, not the sole subject.

Body appeal works best when combined with:
- An action (pulling, pushing, dodging).
- A situation (narrow space, high altitude, slippery surface).
- A reaction (flinching, smiling through strain, focusing intensely).
- Environmental interaction (wind, gravity, friction).

**Avoid reducing every idea to:**
- Cleavage or rear view without context.
- Low viewpoint angles solely for silhouette emphasis.
- "Large breasts/buttocks" as the only descriptor of appeal.

Attach sensuality to character, emotion, context, and movement to make it memorable.

---

## Hard Anti-Pattern Rules (Cycle 025 Corrections)

Based on Cycle 023 failures, the following patterns are **prohibited** or **strictly limited**:

### 1. The "Mechanical Jam" Cluster
In Cycle 023, multiple premises involved prying, pulling cables, or twisting valves.
- **Rule:** Limit primary interactions with machinery (prying, turning wheels, pulling levers) to a maximum of **2** per batch.
- **Correction:** Use biological, environmental, or social interactions instead (e.g., dodging a falling plant, catching a dropped item, reacting to a sound).

### 2. The "Fluid/Steam" Overuse
Cycle 023 relied heavily on steam blasts and fluid leaks as generic causes.
- **Rule:** Limit "steam/fluid explosion" as the primary visual hook to **1** per batch.
- **Correction:** If using fluids, specify *why* (e.g., "coolant spray from a specific broken pipe") rather than generic "mist."

### 3. The "Precairous Balance" Trap
Cycle 023 featured multiple balancing/climbing scenes that felt repetitive and lacked unique narrative stakes.
- **Rule:** Limit "balancing on a beam/edge" to **1** per batch, unless the *reason* for the balance is highly specific (e.g., rescuing a pet, retrieving a key item).
- **Correction:** Prefer grounded actions with dynamic weight shifts over static hanging/balancing poses.

### 4. Atmospheric Wallpaper
Cinematic shots in Cycle 023 risked becoming scenic views.
- **Rule:** Every Cinematic shot must contain a **distinct narrative event** involving the character’s body or immediate prop interaction. The background is support, not subject.

---

## Batch-Level Diversity Enforcement

To prevent repetition within a single generation run (e.g., 20 premises), apply these strict quotas:

1. **Hook Family Limit:** No more than **2** premises may share the same primary hook family (e.g., "Wind Interaction," "Mechanical Jam," "Dodge/Leap").
2. **Verb Diversity Check:** The primary action verb (e.g., *prying, pulling, twisting, dodging*) must not appear as the main descriptor more than **3** times in the entire batch.
3. **Location Rotation:** Do not use the same specific location type (e.g., "Industrial Shaft," "Cathedral Ruin") for more than **2** premises unless the angle and interaction are radically different.
4. **Emotional Range:** Ensure the batch includes at least:
   - 1 premise of *Playful/Mischievous* energy.
   - 1 premise of *Stoic/Controlled* tension.
   - 1 premise of *Surprised/Reactive* shock.
   - 1 premise of *Focused/Determined* action.

---

## Category Rules

### Closeup (4 per batch)
- **Focus:** Face, expression, and immediate prop interaction near the head/chest.
- **Requirement:** Must show a specific micro-reaction to a cause (e.g., flinching from a spark, squinting at light).
- **Avoid:** Generic "looking at viewer" or passive beauty shots.

### Medium (4 per batch)
- **Focus:** Torso and upper legs; clear body language and clothing interaction.
- **Requirement:** Must show the character’s center of gravity shifting in response to a force.
- **Avoid:** Standing straight with arms at sides.

### Fullbody (4 per batch)
- **Focus:** Entire silhouette, limb placement, and relationship to the environment.
- **Requirement:** Must demonstrate weight distribution or dynamic tension (e.g., one leg planted firmly, other raised).
- **Avoid:** Symmetrical, static standing poses.

### Dynamic (4 per batch)
- **Focus:** Motion blur, extreme angles, mid-action freeze-frame.
- **Requirement:** Must capture a moment of peak kinetic energy (mid-jump, mid-slide, mid-dodge).
- **Avoid:** "Running in place" or generic combat stances without context.

### Cinematic (4 per batch)
- **Focus:** Wide composition with depth, but character-centered narrative event.
- **Requirement:** Must include a specific environmental interaction that affects the character’s pose or expression. The background must frame the action, not replace it.
- **Avoid:** Scenic vistas where the character is small and passive.

---

## Micro-Story & Animation Potential

Every premise should function as a "frame from a larger moment."

**Causal Chain Requirement:**
1. **Trigger:** What happened immediately before? (Visible or inferable).
2. **Action:** What is the character doing *now* in response?
3. **Consequence:** What will happen next if they fail/succeed?

**Animation Test:**
Can this premise be animated into a 5–10 second clip without inventing new actions?
- *Yes:* "She dodges a falling brick" → Clip: Brick falls, she ducks, brick hits ground.
- *No:* "She looks sad in the rain" → Clip requires added context or action to avoid being static.

---

## Final Acceptance Checklist

Before accepting a premise for inclusion in the batch, verify:

### Character & Identity
- [ ] Is the character recognizable via supported profile traits?
- [ ] Are there no factual drifts (unlisted scars, wrong hair color)?
- [ ] Does the personality match the reaction (e.g., stoic character doesn't scream unless justified)?

### Visual Appeal & Composition
- [ ] Is the composition dynamic (diagonal lines, leading eyes)?
- [ ] Is body appeal integrated into the action/pose?
- [ ] Does the lighting highlight features and mood without flattening depth?

### Hook & Story (Causality)
- [ ] **Cause:** What specific event triggered this moment? (Must be visible or inferable).
- [ ] **Reaction:** How is the character physically/emotionally responding?
- [ ] **Consequence:** Is there a secondary effect (clothing shift, object movement)?
- [ ] Would the viewer ask "What happens next?"

### Diversity & Repetition Control
- [ ] Does this premise violate the **"Max 2 per Hook Family"** rule?
- [ ] Have I repeated the primary action verb more than **3** times in this batch?
- [ ] Is the location distinct from previous premises in the sequence?
- [ ] If using "balancing" or "prying," have I hit the limit for that specific mechanic?

### Animation & Motion
- [ ] Can this become a short video clip without inventing new actions?
- [ ] Is there implied movement (hair, cloth, debris)?
- [ ] Does the pose suggest a clear direction of force or motion?

---

## Quality Standard

A strong premise should feel like:

**Character + Appeal + Personality + Moment + Future Motion**

Not merely:

**Character + Pretty Image.**
