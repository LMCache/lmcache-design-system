# Two Inks and a Ground
## LMCache Design System — Specification

**Project:** LMCache
**Revision:** A — first consolidated system. Supersedes nothing; there was no written system before this.
**Date:** 21 September 2026
**Companion files:** `tokens/lmcache-tokens.css` (normative), `tokens/lmcache-theme-toggle.js`, `tokens/lmcache-docs-overrides.css`
**Method:** every value here was read off the live properties on 21 September 2026 by computed style, not from a mockup. Every contrast figure was computed, not estimated.

---

## §0. The argument

LMCache already has an identity. Two inks — orange `#FE8444` and teal `#139BAE` — split across one wordmark, sitting on a pale teal ground. It works, people recognise it, and it did not need inventing.

What it did not have was a written system, and three things followed from that. The marketing site and the blog stayed in sync only because they share one Elementor kit, which is a coincidence of tooling rather than a decision. The documentation site drifted completely and now carries none of the brand. And the colors that do most of the visible work — the heading teal, the page ground, the link orange — were never tokens at all. They were typed into widgets, and three of them fail WCAG AA.

So this document does two jobs. It records what exists, and it closes the gaps that recording it exposed.

**The one idea that governs every judgment call here: the brand pair was built for a dark ground, and spends most of its life on a light one.** Orange measures 7.05:1 against Ink `#001F23` and 2.44:1 against white. Teal measures 6.62:1 and 3.32:1. That single asymmetry explains most of the rules below — why there are separate text inks for light grounds, why button labels are Ink rather than white, and why the dark theme is the native one rather than an inversion bolted on afterwards.

### §0.1 Relationship to Tensormesh

Tensormesh corporate material is out of scope. Nothing here crosses to a company property, and no LMCache asset is reused in a Tensormesh context.

---

## §1. What is actually live

Read on 21 September 2026.

| Property | Platform | Theme tokens | Conformance |
|---|---|---|---|
| `lmcache.ai` | WordPress · Hello Elementor · Elementor kit 1568 | Elementor globals, 14 named colors | Reference. Everything below is derived from it. |
| `blog.lmcache.ai` | WordPress · same theme · same kit | Byte-identical global set | Conforming, with one contrast failure (§3.5) |
| `docs.lmcache.ai` | Sphinx · `sphinxawesome_theme` · Tailwind + shadcn HSL | Stock slate. Zero overlap. | **Non-conforming.** See §11. |

The two WordPress properties share a theme toggle that writes `localStorage.theme` and swaps a class on `<body>`. The docs site has a different toggle writing a class on `<html>`. Both are supported in §5.

---

## §2. Ground

Roughly ninety percent of any surface is ground, and it should be quiet. Both themes are native. Neither is the other one inverted.

| Token | Hex | Role |
|---|---|---|
| White | `#FFFFFF` | Light page ground |
| Mist | `#F0FAFB` | Light section and card ground — the surface most LMCache pages are actually made of |
| Ink | `#001F23` | Dark ground. A near-black with a teal cast, which is what keeps it from reading as generic dark mode. |
| Abyss | `#013138` | Raised surface on dark |
| Rule | `#006573` | Hairline |
| Mist Ink | `#ABCCCF` | Body text on dark — 10.05:1 on Ink |

**Mist `#F0FAFB` is the single most important value in this document, and until now it was not a token.** It is painted on twelve to thirteen containers on the home page and ten on the blog, it is what a visitor actually looks at, and it existed only as a literal typed into Elementor. Any conformance work starts by naming it.

---

## §3. The brand pair, and what it can and cannot do

| Token | Hex | On White | On Mist | On Ink | On Abyss |
|---|---|---|---|---|---|
| Orange | `#FE8444` | 2.44 | 2.30 | **7.05** | **5.74** |
| Teal | `#139BAE` | 3.32 | 3.12 | **5.19** | 4.22 |

Both are **graphic colors on light grounds** — fills, marks, rules, and the wordmark. Neither is text there. On dark grounds both are text-safe and comfortable.

### §3.1 Text-safe variants for light grounds

Every figure measured against both light grounds, because a value that clears white can still fail on Mist.

| Role | Hex | On White | On Mist |
|---|---|---|---|
| Harbor — headings | `#146773` | 6.53 | 6.15 |
| Teal text — links, accents | `#0E7A89` | 5.04 | 4.75 |
| Orange text — warm accent as type | `#B84708` | 5.33 | 5.01 |
| Body — secondary prose | `#4A777C` | 4.98 | 4.68 |
| Ink — display and primary prose | `#001F23` | 17.21 | 16.20 |

Harbor `#146773` is already the de-facto heading color across both WordPress sites. It was never a token; it is one now.

### §3.2 Text-safe variants for dark grounds

| Role | Hex | On Ink | On Abyss |
|---|---|---|---|
| White — headings, primary prose | `#FFFFFF` | 17.21 | 14.02 |
| Mist Ink — body prose | `#ABCCCF` | 10.05 | 8.19 |
| Teal bright — links, accents | `#25B0C3` | 6.62 | 5.39 |
| Orange — warm accent, unchanged | `#FE8444` | 7.05 | 5.74 |
| Body dark — tertiary | `#7FB0B6` | 7.20 | 5.87 |

Brand teal `#139BAE` clears AA on Ink at 5.19 but drops to 4.22 on Abyss, so raised surfaces take Teal bright.

### §3.3 Boundaries and focus

A divider that separates meaning is a UI component and owes 3:1. A purely decorative hairline does not.

Rule `#006573` measures 6.75 on white and **2.55 on Ink**, so it cannot carry a meaningful boundary in the dark theme. Divider dark `#1A8C9C` measures 4.32 on Ink and 3.52 on Abyss, and is the dark-theme border.

Focus takes brand teal `#139BAE` in both themes. It is the one value clearing 3:1 against all four grounds — 3.32, 3.12, 5.19, 4.22 — which means one focus ring, no theme branch.

### §3.4 The button rule, which is the one most easily got wrong

> **White text on the brand orange measures 2.44:1. Ink text on it measures 7.05:1. Ink is the label color on every brand fill, in both themes.**

White on brand teal is 3.32 and fails as well. This is counter-intuitive — a saturated fill reads as "dark, so put white on it" — and it is wrong for both of these inks. Where a filled control genuinely needs a white label, the fill is Harbor `#146773` (6.53:1) or Ink, not a brand ink.

### §3.5 Two live failures

`blog.lmcache.ai` sets its "Read Article" link to `#D15312`, which measures 4.24 on white and 3.99 on Mist. It misses AA on both. Replace with Orange text `#B84708`.

Both WordPress sites set secondary prose to `#528E94`, measuring 3.71 on white and 3.50 on Mist. It misses AA on both, and it is the body color, so the failure is on nearly every paragraph. Replace with Body `#4A777C`.

### §3.6 Tints

`rgba(254,132,68,.12)` and `rgba(19,155,174,.12)` are chip and pill grounds, both already in use. They are fills. Nothing legible is ever set in a tint.

---

## §4. Status — reserved, and never borrowed from the brand pair

Orange means LM. It does not mean warning, and an interface that uses it for both teaches the reader nothing. Status always carries an icon and a label as well as color.

| Status | Light | On White | Dark | On Ink |
|---|---|---|---|---|
| Success | `#1F7A4D` | 5.32 | `#4FBE86` | 7.41 |
| Warning | `#8A5200` | 6.39 | `#E0A43C` | 7.82 |
| Danger | `#B3123F` | 6.83 | `#F2708F` | 6.14 |
| Info | `#00707E` | 5.80 | `#39B7C9` | 7.20 |

Danger is a crimson rather than a red, chosen so it cannot be mistaken for the brand orange at a glance.

---

## §5. The two themes, and the switching contract

### §5.1 The contract

The theme class lives on `<body>` as `.light-mode` or `.dark-mode`, and the choice persists in `localStorage` under the key `theme` with the values `light` and `dark`. That is what `lmcache.ai` and `blog.lmcache.ai` already ship, and this system keeps it rather than inventing a cleaner one, because keeping it means no existing CSS has to change.

### §5.2 The dark theme

Ink ground, Abyss for raised surfaces, white headings, Mist Ink body, Teal bright links, orange unchanged. Full mapping in `tokens/lmcache-tokens.css` §5.

This is the ground the brand pair is strongest on, and the dark theme should be treated as a first-class surface rather than a courtesy. Event assets, social cards and signage all default to it for that reason (§10).

### §5.3 Three faults in the live switch, and the fixes

The live implementation works, and three things about it are worth correcting. `tokens/lmcache-theme-toggle.js` is the corrected version and holds the same contract.

The first is that it **defaults to light and never reads the operating system preference**. `localStorage.getItem('theme') || 'light'` means a visitor whose machine is set to dark gets a bright page and has to ask twice. The corrected script treats an absent stored value as "follow the OS", and keeps following it until the visitor chooses a side explicitly.

The second is the anti-flash technique. The live script injects `body { opacity: 0 !important }` and removes it on `DOMContentLoaded`. With JavaScript disabled, or a script that fails to load, the page is blank rather than merely mis-themed. The corrected script stamps the theme on `<html>` from a blocking inline snippet before first paint and never hides anything.

The third is that the two toggle buttons are Elementor icon widgets with no accessible state. They become real buttons carrying `aria-pressed`.

### §5.4 The docs site's different contract

`sphinxawesome_theme` sets `.dark` on `<html>`. Rather than force it onto the body-class contract, `tokens/lmcache-docs-overrides.css` maps `.dark`, `body.dark-mode`, and `html[data-theme="dark"]` to the same declarations, so one stylesheet serves either mechanism and the docs keep the switch they already have.

---

## §6. Type

| Family | Role | Weights |
|---|---|---|
| **Geist** | Headings, UI labels, buttons, eyebrows, all display | 500, 700 |
| **Inter** | Body prose | 400, 600 |
| **Geist Mono** | Identifiers, config keys, code, URLs, the ASCII mark | 400, 500 |
| **Gloria Hallelujah** | One accent word. See §6.5. | 400 |

No serif. Not in print either — the print pieces in §10 are signage and short-form, where a serif buys nothing and costs legibility at distance.

### §6.1 The scale

Measured off `lmcache.ai`, extended at both ends for signage.

| Step | Size | Use |
|---|---|---|
| −1 | 12px | Meta, eyebrows, dates, categories |
| 0 | 14px | Body default |
| 1 | 16px | Lead paragraph |
| 2 | 22px | Card title — Geist 500 |
| 3 | 32px | Section head — Geist 700 |
| 4 | 42px | Page title — Geist 700 |
| 5 | 48px | Hero — Geist 700 |
| 6 | 72px | Poster |
| 7 | 120px | Banner |

### §6.2 Case

The live sites apply `text-transform: capitalize` to nearly every heading, which is why the hero currently renders as "Building The Foundation Of AI Memory Tensor With KV Cache Infrastructure". CSS capitalisation cannot tell a preposition from a noun and will keep producing "Of" and "With".

**Set headings in sentence case in the source text and remove `text-transform` from heading styles.** Uppercase is reserved for eyebrows and labels, where it takes `.11em` tracking.

### §6.3 Line height

The kit sets body line-height to `1.3em`. That is a UI density, and it is too tight for prose; the docs site inherits `1.5` from Tailwind and reads better for it. Body prose takes **1.55**, headings take 1.2, and 1.3 stays for compact UI rows. Running measure is about 68 characters.

### §6.4 Figures

Numerals in tables and stat rows are tabular and aligned. The stat strip on the home page — stars, contributors, downloads, members — is a table of figures and should not reflow its columns as the numbers grow.

### §6.5 The handwriting

`lmcache.ai` sets one word, "dream", in Gloria Hallelujah inside an otherwise monospaced tagline. It is the most human thing on the site, and it survives into this system with a hard limit: **one word per page, maximum, and never in a heading, a label, a button, or anything a reader must act on.** It is a wink, and a wink repeated is a twitch.

---

## §7. Space, rule, radius

The 4px scale: 4, 8, 12, 16, 24, 32, 48, 64, 96, 144.

Radius is 16px for cards, matching both WordPress sites; 8px for small controls; pill for chips and stat badges. Containers run to 1400px, prose to 800px.

This system uses **rules, not shadows**. Neither live site leans on elevation, and a hairline in Rule or Divider dark separates things more honestly than a blur does.

---

## §8. The marks

### §8.1 The wordmark

A single-weight lowercase-counters wordmark, 114 × 20, split across the two inks: `LM` in orange, `Cache` in teal. There is no symbol, no monogram lockup, and no mascot. The wordmark is the whole identity, which is a strength worth protecting.

`marks/svg/lmcache-wordmark.svg` is the master. On dark grounds use `-on-dark`, which lifts the teal to `#25B0C3` so the two halves stay equally present; at `#139BAE` the Cache half recedes against Ink while the orange stays forward, and the mark reads lopsided.

### §8.2 Single-ink reproduction

Embroidery, engraving, one-plate print and fax take `-mono-ink` or `-mono-white`. Both halves take the one ink. **Never simulate the two-color split with tints of a single ink** — an even wordmark is the correct monochrome form, and a two-tint one reads as a printing error.

### §8.3 Minimum sizes, measured

| Asset | Floor |
|---|---|
| Full wordmark | 96px wide on screen, 25mm in print |
| Stacked lockup with descriptor | 180px wide |
| Favicon / app icon | Use the LM glyph alone, never the full wordmark |

The wordmark is 5.7:1 wide. Below about 96px the counters close and it reads as a smear, which is exactly what happens in a 32px favicon slot. `marks/svg/lmcache-favicon.svg` is the LM glyph on an Ink tile, and the tile is what makes one favicon work on every ground.

### §8.4 The docs logo, which is the current weak point

`docs.lmcache.ai` uses `lmcache-logo_crop.png` — raster, and plated on an opaque white rectangle. On the dark ground it floats as a bright box. This is the one defect in §11 that CSS cannot fix; it needs the SVG swapped in at `html_favicon` and in the header.

### §8.5 The ASCII mark

`lmcache/banner.py` prints a figlet "standard" wordmark at startup, `LM` in Solarized orange `#cb4b16` and `Cache` in Solarized cyan `#2aa198`. It has already been printed on swag, and it earns a place in the system as **an optional third mark for physical and playful contexts**.

Where it may be used: swag of every kind, terminal-adjacent material, sticker sheets, conference-booth texture, the quiet background field on event cards and posters, editorial illustration for a CLI post. Long narrow objects suit it particularly — a pen, a lanyard, a bottle, a nail file — and `-vertical` exists for exactly that.

Where it may not: as the logo on a website header, in a lockup with the vector wordmark, on a name badge, or anywhere the vector wordmark is the correct mark and the ASCII version is being substituted for novelty.

Two rules keep it from breaking. **The ASCII mark is monospace-dependent, and if the font is missing the character grid collapses and the letterforms dissolve.** Ship it as text SVG only where a webfont is guaranteed; for print, swag and any vendor handoff, convert the text to outlines first or send `marks/ascii/lmcache-ascii.txt` and let the vendor set it in their own mono. Second, when it is used as a background field it sits at 10–12% opacity and nothing is set on top of it that a reader must decode.

On color: the CLI prints Solarized because a terminal palette is what it lives in, and that is correct there. The printed and screen forms take the brand pair instead, or the whiteprint pair on bone stock. Three orange-and-teal pairs now exist in the LMCache world — brand, whiteprint, Solarized — and they are not reconciled deliberately, because each is right for its own surface. §9 covers why.

### §8.6 Clear space

X is the height of the wordmark — 20 units in the 114 × 20 master, 0.175 × its width, since the mark has no descenders. Standard clear space is **½X on every side**. Fixed-height UI rows — nav bars, footers, partner strips — may go to ¼X and never less. Beside another logo, the gap is 1X.

| Wordmark width | X | ½X |
|---|---|---|
| 96px (floor) | 17px | 8px |
| 228px | 40px | 20px |
| 456px | 80px | 40px |
| 25mm (print floor) | 4.4mm | 2.2mm |
| 50mm | 8.8mm | 4.4mm |

The stacked lockup takes ½X of its own wordmark around the whole lockup, descriptor included. The LM tile and the avatars carry their own ground, so the tile edge is the boundary and nothing is set on the tile.

---

## §9. Whiteprint

The whiteprint is the house image style for the LMCache blog, defined in the `lmcache-whiteprint` skill: violet-blue linework on bone paper, two risograph spot inks as halftone, one pixel out of registration.

| Ink | Hex | Means |
|---|---|---|
| Paper | `#F7F4EE` | The stock. Full bleed, always. |
| Blueline | `#2E3A8C` | Structure, mechanism, dimensions, all lettering |
| Vermilion | `#D9491F` | Hot — in flight, plaintext, failure |
| Teal | `#12817E` | Cold — at rest, sealed, durable |

### §9.1 The whiteprint is part of this system and is not this system

It is a **drawing convention for technical figures**, not a brand skin. Its inks are fixed literals that are never themed, because a whiteprint is a printed sheet and sits on its own paper whether the page around it is light or dark. Its bone `#F7F4EE` is not a brand ground and never becomes one.

The temptation, having two handsome ink pairs, is to merge them. Do not. The brand pair identifies LMCache; the whiteprint pair encodes cache temperature inside a drawing. A reader who has seen two sheets knows what a vermilion region means, and that meaning is worth more than palette tidiness.

### §9.2 Where whiteprint governs

Technical figures in blog posts, including the `og:image` hero for a post that has a sheet set. Diagrams in a technical talk. Illustration for a deep-dive explainer.

### §9.3 Where it does not

The marketing site, the docs site chrome, event cards, signage, badges, slides that are not technical figures, and swag — with one exception below. A whiteprint sheet dropped onto an event poster turns the poster into a figure without an argument.

### §9.4 The one crossing, which is the useful one

**A whiteprint sheet is the right image for an event about the thing the sheet draws.** A meetup on KV cache encryption can carry the encryption post's Sheet 1 as its event image, and it will be the most substantive image at the conference. When that happens, the sheet keeps its own bone paper and its own four inks and is **placed on the card as an image with a margin of Ink or Mist around it**. It is never bled to the card edge, never recolored to the brand pair, and never has brand type set on top of it. The card frames the sheet; the sheet does not become the card.

`marks/ascii/lmcache-ascii-mark-bone.svg` is the one asset that mixes the two deliberately: the ASCII mark in whiteprint inks on whiteprint paper, for swag printed on bone stock alongside whiteprint material.

---

## §10. Event and print assets

All templates live in `templates/`, carry placeholder fields in `{{UPPER_SNAKE}}`, and include a guides layer with the id `guides` that is deleted in one action before export. Print templates are drawn in millimetres at one unit to the millimetre, with 3mm bleed; the trim size is named in the filename.

**One field name per field, declared in `templates/fields.py`.** Revision A used three names for the same two fields — `EVENT`/`TITLE_LINE_2` on the squares, `HEADLINE`/`SECOND_LINE` on the posters, `HEADLINE`/`LINE_TWO` on the social cards — which was survivable while templates were filled one at a time by hand, and an obstacle the moment a whole set had to be filled for one event. The registry is now the vocabulary, and `_build_templates.py` validates the generated SVGs against it on every build: a placeholder that is not declared, a declared field that is not drawn, and any free-text placeholder left in a template all fail the build. Adding a field means adding it to `fields.py` first.

### §10.1 Screen

| File | Size | Notes |
|---|---|---|
| `event-square-1080.svg` | 1080 × 1080 | Luma, Meetup, Instagram. 72px safe margin clears Luma's corner rounding. |
| `event-square-1200.svg` | 1200 × 1200 | Higher-resolution square |
| `event-square-1080-light.svg` | 1080 × 1080 | Mist ground, for contexts already sitting on dark |
| `social-og-1200x630.svg` | 1200 × 630 | `og:image` |
| `social-linkedin-1200x627.svg` | 1200 × 627 | |
| `social-x-1600x900.svg` | 1600 × 900 | X crops toward 2:1; keep the title inside the guide. |

Square cards default to the Ink ground. A square event thumbnail is usually seen at 200px in a list beside a dozen others, and Ink with an orange kicker separates from a wall of white cards in a way that Mist does not. **Check every square at 200px before shipping it** — if the second title line stops being readable, the title is too long, and the fix is a shorter title rather than smaller type.

**Revision C changed the square, and only the square.** The card sits at the top of a page that already carries the date, the address, and the agenda, and it is posted to a listing that renders those fields itself. Revisions A and B both repeated them, which made the thumbnail a worse version of the page underneath it rather than an entry to it. The square now answers one question — what kind of afternoon is this — and nothing else.

Off the card: the date and time line, the venue and city line, the standfirst, and the three bulleted value lines. On it: `BLURB_1`, `BLURB_2`, and `BLURB_3`, three short lines naming what the afternoon is, joined by orange plus signs set in a left gutter. Separate fields rather than one because SVG does not wrap, so the break is a decision someone makes rather than one the renderer makes badly.

**Line count sets the type size**, and the rule is worth stating because it is the opposite of the intuition. The widest line is the only one that matters — it has to fit 936px of safe width — so breaking the same sentence across more lines shortens the binding line and buys type. Measured in Geist Medium against real advance widths rather than estimated:

| Blurb form | Binding line | Width | Largest type that fits | At 200px |
|---|---|---|---|---|
| Two lines | `Networking reception + Engineering sessions` | 21.51em | 43.5px | 8.1px |
| Three lines | `Hands-on with KV cache management` | 18.12em | 51.6px | 9.6px |
| Three lines, one word cut | `Hands-on KV cache management` | 15.80em | 59.3px | 11.0px |

The shipped card sets 52px, which leaves the binding line 114px of slack against the safe edge. Two of those steps came free: the plus signs moved into the gutter, where they cost the binding line nothing rather than the 2.3em a `+ ` prefix costs on the line least able to afford it.

The last step came from deleting the word "with". **At thumbnail size a word is worth more as type than as text** — cutting one bought eight points, and eight points is the difference between a line a reader parses and a line a reader skips. Keep each blurb line under about twenty-eight characters.

Dropping four lines of detail is what paid for the rest. The title went from 84 to 104, the body copy from 32 to 42, and the sponsor row moved onto the footer rule where it no longer competes with a date. **Sizes on this card answer the 200px view rather than the 1080px one** — divide by 5.4 to see what a reader in a listing gets, and if a line fails there, cut the line rather than the type.

`DATE`, `TIME`, `VENUE`, and `CITY` are still required fields. The posters, the banner, and the landing page all want them. They are absent from the square's entry in `fields.py` deliberately, and that absence is the design.

Two faults from Revision A were fixed along the way. The ASCII texture bled off one edge only, which read as a clipping fault rather than as texture; it now bleeds off the top-right corner, where two edges cut it and the intent is unambiguous. And the kicker was set in Orange `#FE8444` on both grounds, which is 7.05:1 on Ink and **2.44:1 on Mist** — a straight failure on the light variant. Kicker text now takes Orange Text `#B84708` on light, measured at 5.01:1. Rules and ticks are graphics rather than text and keep the brand value on both grounds.

### §10.2 Print

| File | Trim | Notes |
|---|---|---|
| `poster-a2-420x594.svg` | A2 | |
| `poster-a1-594x841.svg` | A1 | |
| `poster-24x36in.svg` | 610 × 914mm | US |
| `banner-retractable-850x2000.svg` | 850 × 2000mm | Bottom 250mm is cassette dead zone, marked on the guides layer. Nothing meaningful goes there. |
| `table-tent-a5.svg` | A5 landscape | Mist ground — see below |
| `name-badge-4x3in.svg` | 102 × 76mm | |

The table tent is the one print piece on a light ground. Table tents sit under warm room light at reading distance, where a large Ink field reads as a black slab and picks up every fingerprint. The posters and the banner stay on Ink, because they are read at three metres, and there the brand pair's 7.05:1 on Ink is the whole argument.

Badges: the name is the artefact's only real job. Geist Bold at 11mm holds fourteen characters inside the 90mm box; a longer name drops a step rather than crossing the safe edge. The role stripe along the bottom edge changes fill per role and keeps its position, so a room can be read at a glance.

### §10.3 Handing off to a printer

Send outlined vector, CMYK-converted by the vendor from these sRGB values rather than by you, and state that the Ink ground is a rich black rather than a 100K black — a 100K flat on a large poster prints as a grey sheet with visible roller banding. Ink `#001F23` at a typical GRACoL conversion lands near C82 M62 Y58 K72; confirm against the vendor's own profile rather than trusting that number.

Delete the `guides` group. It is magenta and green specifically so that it is impossible to miss if it survives to proof.

### §10.4 The event landing page

`templates/event-landing.html` is a single self-contained page built on the token file, with the theme toggle wired in. Replace the `{{BRACES}}` and the structured-data block at the head, and it is ready to publish.

### §10.5 Filling the set for an event

    cd events && python3 fill.py 2026-10-06-samsung-workshop --png

`events/<slug>/event.txt` holds one event's copy in a flat `KEY: value` format, with `>` continuing a line and `[agenda]` / `[speakers]` opening repeating blocks for the landing page. `fill.py` checks it against `fields.py`, fills every template, expands the repeats, strips the guides layer, and writes `events/<slug>/out/`. A typo in a field name is an error with a line number rather than a `{{BRACE}}` that survives to a printed poster.

The event file is committed; `out/` is not, because it regenerates. Three templates are rendered once as a courtesy and really want a copy per instance: the table tent is per session, the badge is per attendee.

`--png` rasterises the squares and social cards through whichever of `rsvg-convert`, `resvg`, `inkscape`, or `chromium` is on PATH. **It is not optional to have the faces installed first.** SVG cannot embed a font, every template names Geist, Inter, and Geist Mono by family, and a machine without them renders the whole set in system sans without complaining. Install `fonts/ttf-install/` once per machine.

---

## §11. Conformance

### §11.1 `lmcache.ai` and `blog.lmcache.ai`

Conforming, with four corrections, all small and all in the custom CSS rather than the theme.

Secondary prose moves from `#528E94` to `#4A777C` (§3.5). The blog's article link moves from `#D15312` to `#B84708` (§3.5). Heading `text-transform: capitalize` comes off and headings are set in sentence case in the source (§6.2). Body line-height moves from 1.3 to 1.55 (§6.3).

Then the two values that were never tokens — Mist `#F0FAFB` and Harbor `#146773` — get added to the Elementor global set, so the next page built does not retype them.

### §11.2 `docs.lmcache.ai`

Non-conforming. It carries none of the brand: system sans rather than Geist and Inter, Tailwind slate rather than the teal family, ground `#030711` rather than Ink, and a plated raster logo.

`tokens/lmcache-docs-overrides.css` closes this without forking the theme, and its header carries the install steps. Three of the four steps are a stylesheet and a line in `conf.py`. The fourth — replacing the raster logo with the SVG — is the one that needs a real asset change, and it is the most visible of the four.

Two details in the existing `docs/source/_static/custom.css` are worth fixing while there. It forces `.mermaid { background-color: #ffffff !important }`, which paints a hard white box on every diagram in the dark theme, the same bug as the plated logo. And the Sphinx config points `html_favicon` at a PNG, where the SVG favicon in `marks/svg/` works at every size.

### §11.3 Ordering the work

The logo swap and the Mermaid white box are what a visitor notices in the first second on a dark screen. The token overlay is what makes the site feel like the same organisation. The font self-hosting matters most for the enterprise and university networks that block font CDNs, which is a meaningful share of the docs audience. Do them in that order.

The faces are no longer a thing to go and find. `fonts/` carries Geist, Geist Mono, and Inter at 400/500/600/700 as woff2 and TTF, both under OFL 1.1 with `fsType` 0, alongside `lmcache-fonts.css` for a normal page and `lmcache-fonts-embedded.css` for anything that has to survive as one file. Point the docs theme at the first of those and the CDN question is closed.

---

## §12. Keeping this in sync

A change to any value touches three files, and they move together or not at all:

    tokens/lmcache-tokens.css              normative — governs on any conflict
    docs/LMCache-design-system-spec.md     this document
    spec-page/index.html                   the rendered proof

A change to the template field vocabulary touches two more:

    templates/fields.py                    normative for field names
    docs/LMCache-design-system-spec.md     §10

`templates/_build_templates.py` fails the build when the SVGs and `fields.py` disagree, so that pair cannot drift silently. The three files above have no such check between them, which is why they need the discipline.

Two copies that disagree are worse than one that is out of date.

**Never assert a contrast ratio you have not computed.** Every figure in this document was measured on 21 September 2026 against the named ground. If you change a value, measure it against both grounds of both themes before it ships.
