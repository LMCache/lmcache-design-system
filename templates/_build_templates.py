#!/usr/bin/env python3
"""Generate the LMCache event and print template set.

Every template is hand-authored SVG with placeholder copy in {{BRACES}}
and a guides layer that can be deleted in one action before export.

Run from this directory:  python3 _build_templates.py
"""
import re, pathlib, sys

from fields import FIELDS, TEMPLATE_FIELDS, unknown

HERE = pathlib.Path(__file__).resolve().parent
MARKS = HERE.parent / 'marks' / 'svg'
SRC = (MARKS / '_source-wordmark.svg').read_text()
_P = re.findall(r'<path d="([^"]+)" fill="(#[0-9A-Fa-f]{6})"', SRC)
LM    = [d for d, f in _P if f.upper() == '#FE8444']
CACHE = [d for d, f in _P if f.upper() == '#139BAE']
MARK_W, MARK_H = 114.0, 20.0

# ── Tokens, mirrored from tokens/lmcache-tokens.css ──────────────────
INK, ABYSS, MIST, WHITE = '#001F23', '#013138', '#F0FAFB', '#FFFFFF'
ORANGE, TEAL, TEAL_BRIGHT = '#FE8444', '#139BAE', '#25B0C3'
HARBOR, MISTINK, RULE, DIVDARK = '#146773', '#ABCCCF', '#006573', '#1A8C9C'
ORANGE_TEXT, TEAL_TEXT, BODY_LIGHT = '#B84708', '#0E7A89', '#4A777C'
DISPLAY = "'Geist',ui-sans-serif,system-ui,-apple-system,sans-serif"
BODY    = "'Inter',ui-sans-serif,system-ui,-apple-system,sans-serif"
MONO    = "'Geist Mono','IBM Plex Mono',ui-monospace,monospace"

ASCII_LM = (" _     __  __ ", "| |   |  \\/  |", "| |   | |\\/| |",
            "| |___| |  | |", "|_____|_|  |_|")
ASCII_CA = ("  ____           _          ", " / ___|__ _  ___| |__   ___ ",
            "| |   / _` |/ __| '_ \\ / _ \\", "| |__| (_| | (__| | | |  __/",
            " \\____\\__,_|\\___|_| |_|\\___|")


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def wordmark(x, y, width, lm_fill=ORANGE, cache_fill=TEAL, ind='  '):
    """Place the wordmark with its left edge at x, top at y, at `width` wide."""
    k = width / MARK_W
    o = [f'{ind}<g transform="translate({x:.2f},{y:.2f}) scale({k:.5f})">']
    o += [f'{ind}  <path fill="{lm_fill}" d="{d}"/>' for d in LM]
    o += [f'{ind}  <path fill="{cache_fill}" d="{d}"/>' for d in CACHE]
    o.append(f'{ind}</g>')
    return '\n'.join(o)


def ascii_block(x, y, size, lm_fill, cache_fill, opacity=1.0, ind='  '):
    adv = size * 0.6
    o = [f'{ind}<g opacity="{opacity}" font-family="{MONO}" font-size="{size:.2f}" '
         f'font-weight="500" xml:space="preserve" style="white-space:pre">']
    for i, (l, c) in enumerate(zip(ASCII_LM, ASCII_CA)):
        yy = y + size * (i + 0.8)
        o.append(f'{ind}  <text x="{x:.2f}" y="{yy:.2f}" fill="{lm_fill}">{esc(l)}</text>')
        o.append(f'{ind}  <text x="{x + 15*adv:.2f}" y="{yy:.2f}" fill="{cache_fill}">{esc(c)}</text>')
    o.append(f'{ind}</g>')
    return '\n'.join(o)


def guides(w, h, safe, bleed=0, note=''):
    """A deletable guides layer. id='guides' so one selection removes it."""
    o = [f'  <g id="guides" opacity="0.85">',
         f'    <!-- DELETE THIS WHOLE GROUP BEFORE EXPORT -->']
    o.append(f'    <rect x="{safe}" y="{safe}" width="{w-2*safe}" height="{h-2*safe}" '
             f'fill="none" stroke="#FF00AA" stroke-width="{max(1,w/900):.2f}" '
             f'stroke-dasharray="{w/90:.1f} {w/90:.1f}"/>')
    if bleed:
        o.append(f'    <rect x="{bleed}" y="{bleed}" width="{w-2*bleed}" height="{h-2*bleed}" '
                 f'fill="none" stroke="#00FFAA" stroke-width="{max(1,w/900):.2f}"/>')
    if note:
        o.append(f'    <text x="{safe}" y="{safe - w/120:.1f}" font-family="{MONO}" '
                 f'font-size="{w/75:.1f}" fill="#FF00AA">{esc(note)}</text>')
    o.append('  </g>')
    return '\n'.join(o)


def svg(name, w, h, body, unit='', desc=''):
    wa = f'{w}{unit}'
    ha = f'{h}{unit}'
    out = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
           f'width="{wa}" height="{ha}">\n'
           f'  <title>{esc(desc or name)}</title>\n{body}\n</svg>\n')
    (HERE / name).write_text(out)
    print(f'  {name:<38} {w}x{h}{unit}')


# ═══════════════════════════════════════════════════════════════════
#  SCREEN — square event card (Luma, Meetup, Instagram, Slack unfurl)
# ═══════════════════════════════════════════════════════════════════
def square(name, S, ground=INK, on_dark=True):
    """The square event card — Luma, Meetup, Instagram, Slack unfurl.

    Revision C. The card sits at the top of a page that already carries the
    date, the address, and the agenda. Revision B repeated all of it, which
    made the thumbnail a worse version of the page underneath it rather than
    an entry to it. It now answers one question — what kind of afternoon is
    this — and leaves the practical detail to the fields Luma renders itself
    and to the landing page.

    What went: the date and time line, the venue and city line, the separate
    standfirst, and the three bulleted value lines. What replaced them: one
    two-line blurb naming what the afternoon actually is.

    Type sizes here answer the 200px view, not the 1080px one. Divide by 5.4
    to see what a reader in a listing gets. Dropping four lines of detail is
    what bought the title its extra 12px and the blurb its extra 9px.
    """
    teal    = TEAL_BRIGHT if on_dark else TEAL
    fg      = WHITE if on_dark else INK
    second  = MISTINK if on_dark else BODY_LIGHT
    rule    = DIVDARK if on_dark else RULE
    # Orange is 7.05:1 on Ink and 2.44:1 on Mist. The kicker is text, so on a
    # light ground it takes the derived ink, not the brand value. Rules and
    # ticks are graphics and keep the brand value on both grounds.
    kicker  = ORANGE if on_dark else ORANGE_TEXT
    sponsor = fg if on_dark else HARBOR
    u       = S / 1080.0          # one unit, so the layout scales exactly
    safe    = 72 * u              # 6.7% — clears Luma's rounded-corner crop

    def T(x, y, size, fill, text, font=DISPLAY, weight=None, track=None,
          anchor=None):
        a = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'font-family="{font}"',
             f'font-size="{size:.1f}"']
        if weight: a.append(f'font-weight="{weight}"')
        if track:  a.append(f'letter-spacing="{track}"')
        if anchor: a.append(f'text-anchor="{anchor}"')
        return f'  <text {" ".join(a)} fill="{fill}">{text}</text>'

    b = [f'  <rect width="{S}" height="{S}" fill="{ground}"/>']
    # The swag mark as texture, bled off the TOP-RIGHT corner so the crop reads
    # as deliberate rather than as a clipping fault.
    b.append(ascii_block(S*0.55, -S*0.02, 26*u, ORANGE, teal, opacity=0.08))
    b.append(wordmark(safe, safe, 320*u, ORANGE, teal))

    b.append(T(safe, safe+130*u, 30*u, kicker, '{{KICKER}}', weight=500, track='0.11em'))
    b.append(T(safe, safe+280*u, 104*u, fg,   '{{TITLE_1}}', weight=700))
    b.append(T(safe, safe+400*u, 104*u, teal, '{{TITLE_2}}', weight=700))
    b.append(f'  <line x1="{safe:.1f}" y1="{safe+474*u:.1f}" x2="{safe+180*u:.1f}" '
             f'y2="{safe+474*u:.1f}" stroke="{ORANGE}" stroke-width="{6*u:.1f}"/>')

    # The blurb, on three lines with the plus signs in a left gutter.
    #
    # Line count sets the type size, because the widest line is what has to
    # fit 936px of safe width. Measured in Geist Medium against the real
    # advance widths: Revision C's two-line form had a 21.5em binding line
    # and could not exceed 41px. Breaking to three drops the binding line to
    # 15.8em and allows 52px. Pulling the plus signs into the gutter is part
    # of that — a '+ ' prefix costs about 2.3em on the line least able to
    # afford it.
    #
    # The rest came from cutting one word. "Hands-on with KV cache
    # management" allows 48px; "Hands-on KV cache management" allows 56. At
    # thumbnail size a word is worth more as type than as text.
    gut = 46 * u
    for i, key in enumerate(('{{BLURB_1}}', '{{BLURB_2}}', '{{BLURB_3}}')):
        y = safe + (556 + 68*i) * u
        if i:
            b.append(T(safe, y, 52*u, ORANGE, '+', weight=500))
        b.append(T(safe+gut, y, 52*u, fg, key, weight=500))

    # Sponsors and the domain share the footer. With the date and address gone
    # there is no competition for the line, and the backing reads as backing.
    fy = S - safe
    b.append(f'  <line x1="{safe:.1f}" y1="{fy-72*u:.1f}" x2="{S-safe:.1f}" '
             f'y2="{fy-72*u:.1f}" stroke="{rule}" stroke-width="{2*u:.1f}"/>')
    b.append(f'  <text x="{safe:.1f}" y="{fy-18*u:.1f}" font-family="{BODY}" '
             f'font-size="{26*u:.1f}" fill="{second}">Sponsored by '
             f'<tspan font-family={DISPLAY!r} font-size="{30*u:.1f}" font-weight="600" '
             f'fill="{sponsor}">{{{{SPONSOR_1}}}}</tspan> and '
             f'<tspan font-family={DISPLAY!r} font-size="{30*u:.1f}" font-weight="600" '
             f'fill="{sponsor}">{{{{SPONSOR_2}}}}</tspan></text>')
    b.append(T(S-safe, fy-18*u, 27*u, teal, 'lmcache.ai', font=MONO, anchor='end'))
    b.append(guides(S, S, safe, note='SAFE AREA — delete #guides before export'))
    svg(name, S, S, '\n'.join(b), desc='LMCache square event card')


# ═══════════════════════════════════════════════════════════════════
#  SCREEN — og:image / social card, 1.91:1
# ═══════════════════════════════════════════════════════════════════
def social(name, W, H, ground=INK):
    u = W / 1200.0
    safe = 64 * u
    b = [f'  <rect width="{W}" height="{H}" fill="{ground}"/>']
    b.append(ascii_block(W*0.58, H*0.54, 22*u, ORANGE, TEAL_BRIGHT, opacity=0.10))
    b.append(wordmark(safe, safe, 230*u, ORANGE, TEAL_BRIGHT))
    b.append(f'  <text x="{safe:.1f}" y="{safe+104*u:.1f}" font-family="{DISPLAY}" '
             f'font-size="{22*u:.1f}" font-weight="500" letter-spacing="0.11em" '
             f'fill="{ORANGE}">{{{{KICKER}}}}</text>')
    b.append(f'  <text x="{safe:.1f}" y="{safe+188*u:.1f}" font-family="{DISPLAY}" '
             f'font-size="{62*u:.1f}" font-weight="700" fill="{WHITE}">{{{{TITLE_1}}}}</text>')
    b.append(f'  <text x="{safe:.1f}" y="{safe+262*u:.1f}" font-family="{DISPLAY}" '
             f'font-size="{62*u:.1f}" font-weight="700" fill="{TEAL_BRIGHT}">{{{{TITLE_2}}}}</text>')
    b.append(f'  <line x1="{safe:.1f}" y1="{safe+312*u:.1f}" x2="{safe+140*u:.1f}" '
             f'y2="{safe+312*u:.1f}" stroke="{ORANGE}" stroke-width="{5*u:.1f}"/>')
    b.append(f'  <text x="{safe:.1f}" y="{H-safe+6*u:.1f}" font-family="{BODY}" '
             f'font-size="{24*u:.1f}" fill="{MISTINK}">{{{{STANDFIRST}}}}</text>')
    b.append(f'  <text x="{W-safe:.1f}" y="{H-safe+6*u:.1f}" text-anchor="end" '
             f'font-family="{MONO}" font-size="{24*u:.1f}" fill="{TEAL_BRIGHT}">lmcache.ai</text>')
    b.append(guides(W, H, safe, note='Twitter crops to 2:1 — keep the title inside'))
    svg(name, W, H, '\n'.join(b), desc='LMCache social card')


# ═══════════════════════════════════════════════════════════════════
#  PRINT — everything below is drawn in MILLIMETRES at 1 unit = 1 mm.
#  Export at 300 dpi (multiply by 11.811) or keep as vector.
#  Bleed 3 mm on every print piece. Trim is the artboard edge.
# ═══════════════════════════════════════════════════════════════════
def poster(name, Wmm, Hmm, bleed=3, ground=INK):
    W, H = Wmm + 2*bleed, Hmm + 2*bleed     # artboard includes bleed
    u = Wmm / 420.0                          # A2 width is the reference
    safe = bleed + 18*u
    b = [f'  <rect width="{W}" height="{H}" fill="{ground}"/>']
    b.append(ascii_block(W*0.40, H*0.63, 7.2*u, ORANGE, TEAL_BRIGHT, opacity=0.11))
    b.append(wordmark(safe, safe, 110*u, ORANGE, TEAL_BRIGHT))
    b.append(f'  <text x="{safe:.2f}" y="{safe+40*u:.2f}" font-family="{DISPLAY}" '
             f'font-size="{8*u:.2f}" font-weight="500" letter-spacing="0.11em" '
             f'fill="{ORANGE}">{{{{KICKER}}}}</text>')
    for i, key in enumerate(('{{TITLE_1}}', '{{TITLE_2}}')):
        col = WHITE if i == 0 else TEAL_BRIGHT
        b.append(f'  <text x="{safe:.2f}" y="{safe+(76+30*i)*u:.2f}" font-family="{DISPLAY}" '
                 f'font-size="{26*u:.2f}" font-weight="700" fill="{col}">{key}</text>')
    b.append(f'  <line x1="{safe:.2f}" y1="{safe+124*u:.2f}" x2="{safe+52*u:.2f}" '
             f'y2="{safe+124*u:.2f}" stroke="{ORANGE}" stroke-width="{2*u:.2f}"/>')
    b.append(f'  <text x="{safe:.2f}" y="{safe+146*u:.2f}" font-family="{BODY}" '
             f'font-size="{9*u:.2f}" fill="{MISTINK}">{{{{STANDFIRST}}}}</text>')
    fy = H - safe
    b.append(f'  <line x1="{safe:.2f}" y1="{fy-42*u:.2f}" x2="{W-safe:.2f}" y2="{fy-42*u:.2f}" '
             f'stroke="{DIVDARK}" stroke-width="{0.6*u:.2f}"/>')
    b.append(f'  <text x="{safe:.2f}" y="{fy-24*u:.2f}" font-family="{DISPLAY}" '
             f'font-size="{11*u:.2f}" font-weight="700" fill="{WHITE}">{{{{DATE}}}} · {{{{VENUE}}}}</text>')
    b.append(f'  <text x="{safe:.2f}" y="{fy-8*u:.2f}" font-family="{MONO}" '
             f'font-size="{8*u:.2f}" fill="{TEAL_BRIGHT}">lmcache.ai</text>')
    # QR well — square, because the system uses rules not rounded boxes
    q = 34*u
    b.append(f'  <rect x="{W-safe-q:.2f}" y="{fy-q-6*u:.2f}" width="{q:.2f}" height="{q:.2f}" '
             f'fill="{WHITE}"/>')
    b.append(f'  <text x="{W-safe-q/2:.2f}" y="{fy-q/2-4*u:.2f}" text-anchor="middle" '
             f'font-family="{MONO}" font-size="{4.5*u:.2f}" fill="{INK}">{{{{QR}}}}</text>')
    b.append(guides(W, H, safe, bleed=bleed,
                    note=f'TRIM {Wmm}x{Hmm}mm · BLEED {bleed}mm (green) · SAFE (pink)'))
    svg(name, round(W,2), round(H,2), '\n'.join(b), unit='mm',
        desc=f'LMCache poster {Wmm}x{Hmm}mm')


def retractable(name, Wmm=850, Hmm=2000, ground=INK):
    """Retractable / roll-up banner. The bottom ~250mm sits in the base
    cassette and is never seen — nothing meaningful goes there."""
    bleed = 0                       # roll-ups are printed oversize by the vendor
    W, H = Wmm, Hmm
    u = Wmm / 850.0
    safe = 70*u
    dead = 250*u                    # cassette dead zone
    b = [f'  <rect width="{W}" height="{H}" fill="{ground}"/>']
    b.append(ascii_block(W*0.06, H*0.58, 15*u, ORANGE, TEAL_BRIGHT, opacity=0.10))
    b.append(wordmark((W-420*u)/2, 150*u, 420*u, ORANGE, TEAL_BRIGHT))
    b.append(f'  <text x="{W/2:.1f}" y="{300*u:.1f}" text-anchor="middle" font-family="{DISPLAY}" '
             f'font-size="{26*u:.1f}" font-weight="500" letter-spacing="0.11em" '
             f'fill="{ORANGE}">{{{{KICKER}}}}</text>')
    for i, (key, col) in enumerate((('{{TITLE_1}}', WHITE), ('{{TITLE_2}}', TEAL_BRIGHT))):
        b.append(f'  <text x="{W/2:.1f}" y="{(470+92*i)*u:.1f}" text-anchor="middle" '
                 f'font-family="{DISPLAY}" font-size="{72*u:.1f}" font-weight="700" fill="{col}">{key}</text>')
    b.append(f'  <line x1="{W/2-90*u:.1f}" y1="{640*u:.1f}" x2="{W/2+90*u:.1f}" y2="{640*u:.1f}" '
             f'stroke="{ORANGE}" stroke-width="{6*u:.1f}"/>')
    b.append(f'  <text x="{W/2:.1f}" y="{710*u:.1f}" text-anchor="middle" font-family="{BODY}" '
             f'font-size="{30*u:.1f}" fill="{MISTINK}">{{{{STANDFIRST}}}}</text>')
    # Three stacked value lines — the read at walking pace
    for i in range(3):
        y = (860 + 110*i)*u
        b.append(f'  <line x1="{safe:.1f}" y1="{y-40*u:.1f}" x2="{W-safe:.1f}" y2="{y-40*u:.1f}" '
                 f'stroke="{DIVDARK}" stroke-width="{1.5*u:.1f}"/>')
        b.append(f'  <text x="{safe:.1f}" y="{y:.1f}" font-family="{DISPLAY}" font-size="{38*u:.1f}" '
                 f'font-weight="500" fill="{WHITE}">{{{{POINT_{i+1}}}}}</text>')
    qy = H - dead - 340*u
    q  = 260*u
    b.append(f'  <rect x="{(W-q)/2:.1f}" y="{qy:.1f}" width="{q:.1f}" height="{q:.1f}" fill="{WHITE}"/>')
    b.append(f'  <text x="{W/2:.1f}" y="{qy+q/2:.1f}" text-anchor="middle" font-family="{MONO}" '
             f'font-size="{28*u:.1f}" fill="{INK}">{{{{QR}}}}</text>')
    b.append(f'  <text x="{W/2:.1f}" y="{qy+q+52*u:.1f}" text-anchor="middle" font-family="{MONO}" '
             f'font-size="{32*u:.1f}" fill="{TEAL_BRIGHT}">lmcache.ai</text>')
    b.append(f'  <g id="guides" opacity="0.85">')
    b.append(f'    <!-- DELETE #guides BEFORE EXPORT -->')
    b.append(f'    <rect x="{safe:.1f}" y="{safe:.1f}" width="{W-2*safe:.1f}" height="{H-dead-safe:.1f}" '
             f'fill="none" stroke="#FF00AA" stroke-width="2" stroke-dasharray="14 14"/>')
    b.append(f'    <rect x="0" y="{H-dead:.1f}" width="{W}" height="{dead:.1f}" fill="#FF00AA" opacity=".18"/>')
    b.append(f'    <text x="{safe:.1f}" y="{H-dead+40*u:.1f}" font-family="{MONO}" font-size="{22*u:.1f}" '
             f'fill="#FF00AA">CASSETTE DEAD ZONE — {int(dead/u)}mm, never visible</text>')
    b.append('  </g>')
    svg(name, W, H, '\n'.join(b), unit='mm', desc='LMCache retractable banner 850x2000mm')


def table_tent(name, Wmm=148, Hmm=105, ground=MIST):
    """A5 landscape table tent, light ground — these sit under warm room
    light on a table, where Ink reads as a black slab."""
    bleed = 3
    W, H = Wmm + 2*bleed, Hmm + 2*bleed
    u = Wmm / 148.0
    safe = bleed + 8*u
    b = [f'  <rect width="{W}" height="{H}" fill="{ground}"/>']
    b.append(wordmark(safe, safe, 52*u, ORANGE, TEAL))
    b.append(f'  <text x="{safe:.2f}" y="{safe+30*u:.2f}" font-family="{DISPLAY}" '
             f'font-size="{5*u:.2f}" font-weight="500" letter-spacing="0.11em" '
             f'fill="{ORANGE_TEXT}">{{{{SESSION}}}}</text>')
    b.append(f'  <text x="{safe:.2f}" y="{safe+50*u:.2f}" font-family="{DISPLAY}" '
             f'font-size="{14*u:.2f}" font-weight="700" fill="{HARBOR}">{{{{SESSION_TITLE}}}}</text>')
    b.append(f'  <line x1="{safe:.2f}" y1="{safe+60*u:.2f}" x2="{safe+26*u:.2f}" y2="{safe+60*u:.2f}" '
             f'stroke="{ORANGE}" stroke-width="{1.2*u:.2f}"/>')
    b.append(f'  <text x="{safe:.2f}" y="{H-safe-6*u:.2f}" font-family="{BODY}" '
             f'font-size="{5.5*u:.2f}" fill="{BODY_LIGHT}">{{{{SPEAKER}}}} — {{{{AFFILIATION}}}}</text>')
    b.append(f'  <text x="{W-safe:.2f}" y="{H-safe-6*u:.2f}" text-anchor="end" font-family="{MONO}" '
             f'font-size="{5*u:.2f}" fill="{TEAL_TEXT}">lmcache.ai</text>')
    b.append(guides(W, H, safe, bleed=bleed, note=f'A5 tent · fold at top edge · TRIM {Wmm}x{Hmm}mm'))
    svg(name, round(W,2), round(H,2), '\n'.join(b), unit='mm', desc='LMCache A5 table tent')


def badge(name, Wmm=102, Hmm=76, ground=WHITE):
    """4x3in name badge. Name is set large enough to read across a
    handshake — that is the whole job of the artefact."""
    bleed = 3
    W, H = Wmm + 2*bleed, Hmm + 2*bleed
    u = Wmm / 102.0
    safe = bleed + 6*u
    b = [f'  <rect width="{W}" height="{H}" fill="{ground}"/>']
    b.append(f'  <rect x="0" y="0" width="{W}" height="{14*u:.2f}" fill="{INK}"/>')
    b.append(wordmark(safe, 4*u, 44*u, ORANGE, TEAL_BRIGHT))
    b.append(f'  <text x="{W-safe:.2f}" y="{10*u:.2f}" text-anchor="end" font-family="{DISPLAY}" '
             f'font-size="{4.4*u:.2f}" font-weight="500" letter-spacing="0.11em" '
             f'fill="{MISTINK}">{{{{EVENT_SHORT}}}}</text>')
    b.append(f'  <text x="{safe:.2f}" y="{36*u:.2f}" font-family="{DISPLAY}" '
             f'font-size="{11*u:.2f}" font-weight="700" fill="{INK}" '
             f'textLength="{min(90, 9*0.62*11)*u:.2f}" lengthAdjust="spacingAndGlyphs">{{{{FIRST_NAME}}}}</text>')
    b.append(f'  <!-- Name fit: 11mm Geist Bold holds 14 characters inside the 90mm box. '
             f'A longer name drops to 9mm; do not let it cross the safe edge. -->')
    b.append(f'  <text x="{safe:.2f}" y="{50*u:.2f}" font-family="{DISPLAY}" '
             f'font-size="{8*u:.2f}" font-weight="500" fill="{HARBOR}">{{{{LAST_NAME}}}}</text>')
    b.append(f'  <text x="{safe:.2f}" y="{64*u:.2f}" font-family="{BODY}" '
             f'font-size="{5.5*u:.2f}" fill="{BODY_LIGHT}">{{{{AFFILIATION}}}}</text>')
    # Role stripe — swap the fill per role, keep the position
    b.append(f'  <rect x="0" y="{H-7*u:.2f}" width="{W}" height="{7*u:.2f}" fill="{TEAL}"/>')
    b.append(f'  <text x="{safe:.2f}" y="{H-2.2*u:.2f}" font-family="{DISPLAY}" '
             f'font-size="{4.4*u:.2f}" font-weight="700" letter-spacing="0.11em" '
             f'fill="{INK}">{{{{ROLE}}}}</text>')
    b.append(guides(W, H, safe, bleed=bleed, note=f'TRIM {Wmm}x{Hmm}mm (4x3in)'))
    svg(name, round(W,2), round(H,2), '\n'.join(b), unit='mm', desc='LMCache name badge')



# ═══════════════════════════════════════════════════════════════════
#  VALIDATION — the templates and the field registry move together.
#  Run as part of every build; a drifting placeholder fails the build
#  rather than surfacing later as an unfilled {{BRACE}} on a poster.
# ═══════════════════════════════════════════════════════════════════
def validate():
    bad = 0
    for name, declared in sorted(TEMPLATE_FIELDS.items()):
        found = set(re.findall(r'\{\{([A-Z0-9_]+)\}\}', (HERE / name).read_text()))
        stray = unknown(sorted(found))
        undrawn = sorted(set(declared) - found)
        extra = sorted(found - set(declared) - set(stray))
        if stray:
            print(f'  FAIL {name}: placeholder not in fields.py: {", ".join(stray)}'); bad += 1
        if undrawn:
            print(f'  FAIL {name}: declared in fields.py but not drawn: {", ".join(undrawn)}'); bad += 1
        if extra:
            print(f'  FAIL {name}: drawn but not declared for this template: {", ".join(extra)}'); bad += 1
    leftover = set()
    for name in TEMPLATE_FIELDS:
        leftover |= set(re.findall(r'\{\{([^}]*)\}\}', (HERE / name).read_text()))
    loose = sorted(n for n in leftover if not re.fullmatch(r'[A-Z0-9_]+', n))
    if loose:
        print(f'  FAIL free-text placeholders remain: {", ".join(loose)}'); bad += 1
    print('field-registry check: ' + ('PASS' if not bad else f'FAIL ({bad})'))
    return 1 if bad else 0


if __name__ == '__main__':
    print('Screen:')
    square('event-square-1080.svg', 1080)
    square('event-square-1200.svg', 1200)
    square('event-square-1080-light.svg', 1080, ground=MIST, on_dark=False)
    social('social-og-1200x630.svg', 1200, 630)
    social('social-linkedin-1200x627.svg', 1200, 627)
    social('social-x-1600x900.svg', 1600, 900)
    print('Print (mm, 3mm bleed):')
    poster('poster-a2-420x594.svg', 420, 594)
    poster('poster-a1-594x841.svg', 594, 841)
    poster('poster-24x36in.svg', 610, 914)
    retractable('banner-retractable-850x2000.svg')
    table_tent('table-tent-a5.svg')
    badge('name-badge-4x3in.svg')
    print()
    sys.exit(validate())
