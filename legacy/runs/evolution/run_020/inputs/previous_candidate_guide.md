# Viral Premise Guide v2.2 (Candidate) — Cycle 019

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

- **Valid Causes:** A specific object falling, a machine malfunctioning, a sudden change in lighting/temperature, an interaction with another entity (even off-screen), a physical obstacle requiring navigation, a slip, a catch, a dodge, a specific prop interaction.
- **Invalid Causes:** "Vibration" without a source, "invisible wind," general "danger," or abstract emotional shifts without physical manifestation.

---

## Character Identity Priority & Factual Safeguards

Every premise must preserve the identity of the original character. The character should remain recognizable through:
- Face (or blindfold/eye mask if applicable)
- Hairstyle and hair accessories
- Iconic accessories (gloves, ribbons, weapons)
- Clothing design and silhouette
- Personality flavor

**Factual Identity Safeguards:**
1. **No Canon Invention**: Do not introduce items, colors, or body modifications not present in the character's standard profile unless explicitly part of a "damaged state" narrative (e.g., torn sleeve).
2. **Silhouette Integrity**: The character’s unique silhouette must be readable even without facial details.
3. **Personality Consistency**: A stoic character should not suddenly act manic unless the cause is extreme shock; a playful character should not appear terrified unless the threat is immediate and physical.

Do not replace the character with a generic attractive person. The goal is: "an attractive and interesting version of this character," not "a random attractive character using the same aesthetic."

---

## Visual Appeal Philosophy & Body As A Hook

Visual attractiveness is an intentional component of the dataset. It is one of the primary reasons a viewer stops scrolling.

**The Ideal Formula:**
`Attractive Character + Interesting Moment`
*(Not just `Attractive Character Only`)*

### Body Appeal Guidelines
Body emphasis is desirable when coherent with the character and composition. A voluptuous yet athletic silhouette is generally desirable. Use body language to communicate confidence, curiosity, playfulness, or emotion.

**Valid Visual Hooks:**
- Fitted clothing showing muscle definition or tension.
- Silhouette highlights (waist, hips, legs) emphasized by pose or lighting.
- Clothing physics: fabric stretching, flaring, or clinging due to movement or environment.
- Strategic exposure: glimpses of skin or undergarments caused by *action* (e.g., arm raised, leaning back), not just static posing.

**Hard Anti-Patterns for Body Appeal:**
1. **The "Cleavage First" Trap**: If the main hook is only large breasts without a distinct action or story beat, reject it.
2. **Static Sensuality**: Do not use low-angle shots solely to emphasize rear/thighs unless there is a visible cause (e.g., bending to pick something up, sliding under an obstacle).
3. **Generic Beauty**: Avoid poses that could be applied to any character without losing meaning.

---

## Micro-Story & Causality

Every premise must tell a micro-story of 1–2 seconds duration. The frame must capture the *middle* of an event, not the beginning or end.

**The Cause-Effect Chain:**
1. **Trigger**: A specific physical event occurs (e.g., a pipe bursts, a door slams).
2. **Reaction**: The character responds physically (dodging, bracing, adjusting).
3. **Consequence/Result**: Visible change in state (disheveled hair, wet clothing, strained muscles, shifted weight).

**Specificity Requirement:**
- Avoid abstract causes like "tension" or "danger."
- Use concrete nouns: "steam jet," "shattered glass," "slipping boot," "snapping rope."

---

## Animation Potential

A strong premise should feel like a frame from a 5–10 second clip.

**Animation Readiness Checks:**
- Is there implied directional energy? (e.g., motion blur, trailing fabric).
- Can the next 3 seconds of action be predicted without inventing new context?
- Does the pose suggest momentum or recoil?

Avoid static "hero poses" that freeze time. Prefer dynamic stances: mid-step, mid-turn, mid-reaction.

---

## Category-Specific Rules

To ensure batch-level diversity, each premise category must adhere to specific constraints:

### 1. Closeup (Face/Upper Body)
- **Focus**: Expression and immediate physical reaction.
- **Rule**: Must show a *specific* interaction with the environment or self.
- **Anti-Pattern**: Do not use "hand shielding face" or "adjusting blindfold" as the default hook for every closeup. Vary the action: wiping sweat, catching a falling object near the head, reacting to sound (head turn), adjusting gear on chest/shoulder.
- **Requirement**: At least one distinct prop or environmental element must be visible in the foreground or mid-ground interacting with the character.

### 2. Medium Shot (Waist Up)
- **Focus**: Body language and torso tension.
- **Rule**: Must show upper body mechanics (twisting, bracing, reaching).
- **Anti-Pattern**: Avoid generic "standing with arms crossed." Use active stances: leaning forward, twisting away from impact, gripping a railing/handle.
- **Requirement**: Clothing physics must be visible (e.g., sleeves flaring, collar shifting).

### 3. Fullbody
- **Focus**: Silhouette and lower body dynamics.
- **Rule**: Must show weight distribution and leg engagement.
- **Anti-Pattern**: Avoid "standing on one leg" or "walking forward." Use specific actions: crouching to slide under, lunging to catch, stepping over debris with purpose.
- **Requirement**: Interaction with the ground or a large prop (door, crate, machine part) is mandatory.

### 4. Dynamic
- **Focus**: High-energy motion and impact.
- **Rule**: Must capture the peak of an action (impact, jump, dodge).
- **Anti-Pattern**: Avoid "running in place." Use specific hazards: dodging a projectile, colliding with a surface, swinging from a point.
- **Requirement**: Motion blur or debris particles must be present to convey speed/force.

### 5. Cinematic (Wide)
- **Focus**: Character within environment, but character is the subject.
- **Rule**: The setting amplifies the moment; it does not dominate it.
- **Anti-Pattern**: Avoid "character small in landscape." Ensure the character’s action is readable from a distance.
- **Requirement**: A clear line of sight between the character and the source of tension (e.g., looking at the collapsing structure, facing the off-screen enemy).

---

## Batch-Level Diversity Enforcement

To prevent repetition within a single generation batch (e.g., 20 premises), apply these hard limits:

1. **Hook Family Limit**: No more than **2** premises can share the same primary hook family (e.g., "Wind/Flare," "Steam/Burst," "Balance/Swipe").
2. **Location Variety**: At least **6 distinct locations/settings** must be used across the batch. Do not reuse the same specific prop setup (e.g., "broken vent") more than twice.
3. **Emotional Tone Spread**: The batch must include a mix of:
   - Stoic/Composed (max 5)
   - Playful/Mischievous (min 2)
   - Strained/Effortful (min 4)
   - Surprised/Shocked (min 3)
   - Fierce/Determined (min 3)
4. **Camera Angle Rotation**: Ensure a mix of eye-level, low-angle, high-angle, and over-the-shoulder shots. No more than 5 premises should use the same camera angle type.

---

## Hard Anti-Pattern Rules

Reject any premise that falls into these categories:

1. **The "Contemplative Ruin" Trap**: Character standing still in a ruined city/cathedral/rain looking sad or thoughtful without a physical trigger.
2. **The "Generic Combat" Pose**: Holding weapon in standard ready stance with no enemy visible and no environmental interaction.
3. **The "Abstract Cause" Fallacy**: Using words like "vibration," "pressure," or "tension" without a visible source (e.g., no shaking object, no visible wind source).
4. **The "Beauty Shot" Default**: Character posing in an attractive way with no narrative reason for the pose.
5. **Repetitive Closeup Hooks**: Using "hand near face/blindfold" for more than 2 premises in a batch without varying the specific action (e.g., one wiping, one catching, one turning).

---

## Acceptance Checklist

Before accepting a premise, verify:

### Character
- [ ] Is the character recognizable through silhouette and key accessories?
- [ ] Does the personality match the reaction?
- [ ] Are there any factual errors (wrong color, missing item)?

### Visual Appeal
- [ ] Is the composition visually striking?
- [ ] Is body appeal integrated into the action (not just static posing)?
- [ ] Does the lighting highlight key features without blowing out details?

### Hook & Causality
- [ ] Is there a **visible cause** for the action?
- [ ] Is the micro-story clear in a single glance?
- [ ] Would removing the setting leave the premise mostly intact (character-centered)?

### Animation Potential
- [ ] Can this be animated for 5–10 seconds without inventing new context?
- [ ] Is there implied directional energy or momentum?

### Diversity & Repetition
- [ ] Does this violate any batch-level diversity limits (max 2 per hook family)?
- [ ] Is the location distinct from the previous premise in the sequence?
- [ ] Is the emotional tone different from the last 3 premises?

---

## Cycle 019 Specific Corrections

Based on Cycle 018 failures, explicitly avoid:
1. **Closeup Repetition**: In Cycle 018, 3/5 closeups involved hands near the face/head. In Cycle 019, ensure at least 2 closeups involve interactions with *weapons*, *feet/boots* (looking down), or *distant objects* (reaching/catching) rather than just face shielding.
2. **Generic Hazards**: Replace generic "oil slicks" and "spikes" with specific narrative elements: "enemy debris," "unique machine parts," "collapsing architecture pieces." The hazard should feel part of the story, not a platformer obstacle.
3. **Abstract Causes**: If using "vibration" or "wind," pair it with a visible source (e.g., "steam jet from cracked pipe," "gust from open blast door").

**Success Signal for Cycle 019:**
- 0 purely contemplative scenes.
- Max 2 premises per "hook family."
- At least 6 different locations.
- All Fullbody/Cinematic shots have specific physical interactions (not just standing/balancing).
- Closeup variety: No more than 2
