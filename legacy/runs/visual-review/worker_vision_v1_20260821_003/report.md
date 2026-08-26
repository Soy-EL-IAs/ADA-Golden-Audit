# Worker Vision v1 benchmark

- Model: `qwen/qwen3-vl-8b`
- Cases: 15
- Worker load: 2.672s
- Mean review: 2.343s
- Verdicts: PASS 5, REVIEW 1, REJECT 8

## Results

- `2b_closeup_blindfold_ok` — **REJECT**; identity 8/10, anatomy 7/10, appeal 9/10, viral 9/10. Critical occlusion contradiction: blindfold fails to cover both eyes as required. Hair and outfit details are inconsistent between halves, violating canonical accuracy.
- `2b_blindfold_eye_visible` — **REJECT**; identity 10/10, anatomy 9/10, appeal 8/10, viral 7/10. The premise explicitly states 'Blindfold removed: 2B gazes forward with her blue eyes visible', but the right image (Klein result) shows her blindfold still covering her eye. This is a critical contradiction to the stated premise and violates the core visual requirement.
- `2b_seated_source_drift` — **REJECT**; identity 10/10, anatomy 7/10, appeal 8/10, viral 9/10. Critical visual drift and anatomical errors, including malformed hands and incorrect footwear, violate the expected pose and blindfold requirement.
- `2b_corridor` — **REJECT**; identity 10/10, anatomy 8/10, appeal 9/10, viral 9/10. Critical anatomical errors in both hands and legs, including malformed fingers and misaligned joints, render the image unsuitable for use as a reference or first frame.
- `2b_fullbody_guard` — **PASS**; identity 10/10, anatomy 10/10, appeal 9/10, viral 9/10. Perfect match to source prompt: single 2B, canonical outfit, blindfold, sword, ruined plaza, dusk lighting. No anatomical errors. Visuals are clean, impactful, and suitable for reference.
- `2b_walking` — **REJECT**; identity 9/10, anatomy 7/10, appeal 8/10, viral 8/10. Left image violates single-subject requirement by including another character. Right image has occlusion contradiction: eyes visible through blindfold, which contradicts canonical design.
- `2b_airborne_action` — **REJECT**; identity 10/10, anatomy 6/10, appeal 8/10, viral 9/10. The left image contains severe anatomical inconsistencies and visual drift from the source, making it unsuitable as a reference. The right image, while more faithful, still has minor anatomical issues and a different visual style that breaks continuity with the source.
- `2b_rolling_action` — **ERROR**: Unterminated string starting at: line 10 column 21 (char 412)
- `2b_duplicate_pair` — **REJECT**; identity 5/10, anatomy 5/10, appeal 7/10, viral 6/10. The image contains two identical 2B characters, violating the expected single-subject requirement. This is a critical duplication issue. Additionally, there are serious anatomical inconsistencies and significant visual drift between the source and Klein versions, including hand positioning and limb proportions. The presence of two subjects invalidates the PASS verdict.
- `2b_profile_fullbody` — **PASS**; identity 10/10, anatomy 10/10, appeal 9/10, viral 9/10. Subject is correctly identified as 2B with accurate hair, blindfold, and outfit. Anatomy is consistent and well-proportioned. Lighting and composition are strong. No occlusion contradictions or drift. Both halves are visually appealing and suitable as reference frames.
- `tifa_v26_closeup` — **REVIEW**; identity 9/10, anatomy 8/10, appeal 9/10, viral 9/10. The Klein rendering deviates from the source in eye color and stylistic fidelity, but otherwise preserves Tifa's identity and outfit. The differences are visually noticeable but not critical, making it suitable for review rather than rejection.
- `tifa_v26_rain_closeup` — **PASS**; identity 10/10, anatomy 10/10, appeal 9/10, viral 9/10. Both images accurately depict Tifa Lockhart from Final Fantasy VII Remake with correct identity, outfit, hair, and expression. Anatomy is consistent and well-rendered. Visuals are cinematic and appealing with strong lighting and detail. No occlusion contradictions or drift. Suitable for reference.
- `tifa_v26_fullbody` — **PASS**; identity 10/10, anatomy 10/10, appeal 9/10, viral 9/10. Perfect match to Tifa Lockhart's canonical outfit and identity from Final Fantasy VII Remake. Both halves show single subject with accurate anatomy, proportions, and attire. Klein result faithfully preserves the source's visual style while enhancing realism without drift. No occlusion contradictions, no duplicate subjects, and strong visual appeal suitable for reference or viral use.
- `tifa_v26_dynamic` — **REJECT**; identity 9/10, anatomy 7/10, appeal 8/10, viral 8/10. Critical visual drift in boots and Mako glow, plus broken hand anatomy and occlusion inconsistencies prevent approval.
- `tifa_camera_and_back_drift` — **PASS**; identity 10/10, anatomy 10/10, appeal 9/10, viral 9/10. Subject is correctly identified as Tifa Lockhart with canonical Remake outfit. Anatomy is accurate and consistent across both halves. No duplicate subjects or occlusion contradictions. Visuals are clean, cinematic, and suitable for reference. Minor drift in composition is noted but not critical.
