#!/usr/bin/env python3
"""Build the LMCache design-system spec page.

Self-contained on purpose: the token CSS and the wordmark paths are
inlined, so the page can be opened from disk, emailed, or dropped on a
static host with nothing beside it.

Regenerate after any change to tokens/lmcache-tokens.css.
"""
import pathlib, re, sys

HERE   = pathlib.Path(__file__).resolve().parent
ROOT   = HERE.parent
TOKENS = (ROOT / 'tokens' / 'lmcache-tokens.css')
MARK   = (ROOT / 'marks' / 'svg' / '_source-wordmark.svg')

def srgb(c):
    c/=255.0
    return c/12.92 if c<=0.04045 else ((c+0.055)/1.055)**2.4
def lum(h):
    h=h.lstrip('#'); r,g,b=(int(h[i:i+2],16) for i in (0,2,4))
    return 0.2126*srgb(r)+0.7152*srgb(g)+0.0722*srgb(b)
def cr(a,b):
    la,lb=lum(a),lum(b); hi,lo=max(la,lb),min(la,lb)
    return (hi+0.05)/(lo+0.05)
def badge(r, need=4.5):
    if r>=7:   return '<span class="r aaa">AAA %.2f</span>'%r
    if r>=need:return '<span class="r aa">AA %.2f</span>'%r
    if r>=3:   return '<span class="r ui">UI %.2f</span>'%r
    return '<span class="r no">%.2f</span>'%r

tokens_css = TOKENS.read_text() if TOKENS.exists() else '/* tokens file not found */'
src = MARK.read_text() if MARK.exists() else ''
P   = re.findall(r'<path d="([^"]+)" fill="(#[0-9A-Fa-f]{6})"', src)
LM    = [d for d,f in P if f.upper()=='#FE8444']
CACHE = [d for d,f in P if f.upper()=='#139BAE']

def wordmark(h=28, lmf='var(--accent-warm)', cf='var(--accent)'):
    o=[f'<svg class="wm" viewBox="0 0 114 20" height="{h}" role="img" aria-label="LMCache">']
    o+= [f'<path fill="{lmf}" d="{d}"/>' for d in LM]
    o+= [f'<path fill="{cf}" d="{d}"/>' for d in CACHE]
    o.append('</svg>')
    return ''.join(o)

WHITE,MIST,INK,ABYSS = '#FFFFFF','#F0FAFB','#001F23','#013138'

GROUNDS=[('White','#FFFFFF','Light page ground'),('Mist','#F0FAFB','Light section and card ground'),
         ('Ink','#001F23','Dark ground'),('Abyss','#013138','Raised surface on dark'),
         ('Rule','#006573','Hairline'),('Mist Ink','#ABCCCF','Body text on dark')]
BRAND=[('Orange','#FE8444','The LM half of the wordmark'),('Teal','#139BAE','The Cache half')]
LIGHT_TEXT=[('Ink','#001F23','Display and primary prose'),('Harbor','#146773','Headings'),
            ('Teal text','#0E7A89','Links and accents'),('Orange text','#B84708','Warm accent as type'),
            ('Body','#4A777C','Secondary prose')]
DARK_TEXT=[('White','#FFFFFF','Headings and primary prose'),('Mist Ink','#ABCCCF','Body prose'),
           ('Teal bright','#25B0C3','Links and accents'),('Orange','#FE8444','Warm accent'),
           ('Body dark','#7FB0B6','Tertiary'),('Divider dark','#1A8C9C','Meaningful boundary')]
STATUS=[('Success','#1F7A4D','#4FBE86'),('Warning','#8A5200','#E0A43C'),
        ('Danger','#B3123F','#F2708F'),('Info','#00707E','#39B7C9')]
WP=[('Paper','#F7F4EE','The stock'),('Blueline','#2E3A8C','Structure and all lettering'),
    ('Vermilion','#D9491F','Hot — in flight, plaintext'),('Teal','#12817E','Cold — at rest, sealed')]
SCALE=[('−1','12px','Meta, eyebrows, dates'),('0','14px','Body default'),('1','16px','Lead paragraph'),
       ('2','22px','Card title — Geist 500'),('3','32px','Section head — Geist 700'),
       ('4','42px','Page title'),('5','48px','Hero'),('6','72px','Poster'),('7','120px','Banner')]

def swatch_row(name,hex_,note,grounds):
    cells=''.join(f'<td>{badge(cr(hex_,g))}</td>' for g in grounds)
    return (f'<tr><td class="sw"><span class="chip" style="background:{hex_}"></span>'
            f'<b>{name}</b></td><td><code>{hex_}</code></td>{cells}<td class="note">{note}</td></tr>')

FAILS = []
def check(label, hex_, ground, need=4.5):
    r=cr(hex_,ground)
    if r<need: FAILS.append(f'{label}: {hex_} on {ground} = {r:.2f} (need {need})')
    return r

# ── Assemble ────────────────────────────────────────────────────────
H = []
A = H.append

A(f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>LMCache Design System</title>
<meta name="description" content="Rendered proof of the LMCache design system — every swatch, ratio, type step and component in both themes.">
<meta name="theme-color" content="#001F23">
<script>
(function(){{try{{var s=localStorage.getItem('theme');
var t=(s==='light'||s==='dark')?s:(matchMedia('(prefers-color-scheme: dark)').matches?'dark':'light');
document.documentElement.setAttribute('data-theme',t);}}catch(e){{}}}})();
</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;700&family=Geist+Mono:wght@400;500&family=Inter:wght@400;600&family=Gloria+Hallelujah&display=swap" rel="stylesheet">
<style>
{tokens_css}
</style>
<style>
  *,*::before,*::after{{box-sizing:border-box}}
  body{{margin:0}}
  .wrap{{max-width:1180px;margin:0 auto;padding:0 24px}}
  .wm{{display:block;width:auto}}

  header.sp{{position:sticky;top:0;z-index:20;background:var(--bg);
    border-bottom:1px solid var(--border);padding:14px 0}}
  header.sp .wrap{{display:flex;align-items:center;gap:20px}}
  header.sp .tag{{font-family:var(--font-mono);font-size:12px;color:var(--fg-secondary)}}
  .spacer{{flex:1}}
  .themeswitch{{display:flex;gap:2px}}
  .themeswitch button{{background:none;border:0;padding:7px;border-radius:999px;cursor:pointer;
    color:var(--fg-secondary);line-height:0}}
  .themeswitch button[aria-pressed="true"]{{background:var(--surface-accent);color:var(--accent)}}

  .hero{{padding:72px 0 48px}}
  h1{{font-family:var(--font-display);font-weight:700;font-size:clamp(2rem,6vw,48px);
    line-height:1.2;margin:0 0 12px;color:var(--fg-heading)}}
  .lede{{font-size:16px;color:var(--fg-secondary);max-width:62ch;line-height:1.55;margin:0}}

  section{{padding:56px 0;border-top:1px solid var(--border-soft)}}
  h2{{font-family:var(--font-display);font-weight:700;font-size:32px;line-height:1.2;
    color:var(--fg-heading);margin:0 0 8px}}
  h2 .num{{font-family:var(--font-mono);font-size:15px;font-weight:400;color:var(--accent-warm);
    display:block;margin-bottom:8px;letter-spacing:.11em}}
  h3{{font-family:var(--font-display);font-weight:500;font-size:22px;color:var(--fg-heading);
    margin:36px 0 12px}}
  p{{line-height:1.55;max-width:68ch;color:var(--fg)}}
  p.sub{{color:var(--fg-secondary);margin:0 0 28px}}
  a{{color:var(--fg-link)}}
  code{{font-family:var(--font-mono);font-size:.92em;background:var(--surface-accent);
    padding:2px 6px;border-radius:6px}}

  table{{width:100%;border-collapse:collapse;margin:16px 0;font-size:13px}}
  th{{text-align:left;font-family:var(--font-display);font-size:11px;letter-spacing:.11em;
    text-transform:uppercase;color:var(--accent-warm);font-weight:500;
    padding:0 10px 10px 0;border-bottom:1px solid var(--border)}}
  td{{padding:11px 10px 11px 0;border-bottom:1px solid var(--border-soft);vertical-align:middle}}
  td.note{{color:var(--fg-secondary)}}
  td.sw b{{font-weight:600}}
  .chip{{display:inline-block;width:22px;height:22px;border-radius:5px;margin-right:10px;
    vertical-align:-6px;border:1px solid var(--border-soft)}}
  .r{{font-family:var(--font-mono);font-size:11px;padding:3px 7px;border-radius:5px;white-space:nowrap}}
  .r.aaa{{background:rgba(31,122,77,.18);color:var(--status-success)}}
  .r.aa {{background:rgba(31,122,77,.12);color:var(--status-success)}}
  .r.ui {{background:rgba(138,82,0,.16);color:var(--status-warning)}}
  .r.no {{background:rgba(179,18,63,.16);color:var(--status-danger)}}

  .grid{{display:grid;gap:16px}}
  .g2{{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}}
  .g3{{grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}}
  .card{{background:var(--bg-raised);border:1px solid var(--border-soft);
    border-radius:var(--radius);padding:20px}}
  .card h4{{font-family:var(--font-display);font-size:14px;margin:0 0 6px;color:var(--fg-heading)}}
  .card p{{font-size:13px;color:var(--fg-secondary);margin:0}}

  .demo{{border:1px solid var(--border-soft);border-radius:var(--radius);overflow:hidden;
    margin:16px 0}}
  .demo .bar{{font-family:var(--font-mono);font-size:11px;padding:8px 14px;
    background:var(--surface-accent);color:var(--fg-secondary);
    border-bottom:1px solid var(--border-soft)}}
  .demo .body{{padding:24px}}
  .onlight{{background:#F0FAFB;color:#001F23}}
  .ondark {{background:#001F23;color:#FFFFFF}}

  .btn{{display:inline-block;font-family:var(--font-display);font-weight:700;font-size:15px;
    padding:12px 24px;border-radius:999px;text-decoration:none;border:2px solid transparent;
    cursor:pointer}}
  .btn-primary{{background:#FE8444;color:#001F23}}
  .btn-teal{{background:#139BAE;color:#001F23}}
  .btn-solid{{background:#146773;color:#FFFFFF}}
  .btn-ghost{{background:transparent;border-color:currentColor}}
  .btn-bad{{background:#FE8444;color:#FFFFFF}}
  .btnrow{{display:flex;gap:12px;flex-wrap:wrap;align-items:center}}

  .typerow{{display:flex;align-items:baseline;gap:20px;padding:14px 0;
    border-bottom:1px solid var(--border-soft)}}
  .typerow .meta{{font-family:var(--font-mono);font-size:11px;color:var(--fg-secondary);
    min-width:150px;flex:0 0 auto}}
  .typerow .samp{{font-family:var(--font-display);font-weight:700;color:var(--fg-heading);
    line-height:1.1;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}}

  .asciibox{{font-family:var(--font-mono);font-size:13px;line-height:1;white-space:pre;
    overflow-x:auto;padding:20px;background:var(--bg-raised);border-radius:var(--radius);
    border:1px solid var(--border-soft)}}
  .asciibox .lm{{color:var(--accent-warm)}}
  .asciibox .ca{{color:var(--accent)}}

  .marks{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:14px}}
  .markcell{{border:1px solid var(--border-soft);border-radius:var(--radius);
    padding:26px 18px;text-align:center}}
  .markcell .cap{{font-family:var(--font-mono);font-size:11px;color:var(--fg-secondary);
    margin-top:14px;display:block}}

  .callout{{border-left:3px solid var(--accent-warm);padding:4px 0 4px 18px;margin:24px 0}}
  .callout p{{margin:0}}
  .callout.bad{{border-left-color:var(--status-danger)}}

  footer.sp{{border-top:1px solid var(--border);padding:40px 0 64px;margin-top:40px;
    color:var(--fg-secondary);font-size:13px}}
</style>
</head>
<body>

<header class="sp"><div class="wrap">
  {wordmark(20)}
  <span class="tag">DESIGN SYSTEM · REV A</span>
  <span class="spacer"></span>
  <div class="themeswitch">
    <button type="button" data-theme-set="light" aria-pressed="false" aria-label="Use light theme"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg></button>
    <button type="button" data-theme-set="dark" aria-pressed="false" aria-label="Use dark theme"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M21 12.8A9 9 0 1111.2 3a7 7 0 009.8 9.8z"/></svg></button>
  </div>
</div></header>

<main>
<div class="wrap hero">
  <h1>Two inks and a ground</h1>
  <p class="lede">The rendered proof of the LMCache design system. Every ratio on this page was
  computed against the named ground at build time, not typed in. Switch the theme in the header —
  both are native, and nothing here is an inversion of the other.</p>
</div>
''')

# ── §2 Ground ───────────────────────────────────────────────────────
A('<section><div class="wrap"><h2><span class="num">§2</span>Ground</h2>')
A('<p class="sub">Roughly ninety percent of any surface. Mist <code>#F0FAFB</code> is the '
  'surface most LMCache pages are actually made of, and until this revision it was not a token.</p>')
A('<table><thead><tr><th>Token</th><th>Hex</th><th>on White</th><th>on Mist</th>'
  '<th>on Ink</th><th>on Abyss</th><th>Role</th></tr></thead><tbody>')
for n,h,note in GROUNDS: A(swatch_row(n,h,note,[WHITE,MIST,INK,ABYSS]))
A('</tbody></table></div></section>')

# ── §3 Brand pair ───────────────────────────────────────────────────
A('<section><div class="wrap"><h2><span class="num">§3</span>The brand pair</h2>')
A('<p class="sub">Graphic colors on light grounds — fills, marks, rules and the wordmark. '
  'Text-safe on dark. The asymmetry below is the single fact that shapes most of this system.</p>')
A('<table><thead><tr><th>Token</th><th>Hex</th><th>on White</th><th>on Mist</th>'
  '<th>on Ink</th><th>on Abyss</th><th>Role</th></tr></thead><tbody>')
for n,h,note in BRAND: A(swatch_row(n,h,note,[WHITE,MIST,INK,ABYSS]))
A('</tbody></table>')

A('<h3>Text-safe on light grounds</h3>')
A('<table><thead><tr><th>Token</th><th>Hex</th><th>on White</th><th>on Mist</th><th>Role</th></tr></thead><tbody>')
for n,h,note in LIGHT_TEXT:
    check(n,h,WHITE); check(n,h,MIST)
    A(f'<tr><td class="sw"><span class="chip" style="background:{h}"></span><b>{n}</b></td>'
      f'<td><code>{h}</code></td><td>{badge(cr(h,WHITE))}</td><td>{badge(cr(h,MIST))}</td>'
      f'<td class="note">{note}</td></tr>')
A('</tbody></table>')

A('<h3>Text-safe on dark grounds</h3>')
A('<table><thead><tr><th>Token</th><th>Hex</th><th>on Ink</th><th>on Abyss</th><th>Role</th></tr></thead><tbody>')
for n,h,note in DARK_TEXT:
    need = 3.0 if 'Divider' in n else 4.5
    check(n,h,INK,need); check(n,h,ABYSS,need)
    A(f'<tr><td class="sw"><span class="chip" style="background:{h}"></span><b>{n}</b></td>'
      f'<td><code>{h}</code></td><td>{badge(cr(h,INK),need)}</td><td>{badge(cr(h,ABYSS),need)}</td>'
      f'<td class="note">{note}</td></tr>')
A('</tbody></table>')

# The button rule
A(f'''<h3>§3.4 &nbsp;The button rule</h3>
<div class="callout"><p><b>White text on the brand orange measures {cr("#FFFFFF","#FE8444"):.2f}:1.
Ink text on it measures {cr("#001F23","#FE8444"):.2f}:1. Ink is the label color on every brand fill,
in both themes.</b></p></div>
<div class="demo"><div class="bar">CORRECT — Ink labels on brand fills; white only on Harbor or Ink</div>
<div class="body onlight"><div class="btnrow">
<a class="btn btn-primary" href="#">Register &nbsp;{badge(cr("#001F23","#FE8444"))}</a>
<a class="btn btn-teal" href="#">Read docs &nbsp;{badge(cr("#001F23","#139BAE"))}</a>
<a class="btn btn-solid" href="#">Get started &nbsp;{badge(cr("#FFFFFF","#146773"))}</a>
<a class="btn btn-ghost" href="#" style="color:#0E7A89">Learn more</a>
</div></div></div>
<div class="demo"><div class="bar">WRONG — white on a brand fill</div>
<div class="body onlight"><div class="btnrow">
<a class="btn btn-bad" href="#">Register &nbsp;{badge(cr("#FFFFFF","#FE8444"))}</a>
</div></div></div>''')
A('</div></section>')

# ── §4 Status ───────────────────────────────────────────────────────
A('<section><div class="wrap"><h2><span class="num">§4</span>Status — reserved</h2>')
A('<p class="sub">Orange means LM. It does not mean warning. Status always carries an icon and a '
  'label as well as color, and Danger is a crimson so it cannot be read as the brand orange.</p>')
A('<table><thead><tr><th>Status</th><th>Light</th><th>on White</th><th>on Mist</th>'
  '<th>Dark</th><th>on Ink</th><th>on Abyss</th></tr></thead><tbody>')
for n,l,d in STATUS:
    check(n+' light',l,WHITE); check(n+' light',l,MIST)
    check(n+' dark',d,INK);    check(n+' dark',d,ABYSS)
    A(f'<tr><td><b>{n}</b></td>'
      f'<td class="sw"><span class="chip" style="background:{l}"></span><code>{l}</code></td>'
      f'<td>{badge(cr(l,WHITE))}</td><td>{badge(cr(l,MIST))}</td>'
      f'<td class="sw"><span class="chip" style="background:{d}"></span><code>{d}</code></td>'
      f'<td>{badge(cr(d,INK))}</td><td>{badge(cr(d,ABYSS))}</td></tr>')
A('</tbody></table></div></section>')

# ── §6 Type ─────────────────────────────────────────────────────────
A('<section><div class="wrap"><h2><span class="num">§6</span>Type</h2>')
A('<p class="sub">Geist for display, Inter for prose, Geist Mono for identifiers. No serif. '
  'Headings are set in sentence case in the source — <code>text-transform: capitalize</code> '
  'cannot tell a preposition from a noun, which is why the live hero reads &ldquo;Of&rdquo; and '
  '&ldquo;With&rdquo;.</p>')
for step,size,use in SCALE:
    px=int(size.replace('px',''))
    disp=min(px,56)
    A(f'<div class="typerow"><span class="meta">step {step} · {size}</span>'
      f'<span class="samp" style="font-size:{disp}px">KV cache infrastructure</span>'
      f'<span class="spacer"></span><span class="meta">{use}</span></div>')
A('''<h3>§6.5 &nbsp;The handwriting</h3>
<p>One word per page, maximum. Never in a heading, a label, a button, or anything a reader must
act on. It is a wink, and a wink repeated is a twitch.</p>
<div class="demo"><div class="body onlight">
<span style="font-family:var(--font-mono);font-size:25px;color:#4A777C">Could AI
<span style="font-family:'Gloria Hallelujah',cursive;color:#B84708">dream</span>
with an electric LMCache?</span>
</div></div>''')
A('</div></section>')

# ── §8 Marks ────────────────────────────────────────────────────────
A('<section><div class="wrap"><h2><span class="num">§8</span>The marks</h2>')
A('<p class="sub">No symbol, no monogram lockup, no mascot. The wordmark is the whole identity, '
  'which is a strength worth protecting.</p>')
A(f'''<div class="marks">
  <div class="markcell" style="background:#FFFFFF">
    {wordmark(30,'#FE8444','#139BAE')}<span class="cap" style="color:#4A777C">wordmark · on White</span></div>
  <div class="markcell" style="background:#F0FAFB">
    {wordmark(30,'#FE8444','#139BAE')}<span class="cap" style="color:#4A777C">wordmark · on Mist</span></div>
  <div class="markcell" style="background:#001F23">
    {wordmark(30,'#FE8444','#25B0C3')}<span class="cap" style="color:#ABCCCF">wordmark-on-dark · teal lifted</span></div>
  <div class="markcell" style="background:#001F23">
    {wordmark(30,'#FE8444','#139BAE')}<span class="cap" style="color:#F2708F">brand teal on Ink — Cache half recedes</span></div>
  <div class="markcell" style="background:#F0FAFB">
    {wordmark(30,'#001F23','#001F23')}<span class="cap" style="color:#4A777C">mono-ink · one plate</span></div>
  <div class="markcell" style="background:#001F23">
    {wordmark(30,'#FFFFFF','#FFFFFF')}<span class="cap" style="color:#ABCCCF">mono-white · reversed</span></div>
</div>''')

A('''<h3>Minimum size</h3>
<p>The wordmark is 5.7:1 wide. Below about 96px the counters close and it reads as a smear, which
is exactly what happens in a 32px favicon slot. Use the LM glyph on a tile instead — the tile is
what lets one favicon work on every ground.</p>''')
A(f'''<div class="demo"><div class="bar">RENDERED AT SIZE — 160 / 96 / 64 / 32px wide</div>
<div class="body onlight" style="display:flex;align-items:flex-end;gap:28px;flex-wrap:wrap">
  <div style="text-align:center">{wordmark(28,'#FE8444','#139BAE')}<span style="font-family:var(--font-mono);font-size:10px;color:#4A777C">160px ✓</span></div>
  <div style="text-align:center">{wordmark(17,'#FE8444','#139BAE')}<span style="font-family:var(--font-mono);font-size:10px;color:#4A777C">96px ✓ floor</span></div>
  <div style="text-align:center">{wordmark(11,'#FE8444','#139BAE')}<span style="font-family:var(--font-mono);font-size:10px;color:#B84708">64px ✗</span></div>
  <div style="text-align:center">{wordmark(6,'#FE8444','#139BAE')}<span style="font-family:var(--font-mono);font-size:10px;color:#B3123F">32px ✗ use the LM tile</span></div>
</div></div>''')

# ASCII mark
ASCII_LM=(" _     __  __ ","| |   |  \\/  |","| |   | |\\/| |","| |___| |  | |","|_____|_|  |_|")
ASCII_CA=("  ____           _          "," / ___|__ _  ___| |__   ___ ",
          "| |   / _` |/ __| '_ \\ / _ \\","| |__| (_| | (__| | | |  __/",
          " \\____\\__,_|\\___|_| |_|\\___|")
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
ascii_html='\n'.join(f'<span class="lm">{esc(l)}</span><span class="ca">{esc(c)}</span>'
                     for l,c in zip(ASCII_LM,ASCII_CA))
A(f'''<h3>§8.5 &nbsp;The ASCII mark</h3>
<p>The figlet wordmark <code>lmcache/banner.py</code> prints at startup. It has already been printed
on swag, and it is an optional third mark for physical and playful contexts — stickers, pens,
lanyards, booth texture, the quiet background field on event cards. Not a website header, not a
lockup with the vector wordmark, and not a name badge.</p>
<div class="asciibox">{ascii_html}</div>
<div class="callout bad"><p><b>It is monospace-dependent. If the font is missing the character grid
collapses and the letterforms dissolve.</b> Ship it as text SVG only where a webfont is guaranteed;
for print, swag and any vendor handoff, outline the text first or send the raw
<code>.txt</code> and let the vendor set it in their own mono.</p></div>
<p>The CLI prints Solarized <code>#cb4b16</code> and <code>#2aa198</code>, which is correct in a
terminal. Printed and screen forms take the brand pair, or the whiteprint pair on bone stock.
Three orange-and-teal pairs now exist in the LMCache world, and they stay unreconciled on purpose.</p>''')
A('</div></section>')

# ── §9 Whiteprint ───────────────────────────────────────────────────
A('<section><div class="wrap"><h2><span class="num">§9</span>Whiteprint</h2>')
A('<p class="sub">The house image style for technical figures on the blog. Part of this system, '
  'and not this system. Its inks are fixed literals that are never themed, because a whiteprint is '
  'a printed sheet and sits on its own paper whether the page around it is light or dark.</p>')
A('<div class="demo"><div class="bar">WHITEPRINT INKS — never themed, never merged with the brand pair</div>'
  '<div class="body" style="background:#F7F4EE">')
A('<table style="margin:0"><thead><tr><th style="color:#D9491F">Ink</th><th style="color:#D9491F">Hex</th>'
  '<th style="color:#D9491F">on Paper</th><th style="color:#D9491F">Means</th></tr></thead><tbody>')
for n,h,note in WP:
    rr = cr(h,'#F7F4EE')
    A(f'<tr style="border-color:rgba(46,58,140,.2)"><td style="color:#2E3A8C;border-color:rgba(46,58,140,.2)">'
      f'<span class="chip" style="background:{h};border-color:#2E3A8C"></span><b>{n}</b></td>'
      f'<td style="color:#2E3A8C;border-color:rgba(46,58,140,.2)"><code style="background:rgba(46,58,140,.08)">{h}</code></td>'
      f'<td style="color:#2E3A8C;border-color:rgba(46,58,140,.2)"><span style="font-family:var(--font-mono);font-size:11px">{rr:.2f}</span></td>'
      f'<td style="color:#2E3A8C;border-color:rgba(46,58,140,.2)">{note}</td></tr>')
A('</tbody></table></div></div>')
A('''<div class="grid g2" style="margin-top:20px">
<div class="card"><h4>Where whiteprint governs</h4><p>Technical figures in blog posts, including the
<code>og:image</code> hero for a post with a sheet set. Diagrams in a technical talk. Illustration
for a deep-dive explainer.</p></div>
<div class="card"><h4>Where it does not</h4><p>Marketing site, docs chrome, event cards, signage,
badges, non-figure slides, swag. A whiteprint sheet on an event poster turns the poster into a
figure without an argument.</p></div>
<div class="card"><h4>The one useful crossing</h4><p>A whiteprint sheet is the right image for an
event about the thing the sheet draws. It keeps its own paper and its own four inks, and sits on
the card with a margin of Ink or Mist around it.</p></div>
<div class="card"><h4>Never</h4><p>Bled to the card edge. Recolored to the brand pair. Brand type
set on top of it. The card frames the sheet; the sheet does not become the card.</p></div>
</div>''')
A('</div></section>')

# ── §10 Assets ──────────────────────────────────────────────────────
SCREEN=[('event-square-1080.svg','1080 × 1080','Luma, Meetup, Instagram. 72px safe margin clears Luma&rsquo;s corner crop.'),
        ('event-square-1200.svg','1200 × 1200','Higher-resolution square'),
        ('event-square-1080-light.svg','1080 × 1080','Mist ground, for contexts already on dark'),
        ('social-og-1200x630.svg','1200 × 630','<code>og:image</code>'),
        ('social-linkedin-1200x627.svg','1200 × 627','LinkedIn'),
        ('social-x-1600x900.svg','1600 × 900','X crops toward 2:1 — keep the title inside the guide')]
PRINT=[('poster-a2-420x594.svg','A2 · 420 × 594mm','Ink ground — read at three metres'),
       ('poster-a1-594x841.svg','A1 · 594 × 841mm','Ink ground'),
       ('poster-24x36in.svg','610 × 914mm','US poster'),
       ('banner-retractable-850x2000.svg','850 × 2000mm','Bottom 250mm is cassette dead zone, marked on the guides layer'),
       ('table-tent-a5.svg','A5 landscape','Mist ground — the one light print piece'),
       ('name-badge-4x3in.svg','102 × 76mm','Geist Bold 11mm holds 14 characters in the 90mm box')]

A('<section><div class="wrap"><h2><span class="num">§10</span>Event and print assets</h2>')
A('<p class="sub">Every template carries placeholder copy in <code>{{BRACES}}</code> and a guides '
  'layer with the id <code>guides</code> that deletes in one action before export. Print templates '
  'are drawn in millimetres at one unit to the millimetre, with 3mm bleed.</p>')
A('<h3>Screen</h3><table><thead><tr><th>File</th><th>Size</th><th>Notes</th></tr></thead><tbody>')
for f,s,n in SCREEN: A(f'<tr><td><code>{f}</code></td><td>{s}</td><td class="note">{n}</td></tr>')
A('</tbody></table>')
A('<h3>Print</h3><table><thead><tr><th>File</th><th>Trim</th><th>Notes</th></tr></thead><tbody>')
for f,s,n in PRINT: A(f'<tr><td><code>{f}</code></td><td>{s}</td><td class="note">{n}</td></tr>')
A('</tbody></table>')
A('''<div class="callout"><p>Square cards default to the Ink ground. A square event thumbnail is
usually seen at 200px in a list beside a dozen others, and Ink with an orange kicker separates from
a wall of white cards in a way Mist does not. <b>Check every square at 200px before shipping it</b>
— if the second title line stops being readable, the title is too long, and the fix is a shorter
title rather than smaller type.</p></div>
<div class="callout bad"><p>Delete the <code>guides</code> group before export. It is magenta and
green specifically so it is impossible to miss if it survives to proof.</p></div>''')
A('</div></section>')

# ── §11 Conformance ─────────────────────────────────────────────────
LIVE_FAILS=[('blog.lmcache.ai','Read Article link','#D15312','#B84708',[WHITE,MIST]),
            ('both WP sites','Secondary prose','#528E94','#4A777C',[WHITE,MIST])]
A('<section><div class="wrap"><h2><span class="num">§11</span>Conformance</h2>')
A('<p class="sub">Read off the live properties on 21 September 2026 by computed style.</p>')
A('''<table><thead><tr><th>Property</th><th>Platform</th><th>Status</th></tr></thead><tbody>
<tr><td><code>lmcache.ai</code></td><td class="note">WordPress · Elementor kit 1568</td>
<td><span class="r aa">REFERENCE</span></td></tr>
<tr><td><code>blog.lmcache.ai</code></td><td class="note">Same theme, byte-identical globals</td>
<td><span class="r aa">CONFORMING</span> <span class="note">one contrast failure</span></td></tr>
<tr><td><code>docs.lmcache.ai</code></td><td class="note">Sphinx · sphinxawesome · Tailwind slate</td>
<td><span class="r no">NON-CONFORMING</span></td></tr>
</tbody></table>''')
A('<h3>Two live contrast failures</h3>')
A('<table><thead><tr><th>Where</th><th>Role</th><th>Current</th><th>on White</th><th>on Mist</th>'
  '<th>Replace with</th><th>on White</th><th>on Mist</th></tr></thead><tbody>')
for where,role,cur,new,gs in LIVE_FAILS:
    A(f'<tr><td class="note">{where}</td><td><b>{role}</b></td>'
      f'<td class="sw"><span class="chip" style="background:{cur}"></span><code>{cur}</code></td>'
      f'<td>{badge(cr(cur,WHITE))}</td><td>{badge(cr(cur,MIST))}</td>'
      f'<td class="sw"><span class="chip" style="background:{new}"></span><code>{new}</code></td>'
      f'<td>{badge(cr(new,WHITE))}</td><td>{badge(cr(new,MIST))}</td></tr>')
A('</tbody></table>')
A('''<div class="grid g3" style="margin-top:20px">
<div class="card"><h4>docs — the logo</h4><p>A raster PNG plated on opaque white. On the dark
ground it floats as a bright box. The one defect CSS cannot fix.</p></div>
<div class="card"><h4>docs — the Mermaid box</h4><p><code>custom.css</code> forces
<code>#ffffff !important</code> on every diagram. Same bug as the plated logo.</p></div>
<div class="card"><h4>docs — the token overlay</h4><p><code>lmcache-docs-overrides.css</code> maps
the whole brand onto the theme&rsquo;s HSL variables. A stylesheet and one line in
<code>conf.py</code>.</p></div>
<div class="card"><h4>docs — self-hosted fonts</h4><p>Enterprise and university networks block font
CDNs, and that is a large share of the docs audience.</p></div>
<div class="card"><h4>both — sentence case</h4><p>Remove <code>text-transform: capitalize</code> from
headings and set the case in the source text.</p></div>
<div class="card"><h4>both — line height</h4><p>Body prose moves from 1.3 to 1.55. 1.3 is a UI
density, not a reading one.</p></div>
</div>''')
A('</div></section>')

# ── Self-check ──────────────────────────────────────────────────────
A('<section><div class="wrap"><h2><span class="num">§12</span>Build self-check</h2>')
if FAILS:
    A('<div class="callout bad"><p><b>This build has contrast failures:</b></p><ul>')
    for f in FAILS: A(f'<li><code>{f}</code></li>')
    A('</ul></div>')
else:
    A('<p>Every token in this system meets or exceeds its contrast target against both grounds of '
      'both themes. Checked at build time, on every build.</p>'
      '<p><span class="r aaa">PASS</span> &nbsp;<span class="note" '
      'style="font-family:var(--font-mono);font-size:12px">'
      f'{len(LIGHT_TEXT)+len(DARK_TEXT)+len(STATUS)*2} token/ground pairs verified</span></p>')
A('</div></section>')

A(f'''</main>
<footer class="sp"><div class="wrap">
  <p style="margin:0">LMCache Design System, revision A · 21 September 2026 ·
  <code>tokens/lmcache-tokens.css</code> governs on any conflict.<br>
  Never assert a contrast ratio you have not computed. Every figure on this page is computed at
  build time from the token values themselves.</p>
</div></footer>
<script>
{(ROOT/'tokens'/'lmcache-theme-toggle.js').read_text() if (ROOT/'tokens'/'lmcache-theme-toggle.js').exists() else ''}
</script>
</body></html>''')

out = HERE / 'index.html'
out.write_text('\n'.join(H))
print(f'wrote {out}  ({out.stat().st_size:,} bytes)')
if FAILS:
    print('CONTRAST FAILURES:', *FAILS, sep='\n  ')
    sys.exit(1)
print('contrast self-check: PASS')
