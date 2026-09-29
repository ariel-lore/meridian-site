# Page tweaks: September 2026 (paste-ready for Techie)

**Brand:** Meridian (meridian.dev) · Virtual Bookkeeping  
**Tone:** Warm, technical-founder, plain English. British spelling. No em dashes.  
**Rule:** Do not invent customer counts, star ratings, logos, or fake case studies.  
**Default:** Ship Variant A (process/studio credibility) for hero proof until Bart picks another.

**Staging references:**  
- `/virtual-bookkeeping/` (live)  
- `/for-founders/` (niche page; implement when route exists)  
- `/catch-up-bookkeeping/` (live)  
- `/fit-check/` (form page; wire Formspree)

---

## Placement map

| Block | Primary page | Also place on | Notes |
|-------|--------------|---------------|-------|
| **A. Hero proof line** | `/virtual-bookkeeping/` (under hero CTAs) | `/for-founders/` (same slot) | Use **Variant A** unless Bart picks B or C |
| **B. Three-column comparison** | `/virtual-bookkeeping/` (after “What’s included” / before pricing, or after boundaries) | `/for-founders/` (after founder problem section) | Title: “Pick your operating style” |
| **C. Standard admin sample month** | `/virtual-bookkeeping/` (inside or directly under Light admin / Standard) | Optional short version on `/for-founders/` | Show 3-hour hard cap clearly |
| **D. Catch-up pricing clarity** | `/catch-up-bookkeeping/` (replace or expand pricing section) | Teaser link from main LP catch-up paragraph | Label examples as illustrative |
| **E. Fit-check trust strip** | `/fit-check/` (above the fold, above form) | Compact version above fit-check CTA on main LP and for-founders | Remind: Formspree `YOUR_BOOKKEEPING_FORM_ID` |

---

## A. Hero proof line options

Place directly under the hero primary/secondary CTAs (or under the existing price trust line). One line preferred. Two lines max.

### Variant A: Process / studio credibility (SAFE NOW · ship this by default)

**For `/virtual-bookkeeping/`:**

```
Meridian studio · Async written monthly close · Clear scope, hard admin cap
```

**For `/for-founders/`:**

```
Built for technical founders · Async written close · No weekly meeting treadmill
```

**Optional slightly longer (still safe):**

```
Run by Meridian studio. Capture, categorisation, reconciliation, and a written report each month. Light admin on Standard only, capped at 3 hours.
```

### Variant B: Anonymized outcome placeholder (use only when Bart fills tokens with real data)

Do **not** ship with brackets visible. Replace `[N]` and `[industry]` before publish, or keep Variant A until then.

```
Closed and reconciled books for [N] [industry] teams. Written monthly report, no weekly stand-up required.
```

**Fill-in examples (illustrative structure only; not claims):**

- `[N]` = a real count Bart can defend (e.g. after first clients)
- `[industry]` = e.g. SaaS, product studios, early-stage software

**Secondary placeholder (hours saved: only with real data):**

```
Founders typically recover [X] hours a month once the close is async and documented. Ask us what that looked like for teams like yours.
```

### Variant C: CPA-forward quote placeholder (short, professional)

Ship only after a real CPA partner approves the wording and attribution style.

```
“Clean books and a written close I can work from. No theatre.” - [CPA name / firm], tax partner
```

**Shorter strip version:**

```
“Ready for filing season without a scramble.” - [CPA / firm]
```

Until a quote is approved, do not invent attribution. Keep Variant A.

---

## B. Three-column comparison block

**Section ID / class hint:** `operating-style-comparison`  
**Headline:** Pick your operating style  
**Intro (optional, 1–2 sentences):**

```
Bookkeeping products usually fall into a few patterns. Here is how Meridian’s async written close sits next to a weekly team and an AI finance OS. Clear fit beats clever positioning.
```

### Column 1: Weekly team

**Label:** Weekly team  
**Who it suits:** Founders who want live stand-ups, a bookkeeping pod on the calendar, and someone to talk through every exception in a meeting.  
**Cadence:** Weekly (sometimes biweekly) calls plus ongoing Slack or portal chatter.  
**Meetings:** Expected. Status often lives in the call, not only in writing.  
**Admin:** Varies by package. Often bookkeeping-heavy; admin may be limited or sold separately.  
**Price signal:** Typically mid-to-higher monthly retainers; packages and add-ons vary by vendor.  
**What you get:** Human team, meeting rhythm, books kept current if the process holds. More calendar load.

**Examples of this category (category names only, not a bash list):** firms and services in the weekly virtual bookkeeping team mould (e.g. Xendoo-style, BK360-style offerings).

### Column 2: AI finance OS

**Label:** AI finance OS  
**Who it suits:** Teams that want a software-first finance stack, dashboards, and automation, and are ready to adopt a platform as the system of record for ops.  
**Cadence:** Continuous product workflows; human support tiers vary.  
**Meetings:** Usually fewer by default; support is product- and ticket-led.  
**Admin:** Platform workflows and rules; “done for you” depth depends on plan.  
**Price signal:** Often platform SaaS pricing plus higher tiers for human coverage.  
**What you get:** Software leverage, visibility, and automation. You still need process discipline and clear ownership of exceptions.

**Examples of this category:** Pilot-, Zeni-, and Median-style AI / finance OS approaches (category peers; not a claim that Meridian replaces their full stack).

### Column 3: Meridian async written close (highlight)

**Label:** Meridian async written close  
**Who it suits:** Technical founders, SaaS, and product operators who want the month closed in writing, with optional light admin, and who do not want a weekly meeting habit.  
**Cadence:** Monthly close. Written report. Exception lists when something needs a decision.  
**Meetings:** Not the default. Calls only when a decision actually needs one.  
**Admin:** On **Standard** only: finance inbox triage, finance-adjacent scheduling, docs filing. Hard cap **3 hours/mo**. Starter is books only.  
**Price signal:** Starter from **$299/mo** (books only). Standard from **$449/mo** (books + light admin). Catch-up from **$200 per month behind**.  
**What you get:** Capture, categorisation, reconciliation, written monthly report. Clear boundaries. Not a CPA. Not a full EA. Not weekly stand-ups.

**Closest peers (honest, not copycat):** Merritt (price/focus shape), Median (ICP honesty). Meridian’s wedge is the **async written close** plus **capped light admin**.

**Footer note under the grid:**

```
Not sure which style you need? Start a fit check. We will say if Meridian is the wrong tool and point you toward a better fit when we can.
```

**CTA under block:** Start a fit check · hello@meridian.dev

---

## C. Standard admin “sample month” (3 hours)

**Headline:** What 3 hours of light admin looks like  
**Subhead:** Standard only. Finance-adjacent work that keeps the close and the paperwork moving. Not a full EA. Not personal errands.

**Sample month (illustrative split: adjust labels in UI as needed):**

```
Hour 1: Finance inbox triage
• Sort finance and ops mail that affects books, vendors, and billing
• Flag what needs your decision; draft short replies where useful
• Leave personal and non-finance noise alone

Hour 2: Scheduling (finance-adjacent)
• Hold and confirm the meetings that unblock money or compliance (CPA, bank, vendor, board packet timing)
• Keep calendars clear of “another books stand-up” unless you ask for one

Hour 3: Documents filing
• Name, file, and route contracts, statements, invoices, and vendor docs
• Keep a path your future self (and your CPA) can find
```

**Hard-cap / overage note (required):**

```
Hard cap: 3 hours a month on Standard. Work past the cap is out of scope and quoted separately before it starts. Starter does not include admin.
```

**Boundary reminder (one line under the note):**

```
Light admin is not CPA or tax advice, not weekly meetings, and not full executive-assistant cover.
```

---

## D. Catch-up pricing clarity module

**Page:** `/catch-up-bookkeeping/`  
**Headline:** Catch-up pricing, said plainly  
**Lead:**

```
Catch-up is from $200 per month behind. That is the public starting point, not a flat fee for every set of books. We quote after the fit check. Simple, clean books can be lower. Complex books are higher. Then you can move onto Starter or Standard if you want an ongoing close.
```

### Worked examples (ILLUSTRATIVE ONLY)

Add a visible label above the cards:

```
Illustrative examples only. Final quote after the fit check.
```

#### Example 1: Simple, 3 months behind → then Starter

```
Situation: One entity. QBO or Xero already in place. Receipts mostly in one place. Few transfers to untangle.

Illustrative catch-up range: about $600–$900 (3 × from $200/mo behind, adjusted for simplicity).

Then ongoing: Starter from $299/mo (async monthly close only, no admin).
```

#### Example 2: Messy, 6 months behind → then Standard

```
Situation: Mixed Stripe/PayPal exports, email receipts, categorisation drift, and a CPA asking for numbers. You also want light admin after you are current.

Illustrative catch-up range: about $1,500–$2,400+ (6 months × complexity above the floor).

Then ongoing: Standard from $449/mo (close + light admin, 3 hr/mo hard cap). A Standard promo of $399/mo is available on request; $449 is the published price.
```

#### Example 3: “Quote before work” contrast

```
How Meridian works: fit check → scoped quote → work starts. You see the number before we dig into the backlog.

How some other offers work: free or cheap catch-up tied to a long annual commitment, or a large fixed onboard fee before you know fit. Those can be fine for some teams. We prefer a clear project quote and an optional monthly retainer you choose after the baseline is clean.
```

Do not name competitors as scams. Keep the contrast honest and calm.

**Closing lines for the module:**

```
Books behind? Start a fit check. Reply in 1 business day. hello@meridian.dev
```

---

## E. Fit-check trust strip (above the fold)

**Page:** `/fit-check/` (and compact clones above CTAs on other bookkeeping pages)

### Exact short lines (primary strip)

```
Reply in 1 business day · No weekly meeting upsell · Not a CPA.
```

### Secondary line (directly under, or as helper text near the “plan interest” field)

```
Not sure? Choose Not sure. We’ll recommend Starter vs Standard.
```

### Optional third line (micro trust)

```
Fit check first. Quote before catch-up work. Boundaries in writing.
```

### Formspree reminder for Techie

- Wire the fit-check form to Formspree (or current form backend).  
- Replace placeholder `YOUR_BOOKKEEPING_FORM_ID` with the real form ID before launch.  
- Confirm success redirect / thank-you page and hello@meridian.dev notification.  
- Do not ship a dead form. If the ID is not ready, keep the email CTA (`mailto:hello@meridian.dev`) as a working fallback and mark the form “coming online.”

**Suggested compact strip above “Start a fit check” buttons on `/virtual-bookkeeping/` and `/for-founders/`:**

```
Reply in 1 business day · No weekly meeting upsell · Not a CPA.
```

---

## F. Implement checklist (for Techie)

1. Ship **Variant A** hero proof on main LP (+ for-founders when live).  
2. Add comparison block on main LP (and for-founders).  
3. Add Standard sample-month block under light admin.  
4. Expand catch-up pricing with the three illustrative examples.  
5. Add fit-check trust strip; wire Formspree (`YOUR_BOOKKEEPING_FORM_ID`).  
6. Do not publish Variant B/C until Bart fills real tokens / CPA approval.  
7. Match existing British spelling and Meridian plain-English voice. No em dashes.

---

## Copy paste kit (minimal HTML-ish structure)

Techie may use site components instead. Structure only:

```html
<!-- Hero proof: Variant A -->
<p class="proof-line">Meridian studio · Async written monthly close · Clear scope, hard admin cap</p>

<!-- Comparison: three columns as in section B -->

<!-- Sample month: section C -->

<!-- Catch-up examples: section D, each card tagged “Illustrative” -->

<!-- Fit-check strip -->
<p class="trust-strip">Reply in 1 business day · No weekly meeting upsell · Not a CPA.</p>
<p class="trust-strip-secondary">Not sure? Choose Not sure. We’ll recommend Starter vs Standard.</p>
```

