# Meridian — static marketing site

Production-ready static site for **Meridian** (senior software studio), flagship service **Vibe Code Rescue**, and productized sibling offerings at `/customer-growth/` and `/virtual-bookkeeping/`.

- Real HTML files (not SPA-only) for crawlers and `llms.txt`
- Mobile-first, indigo/slate palette, Inter + system fonts
- Canadian English (en-CA)
- Last content update: **27 September 2026**

## Preview locally

```bash
cd site
npm run preview
# equivalent: python3 -m http.server 4173
# alternative: npm run preview:npx   (uses npx serve)
```

Open http://localhost:4173

Regenerate HTML from the Python builder (optional — committed HTML is already built):

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

The request form at `/request/` (and `/diagnostic/`) uses:

```html
data-formspree="https://formspree.io/f/YOUR_FORM_ID"
```

Replace `YOUR_FORM_ID` with your Formspree form id. Until then, submit falls back to `mailto:hello@meridian.dev` and shows a local success state.

## Open items

- Register/connect real domain (canonical URLs currently use `https://meridian.dev`)
- Provision `hello@meridian.dev` (or update contact everywhere)
- Set Formspree form id
- Optional: OG image asset, analytics, Calendly link

## AEO / SEO

See `BUILD_NOTES.md` for page inventory and schema / `llms.txt` details.
