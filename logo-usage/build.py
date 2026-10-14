#!/usr/bin/env python3
"""Build the LMCache logo usage pages and the logo kit from template.html and marks/.

    cd logo-usage && python3 build.py

For English and for each translation in i18n/, writes:
    logo-usage/index[.LANG].html               stand-alone page (open it in a browser)
    logo-usage/wordpress-snippet[.LANG].html   paste into one Elementor HTML widget on lmcache.ai
and once:
    dist/lmcache-logo-kit.zip                  upload to the lmcache.ai media library

Every mark is inlined from marks/, so the pages work with no other files.
Exits non-zero if a placeholder is unresolved or a translation key is not found in the template.
"""
import html
import json
import pathlib
import re
import sys
import urllib.parse
import zipfile

REPO_URL = "https://github.com/LMCache/lmcache-design-system"
# The media library address for the kit. WordPress puts an upload made in
# October 2026 under /2026/10/; change this if the upload lands elsewhere.
KIT_URL = "https://lmcache.ai/wp-content/uploads/2026/10/lmcache-logo-kit.zip"
PAGE_URL = "https://lmcache.ai/en/logo-usage/"
TITLE = "LMCache Logo Usage"
DESCRIPTION = ("How to use the LMCache wordmark: files for every background, clear space, "
               "minimum sizes, colors, and what to avoid.")

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
MARKS = ROOT / "marks"


def path(name):
    if name == "ascii-txt":
        return MARKS / "ascii" / "lmcache-ascii.txt"
    if name.startswith("ascii"):
        return MARKS / "ascii" / f"lmcache-{name}.svg"
    return MARKS / "svg" / f"lmcache-{name}.svg"


def raw(name):
    text = path(name).read_text()
    return text if name == "ascii-txt" else re.sub(r">\s+<", "><", text).strip()


def uri(name):
    mime = "text/plain" if name == "ascii-txt" else "image/svg+xml"
    return "data:%s;charset=utf-8,%s" % (mime, urllib.parse.quote(raw(name), safe=" /:=;,.-_()'"))


CROSS = ('<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 4l8 8M12 4l-8 8" '
         'stroke="currentColor" stroke-width="2" fill="none"/></svg>')
CHECK = ('<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3.2 3L13 4.5" '
         'stroke="currentColor" stroke-width="2" fill="none"/></svg>')


# ── Translation ────────────────────────────────────────────────────────────
# Keys are the English strings exactly as they appear in template.html: text
# between tags, alt and aria-label values, and download-link labels. A leading
# ~ in a translation removes the whitespace before it; a trailing ~ removes the
# whitespace after it (for languages that attach particles to a link).

LABEL_INDEX = {"dl": 2, "png": 3, "yes": 1, "no": 1}


def translate(template, strings, lang):
    used = set()

    def look(text):
        if text in strings:
            used.add(text)
            return strings[text]
        return None

    start = template.index('<div class="lmc-logo"')
    end = template.index("<script>")
    head, body, tail = template[:start], template[start:end], template[end:]

    def attr(m):
        t = look(m.group(2))
        return '%s="%s"' % (m.group(1), html.escape(t, quote=True)) if t else m.group(0)
    body = re.sub(r'(alt|aria-label)="([^"]*)"', attr, body)

    def label(m):
        parts = m.group(1).split(":")
        i = LABEL_INDEX.get(parts[0])
        if i is None:
            return m.group(0)
        if parts[0] == "no" and len(parts) == 1:
            parts.append("Don't")
        if parts[0] == "png" and len(parts) == 3:
            return m.group(0)  # numeric default label, e.g. "PNG 1200px"
        if i < len(parts):
            t = look(parts[i])
            if t:
                parts[i] = t.replace(":", "：")
        return "{{" + ":".join(parts) + "}}"
    body = re.sub(r"\{\{([^}]+)\}\}", label, body)

    def text(m):
        node = m.group(1)
        core = node.strip()
        t = look(core)
        if not t:
            return m.group(0)
        lead = node[: len(node) - len(node.lstrip())]
        trail = node[len(node.rstrip()):]
        if t.startswith("~"):
            t, lead = t[1:], ""
        if t.endswith("~"):
            t, trail = t[:-1], ""
        return ">" + lead + html.escape(t, quote=False) + trail + "<"
    body = re.sub(r">([^<>{}]+)<", text, body)

    missing = [k for k in strings if k not in used and k not in (TITLE, DESCRIPTION)]
    if missing:
        sys.exit("%s: %d translation keys not found in template.html:\n  %s" % (
            lang, len(missing), "\n  ".join(missing)))
    return head + body + tail


# ── Placeholders ───────────────────────────────────────────────────────────

def make_placeholder(lang):
    def placeholder(match):
        parts = match.group(1).split(":")
        kind = parts[0]
        if kind == "lang":
            return lang
        if kind == "repo":
            return REPO_URL
        if kind == "kit":
            return KIT_URL
        if kind == "img":
            return uri(parts[1])
        if kind == "dl":
            name = parts[1]
            label = parts[2] if len(parts) > 2 else "SVG"
            return '<a href="%s" download="%s" data-lmc-svg="%s">%s</a>' % (
                uri(name), path(name).name, name, html.escape(label))
        if kind == "png":
            name, width = parts[1], parts[2]
            label = parts[3] if len(parts) > 3 else "PNG %spx" % width
            filename = parts[4] if len(parts) > 4 else "lmcache-%s-%s.png" % (name, width)
            if len(parts) <= 4 and name.endswith("-512") and width == "512":
                filename = "lmcache-%s.png" % name
            return '<a href="#" data-lmc-png="%s" data-w="%s" download="%s">%s</a>' % (
                name, width, filename, html.escape(label))
        if kind == "no":
            return '<span class="lmc-verdict lmc-no">%s%s</span>' % (
                CROSS, html.escape(parts[1] if len(parts) > 1 else "Don't"))
        if kind == "yes":
            return '<span class="lmc-verdict lmc-yes">%s%s</span>' % (CHECK, html.escape(parts[1]))
        if kind == "ascii":
            lines = (MARKS / "ascii" / "lmcache-ascii.txt").read_text().rstrip("\n").split("\n")
            return "\n".join('<span class="o">%s</span><span class="c">%s</span>' % (
                html.escape(line[:14]), html.escape(line[14:].rstrip())) for line in lines)
        raise ValueError("unknown placeholder: " + match.group(0))
    return placeholder


STANDALONE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="icon" href="../marks/svg/lmcache-favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="../fonts/lmcache-fonts.css">
<style>body{{margin:0;padding:0 20px;background:#F0FAFB}}@media (prefers-color-scheme:dark){{body{{background:#001F23}}}}</style>
</head>
<body>
{body}
</body>
</html>
"""

KIT_README = """LMCache logo kit

Usage guidelines: {page}
Source files:     {repo}

svg/    Wordmark, lockups, favicon, app icon, and avatars. Use these first.
png/    Raster versions for tools that do not accept SVG.
ascii/  The ASCII mark, for swag and terminal-style material.

LMCache and the LMCache logo are trademarks of Tensormesh. The artwork is
published under the Apache License 2.0, which does not grant trademark rights.
Merchandise of any kind needs written permission from the LMCache maintainers.
"""


def build_kit(out):
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for sub in ("svg", "png", "ascii"):
            for f in sorted((MARKS / sub).iterdir()):
                if f.is_file() and not f.name.startswith(("_", ".")):
                    z.write(f, f"lmcache-logo-kit/{sub}/{f.name}")
        z.writestr("lmcache-logo-kit/README.txt", KIT_README.format(page=PAGE_URL, repo=REPO_URL))
    return out


def render(template, lang, suffix, title, description):
    snippet = re.sub(r"\{\{([^}]+)\}\}", make_placeholder(lang), template)
    if "{{" in snippet:
        sys.exit("%s: unresolved placeholder in template.html" % lang)
    (HERE / f"wordpress-snippet{suffix}.html").write_text(snippet)
    (HERE / f"index{suffix}.html").write_text(STANDALONE.format(
        lang=lang, title=html.escape(title), description=html.escape(description, quote=True), body=snippet))
    return [f"wordpress-snippet{suffix}.html", f"index{suffix}.html"]


def main():
    template = (HERE / "template.html").read_text()
    written = render(template, "en", "", TITLE, DESCRIPTION)
    for f in sorted((HERE / "i18n").glob("*.json")):
        data = json.loads(f.read_text())
        lang, strings = data["lang"], data["strings"]
        translated = translate(template, strings, lang)
        written += render(translated, lang, "." + lang, strings.get(TITLE, TITLE),
                          strings.get(DESCRIPTION, DESCRIPTION))
    kit = build_kit(ROOT / "dist" / "lmcache-logo-kit.zip")
    print("wrote " + ", ".join("logo-usage/" + w for w in written))
    print("wrote %s (%d KB)" % (kit.relative_to(ROOT), kit.stat().st_size // 1024))


if __name__ == "__main__":
    main()
