# Marks

## Which asset, on which ground

| Ground | Asset |
|---|---|
| White or Mist | `svg/lmcache-wordmark.svg` |
| Ink or Abyss | `svg/lmcache-wordmark-on-dark.svg` — teal lifted to `#25B0C3` |
| One plate, dark ink | `svg/lmcache-wordmark-mono-ink.svg` |
| One plate, reversed | `svg/lmcache-wordmark-mono-white.svg` |
| With a descriptor | `svg/lmcache-lockup-stacked.svg` / `-on-dark` |
| Favicon, any ground | `svg/lmcache-favicon.svg` |
| App icon | `svg/lmcache-appicon-512.svg` |
| GitHub / Slack / Luma avatar | `svg/lmcache-avatar-512-dark.svg` / `-light` |

On dark, use `-on-dark`. At `#139BAE` the Cache half recedes against Ink while the orange stays
forward, and the mark reads lopsided.

## Clear space

X is the height of the wordmark. The wordmark has no descenders, so X is the full
height of the artwork: 20 units in the 114 × 20 master, or 0.175 × its width.

| Context | Clear space on every side |
|---|---|
| Standard | ½X |
| Fixed-height UI rows — nav bars, footers, partner strips | ¼X, never less |
| Next to another logo | 1X between the two marks |

At the 96px floor, X is about 17px and ½X is 8px. At 228px wide it is 20px; at
456px, 40px. In print at the 25mm floor, ½X is 2.2mm; at 50mm, 4.4mm. The
stacked lockup takes ½X of its own wordmark around the whole lockup, descriptor
included. The LM tile and the avatars carry their own ground: nothing goes on the
tile, and the tile edge is the boundary.

## Minimum sizes, measured

Full wordmark: **96px wide on screen, 25mm in print.** The wordmark is 5.7:1 wide, and below about
96px the counters close and it reads as a smear. Stacked lockup: 180px wide.

**There is no small wordmark.** Below the floor, use the LM glyph on a tile — `lmcache-favicon.svg`.
The tile carries its own ground, which is what makes one favicon correct everywhere.

## Single ink

Both halves take the one ink. Never simulate the two-color split with tints of a single ink; an
even wordmark is the correct monochrome form, and a two-tint one reads as a printing error.

## The ASCII mark

`ascii/lmcache-ascii-mark.svg` and variants, plus `ascii/lmcache-ascii.txt`.

Optional third mark, for swag, stickers, terminal-adjacent material, booth texture, and the quiet
background field on event cards at 10–12% opacity. Long narrow objects suit it — a pen, a lanyard,
a bottle, a nail file — and `-vertical` exists for those.

Not a website header, not a lockup with the vector wordmark, and not a name badge.

`-bone` is the whiteprint-ink version on whiteprint paper, for swag printed on bone stock alongside
whiteprint material. It is the one asset that mixes the two systems deliberately.

**Outline the text before any print or vendor handoff.** It is monospace-dependent and dissolves
without its font. Sending the `.txt` and letting the vendor set it in their own mono also works.

## Source

`svg/_source-wordmark.svg` is the file served at
`lmcache.ai/wp-content/uploads/2026/05/logo.svg`, retrieved 21 September 2026. Every vector asset
here is generated from its paths by the scripts in this repository, so the mark itself is never
redrawn by hand.
