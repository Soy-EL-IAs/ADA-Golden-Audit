# MiniMax Agent runtime

Create one video prompt from the approved image. Preserve the approved first-frame identity, composition, pose and visual continuity.

First, define the Minimum Hook Contract:
- visual_hook: what is about to happen (physical cause/effect, reaction, reveal)
- motion_trigger: the initial motion that breaks the static frame
- escalation: how the event develops
- payoff: the climax or reaction
- end_state: the final stable readable ending

Then, write the MiniMax video prompt explicitly describing temporal progression. Use this exact structure:
00:00
[exact continuation of Picture 1]

00:00–00:02
[hook begins]

00:02–00:05
[escalation]

00:05–00:07
[payoff / reaction]

[final moment]
[stable readable ending]

Specify only restrained temporal motion, continuity constraints and the requested workflow/duration. Do not redesign the image, add a new subject, alter identity, or write image-generation prompts.
