# Techie brief: Virtual Bookkeeping page tweaks (Sept 2026)

**Owner:** Techie (implement) · Bart (pick proof variant if not default)  
**Copy source:** `15-page-tweaks-sept-2026.md` · proof system: `16-proof-points.md`  
**Rule:** Ship these exact blocks unless Bart picks a different proof variant.

---

## Implement order

1. **Fit-check trust strip + Formspree**: `/fit-check/` (and compact strip on CTAs). Wire `YOUR_BOOKKEEPING_FORM_ID`. Do not launch a dead form; keep `mailto:hello@meridian.dev` as fallback.  
2. **Hero proof line (Variant A)**: `/virtual-bookkeeping/` and `/for-founders/` when that route exists.  
3. **Standard admin sample month**: under Light admin / Standard on main LP. Include hard-cap note.  
4. **Three-column comparison**: “Pick your operating style” on main LP; mirror on for-founders.  
5. **Catch-up pricing clarity**: three illustrative examples on `/catch-up-bookkeeping/`.  
6. **Proof Variant B/C**: only after Bart fills tokens or approves a CPA quote (`16-proof-points.md` checklist).

---

## Pages to touch

| Page | Status (staging at brief time) | Blocks |
|------|--------------------------------|--------|
| `/virtual-bookkeeping/` | Live | A (Variant A), B, C, E compact |
| `/for-founders/` | May 404 until built | A (founders Variant A), B, E compact, optional short C |
| `/catch-up-bookkeeping/` | Live | D |
| `/fit-check/` | May 404 until built | E full strip + form wiring |

Staging root:  
`http://meridian-studio-site-543052825935.s3-website-us-west-2.amazonaws.com/`

---

## Exact defaults (do not improvise metrics)

- Hero proof: **Variant A** (process/studio). Not B or C until Bart says so.  
- Trust strip: `Reply in 1 business day · No weekly meeting upsell · Not a CPA.`  
- Helper: `Not sure? Choose Not sure. We’ll recommend Starter vs Standard.`  
- Prices: Starter from **$299/mo**; Standard from **$449/mo** (promo **$399** on request OK in FAQ/pricing notes); catch-up from **$200 per month behind**.  
- Admin: Standard only, **3 hr/mo hard cap**.  
- Spelling: British (categorisation, organised). No em dashes.  
- No invented customer counts, stars, logos, or quotes.

---

## Formspree checklist

- [ ] Replace `YOUR_BOOKKEEPING_FORM_ID` with production ID  
- [ ] Notify `hello@meridian.dev`  
- [ ] Thank-you / success state  
- [ ] “Not sure” path for Starter vs Standard preserved in field options  
- [ ] Spam honeypot / basic rate limit if available  

---

## QA before ship

- [ ] Every new block matches `15-page-tweaks-sept-2026.md` wording  
- [ ] Catch-up examples labelled **Illustrative**  
- [ ] Comparison names categories (Weekly team / AI finance OS / Meridian), tone clear not snarky  
- [ ] No `[N]`, `[industry]`, or `[CPA name]` visible on production  
- [ ] Mobile: three columns stack cleanly  
- [ ] CTAs still go to fit check + `hello@meridian.dev`  

---

## Done means

Paste-ready blocks from `15` are on the right pages, Formspree is live or email fallback is obvious, README index lists `15`, `16`, and this brief, and nothing fabricated was added for “social proof.”
