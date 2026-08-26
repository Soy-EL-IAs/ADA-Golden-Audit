# Hook Premise v2 and Render Intent

Hook Premise v2 replaces a model-shaped premise with a renderer-neutral description of
the image moment. `render_intent` is constrained to anime, semi-realistic and
photorealistic and is compiled differently by Lustify and Miaomiao.

`ResolvedRenderSpecV2` is current semantic provenance. `ResolvedRenderSpecV1` remains
written/read as a compatibility adapter where old stage-plan and historical mission
readers require it. New renderer receipts use generic renderer IDs and preset IDs.

This design allows a future renderer or conditioning mode to consume the same scene
intent without renaming it after Illustrious or Klein.
