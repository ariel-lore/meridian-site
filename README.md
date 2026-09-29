# Meridian static marketing site

Production-ready static site for **Meridian** (senior software studio), flagship service **Vibe Code Rescue**, and packaged services at `/customer-growth/` and `/virtual-bookkeeping/`.

- Real HTML files (not SPA-only) for crawlers and `llms.txt`
- Mobile-first, indigo/slate palette, Inter + system fonts
- Canadian English (en-CA)
- Last content update: **29 September 2026**

## Preview locally

```bash
cd site
npm run preview
# equivalent: python3 -m http.server 4173
# alternative: npm run preview:npx   (uses npx serve)
```

Open http://localhost:4173

Regenerate HTML from the Python builder (optional; committed HTML is already built):

```bash
npm run build
# or: python3 build.py
```

No build step is required to deploy: the directory is the site root.

## Deploy

Point any static host at this `site/` folder (or its contents).

### Vercel
- Import the repo; set **Root Directory** to `site` (or `vibe-code-rescue/site`)
- Framework: Other; output = site root (no build, or `python3 build.py` if you want regen)
- Or CLI: `npx vercel` from `site/`

### Netlify
- Base directory: `site`
- Publish directory: `.` (same folder)
- Or drag-and-drop the `site/` folder in the Netlify UI

### Cloudflare Pages
- Root / build output: `site`
- Build command: empty or `python3 build.py`
- Output directory: `.`

## Formspree

The rescue / customer-growth form at `/request/` (and `/diagnostic/`) uses:

```html
data-formspree="https://formspree.io/f/YOUR_FORM_ID"
```

Replace `YOUR_FORM_ID` with your Formspree form id. Until then, submit falls back to `mailto:hello@meridian.dev` and shows a local success state.

Bookkeeping does **not** use that form. The fit check at `/virtual-bookkeeping/fit-check/` posts to `BOOKS_FORM` in `build.py`:

```text
https://formspree.io/f/YOUR_BOOKKEEPING_FORM_ID
```

`YOUR_BOOKKEEPING_FORM_ID` is still a placeholder. Email is not delivered until it is replaced with a Formspree form whose inbox is `hello@meridian.dev`. Until then, submit opens a mailto draft to `hello@meridian.dev` and shows the thank-you message. The draft is not sent until the visitor sends it from their mail app.

Published prices on the bookkeeping pages: Starter from $299/month (close only), Standard from $449/month (close plus light admin, capped at 3 hours a month), catch-up from $200 per month behind. A Standard launch promo of $399/month is noted on the page; $449 is the published price. Any auto-reply should use those figures.

Do not point bookkeeping traffic at `/request/` or `/diagnostic/`. Those pages redirect `?interest=virtual-bookkeeping` (and catch-up) to the fit check.

## Analytics

No analytics snippet is installed. `js/main.js` emits events only when `window.dataLayer`, `window.gtag`, or `window.plausible` already exists:

- `bookkeeping_fit_check_submit`: inquiry, source, package, software, behind, needs, budget, timing, delivery (`formspree`, `mailto`, or `mailto_fallback`). No name, email, or free text.
- `bookkeeping_cta_click`: label and href, from `data-track` on bookkeeping calls to action.

To collect them, add the provider snippet in `head()` (or before `js/main.js`) and confirm the provider name matches one of those three.

## Open items

- Register/connect real domain (canonical URLs currently use `https://meridian.dev`)
- Provision `hello@meridian.dev` (or update contact everywhere)
- Set Formspree form id for the rescue form (`YOUR_FORM_ID`)
- Set a separate Formspree form id for bookkeeping (`YOUR_BOOKKEEPING_FORM_ID` in `build.py`)
- Optional: OG image asset, analytics snippet, Calendly link

## AEO / SEO

See `BUILD_NOTES.md` for page inventory and schema / `llms.txt` details.
