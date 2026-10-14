# Fonts

Three families, self-hosted. Latin subset, weights 400 / 500 / 600 / 700.

    woff2/                  Web delivery
    ttf-install/            Install locally; also what a print vendor wants
    licenses/               OFL 1.1 text for both projects
    lmcache-fonts.css       @font-face, linked to woff2/
    lmcache-fonts-embedded.css   @font-face, base64 inline — single-file pages

## Why these are here rather than on a CDN

Spec §11.3: enterprise and university networks block third-party font CDNs, and
that is a meaningful share of both the docs audience and the room at a
university-hosted meetup. A page that silently falls back to system sans is a
page that does not look like LMCache.

There is a second reason, specific to this repository. Every template in
`templates/` is SVG that names `Geist`, `Inter`, and `Geist Mono` by family.
SVG has no font embedding, so a template is only correct on a machine that has
the faces. Installing `ttf-install/` is what makes the templates render as
drawn, and it is the first thing to do on a new machine.

## Licence

Both are SIL Open Font License 1.1 with `fsType` 0, so they may be embedded in
PDFs, self-hosted, and passed to a print vendor without further permission.
Keep `licenses/` alongside any redistribution.

## Which file to use

A normal page links `lmcache-fonts.css` and ships the `woff2/` directory beside
it. A page that has to survive as one file — an emailed spec, an artifact, a
landing page pasted into a CMS — uses `lmcache-fonts-embedded.css` instead and
carries the faces in the stylesheet. The embedded form is 256 KB against 2.5 KB;
use it when a single file is the point, and not otherwise.

## Print handoff

Send `ttf-install/` with the outlined artwork, or outline the text and send
nothing. Do not assume the vendor has Geist; almost none do.

## The handwriting face

`--font-hand` in the token file names Gloria Hallelujah, at one word per page
maximum (spec §6.5). It is not vendored here. It is a Google Fonts face used
rarely and never in print, and adding it would put a fourth family in the
install step for one word.
