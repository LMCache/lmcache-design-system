# Logo usage page

The public guidelines for the LMCache name and logo, built from one template into two pages.

    template.html            The source. Edit this file only.
    build.py                 Builds everything below. Run it after any change here or in marks/.
    index.html               Stand-alone page. Open it in a browser from this directory.
    wordpress-snippet.html   The same page for lmcache.ai, pasted into one Elementor HTML widget.

`build.py` also writes `dist/lmcache-logo-kit.zip` (ignored by git), which is the download
served from the lmcache.ai media library.

## Rebuilding

    cd logo-usage && python3 build.py

Every mark is inlined from `marks/` as a data URI, so neither page needs any other file. PNG
downloads are drawn from the SVGs in the visitor's browser. The build exits non-zero if a
placeholder in the template is not resolved.

## Publishing to lmcache.ai

1. Upload `dist/lmcache-logo-kit.zip` to the WordPress media library. Keep the filename.
2. If the upload's address differs from `KIT_URL` in `build.py`, change it and rebuild.
3. Open the `logo-usage` page in Elementor. Paste all of `wordpress-snippet.html` into its one
   HTML widget, replacing what is there. Update.

The page needs an administrator account, because WordPress strips inline SVG and scripts from
other roles. Its styles follow the site's `body.light-mode` / `body.dark-mode` switch.
