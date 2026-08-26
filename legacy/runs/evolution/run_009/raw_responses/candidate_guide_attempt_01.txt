# Viral Premise Guide v1.3 (Candidate)

## 1. Purpose & Scope

This guide defines how Ada creates original character premises for image generation datasets. It is an experimental evolution of the Production Baseline (v1.2), incorporating lessons from the Extreme Diagnostic Test and Iteration Report v1.

**Goal:** Create visually memorable, attention-grabbing concepts with strong potential for:
- Image generation fidelity
- Social media scroll-stopping appeal
- Animation seeds (5–10 second loops)
- Character engagement through micro-storytelling

A successful premise is a **frame taken from a larger moment**. It must answer: *What just happened?* and *What happens next?*

**Status:** Experimental Candidate. Do not claim to update production files directly. Preserve non-explicit boundaries while maximizing visual impact.

---

## 2. Core Philosophy: The "Active Attraction" Formula

The baseline (v1.2) suffered from "contemplative drift" (ruins, rain, static beauty). The extreme test suffered from "repetitive teasing" (mirrors, wind, generic smirks). v1.3 corrects both by enforcing **Causal Premise Requirements**.

### The Formula
A strong premise must contain at least three of the following, with **at least one** being a *visible event*:

1.  **Recognizable Identity:** Character-specific traits (face, silhouette, iconic gear).
2.  **Visual Appeal:** Deliberate emphasis on attractive features (silhouette, posture, clothing fit) integrated into the action.
3.  **Personality in Action:** The character’s specific temperament dictates *how* they react to the event.
4.  **Causal Event:** A distinct trigger (wind, object drop, surprise, physical strain) that causes a visible reaction.
5.  **Motion Potential:** Implied movement that allows for a short animation loop without inventing new actions.

**Weak Premise:** "2B standing in a ruined cathedral."  
*Why it fails:* No causal event. Contemplative drift. Identity is passive.

**Strong Premise (v1.3 Standard):** "2B catches a falling data chip with one hand while her other hand frantically adjusts the strap of her bodysuit that slipped during the movement, her expression shifting from concentration to mild annoyance."  
*Why it works:* Causal event (chip falling), visible reaction (adjusting strap), personality (annoyance/concentration), identity maintained.

---

## 3. Character Identity & Factual Safeguards

Identity is a **hard constraint**, not a suggestion. The character must remain recognizable without relying on generic "attractive person" tropes.

### Identity Anchors
Every premise must preserve:
-   **Face & Expression:** Specific to the character’s canon or defined profile.
-   **Hairstyle:** Including specific accessories (e.g., blindfold, hair ties).
-   **Iconic Accessories/Props:** Weapons, gear, unique clothing elements.
-   **Silhouette:** The overall shape of the body and outfit.

### Factual Identity Safeguards
To prevent "hallucinated canon" or generic drift:
1.  **No Invented Lore:** Do not introduce specific enemies, locations, or plot points unless explicitly supported by the local character profile. Use *generic* environmental elements (e.g., "metallic structure," "neon light") rather than named canon sites unless verified.
2.  **Personality Consistency:** The reaction must match the character’s known temperament. If the character is stoic, they should not be laughing hysterically unless there is a strong causal reason for the break in composure.
3.  **Clothing Logic:** Clothing must behave physically. Fabric weight, tear patterns, and fit must make sense within the action.

---

## 4. Visual Appeal & Body Language

Visual appeal is an intentional component of the dataset. It is the "stop-scroll" hook. However, it must be **integrated** into the premise, not merely appended.

### Principles
-   **Deliberate Attraction:** Do not make characters visually neutral by default. Emphasize attractive proportions (waist, hips, legs) when coherent with the pose.
-   **Body as Hook, Not Whole Premise:** A body-focused image is weak if it lacks a *reason* for the pose. The pose must be caused by an event or action.
    -   *Bad:* "2B in a low-angle shot showing her legs." (Generic beauty shot)
    -   *Good:* "2B stepping over a debris pile, one leg extended high, emphasizing thigh muscles and silhouette, while looking down at the obstacle with focused determination." (Action-driven appeal)

### Body Language Requirements
Poses must communicate emotion or intent:
-   Confidence vs. Vulnerability
-   Playfulness vs. Seriousness
-   Effort vs. Ease

**Rule:** If removing the character’s body from the image leaves no story, the premise is too weak. The body must be *doing* something.

---

## 5. Causal Premise Requirements (The Anti-Contemplation Rule)

This section directly addresses the weakness of v1.2 (too many static/atmospheric images).

### The "Cause + Effect" Test
Every premise must include:
1.  **A Cause:** A physical or emotional trigger.
    -   *Examples:* Wind gust, object slipping, sudden noise, physical strain, interaction with a prop.
2.  **An Effect (Visible Reaction):** A specific change in posture, expression, or clothing state.
    -   *Examples:* Hair blowing across face, hand reaching out, eyebrows furrowing, fabric tightening/stretching, weight shift.

### Prohibited "Static" Patterns
Avoid premises where the character is merely:
-   Standing still looking at the viewer (unless reacting to something).
-   Posing in a landscape with no interaction.
-   Waiting for an event that hasn't happened yet.

**Exception:** A static pose is acceptable only if it is the *peak* of an implied motion (e.g., mid-jump, mid-turn) or if the character is actively engaged in a subtle task (e.g., cleaning weapon, checking device).

---

## 6. Batch-Level Diversity Enforcement

To prevent "extreme" drift (repetitive smirks/mirrors/wind), apply these hard limits per batch of 20 premises:

### Category Distribution
Each batch must contain exactly:
-   **4 Closeup:** Focus on face/upper body, emphasizing expression and subtle micro-movements.
-   **4 Medium:** Waist-up or three-quarter view, balancing identity and environment interaction.
-   **4 Fullbody:** Emphasizing silhouette, posture, and full-body dynamics.
-   **4 Dynamic:** Implies high energy, motion blur potential, or complex physical action.
-   **4 Cinematic:** Wide or dramatic angle, but still requiring a specific character-focused event (not just scenery).

### Hook Family Limits
No single "hook family" may appear more than **2 times** in a batch of 20.
*Hook Families Examples:*
-   Wind/Hair disruption
-   Mirror/Reflection interaction
-   Falling/Catching objects
-   Clothing adjustment (straps, tearing)
-   Physical strain/Lifting/Pushing
-   Surprise/Shock reaction

### Emotional Variety
Ensure at least **5 distinct emotional tones** are represented in the batch. Do not default to "cool/confident" for all premises. Include:
-   Annoyance/Irritation
-   Curiosity/Interest
-   Effort/Strain
-   Playfulness/Mischief
-   Focus/Determination

---

## 7. Hard Anti-Pattern Rules

Reject any premise that violates the following:

1.  **The "Wallpaper" Trap:** If the image could be a background for text without losing meaning, it is too weak. The character must interact with the space.
2.  **Generic Beauty Shot:** No context, no action, just an attractive pose.
3.  **Atmospheric Drift:** Using rain, fog, or ruins solely to set a mood rather than driving character interaction. (e.g., "Rain makes her clothes wet" is weak; "She wipes rain from her face and checks her device for static interference" is strong).
4.  **Repetitive Teasing:** If the premise relies entirely on "accidental reveal" or "wind blowing skirt/hair" without a secondary action, it is rejected unless the batch limit allows it (max 2 per batch).
5.  **Canon Inflation:** Introducing specific named enemies, bosses, or plot events not present in the local character profile.

---

## 8. Animation Potential Check

A premise must be animatable for 5–10 seconds without inventing new actions.

**Questions to Ask:**
-   Can I loop this motion? (e.g., adjusting a strap repeatedly, catching an object and holding it)
-   Is the motion physically plausible? (Does the weight shift make sense?)
-   Does the expression change subtly over time? (e.g., from focus to slight smile)

If the premise requires a complex sequence of unrelated events to animate, simplify it. Focus on **one continuous action**.

---

## 9. Acceptance Checklist

Before finalizing any premise, verify all boxes:

### Identity
- [ ] Is the character recognizable via face/hair/gear?
- [ ] Does the personality match the reaction?
- [ ] Are there no factual errors regarding canon traits (unless explicitly allowed)?

### Causality & Action
- [ ] Is there a visible **Cause** (trigger)?
- [ ] Is there a visible **Effect** (reaction/action)?
- [ ] Is the character actively doing something, not just standing?

### Visual Appeal
- [ ] Is the body language intentional and attractive?
- [ ] Does the composition highlight the character’s silhouette or features?
- [ ] Is the appeal integrated into the action (not separate from it)?

### Diversity & Repetition
- [ ] Does this premise fit within the batch category limit?
- [ ] Is the hook family used fewer than 2 times in this batch?
- [ ] Is the emotional tone different from the previous premise?

### Animation
- [ ] Can this be animated as a short loop without new actions?
- [ ] Is the motion physically plausible?

**Final Verdict:** If any box is unchecked, revise the premise. Do not average; choose the stronger element and reinforce it.
