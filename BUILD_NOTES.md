# BUILD_NOTES — Meridian site

**Built:** 27 September 2026 (PT)  
**Path:** `/workspace/vibe-code-rescue/site/`  
**Stack:** Plain HTML + CSS + minimal JS; `build.py` regenerates pages

## Pages created (26 HTML)

| URI | Purpose |
|-----|---------|
| `/` | Meridian home — promise, experience, services grid, CTA |
| `/vibe-code-rescue/` | Full product page + FAQPage schema + sample audit link |
| `/product-engineering/` | Stub — coming soon / inquire |
| `/security-hardening/` | Stub — coming soon / inquire |
| `/fractional-cto/` | Stub — coming soon / inquire |
| `/customer-growth/` | Scoped customer-growth package — root path, not under `/services/` |
| `/virtual-bookkeeping/` | Monthly bookkeeping and admin package — root path, not under `/services/` |
| `/pricing/` | Transparent ladder + not-for-you |
| `/request/` | Lead capture form |
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
- `last updated: 27 September 2026` on key pages
- Internal linking: tool ↔ symptom ↔ pricing ↔ request
- `/robots.txt` allows GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-User, anthropic-ai, PerplexityBot, Google-Extended, Googlebot
- Real markdown `/llms.txt` and `/llms-full.txt` (not HTML shells)
- `/sitemap.xml` with 29 URLs
- Sample redacted audit: `/artifacts/sample-audit.md`

## Design

- Brand mark: geometric indigo circle/cross SVG (CSS/SVG, original)
- Palette: indigo/slate
- Font: Inter (Google) with system fallbacks
- Mobile-first nav with toggle; sticky header

## Positioning copy used

Senior engineers who salvage AI-built apps into production-ready software. Audit in 48 hours. Fix security, auth, data, and payments first. Keep what works. Fixed scope. You own the code. Optional AI guardrails after rescue. Empathy, no shame.

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
