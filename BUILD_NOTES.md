# BUILD_NOTES: Meridian site

**Built:** 29 September 2026 (PT)  
**Path:** site root (`build.py` writes HTML next to itself)  
**Stack:** Plain HTML + CSS + minimal JS; `build.py` regenerates pages

## Pages created (30 HTML)

| URI | Purpose |
|-----|---------|
| `/` | Meridian home: studio intro, rescue, services, CTA |
| `/vibe-code-rescue/` | Full product page + FAQPage schema + sample audit link |
| `/product-engineering/` | Stub: not packaged yet / inquire |
| `/security-hardening/` | Stub: not packaged yet / inquire |
| `/fractional-cto/` | Stub: not packaged yet / inquire |
| `/customer-growth/` | Scoped customer-growth package. Root path, not under `/services/` |
| `/virtual-bookkeeping/` | Monthly bookkeeping page: pricing, onboarding, FAQ. Root path, not under `/services/` |
| `/virtual-bookkeeping/fit-check/` | Dedicated bookkeeping fit-check form (not the rescue diagnostic) |
| `/virtual-bookkeeping/for-founders/` | Founders / SaaS / product operators |
| `/virtual-bookkeeping/for-ecommerce/` | Shorter ecommerce niche page |
| `/catch-up-bookkeeping/` | Catch-up project, then handoff to the monthly close |
| `/pricing/` | Rescue ladder, plus published bookkeeping starting prices |
| `/request/` | Software diagnostic lead form. Bookkeeping interest redirects to the fit check |
| `/diagnostic/` | Alias of request form |
| `/rescue/lovable/` … `/rescue/windsurf/` | 7 tool pages (incl. Windsurf bonus) |
| `/problems/*` | 5 symptom pages |
| `/faq/` | Site FAQ + FAQPage schema |
| `/about/` | Studio / entity |
| `/guides/what-is-vibe-code-rescue/` | Definitional guide |
| `/guides/rescue-vs-rewrite/` | Decision guide |

## AEO / SEO features

- Organization + ProfessionalService JSON-LD (home, about, key pages)
- Service JSON-LD on service and tool pages
- FAQPage JSON-LD on VCR, FAQ, pricing, tool, problem, guide pages
- BreadcrumbList JSON-LD where breadcrumbs appear
- Answer-first paragraphs under H1
- Open Graph + Twitter card tags on every HTML page
- `last updated: 29 September 2026` on key pages
- Internal linking: tool ↔ symptom ↔ pricing ↔ request
- `/robots.txt` allows GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-User, anthropic-ai, PerplexityBot, Google-Extended, Googlebot
- Real markdown `/llms.txt` and `/llms-full.txt` (not HTML shells)
- `/sitemap.xml` with 33 URLs
- Sample redacted audit: `/artifacts/sample-audit.md`

## Design

- Brand mark: geometric indigo circle/cross SVG (CSS/SVG, original)
- Palette: indigo/slate
- Font: Inter (Google) with system fallbacks
- Mobile-first nav with toggle; sticky header

## Positioning copy used

Senior studio. Vibe Code Rescue: written diagnostic in about 48 hours, then a fixed scope on security, auth, data, and payments. Keep what works. The client owns the code. Bookkeeping prices stay Starter from $299/month, Standard from $449/month (featured), catch-up from $200 per month behind. Copy revised so it reads like a person wrote it, with no em dashes.

## No invented proof

No fake case-study metrics or client names.

## Generator

Source modules: `build.py` (assembled). Intermediate `_*.py` fragments may remain for regeneration; safe to delete intermediates and keep `build.py`.

## Content hashing (Vite-style)

`build.py` → `prepare_hashed_assets()`:

1. SHA-256 of `css/styles.css` and `js/main.js` (first 8 hex chars)
2. Emits `css/styles.<hash>.css` and `js/main.<hash>.js` (sources kept locally)
3. Prunes stale `styles.*.css` / `main.*.js` copies
4. All generated HTML links the hashed filenames only

Deploy: `./deploy.sh` (or `npm run deploy`) syncs to S3 with:

- Hashed CSS/JS: `Cache-Control: public, max-age=31536000, immutable`
- HTML: `Cache-Control: no-cache`
- Unhashed `css/styles.css` / `js/main.js` are **not** synced and are deleted from S3 if present
