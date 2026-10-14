# LMCache Design System

The canonical source for LMCache's visual identity. Revision A, 21 September 2026.

    docs/LMCache-design-system-spec.md   The specification. Read this first.
    tokens/lmcache-tokens.css            Normative values — governs on any conflict
    tokens/lmcache-theme-toggle.js       The light/dark switch, matching the live contract
    tokens/lmcache-docs-overrides.css    Conformance overlay for docs.lmcache.ai
    marks/svg/  marks/png/               Wordmark, lockups, favicons, avatars
    marks/ascii/                         The CLI banner mark, for swag and physical things
    fonts/                               Geist, Geist Mono, Inter — woff2, TTF, licences
    templates/                           Event and print SVG templates + event landing page
    templates/fields.py                  The field vocabulary, normative for placeholder names
    events/                              One directory per event; fill.py renders the set
    spec-page/index.html                 Rendered proof — every swatch and ratio, both themes
    logo-usage/                          Public logo guidelines: stand-alone page, lmcache.ai snippet, kit build

## Start here

Open `spec-page/index.html` in a browser. It renders every token against every ground with the
contrast ratio computed at build time, and it has a working theme switch. If a value in the spec
and a value on that page disagree, the token file is right and both of the others are stale.

## The short version

Two inks — orange `#FE8444` and teal `#139BAE` — split across one wordmark. No symbol, no mascot.
Geist for display, Inter for prose, Geist Mono for identifiers, no serif anywhere.

The fact that shapes everything else: **the brand pair was built for a dark ground and spends most
of its life on a light one.** Orange is 7.05:1 on Ink and 2.44:1 on white. That is why light grounds
get their own text inks, why button labels are Ink rather than white, and why the dark theme is
native rather than an inversion.

## Rebuilding

    cd templates  && python3 _build_templates.py    # regenerate every SVG template
    cd spec-page  && python3 build.py               # regenerate the proof page

Both are the test suite and both exit non-zero on failure. `spec-page/build.py` recomputes every
contrast ratio from the token values and fails if any token misses its target; run it after any
colour change. `_build_templates.py` validates the generated SVGs against `templates/fields.py` and
fails on a placeholder that is not declared, a declared field that is not drawn, or free text left
in a `{{brace}}`.

## Logo usage and the logo kit

    cd logo-usage && python3 build.py

That rebuilds the public guidelines page (`logo-usage/index.html`), the lmcache.ai version
(`logo-usage/wordpress-snippet.html`), and the downloadable kit (`dist/lmcache-logo-kit.zip`).
The published page is at https://lmcache.ai/en/logo-usage/. See `logo-usage/README.md`.

## Making the assets for one event

    cd events && python3 fill.py 2026-10-06-samsung-workshop --png

Write `events/<slug>/event.txt`, run that, and `out/` has the twelve filled SVGs, the landing page,
and rasterised squares and social cards, with the guides layer already stripped. See `events/README.md`.

**Install `fonts/ttf-install/` first.** SVG cannot embed a face, every template names Geist, Inter,
and Geist Mono by family, and a machine without them renders the entire set in system sans without
raising an error.

## Three things that are easy to get wrong

**White text on a brand fill fails.** White on orange is 2.44:1, white on teal is 3.32:1. Ink is
the label color on brand fills, in both themes. Where a white label is genuinely wanted, the fill
is Harbor `#146773`.

**The whiteprint is not this system.** It is the drawing convention for technical blog figures, its
four inks are fixed literals that are never themed, and it does not govern the sites, signage, or
swag. See §9 — including the one crossing that is genuinely useful.

**The ASCII mark needs its font.** It is monospace-dependent, and without the font the character
grid collapses. Outline the text before any print or vendor handoff, or send the raw `.txt`.

## Scope

This governs LMCache's own properties. Tensormesh corporate material is out of scope entirely.

## Licensing

Three different sets of terms live here, and they are not interchangeable:

- **Code, docs, tokens, and templates** — [Apache 2.0](LICENSE), the same licence
  LMCache itself ships.
- **The vendored faces in `fonts/`** — SIL Open Font License 1.1, *not* Apache. The
  OFL requires `fonts/licenses/` to travel with them; keep that directory on any
  redistribution. This is the obligation here that is easiest to drop by accident.
- **The LMCache name and wordmark** — trademarks of Tensormesh, a trademark
  question rather than a copyright one. Apache 2.0 grants no trademark rights (§6),
  and merchandise of any kind needs written permission.

[`LICENSING.md`](LICENSING.md) has the detail, including what is fine, what is not,
and what needs permission first.
