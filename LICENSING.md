# Licensing

Three different things live in this repository and they are not under the same
terms. Read this before reusing anything.

## 1. Code, documentation, and templates — Apache 2.0

The specification, the token files, the CSS and JavaScript, the Python build
scripts, the SVG templates, and every document here are under the
[Apache License 2.0](LICENSE) — byte-identical to the licence LMCache itself
ships, so a contributor faces one set of terms across the project.

Use them, fork them, adapt them.

## 2. The vendored fonts — SIL Open Font License 1.1

`fonts/` carries Geist, Geist Mono, and Inter as woff2 and TTF. They are **not**
Apache-licensed and never become so by sitting in this repository.

All three are under the **SIL Open Font License 1.1** with `fsType` 0, which is
what permits both embedding and redistribution. The full text of each licence is
in `fonts/licenses/`, and the OFL requires that it travels with the fonts:

> Keep `fonts/licenses/` alongside any redistribution.

If you vendor these faces into another project, copy that directory too. This is
the one obligation in this repository that is easy to drop by accident.

## 3. The LMCache name and wordmark — a trademark question, not a copyright one

LMCache and the LMCache logo are trademarks of Tensormesh. Copyright in the
artwork in `marks/` is covered by Apache 2.0 above, but that licence
[explicitly does not grant trademark rights](LICENSE) — section 6 — and a
permissive copyright licence has never been the same thing as permission to
represent yourself as the project.

- **Fine:** using these marks to refer to LMCache — in documentation, a talk, an
  integration's "works with" badge, an article about the project.
- **Not fine:** using them as the identity of something that is not LMCache, or
  in a way that suggests the project endorses or produced your work.
- **Not fine without written permission:** merchandise of any kind that carries
  the name or a mark — shirts, stickers, mugs, and other swag — whether it is
  sold or given away. Ask the LMCache maintainers first.

The specification in `docs/LMCache-design-system-spec.md` governs *how* the
marks are drawn and placed. It is a correctness standard, not a grant of
permission. The public summary of these rules is the logo usage page on
`lmcache.ai`.
