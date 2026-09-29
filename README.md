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

## Forms

The bookkeeping fit check and the rescue diagnostic (`/request/` and `/diagnostic/`) POST JSON to the live Lambda URL in `FORM_ENDPOINT` (`build.py`) and `FORM_ENDPOINT` (`js/main.js`):

```text
https://zw6ddzuiurwjyywaeedub55xne0kfovs.lambda-url.us-west-2.on.aws/
```

Submit stays on the page and shows a thank-you state. `mailto:hello@meridian.dev` opens only when that fetch fails on the network. A hidden `company_website` field is the honeypot.

Bookkeeping sends `form=fit-check`, plus name, email, company, `plan` / `plan_interest` (including Not sure), message, notes, and the rest of the fit-check fields. The rescue form sends `form=diagnostic` with the same contact fields and the problem text as message.

Published prices on the bookkeeping pages: Starter from $299/month (close only), Standard from $449/month (close plus light admin, capped at 3 hours a month), catch-up from $200 per month behind. A Standard launch promo of $399/month is noted on the page; $449 is the published price. Any auto-reply should use those figures.

Do not point bookkeeping traffic at `/request/` or `/diagnostic/`. Those pages redirect `?interest=virtual-bookkeeping` (and catch-up) to the fit check.

## Bookkeeping copy index (September 2026)

Source for the live bookkeeping tweaks. Ship **Variant A** only. Do not publish Variant B or C, and do not leave `[N]`, `[industry]`, or `[CPA name]` on a page.

- [15-page-tweaks-sept-2026.md](docs/bookkeeping/15-page-tweaks-sept-2026.md): paste-ready blocks A–E
- [16-proof-points.md](docs/bookkeeping/16-proof-points.md): proof ladder. Variant B/C only after real data
- [TECHIE-BRIEF-tweaks.md](docs/bookkeeping/TECHIE-BRIEF-tweaks.md): implement order and QA

These files stay in the repo for the team. `deploy.sh` does not upload `docs/`.

## Analytics

No analytics snippet is installed. `js/main.js` emits events only when `window.dataLayer`, `window.gtag`, or `window.plausible` already exists:

- `bookkeeping_fit_check_submit`: inquiry, source, package, software, behind, needs, budget, timing, delivery (`lambda` or `mailto_fallback`). No name, email, or free text.
- `bookkeeping_cta_click`: label and href, from `data-track` on bookkeeping calls to action.

To collect them, add the provider snippet in `head()` (or before `js/main.js`) and confirm the provider name matches one of those three.

## Open items

- Register/connect real domain (canonical URLs currently use `https://meridian.dev`)
- Provision `hello@meridian.dev` (or update contact everywhere)
- Optional: OG image asset, analytics snippet, Calendly link

## AEO / SEO

See `BUILD_NOTES.md` for page inventory and schema / `llms.txt` details.
