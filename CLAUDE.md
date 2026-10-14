# LMCache Design System — working notes

Read `docs/LMCache-design-system-spec.md` before changing anything. The token file
`tokens/lmcache-tokens.css` governs on any conflict.

## Authorship

`.claude/rules/git-rules.md` is binding. Karsten Wade is the sole author of record;
no AI trailers, banners, or identities in git history. Enable the hook once per clone:

    git config core.hooksPath .githooks

## Scope

This system governs LMCache's own properties. Tensormesh corporate material is out of
scope entirely.

## Rebuilding — run both after any change

    cd templates && python3 _build_templates.py   # regenerates the SVGs, validates fields.py
    cd spec-page && python3 build.py              # regenerates the proof, recomputes contrast

Both exit non-zero on failure. They are the test suite. `templates/fields.py` is the
single field vocabulary; a placeholder that is not declared there fails the build.

## Never assert a contrast ratio you have not computed

Every figure in the spec was measured against the named ground. Change a value and you
measure it against both grounds of both themes before it ships.
