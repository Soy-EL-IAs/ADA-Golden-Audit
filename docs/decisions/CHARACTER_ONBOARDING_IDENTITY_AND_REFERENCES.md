# Character onboarding: identity and references

Character onboarding has three deliberately separate responsibilities:

```text
Danbooru / booru taxonomy  -> tells ADA WHO the character is and how the ecosystem names it.
Official / trusted sources -> tell ADA HOW the character visually looks.
Generated references       -> help a renderer PRESERVE that identity.
```

`CharacterTagResolver` resolves canonical name, Danbooru tag, franchise, aliases,
and classified taxonomy before any web request. `CharacterReferenceFinder` then
discovers canonical visual references using that identity context. It records the
source page, image URL, source tier, trust origin, and discovery method separately;
an image CDN never erases a page's observed provenance.

The reference manifest v2 has separate `canonical_references` and
`generated_identity_references` collections. Generated references are reserved for
future renderer conditioning and are never evidence of canonical identity.

Reference selection has two stages. Eligibility rejects non-downloadable, invalid,
duplicate, low-resolution, low-identity, and low-utility candidates. Ranking then
orders eligible candidates by identity confidence, reference utility, and provenance
tier. This prevents source trust from rescuing an image of the wrong character.

One strong canonical reference results in `READY_WITH_LIMITED_REFERENCES`; two or
more result in `READY`; zero results remain `BLOCKED`. Existing v1 manifests and
Character Contracts remain readable and are not rewritten.
