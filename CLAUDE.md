# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Static, multilingual (RU default, EN, ZH, AR, TR, HI) landing page for ФарМозг / PharmaBrain (pharmabrain.ru): a catalog of AI agents, AI-first pharma systems, and GxP training courses. There is no build step, package manager, linter, or test suite: plain HTML + vanilla JS, served as static files by Nginx.

Preview locally with any static server, e.g. `python3 -m http.server 8000`, then open http://localhost:8000 (append `?lang=en`, `?lang=ar`, etc. to force a language).

## Architecture

The site is a handful of files that only work together:

- **`index.html`**: all markup, all CSS (inline `<style>`), and all app logic (inline `<script>` at the bottom). It loads `i18n.js`, then `i18n.zh.js`, `i18n.ar.js`, `i18n.tr.js` and `i18n.hi.js`. The script tags carry a `?v=N` cache-buster: bump it whenever the i18n files change, or visitors can get a new page with stale scripts.
- **`i18n.js`**: all content and data, as globals:
  - `window.I18N = { ru: {...}, en: {...} }`: UI strings keyed by id. Supports `{var}` placeholders, filled by `t(key, vars)`. A missing key falls back to `en` (to `ru` for Russian), and then to the key itself.
  - `window.PRODUCTS` (AI-first systems), `window.AGENTS` (ready agents), `window.COURSES` (training programs): catalog items. Localized fields are `{ ru, en }` objects, resolved by `loc(value, lang)`, with the same English fallback. Non-localized fields (such as the `forms` and `topics` arrays and some `name`s) are plain strings.

Static markup is translated through data attributes that `applyStatic()` processes: `data-i18n` (textContent), `data-i18n-html` (innerHTML), `data-i18n-placeholder`, `data-i18n-alt`, `data-i18n-aria`, `data-i18n-title`. When you add visible text, add the key to `ru` and `en` in `I18N` **and to all four `i18n.<lang>.js` files**, then tag the element; don't hardcode text.

The extra languages live in `i18n.<lang>.js`, each a single `addTranslations(lang, { ui, items })` call (defined in `i18n.js`). `ui` mirrors the `I18N.en` keys. `items` is keyed `"PRODUCTS:<id>"`, `"AGENTS:<id>"` or `"COURSES:<id>"` and holds that item's `name`/`full`/`pitch`/`about`/`featuresTitle` text plus an `ai` array of feature descriptions in the same order as the item's `ai`. Adding a catalog item or a feature line means adding its translation to all four files too. Keep `{placeholders}` and HTML tags identical to English.

Arabic is right-to-left: `applyStatic()` sets `dir="rtl"` for languages in `RTL_LANGS`, and the `[dir="rtl"]` rules in the CSS mirror anything positioned with left/right (step lines, quote borders, the appeal photos, the modal). New CSS that uses `left`/`right`, `padding-left` or `border-left` needs a matching `[dir="rtl"]` override. Chinese, Arabic and Hindi use system fonts (Plus Jakarta Sans has no glyphs for them) and get extra heading line-height via `html:lang(..)` rules.

The catalog grid, filter buttons, the detail modal, and the contact-form `<select>` are all rendered by JS from the three data arrays, based on the current `offer` (`agents` | `systems` | `courses`) and category:

- Category ids live in `CAT_IDS`, `AGENT_CAT_IDS`, and `COURSE_CAT_IDS` in the inline script. Each id needs a matching `I18N` key with the prefix `cat_`, `agent_cat_`, or `course_cat_`. A new category needs both.
- An item's `cat` must be one of those ids, or the item won't appear under any filter or in the form select.
- Item images are `images/agents/<img>` for agents and `images/products/<img>` for systems. Courses have no image; they render a CSS `course-shot--<cat>` tile.
- Counts such as "21 агент", "30 систем" and "16 курсов" are hardcoded in `I18N` strings, in both languages (`hero_meta*`, `offer_*_hint`, `appeal_p1`). Update them when you add or remove catalog items.

The page reads like a startup pitch: hero → who we are (`#why`) → the founders' Wikipedia-style appeal (`#appeal`) → press (`#press`, quotes from «Фармацевтический вестник» №10, September 2026) → what we've built (`#catalog` and the sections after it). Section kickers are numbered by hand ("01 · …"), so renumber them when you add or move a section.

The language is picked from the `?lang=` URL param, then `localStorage["farmozg-lang"]`, then the browser language if it's one of `LANGS`, else Russian. The switcher is the `#langSelect` dropdown in the nav.

The contact form POSTs JSON (`name`, `email`, `phone`, `company`, `interest`) to `https://pharmabrain.ru/PharmAI/api/contact`, a separate FastAPI backend that isn't in this repo. It expects `{ success, message | error }` back.

## Product screenshots

`images/products/*.png` (the AI-first system UI mockups) are generated, not hand-made:

```bash
python3 scripts/generate_screenshots.py   # requires Pillow; uses macOS Arial fonts at /System/Library/Fonts/Supplemental
```

Each screen is an `add(dict(file=..., product=..., nav=..., active=..., draw=lambda d: (...), ai=(title, items, actions)))` spec. The script re-renders all of them. `images/agents/*.png` are real screenshots of the agents and aren't generated.

## Deployment

`DEPLOYMENT.md` describes the production setup: Nginx serves the repo from `/var/www/pharmabrain.ru` with `try_files ... /index.html`, uses Certbot for HTTPS, and reverse-proxies `/PharmAI/` to the FastAPI app on `127.0.0.1:8002`. Deploying means updating the files in that web root.
