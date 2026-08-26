# Library Image Model v2

Library no longer equates a Candidate with one image.

```text
Mission / Run
  → Generation (candidate/concept)
      → Library Image: renderer A
      → Library Image: renderer B
```

Every image has its own `asset_id`, renderer, preset, review, favorite state and exact
pixel path. Siblings share `generation_id`; lineage records sibling IDs, selected image,
Mission/Run/Concept and optional `source_asset_id`. A generation selection does not
change the pixels displayed by an individual Library Image.

Automatic sources are restricted to production and historical Pilot renderer outputs.
Model Lab and benchmark receipts require a future explicit Promote to Library action.
Physical directory scanning is not a promotion mechanism.

## Inspector actions

- **Favorite:** writes the image-specific review record and reloads Favorites.
- **Set as hero:** validates that the exact Library Image exists and belongs to the
  character, then persists its image ID in `data/character_db/heroes.json`.
- **Compare:** selects the inspected image, opens the character Compare workspace and
  loads every sibling Library Image with the same generation ID.
- **Generate alternative:** carries exact source image ID and generation ID into Create
  Images, Mission state, M2 generation context and produced candidate lineage.
- **Reinterpret:** uses the single existing Scene Template/Character Contract endpoint;
  no duplicate reinterpret action or prompt-copy path exists.
