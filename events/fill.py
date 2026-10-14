#!/usr/bin/env python3
"""Fill the LMCache template set for one event.

    python3 fill.py 2026-10-06-samsung-workshop
    python3 fill.py 2026-10-06-samsung-workshop --png

Reads `<event>/event.txt`, checks it against the field registry in
templates/fields.py, and writes filled SVGs plus the landing page into
`<event>/out/`. The guides layer is stripped on the way out, so nothing in
`out/` carries the magenta safe-area frame.

No third-party dependencies. The event file is a flat `KEY: value` format
rather than YAML precisely so this stays true — the repository's other
generators are stdlib-only and this one matches them.

PNG rasterisation (--png) needs one of rsvg-convert, resvg, inkscape, or
chromium on PATH, and the faces in fonts/ttf-install/ installed. Without
them the SVGs are still correct; they just have to be rasterised elsewhere.
"""
import argparse, html, pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
TEMPLATES = ROOT / 'templates'
sys.path.insert(0, str(TEMPLATES))

from fields import (FIELDS, PAGE_FIELDS, REPEAT_FIELDS, TEMPLATE_FIELDS,
                    PER_EVENT, PER_SESSION, PER_PERSON)

ALL_FIELDS = {**FIELDS, **PAGE_FIELDS}

# PNG sizes worth having without being asked. Everything else stays vector.
PNG_TARGETS = {
    'event-square-1080.svg':        (1080, 1080),
    'event-square-1200.svg':        (1200, 1200),
    'event-square-1080-light.svg':  (1080, 1080),
    'social-og-1200x630.svg':       (1200, 630),
    'social-linkedin-1200x627.svg': (1200, 627),
    'social-x-1600x900.svg':        (1600, 900),
}


# ── The event file ──────────────────────────────────────────────────
def parse(path):
    """Flat `KEY: value` with `#` comments, `>` continuation lines, and
    `[block]` sections whose repeated keys build a list of records."""
    single, blocks, section, record = {}, {}, None, None
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if line.startswith('>'):                      # continuation
            target = record if record is not None else single
            if not target:
                sys.exit(f'{path}:{lineno}: continuation line with nothing above it')
            key = list(target)[-1]
            target[key] = (target[key] + ' ' + line[1:].strip()).strip()
            continue
        m = re.fullmatch(r'\[([a-z_]+)\]', line.strip())
        if m:                                         # section header
            section = m.group(1)
            if section not in REPEAT_FIELDS:
                sys.exit(f'{path}:{lineno}: unknown section [{section}] — '
                         f'expected one of {", ".join(sorted(REPEAT_FIELDS))}')
            blocks.setdefault(section, [])
            record = None
            continue
        m = re.match(r'([A-Z0-9_]+)\s*:\s*(.*)', line)
        if not m:
            sys.exit(f'{path}:{lineno}: expected `KEY: value`, got {line!r}')
        key, value = m.group(1), m.group(2).strip()
        if section is None:
            single[key] = value
        else:
            first = REPEAT_FIELDS[section][0]
            if record is None or key == first:        # a new record starts on the first field
                record = {}
                blocks[section].append(record)
            record[key] = value
    return single, blocks


def check(single, blocks, path):
    problems = []
    for key in single:
        if key not in ALL_FIELDS:
            near = [f for f in ALL_FIELDS if f.startswith(key[:4])]
            hint = f' — did you mean {near[0]}?' if near else ''
            problems.append(f'unknown field {key}{hint}')
    for name, records in blocks.items():
        allowed = set(REPEAT_FIELDS[name])
        for i, rec in enumerate(records, 1):
            for key in rec:
                if key not in allowed:
                    problems.append(f'[{name}] entry {i}: unknown field {key}')
    required = [f for f, (req, _) in ALL_FIELDS.items() if req]
    drawn = set()
    for fieldset in TEMPLATE_FIELDS.values():
        drawn |= set(fieldset)
    for f in required:
        if f in single:
            continue
        if f in FIELDS and f not in drawn:
            continue
        problems.append(f'missing required field {f} — {ALL_FIELDS[f][1]}')
    if problems:
        print(f'{path}: {len(problems)} problem(s)', file=sys.stderr)
        for p in problems:
            print(f'  {p}', file=sys.stderr)
        sys.exit(1)


# ── Substitution ────────────────────────────────────────────────────
def strip_guides(svg):
    return re.sub(r'\n?  <g id="guides".*?</g>\n?', '\n', svg, flags=re.S)


def substitute(text, values, escape):
    def repl(m):
        key = m.group(1)
        if key not in values:
            return m.group(0)
        v = values[key]
        return html.escape(v, quote=False) if escape else v
    return re.sub(r'\{\{([A-Z0-9_]+)\}\}', repl, text)


def expand_repeats(page, blocks):
    def repl(m):
        name, body = m.group(1), m.group(2)
        records = blocks.get(name, [])
        if not records:
            return ''
        return ''.join(substitute(body, rec, escape=True) for rec in records)
    return re.sub(r'[ \t]*<!-- repeat:([a-z_]+) -->\n(.*?)[ \t]*<!-- /repeat -->\n',
                  repl, page, flags=re.S)


# ── Rasterisation ───────────────────────────────────────────────────
def rasterizer():
    for name, cmd in (('rsvg-convert', ['rsvg-convert', '-w', '{w}', '-h', '{h}', '{src}', '-o', '{dst}']),
                      ('resvg',        ['resvg', '-w', '{w}', '-h', '{h}', '{src}', '{dst}']),
                      ('inkscape',     ['inkscape', '{src}', '-w', '{w}', '-h', '{h}', '-o', '{dst}'])):
        if shutil.which(name):
            return name, cmd
    for chrome in ('chromium', 'chromium-browser', 'google-chrome'):
        if shutil.which(chrome):
            return chrome, [chrome, '--headless', '--disable-gpu', '--default-background-color=00000000',
                            '--screenshot={dst}', '--window-size={w},{h}', '{src}']
    return None, None


def rasterize(out_dir):
    name, template = rasterizer()
    if not name:
        print('  no rasteriser found (rsvg-convert, resvg, inkscape, or chromium) — SVGs only')
        return
    print(f'  PNG via {name}:')
    for svg_name, (w, h) in PNG_TARGETS.items():
        src = out_dir / svg_name
        if not src.exists():
            continue
        dst = src.with_suffix('.png')
        cmd = [a.format(w=w, h=h, src=src, dst=dst) for a in template]
        r = subprocess.run(cmd, capture_output=True)
        if dst.exists():
            print(f'    {dst.name:<34} {w}x{h}  {dst.stat().st_size:,} bytes')
        else:
            print(f'    {dst.name:<34} FAILED: {r.stderr.decode()[:120]}')


# ── Main ────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description='Fill the LMCache template set for one event.')
    ap.add_argument('event', help='event directory under events/')
    ap.add_argument('--png', action='store_true', help='also rasterise the screen assets')
    ap.add_argument('--keep-guides', action='store_true', help='leave the safe-area layer in place')
    args = ap.parse_args()

    event_dir = HERE / args.event
    spec = event_dir / 'event.txt'
    if not spec.exists():
        sys.exit(f'no event file at {spec}')

    single, blocks = parse(spec)
    check(single, blocks, spec)

    out = event_dir / 'out'
    out.mkdir(exist_ok=True)
    print(f'{args.event}')

    for name in sorted(PER_EVENT) + list(PER_SESSION) + list(PER_PERSON):
        src = TEMPLATES / name
        svg = substitute(src.read_text(), single, escape=True)
        if not args.keep_guides:
            svg = strip_guides(svg)
        (out / name).write_text(svg)
        left = sorted(set(re.findall(r'\{\{([A-Z0-9_]+)\}\}', svg)))
        note = f'  unfilled: {", ".join(left)}' if left else ''
        print(f'  {name:<34}{note}')

    page = (TEMPLATES / 'event-landing.html').read_text()
    page = expand_repeats(page, blocks)
    page = substitute(page, single, escape=True)
    (out / 'index.html').write_text(page)
    counts = ', '.join(f'{len(v)} {k}' for k, v in sorted(blocks.items())) or 'no repeat blocks'
    print(f'  index.html                        ({counts})')

    if args.png:
        rasterize(out)
    print(f'\nwritten to {out}')


if __name__ == '__main__':
    main()
