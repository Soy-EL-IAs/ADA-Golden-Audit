# Characters Catalog v1

## Purpose

Characters is the identity-facing catalog for ADA. Each card shows the trusted reference
image, registered name, franchise, number of visible Library images, canonical prompt/tags
and the evidence-backed renderer route.

Reference precedence is explicit: user-selected Hero, cached manifest reference, then the
latest visible Library image only when neither of the first two exists.

## Capability states

- **Green — Lustify direct:** Lustify identity recognition is explicitly confirmed.
- **Yellow — Miaomiao → Lustify:** Lustify direct is explicitly unreliable, Miaomiao is
  confirmed, and the verified Lustify Img2Img fallback exists.
- **Red — blocked:** both Lustify and Miaomiao are explicitly unreliable or unsupported.
- **Grey — not evaluated:** evidence is incomplete. Grey prevents ADA from inventing a red,
  yellow or green claim and preserves the existing unverified route for compatibility.

`config/characters.json` is the source of truth. Image counts and references are joined at
read time from Library, Hero metadata and the registered character reference manifest.

## Production routing

Selecting Lustify for a yellow character stores the user's requested renderer as Lustify,
but production executes a validated Miaomiao identity source followed by Lustify latent
Img2Img. Lustify direct is not submitted.

Selecting Miaomiao always executes only Miaomiao. It does not trigger Lustify or the yellow
fallback. A red route is rejected before a Mission is created.

## Evidence policy

Capability states are never inferred from image count, latest file, model popularity or an
unreviewed output. A state changes only through explicit evidence recorded in the character
registry. Model Lab evidence may support that update but is not scanned automatically.

