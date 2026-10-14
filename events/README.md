# Events

One directory per event. Each holds an `event.txt` you write and an `out/`
directory the script writes.

    python3 fill.py 2026-10-06-samsung-workshop --png

That fills every template in `templates/`, strips the guides layer, expands the
landing page's repeating blocks, and writes the result to `<event>/out/`.

## Starting an event

Copy the nearest previous event's directory, rename it `YYYY-MM-DD-short-name`,
and edit `event.txt`. The script checks the file against `templates/fields.py`
before it renders anything, so a typo in a field name is an error with a line
number rather than a `{{BRACE}}` that survives to a printed poster.

## The event file

Flat `KEY: value`. Lines opening with `>` continue the line above, which is how
prose fields stay readable. A `[section]` header starts a repeating block, and a
new record begins each time the block's first field appears again.

There is no YAML here on purpose. Every other generator in this repository is
standard-library only, and one flat-file parser is cheaper than a dependency
that has to be installed on a machine at a venue.

## What comes out

`out/` carries the twelve SVGs, `index.html`, and — with `--png` — rasterised
squares and social cards. Nothing in `out/` has the magenta safe-area frame; it
is export-ready. Commit `event.txt`, not `out/`.

Three templates are filled once per event as a courtesy but really want a copy
per instance: the table tent is per session, and the name badge is per attendee.
Use the rendered one as the pattern and swap the fields.

## Titles

The square card gives the title two lines at 84px on 1080. Roughly nineteen
characters a line before it crowds the safe edge. **Check the square at 200px
before shipping it**, which is the size it is actually seen at in a Luma list —
if the second line stops being readable there, shorten the title rather than the
type (spec §10.1).

## Sponsor logos

`SPONSOR_1` and `SPONSOR_2` are drawn as separate `tspan`s inside one line on the
square card, in reading order, so each can be replaced with a supplied vector
logo without disturbing the other or the sentence around it.

They are set as type rather than as marks because a sponsor's wordmark is their
asset and not ours to redraw. Ask the sponsor for vector — a real sponsor will
have a brand kit and will send an SVG or EPS — and swap the `tspan` for a `<g>`
or `<image>` sized to the cap height of the surrounding text. Typeset names are a
correct card, not a placeholder; do not approximate a wordmark from memory, and
do not trace one from a raster grab off a website.

Order is the field order. `SPONSOR_1` reads first.

## QR codes

`QR` is the label under the well, not the code. Generate the code against the
registration URL and drop it into the white square at export. The well is square
because this system uses rules rather than rounded boxes.

## Fonts

The SVGs name Geist, Inter, and Geist Mono by family, and SVG cannot embed a
face. Install `fonts/ttf-install/` before rendering or the whole set falls back
to system sans. This is also what `--png` needs.
