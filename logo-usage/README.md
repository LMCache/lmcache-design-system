# Logo usage page

The public guidelines for the LMCache name and logo, built from one template into two pages.

    template.html            The source. Edit this file only.
    build.py                 Builds everything below. Run it after any change here or in marks/.
    i18n/LANG.json           Translations: English source string → translated string.
    index[.LANG].html        Stand-alone page, per language. Open it in a browser from this directory.
    wordpress-snippet[.LANG].html
                             The same page for lmcache.ai, pasted into one Elementor HTML widget.

`build.py` also writes `dist/lmcache-logo-kit.zip` (ignored by git), which is the download
served from the lmcache.ai media library.

## Rebuilding

    cd logo-usage && python3 build.py

Every mark is inlined from `marks/` as a data URI, so neither page needs any other file. PNG
downloads are drawn from the SVGs in the visitor's browser. The build exits non-zero if a
placeholder in the template is not resolved.

## Translations

Each file in `i18n/` maps English strings in `template.html` to one language: Simplified
Chinese (`zh-CN`) and Korean (`ko`). The build fails if a key no longer matches the template,
so a change to English copy shows up as a missing translation rather than shipping half-English.
After changing English text, update the same key in every `i18n/` file.

A translation starting with `~` drops the space before it; one ending in `~` drops the space
after it. Korean uses this to attach a particle directly to a link.

Chinese and Korean text falls back to system CJK sans faces (PingFang, Noto Sans, Microsoft
YaHei, Apple SD Gothic Neo, Malgun Gothic), since Geist and Inter carry Latin only.

## Publishing to lmcache.ai

1. Upload `dist/lmcache-logo-kit.zip` to the WordPress media library. Keep the filename.
2. If the upload's address differs from `KIT_URL` in `build.py`, change it and rebuild.
3. Open the `logo-usage` page in Elementor. Paste all of `wordpress-snippet.html` into its one
   HTML widget, replacing what is there. Update.
4. For each translated page, Polylang links it to the English page. Paste
   `wordpress-snippet.LANG.html` into that page's HTML widget the same way.

The page needs an administrator account, because WordPress strips inline SVG and scripts from
other roles. Its styles follow the site's `body.light-mode` / `body.dark-mode` switch.
