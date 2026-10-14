/* LMCache theme switch — canonical implementation
 * Revision A · 21 September 2026
 *
 * Contract, unchanged from what lmcache.ai and blog.lmcache.ai already
 * ship, so existing CSS keeps working:
 *   - the theme class lives on <body>: .light-mode | .dark-mode
 *   - the choice persists in localStorage under the key "theme"
 *   - values are the strings "light" and "dark"
 *
 * Three things this fixes against the live version:
 *   1. The live script defaults to light and never reads the OS
 *      preference. This one treats "no stored choice" as "follow the
 *      OS", and keeps following it until the visitor picks a side.
 *   2. The live script hides the whole page with body{opacity:0} and
 *      reveals it on DOMContentLoaded. With JS off or slow, the page
 *      is blank. This one stamps the class before first paint from a
 *      blocking inline script and never hides anything.
 *   3. The live buttons have no accessible state. These are real
 *      toggles with aria-pressed.
 *
 * PART 1 must be inlined in <head>, before any stylesheet, and must
 * not be deferred or async — that is what makes it run before paint.
 */

/* ── PART 1 — inline this verbatim in <head> ───────────────────────── */
(function () {
  try {
    var stored = localStorage.getItem('theme');
    var theme = (stored === 'light' || stored === 'dark')
      ? stored
      : (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
    // <body> does not exist yet at this point, so stamp html and let
    // PART 2 mirror it onto body the moment body is parsed.
  } catch (e) {
    document.documentElement.setAttribute('data-theme', 'light');
  }
})();

/* ── PART 2 — the switch itself. Safe to load from a file. ─────────── */
(function () {
  'use strict';

  var KEY = 'theme';
  var mq = window.matchMedia('(prefers-color-scheme: dark)');

  function stored() {
    try {
      var v = localStorage.getItem(KEY);
      return (v === 'light' || v === 'dark') ? v : null;
    } catch (e) { return null; }
  }

  function resolved() {
    return stored() || (mq.matches ? 'dark' : 'light');
  }

  function paint(theme) {
    var b = document.body;
    if (b) {
      b.classList.remove('light-mode', 'dark-mode');
      b.classList.add(theme === 'dark' ? 'dark-mode' : 'light-mode');
    }
    document.documentElement.setAttribute('data-theme', theme);

    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute('content', theme === 'dark' ? '#001F23' : '#FFFFFF');

    document.querySelectorAll('[data-theme-set]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', String(btn.dataset.themeSet === theme));
    });

    document.dispatchEvent(new CustomEvent('lm:themechange', { detail: { theme: theme } }));
  }

  function set(theme) {
    try { localStorage.setItem(KEY, theme); } catch (e) {}
    paint(theme);
  }

  // Follow the OS until the visitor makes a choice of their own.
  mq.addEventListener('change', function () { if (!stored()) paint(resolved()); });

  function init() {
    paint(resolved());
    document.querySelectorAll('[data-theme-set]').forEach(function (btn) {
      if (!btn.hasAttribute('aria-pressed')) btn.setAttribute('aria-pressed', 'false');
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        set(btn.dataset.themeSet === 'dark' ? 'dark' : 'light');
      });
    });
    // Back-compat with the Elementor widgets already on the WP sites.
    var l = document.querySelector('.light-mode-btn'), d = document.querySelector('.dark-mode-btn');
    if (l && !l.dataset.themeSet) l.addEventListener('click', function () { set('light'); });
    if (d && !d.dataset.themeSet) d.addEventListener('click', function () { set('dark'); });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  window.LMCacheTheme = { get: resolved, set: set, clear: function () {
    try { localStorage.removeItem(KEY); } catch (e) {}
    paint(resolved());
  }};
})();

/* Markup for the pair of buttons:
 *
 *   <button type="button" data-theme-set="light" aria-pressed="false"
 *           aria-label="Use light theme">…sun…</button>
 *   <button type="button" data-theme-set="dark"  aria-pressed="false"
 *           aria-label="Use dark theme">…moon…</button>
 */
