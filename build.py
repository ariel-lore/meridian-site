#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import shutil

SITE = Path(__file__).resolve().parent
BASE = "https://meridian.dev"
LAST = "29 September 2026"
CONTACT = "hello@meridian.dev"
# Bookkeeping fit check only. Not the rescue diagnostic form.
# Replace YOUR_BOOKKEEPING_FORM_ID with a Formspree id that delivers to hello@meridian.dev.
# Until then, js/main.js opens a mailto draft and still shows the thank-you state.
BOOKS_FORM = "https://formspree.io/f/YOUR_BOOKKEEPING_FORM_ID"
# Standard light admin. Stated on the page so the retainer is not an open assistant tab.
ADMIN_CAP = "3 hours a month"
FIT_PATH = "virtual-bookkeeping/fit-check/"
BRAND = (
  '<svg class="brand-mark" viewBox="0 0 32 32" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">'
  '<rect width="32" height="32" rx="8" fill="#4338ca"/>'
  '<circle cx="16" cy="16" r="7" fill="none" stroke="#c7d2fe" stroke-width="2"/>'
  '<path d="M16 6v20M6 16h20" stroke="#e0e7ff" stroke-width="1.5" opacity="0.7"/>'
  '<circle cx="16" cy="16" r="2.5" fill="#ffffff"/></svg>'
)

# Content-hashed asset basenames (updated by prepare_hashed_assets)
CSS_FILE = "styles.css"
JS_FILE = "main.js"


def content_hash(path: Path, length: int = 8) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:length]


def prepare_hashed_assets():
    """Copy css/styles.css and js/main.js to Vite-style hashed names; prune stale hashes."""
    global CSS_FILE, JS_FILE
    css_src = SITE / "css" / "styles.css"
    js_src = SITE / "js" / "main.js"
    if not css_src.is_file() or not js_src.is_file():
        raise FileNotFoundError("Expected css/styles.css and js/main.js as source assets")

    css_name = f"styles.{content_hash(css_src)}.css"
    js_name = f"main.{content_hash(js_src)}.js"

    for p in (SITE / "css").glob("styles.*.css"):
        if p.name != css_name:
            p.unlink()
            print("removed stale", p.relative_to(SITE))
    for p in (SITE / "js").glob("main.*.js"):
        if p.name != js_name:
            p.unlink()
            print("removed stale", p.relative_to(SITE))

    shutil.copy2(css_src, SITE / "css" / css_name)
    shutil.copy2(js_src, SITE / "js" / js_name)
    CSS_FILE = css_name
    JS_FILE = js_name
    print("hashed css/" + CSS_FILE)
    print("hashed js/" + JS_FILE)
    return CSS_FILE, JS_FILE


def depth(path):
    parts = [x for x in path.strip("/").split("/") if x]
    return "../" * len(parts) if parts else "./"

def write(rel, content):
    out = SITE / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    print("wrote", rel)

def head(path, title, desc, canonical, extra=""):
    p = depth(path)
    can = BASE + canonical
    return f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{can}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Meridian">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{can}">
<meta property="og:locale" content="en_CA">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}css/{CSS_FILE}">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
{extra}
</head>
<body>
"""

def header(path, variant="studio"):
    p = depth(path)
    if variant == "books":
        nav_cta = (
            f'<a class="nav-cta" href="{p}{FIT_PATH}" '
            f'data-track="bookkeeping_cta_click" data-track-label="nav-fit-check">Start a fit check</a>'
        )
    else:
        nav_cta = f'<a class="nav-cta" href="{p}request/">Request diagnostic</a>'
    return f"""<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{p}">{BRAND}<span>Meridian</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">Menu</button>
    <nav class="nav" id="site-nav">
      <a href="{p}vibe-code-rescue/">Vibe Code Rescue</a>
      <a href="{p}customer-growth/">Customer growth</a>
      <a href="{p}virtual-bookkeeping/">Bookkeeping</a>
      <a href="{p}pricing/">Pricing</a>
      <a href="{p}guides/what-is-vibe-code-rescue/">Guides</a>
      <a href="{p}faq/">FAQ</a>
      <a href="{p}about/">About</a>
      {nav_cta}
    </nav>
  </div>
</header>
"""

def footer(path, variant="studio"):
    p = depth(path)
    books_note = ""
    if variant == "books":
        studio_blurb = "Monthly bookkeeping, delivered as a written close."
        books_note = (
            f'<div class="container"><p class="footer-note">Meridian is a software studio. '
            f'<a href="{p}vibe-code-rescue/">Vibe Code Rescue</a> is a separate engagement.</p></div>'
        )
    else:
        studio_blurb = "Senior software studio. We salvage AI-built apps into production-ready software."
    if variant == "books":
        col_services = f"""<h4>Bookkeeping</h4>
      <ul>
        <li><a href="{p}virtual-bookkeeping/">Monthly close</a></li>
        <li><a href="{p}catch-up-bookkeeping/">Catch-up bookkeeping</a></li>
        <li><a href="{p}virtual-bookkeeping/for-founders/">For founders</a></li>
        <li><a href="{p}virtual-bookkeeping/for-ecommerce/">For ecommerce</a></li>
        <li><a href="{p}{FIT_PATH}">Fit check</a></li>
      </ul>"""
        col_mid = f"""<h4>Studio</h4>
      <ul>
        <li><a href="{p}">Home</a></li>
        <li><a href="{p}customer-growth/">Customer growth</a></li>
        <li><a href="{p}about/">About</a></li>
      </ul>"""
        col_resources = f"""<h4>Resources</h4>
      <ul>
        <li><a href="{p}pricing/">Pricing</a></li>
        <li><a href="{p}faq/">FAQ</a></li>
        <li><a href="{p}llms.txt">llms.txt</a></li>
      </ul>"""
    else:
        col_services = f"""<h4>Services</h4>
      <ul>
        <li><a href="{p}vibe-code-rescue/">Vibe Code Rescue</a></li>
        <li><a href="{p}customer-growth/">Customer growth</a></li>
        <li><a href="{p}virtual-bookkeeping/">Virtual bookkeeping</a></li>
        <li><a href="{p}catch-up-bookkeeping/">Catch-up bookkeeping</a></li>
        <li><a href="{p}virtual-bookkeeping/for-founders/">Bookkeeping for founders</a></li>
        <li><a href="{p}virtual-bookkeeping/for-ecommerce/">Bookkeeping for ecommerce</a></li>
        <li><a href="{p}product-engineering/">Product engineering</a></li>
        <li><a href="{p}security-hardening/">Security hardening</a></li>
        <li><a href="{p}fractional-cto/">Fractional CTO</a></li>
      </ul>"""
        col_mid = f"""<h4>Rescue by tool</h4>
      <ul>
        <li><a href="{p}rescue/lovable/">Lovable</a></li>
        <li><a href="{p}rescue/bolt/">Bolt</a></li>
        <li><a href="{p}rescue/cursor/">Cursor</a></li>
        <li><a href="{p}rescue/v0/">v0</a></li>
        <li><a href="{p}rescue/replit/">Replit Agent</a></li>
        <li><a href="{p}rescue/claude-code/">Claude Code</a></li>
      </ul>"""
        col_resources = f"""<h4>Resources</h4>
      <ul>
        <li><a href="{p}pricing/">Pricing</a></li>
        <li><a href="{p}problems/secrets-exposed/">Common problems</a></li>
        <li><a href="{p}guides/rescue-vs-rewrite/">Rescue vs rewrite</a></li>
        <li><a href="{p}faq/">FAQ</a></li>
        <li><a href="{p}request/">Request diagnostic</a></li>
        <li><a href="{p}llms.txt">llms.txt</a></li>
      </ul>"""
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <div class="footer-brand">{BRAND}<span>Meridian</span></div>
      <p>{studio_blurb}</p>
      <p><a href="mailto:{CONTACT}">{CONTACT}</a></p>
    </div>
    <div>
      {col_services}
    </div>
    <div>
      {col_mid}
    </div>
    <div>
      {col_resources}
    </div>
  </div>
  {books_note}
  <div class="container footer-bottom">
    <span>&copy; 2026 Meridian. All rights reserved.</span>
    <span>Last updated: {LAST}</span>
  </div>
</footer>
<script src="{p}js/{JS_FILE}" defer></script>
</body></html>
"""

def crumbs_html(items):
    parts = []
    for i, (label, href) in enumerate(items):
        if i: parts.append('<span aria-hidden="true">/</span>')
        parts.append(f'<a href="{href}">{label}</a>' if href else f'<span aria-current="page">{label}</span>')
    return '<nav class="breadcrumbs" aria-label="Breadcrumb">' + "".join(parts) + "</nav>"

def crumbs_json(items):
    els = []
    for i, (name, url) in enumerate(items, 1):
        els.append(f'{{"@type":"ListItem","position":{i},"name":"{name}","item":"{BASE}{url}"}}')
    return '<script type="application/ld+json">{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[' + ",".join(els) + "]}</script>"

def faq_schema(faqs):
    ents = []
    for q, a in faqs:
        qe = q.replace('"','\\"')
        ae = a.replace('"','\\"').replace("\n"," ")
        ents.append(f'{{"@type":"Question","name":"{qe}","acceptedAnswer":{{"@type":"Answer","text":"{ae}"}}}}')
    return '<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[' + ",".join(ents) + "]}</script>"

def faq_html(faqs):
    blocks = []
    for q, a in faqs:
        blocks.append(f'<details class="faq-item"><summary>{q}</summary><div class="faq-answer"><p>{a}</p></div></details>')
    return '<div class="faq-list">' + "\n".join(blocks) + "</div>"

def service_schema(name, url, desc, price=None):
    offer = ""
    if price:
        offer = f',"offers":{{"@type":"Offer","priceCurrency":"USD","description":"{price}"}}'
    return (
      '<script type="application/ld+json">'
      f'{{"@context":"https://schema.org","@type":"Service","name":"{name}","serviceType":"{name}",'
      f'"provider":{{"@type":"Organization","name":"Meridian","url":"{BASE}/"}},'
      f'"url":"{BASE}{url}","description":"{desc}","areaServed":["CA","US"]{offer}}}'
      "</script>"
    )

ORG = (
  '<script type="application/ld+json">'
  '{"@context":"https://schema.org","@type":["Organization","ProfessionalService"],'
  '"name":"Meridian","url":"' + BASE + '/","email":"' + CONTACT + '",'
  '"description":"Senior software studio with 30+ years combined experience across video games, finance, and web. Home of Vibe Code Rescue.",'
  '"areaServed":["CA","US","GB","EU"],'
  '"knowsAbout":["Vibe Code Rescue","AI-generated code","Software security","Product engineering","Fractional CTO","Customer growth","Virtual bookkeeping"]}'
  "</script>"
)

def cta(path, title="Ready for a 48-hour diagnostic?", sub="Tell us what you built and where it hurts. No shame. Fixed-scope options after the audit."):
    p = depth(path)
    return f"""<section class="cta-band">
  <div class="container">
    <h2>{title}</h2>
    <p>{sub}</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-primary btn-lg" href="{p}request/">Request diagnostic</a>
      <a class="btn btn-secondary btn-lg" href="{p}pricing/">See pricing</a>
    </div>
  </div>
</section>
"""


VCR_FAQS = [
 ("What is vibe code rescue?",
  "Vibe code rescue is a productized engineering service that takes apps built primarily with AI coding tools and makes them production-ready without a full rewrite — starting with a short diagnostic, then fixed-scope hardening of security, auth, data, and payments."),
 ("How is rescue different from a rewrite?",
  "Rescue keeps the product surface and salvageable code. We rank severity, fix what is dangerous or blocking, and only recommend a rebuild when structure or risk makes salvage uneconomical."),
 ("Which AI tools do you support?",
  "Cursor, Lovable, Bolt, v0, Replit Agent, Claude Code, Windsurf, and similar stacks."),
 ("How fast is the diagnostic?",
  "We aim for a written diagnostic within 48 hours of receiving access and your problem brief. Complex monorepos may need a bit longer — we say so up front."),
 ("What do you deliver?",
  "A severity-ranked audit, keep/harden/rebuild recommendation, fixed-scope rescue quote when appropriate, and after engagement: patched code, rotated-secrets guidance, tests/CI where scoped, deploy notes, and optional AI guardrails."),
 ("Do you keep our AI workflow after rescue?",
  "Yes, if you want it. Optional post-rescue guardrails include agent scope files, Cursor/Claude rules, CI gates, and checklists."),
 ("Will you shame us for vibe coding?",
  "No. Empathy, no shame. Shipping a prototype fast was rational. Production is a different job."),
 ("Who owns the code?",
  "You do. We work in your repo or a fork you control. No hostage source."),
]

GROWTH_FAQS = [
 ("Do I get a weekly marketing call?",
  "No. Customer growth is a scoped package: search, campaigns, landing pages, CRM, and follow-up through to booking. Reporting and questions are async. There is no weekly account-management meeting."),
 ("Is this a fractional CMO or a call-centre follow-up service?",
  "No. A fractional CMO works the plan with you week to week. This package covers the campaign, the pages, the CRM, and the follow-up sequence through to booking. You are not asked to run it, and we do not put a caller on a weekly roster."),
 ("How do leads get followed up?",
  "Follow-up is part of the package: email or SMS sequences and booking, inside the scope you approved. Questions about a lead are handled in writing, not on a standing call."),
 ("What do I need to provide?",
  "Access to the site, ad accounts, and CRM, plus one approval of the offer and the voice. After that, questions and changes stay on the package cadence."),
 ("How do I start?",
  "Use the inquire form and describe the business and the offer. We reply with whether a growth package fits."),
]

BOOKS_FAQS = [
 ("Do you replace my accountant?",
  "No. We keep the books current and documented so your CPA can advise and file. We do not provide tax advice or file returns."),
 ("What software do you work in?",
  "QuickBooks Online and Xero primarily. Wave, spreadsheets, and other tools: say so on the fit check and we will tell you if a migration makes sense."),
 ("How do we communicate?",
  "Async by default — email, shared checklists, and the monthly written report. A call only when a decision actually needs a conversation."),
 ("What is light admin?",
  "Inbox triage, scheduling, and document handling tied to running the business cleanly. It is on Standard only, capped at 3 hours a month. It is not personal errands or full executive-assistant cover. Starter is the monthly close with no admin."),
 ("How much does virtual bookkeeping cost?",
  "Starter is from $299 per month for the async monthly close only. Standard is from $449 per month and adds light admin capped at 3 hours a month. A launch promo of $399 per month is available on request for Standard; $449 is the published price. Catch-up is quoted from $200 per month behind. Simple books can be lower; complex books higher. We confirm the quote before you commit."),
 ("How fast can we start?",
  "After the fit check, usually within one to two weeks once access is granted. Catch-up timing depends on how many months are behind."),
 ("Can you work with my CPA?",
  "Yes. We organise the books and the written report so handoff is straightforward. Tax filing stays with your CPA."),
 ("How do I start virtual bookkeeping?",
  "Use the bookkeeping fit check. We reply within one business day on whether we are a fit and what the next step is."),
]

TOOLS = [
 ("lovable","Lovable",
  "Lovable apps often look finished in preview while hiding client-side auth gaps, weak Supabase RLS, and Stripe stubs. Meridian rescues Lovable builds into production-ready software.",
  ["Preview-quality UI with incomplete server enforcement","Supabase tables with RLS disabled or overly broad policies","Secrets in client-visible config","Stripe Checkout that works in test mode only","Deploy surprises when leaving Lovable hosting assumptions"]),
 ("bolt","Bolt",
  "Bolt prototypes ship fast and often stall on auth, env separation, and production deploy. We salvage Bolt apps without a full rewrite.",
  ["Environment variables confused between preview and prod","Auth patterns that only work in the builder sandbox","Dependency and build failures on Vercel/Netlify","Payment and webhook handlers left as TODOs","AI churn that rewrites the same files unsuccessfully"]),
 ("cursor","Cursor",
  "Cursor-built codebases can be large and inconsistent — agent edits without tests, security holes, and architectural drift. Meridian stabilises Cursor projects for production.",
  ["Inconsistent patterns across agent sessions","Missing tests while features keep landing","Secrets committed or logged","Half-finished refactors left in tree","Fix-loops where the agent regenerates the same bug"]),
 ("v0","v0",
  "v0 shines at UI generation; production gaps show up in data, auth, and backend wiring. We connect v0 frontends to real, safe backends — or harden what you already wired.",
  ["UI-complete, backend-thin applications","Client-only validation presented as security","Ad-hoc API routes without authz checks","No tenancy model for multi-user data","Deploy config missing for real environments"]),
 ("replit","Replit Agent",
  "Replit Agent projects often work in the Replit environment and fail when exported or scaled. We rescue Replit-built apps for production hosting and security.",
  ["Environment-specific assumptions","Networking and binding issues on export","Database URLs and credentials mishandled","Limited separation between demo and live data","Incomplete payment and webhook verification"]),
 ("claude-code","Claude Code",
  "Claude Code can produce ambitious multi-file changes quickly — and leave security and deploy debt. Meridian audits and hardens Claude Code projects with fixed scope.",
  ["Large diffs without regression tests","Auth and RLS treated as follow-ups","Over-abstracted structure that obscures data flow","CI missing or always red","Agent instructions that reintroduce bad patterns"]),
 ("windsurf","Windsurf",
  "Windsurf-assisted codebases share the usual AI failure modes: speed without enforcement. We rescue Windsurf projects with the same security-first salvage approach.",
  ["Rapid feature growth without tenancy review","Copied insecure snippets across files","Deploy pipelines incomplete","Stripe and webhook edge cases ignored","No guardrails for continued AI editing"]),
]

PROBLEMS = [
 ("secrets-exposed","Secrets exposed in an AI-built app",
  "If API keys, tokens, or credentials landed in your repo, client bundle, or chat logs, treat them as burned: rotate first, then fix how the app loads secrets. Meridian flags exposure paths and hardens configuration.",
  ["Rotate every exposed key before anything else","Remove secrets from git history where feasible","Move to server-only env / secret manager","Block client bundles from embedding privileged keys","Add CI checks so secrets do not return"],
  "Exposed secrets are the fastest path from demo to incident. We prioritise rotation guidance and configuration hardening in every rescue."),
 ("rls-tenancy","RLS and tenancy failures",
  "Disabled or weak Row Level Security (and missing tenancy checks) let users read or write each other data. Common in Supabase/Firebase vibe apps. We fix policies and server-side authz before feature work.",
  ["Enable and test RLS on every user-data table","Replace client-trusted user IDs with verified auth context","Add automated tests for cross-tenant denial","Review storage buckets and public URLs","Document the tenancy model for future AI edits"],
  "Tenancy bugs fail diligence and destroy trust. Our audits always include a cross-tenant read/write check."),
 ("stripe-payments","Stripe and payments broken",
  "AI-built Stripe integrations often have test-mode-only checkout, unsigned webhooks, or subscription state that lies. We harden payment flows so money and entitlements match reality.",
  ["Verify webhooks with signing secrets","Reconcile customer and subscription state server-side","Remove client-trusted payment-success flags","Separate test and live keys cleanly","Cover upgrade/cancel/fail paths"],
  "Payments are in our fix-first list with secrets and auth."),
 ("wont-deploy","Works locally / preview, will not deploy",
  "Preview success is not production. Env mismatch, build failures, wrong Node versions, and host assumptions are classic vibe-code blockers. We get you to a repeatable production deploy.",
  ["Align env vars across preview and production","Fix build and SSR/edge assumptions","Pin runtimes and document deploy steps","Add a minimal smoke check post-deploy","Separate demo data from live data"],
  "If preview looks fine but production fails, start with a diagnostic — often a short fixed scope."),
 ("ai-fix-loop","Stuck in an AI fix loop",
  "When the agent keeps fixing the same bug and introducing new ones, you need a human severity map and a stop-the-bleeding scope — not more unscoped prompts.",
  ["Freeze drive-by refactors","Reproduce the bug with a failing test or script","Fix root cause in a minimal diff","Add guardrails before unlocking AI again","Decide salvage vs rewrite with evidence"],
  "Empathy, no shame. Loops happen. We break them with diagnosis and fixed scope."),
]

STUBS = [
 ("product-engineering","Product engineering",
  "Senior product engineering for features, architecture, and shipping cadence — beyond a one-time rescue.",
  "Coming soon as a packaged engagement. If you need ongoing product engineering after a rescue or from a clean start, inquire and we will scope it."),
 ("security-hardening","Security hardening",
  "Focused security hardening for apps with users, payments, or diligence — threat-led, not checkbox theatre.",
  "Coming soon as a packaged engagement. For AI-built apps, start with Vibe Code Rescue diagnostic; for broader hardening, inquire."),
 ("fractional-cto","Fractional CTO",
  "Part-time technical leadership: roadmap, hiring, vendor decisions, and AI delivery guardrails.",
  "Coming soon as a packaged retainer. Many clients start with rescue, then retain fractional CTO hours — inquire to discuss fit."),
]



def page_home():
    path = ""
    p = depth(path)
    title = "Meridian — Senior software studio | Vibe Code Rescue"
    desc = "Meridian is a senior software studio with 30+ years combined experience in games, finance, and web. Home of Vibe Code Rescue — salvage AI-built apps into production-ready software."
    extra = ORG + service_schema("Vibe Code Rescue", "/vibe-code-rescue/",
        "Senior engineers who salvage AI-built apps into production-ready software. Audit in 48 hours.",
        "Diagnostic free–$500; rescue $500–$12,500+")
    body = f"""
{header(path)}
<main>
<section class="hero">
<div class="container">
<p class="hero-kicker">Meridian · Senior software studio</p>
<h1>Production software from AI-built prototypes — and the studio behind it</h1>
<p class="answer-first"><strong>Quick answer:</strong> Meridian is a senior software studio with 30+ years combined experience across video games, finance, and web development. Our flagship service, <a href="{p}vibe-code-rescue/">Vibe Code Rescue</a>, audits AI-built apps in 48 hours, fixes security, auth, data, and payments first, keeps what works, and ships fixed-scope salvage — you own the code.</p>
<p class="meta-line">Last updated: {LAST}</p>
<div class="btn-row">
<a class="btn btn-primary btn-lg" href="{p}request/">Request a 48h diagnostic</a>
<a class="btn btn-secondary btn-lg" href="{p}vibe-code-rescue/">Explore Vibe Code Rescue</a>
</div>
<div class="stat-row">
<div class="stat"><div class="num">30+</div><div class="label">Years combined experience</div></div>
<div class="stat"><div class="num">48h</div><div class="label">Written diagnostic</div></div>
<div class="stat"><div class="num">3</div><div class="label">Domains: games · finance · web</div></div>
</div>
</div>
</section>
<section class="section">
<div class="container">
<h2 class="section-title">What we promise</h2>
<p class="lede">Empathy, no shame. Rescue is not a rewrite. We fix the dangerous parts first, keep the product that already works, and leave you owning every line.</p>
<div class="grid-3" style="margin-top:1.5rem">
<div class="card"><div class="card-icon">01</div><h3>Audit before you commit</h3><p>A written, severity-ranked diagnostic in 48 hours: keep, harden, or rebuild — with a fixed-scope quote when salvage makes sense.</p></div>
<div class="card"><div class="card-icon">02</div><h3>Security &amp; money first</h3><p>Secrets, auth, tenancy/RLS, and payments before polish. The failures that lose customers and diligence get fixed first.</p></div>
<div class="card"><div class="card-icon">03</div><h3>You own the code</h3><p>Fixed scope. Clear deliverables. Optional AI guardrails so you can keep shipping with Cursor, Claude, and friends — safely.</p></div>
</div>
</div>
</section>
<section class="section section-alt">
<div class="container">
<h2 class="section-title">Experience that shows up in production</h2>
<p class="lede">Senior engineers who have shipped under game launch pressure, financial controls, and web scale.</p>
<div class="grid-3" style="margin-top:1.5rem">
<div class="card"><span class="pill">Video games</span><h3>Ship under launch pressure</h3><p>Performance, reliability, and player-facing quality when the date does not move.</p></div>
<div class="card"><span class="pill">Finance</span><h3>Controls &amp; correctness</h3><p>Auth, auditability, and payment flows that survive scrutiny — not demo-day stubs.</p></div>
<div class="card"><span class="pill">Web</span><h3>Product that deploys</h3><p>Multi-tenant SaaS, CI/CD, observability, and the boring glue that keeps apps alive.</p></div>
</div>
</div>
</section>
<section class="section">
<div class="container">
<h2 class="section-title">Services</h2>
<p class="lede">Flagship rescue, plus scoped packages for customer growth and for books and admin.</p>
<div class="grid-2" style="margin-top:1.5rem">
<div class="card"><span class="pill pill-ok">Flagship</span><h3>Vibe Code Rescue</h3><p>Salvage AI-built apps (Cursor, Lovable, Bolt, v0, Replit Agent, Claude Code, Windsurf) into production-ready software. 48h diagnostic. Fixed scope.</p><a class="card-link" href="{p}vibe-code-rescue/">View service →</a></div>
<div class="card"><span class="pill pill-ok">Package</span><h3>Customer growth</h3><p>Search, campaigns, landing pages, CRM, and follow-up through to booking. A scoped package with a clear cadence, not a weekly marketing meeting.</p><a class="card-link" href="{p}customer-growth/">View service →</a></div>
<div class="card"><span class="pill pill-ok">Package</span><h3>Virtual bookkeeping</h3><p>Async monthly close for technical founders. Standard from $449/month, Starter from $299/month, catch-up from $200 per month behind. Tax stays with your CPA.</p><a class="card-link" href="{p}virtual-bookkeeping/">View service →</a></div>
<div class="card"><span class="pill pill-muted">Inquire</span><h3>Product engineering</h3><p>Feature delivery, architecture, and product partnership beyond a one-time rescue.</p><a class="card-link" href="{p}product-engineering/">Learn more →</a></div>
<div class="card"><span class="pill pill-muted">Inquire</span><h3>Security hardening</h3><p>Threat-focused hardening for apps that already have users or diligence on the calendar.</p><a class="card-link" href="{p}security-hardening/">Learn more →</a></div>
<div class="card"><span class="pill pill-muted">Inquire</span><h3>Fractional CTO</h3><p>Ongoing technical leadership after rescue — roadmap, hiring, vendor calls, AI guardrails.</p><a class="card-link" href="{p}fractional-cto/">Learn more →</a></div>
</div>
</div>
</section>
<section class="section section-alt">
<div class="container">
<h2 class="section-title">Built with AI tools? We know their failure modes</h2>
<div class="chip-row">
<a class="chip" href="{p}rescue/lovable/">Lovable</a>
<a class="chip" href="{p}rescue/bolt/">Bolt</a>
<a class="chip" href="{p}rescue/cursor/">Cursor</a>
<a class="chip" href="{p}rescue/v0/">v0</a>
<a class="chip" href="{p}rescue/replit/">Replit Agent</a>
<a class="chip" href="{p}rescue/claude-code/">Claude Code</a>
<a class="chip" href="{p}rescue/windsurf/">Windsurf</a>
</div>
<h3>Common symptoms we fix</h3>
<div class="chip-row">
<a class="chip" href="{p}problems/secrets-exposed/">Secrets exposed</a>
<a class="chip" href="{p}problems/rls-tenancy/">RLS / tenancy</a>
<a class="chip" href="{p}problems/stripe-payments/">Stripe / payments</a>
<a class="chip" href="{p}problems/wont-deploy/">Won't deploy</a>
<a class="chip" href="{p}problems/ai-fix-loop/">AI fix loop</a>
</div>
</div>
</section>
{cta(path)}
</main>
{footer(path)}
"""
    write("index.html", head(path, title, desc, "/", extra) + body)

def page_vcr():
    path = "vibe-code-rescue/"
    p = depth(path)
    title = "Vibe Code Rescue — Salvage AI-built apps | Meridian"
    desc = "Senior engineers who salvage AI-built apps into production-ready software. Audit in 48 hours. Fix security, auth, data, and payments first. Keep what works. Fixed scope. You own the code."
    extra = (crumbs_json([("Home","/"),("Vibe Code Rescue","/vibe-code-rescue/")])
        + service_schema("Vibe Code Rescue","/vibe-code-rescue/",desc,"Diagnostic free–$500; audit $299–$2,500; rescue $500–$12,500+")
        + faq_schema(VCR_FAQS) + ORG)
    crumbs = crumbs_html([("Home",p),("Vibe Code Rescue",None)])
    body = f"""
{header(path)}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<p class="hero-kicker">Meridian service</p>
<h1>Vibe Code Rescue</h1>
<p class="answer-first"><strong>Quick answer:</strong> Senior engineers who salvage AI-built apps into production-ready software. Audit in 48 hours. Fix security, auth, data, and payments first. Keep what works. Fixed scope. You own the code. Optional AI guardrails after rescue. Empathy, no shame.</p>
<p class="meta-line">Last updated: {LAST}</p>
<div class="btn-row">
<a class="btn btn-primary" href="{p}request/">Request 48h diagnostic</a>
<a class="btn btn-secondary" href="{p}pricing/">Pricing ladder</a>
<a class="btn btn-ghost" href="{p}artifacts/sample-audit.md">Sample audit (markdown)</a>
</div></div></section>
<section class="section"><div class="narrow prose">
<h2>Rescue ≠ rewrite</h2>
<p>Most AI-built products are partly salvageable. We do not throw away a working UI or a validated workflow for ego. We stabilise what is dangerous, decide keep vs harden vs rebuild with evidence, then execute a fixed scope you can budget.</p>
<p>Read the full decision guide: <a href="{p}guides/rescue-vs-rewrite/">Rescue vs rewrite</a>.</p>
<h2>Tools we rescue from</h2>
<div class="chip-row">
<a class="chip" href="{p}rescue/cursor/">Cursor</a>
<a class="chip" href="{p}rescue/lovable/">Lovable</a>
<a class="chip" href="{p}rescue/bolt/">Bolt</a>
<a class="chip" href="{p}rescue/v0/">v0</a>
<a class="chip" href="{p}rescue/replit/">Replit Agent</a>
<a class="chip" href="{p}rescue/claude-code/">Claude Code</a>
<a class="chip" href="{p}rescue/windsurf/">Windsurf</a>
</div>
<h2>Process</h2>
<ol class="steps">
<li><strong>Stabilise intake</strong> — Brief + repo access (or export). Do not paste secrets in the form. We confirm NDA if needed.</li>
<li><strong>48-hour diagnostic</strong> — Severity-ranked findings: secrets, auth, tenancy, payments, deploy, architecture debt. Keep / harden / rebuild recommendation.</li>
<li><strong>Fixed-scope rescue</strong> — Quote with boundaries. Security and money paths first. You approve before we cut code.</li>
<li><strong>Harden &amp; hand off</strong> — Patches in your repo, deploy notes, optional tests/CI and AI guardrails so the same bugs do not return.</li>
</ol>
<h2>What we fix first</h2>
<ul>
<li><a href="{p}problems/secrets-exposed/">Exposed secrets</a> and unsafe client bundles</li>
<li>Broken or client-only <strong>auth</strong></li>
<li><a href="{p}problems/rls-tenancy/">RLS / multi-tenant data leaks</a></li>
<li><a href="{p}problems/stripe-payments/">Stripe stubs, unsigned webhooks, broken subscriptions</a></li>
<li><a href="{p}problems/wont-deploy/">Preview works, production will not</a></li>
<li><a href="{p}problems/ai-fix-loop/">AI fix-loop / regression spiral</a></li>
</ul>
<h2>Deliverables</h2>
<ul>
<li>Written diagnostic with severity ranking</li>
<li>Keep / harden / rebuild recommendation</li>
<li>Fixed-scope statement of work when you proceed</li>
<li>Code changes in a repo you own</li>
<li>Rotation / env checklist for secrets</li>
<li>Deploy and runbook notes for the scoped work</li>
<li>Optional: CI gates, agent rules, post-rescue guardrails</li>
</ul>
<div class="callout"><strong>Sample artifact:</strong> See a redacted example of how we write findings — <a href="{p}artifacts/sample-audit.md">sample-audit.md</a>.</div>
<h2>Other productized services</h2>
<p>Meridian is the studio. Two sibling packages sit beside rescue: <a href="{p}customer-growth/">Customer growth</a> (search, campaigns, landing pages, and follow-up) and <a href="{p}virtual-bookkeeping/">Virtual bookkeeping</a> (monthly books and admin). Both are scoped work, not a standing weekly meeting.</p>
<h2>FAQ</h2>
{faq_html(VCR_FAQS)}
</div></section>
{cta(path)}
</main>
{footer(path)}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)

def page_stub(slug, name, blurb, body_text):
    path = f"{slug}/"
    p = depth(path)
    title = f"{name} — Meridian"
    extra = crumbs_json([("Home","/"),(name,f"/{slug}/")]) + service_schema(name, f"/{slug}/", blurb)
    crumbs = crumbs_html([("Home",p),(name,None)])
    body = f"""
{header(path)}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<p class="hero-kicker">Meridian service · Inquire</p>
<h1>{name}</h1>
<p class="answer-first"><strong>Quick answer:</strong> {blurb}</p>
<p class="meta-line">Last updated: {LAST}</p>
<p><span class="pill pill-warn">Coming soon / inquire</span></p>
</div></section>
<section class="section"><div class="narrow prose">
<p>{body_text}</p>
<p>Meanwhile, our flagship offering is ready: <a href="{p}vibe-code-rescue/">Vibe Code Rescue</a>.</p>
{"" if slug != "fractional-cto" else f'<p>If you want a packaged growth or books engagement rather than a weekly leadership retainer, see <a href="{p}customer-growth/">Customer growth</a> and <a href="{p}virtual-bookkeeping/">Virtual bookkeeping</a>.</p>'}
<div class="btn-row">
<a class="btn btn-primary" href="{p}request/?interest={slug}">Inquire</a>
<a class="btn btn-secondary" href="mailto:{CONTACT}?subject={name}%20inquiry">Email {CONTACT}</a>
</div>
</div></section>
</main>
{footer(path)}
"""
    write(path + "index.html", head(path, title, blurb, "/" + path, extra) + body)

OFFERINGS = [
 {
  "slug": "customer-growth",
  "name": "Customer growth",
  "title": "Customer growth — campaigns, pages, and follow-up | Meridian",
  "desc": "A scoped customer-growth package: search, paid campaigns, landing pages, CRM capture, and email or SMS follow-up through to booking. Clear process and a reporting cadence. Not a weekly marketing meeting.",
  "kicker": "Meridian service · Package",
  "quick": "Customer growth is a scoped package for search, paid campaigns, landing pages, CRM capture, and email or SMS follow-up through to booking. You approve the offer once. Reporting and questions stay on that cadence. It is not a weekly marketing meeting, a caller chasing leads, or a fractional CMO engagement.",
  "what_h": "What it is",
  "what": [
   "Search content and paid campaign setup for a defined offer",
   "Landing pages that turn visits into inquiries",
   "CRM capture so every lead has a home",
   "Email and SMS follow-up sequences, and booking, inside the agreed scope",
  ],
  "not": [
   "A weekly marketing call or a roster of follow-up calls",
   "A fractional CMO engagement that needs you to run the plan",
   "An open-ended retainer with someone in your calendar every week",
  ],
  "steps": [
   ("Scope the offer", "Tell us what you sell, where you sell it, and where a new customer should land."),
   ("Build the package", "Campaigns, landing page, CRM, and follow-up sequences. You approve the offer and the voice once."),
   ("Deliver the scope", "Leads, follow-up, and booking stay inside the package. Changes and questions are async."),
   ("Report on cadence", "You receive a clear read of leads and bookings. There is no standing weekly status meeting."),
  ],
  "who": [
   "Owners who want a steady path from attention to a booked conversation",
   "Businesses with a clear offer and a way to take a booking or a sale",
   "Teams who want a defined package and a written cadence, not an open marketing calendar",
  ],
  "not_who": [
   "Brands that want a strategist in the room every week",
   "Offers that change daily and need a new plan each time",
   "Engagements that depend on a standing call for the work to move",
  ],
  "delivery": "A fixed-scope growth package. Setup, follow-up sequences, and a reporting cadence are in the scope. We do not book a weekly account-management meeting.",
  "faqs": GROWTH_FAQS,
  "sibling_slug": "virtual-bookkeeping",
  "sibling_name": "Virtual bookkeeping",
  "sibling_blurb": "monthly books and admin",
  "cta_title": "See if a growth package fits",
  "cta_sub": "Tell us the offer and where a new customer should land. We reply with a scoped next step.",
 },
]


def page_offering(o):
    path = o["slug"] + "/"
    p = depth(path)
    name = o["name"]
    title = o["title"]
    desc = o["desc"]
    faqs = o["faqs"]
    extra = (crumbs_json([("Home", "/"), (name, "/" + path)])
        + service_schema(name, "/" + path, desc)
        + faq_schema(faqs) + ORG)
    crumbs = crumbs_html([("Home", p), (name, None)])
    what_lis = "".join(f"<li>{x}</li>" for x in o["what"])
    not_lis = "".join(f"<li>{x}</li>" for x in o["not"])
    who_lis = "".join(f"<li>{x}</li>" for x in o["who"])
    not_who_lis = "".join(f"<li>{x}</li>" for x in o["not_who"])
    step_lis = "".join(f"<li><strong>{t}</strong> {b}</li>" for t, b in o["steps"])
    body = f"""
{header(path)}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<p class="hero-kicker">{o["kicker"]}</p>
<h1>{name}</h1>
<p class="answer-first"><strong>Quick answer:</strong> {o["quick"]}</p>
<p class="meta-line">Last updated: {LAST}</p>
<div class="btn-row">
<a class="btn btn-primary" href="{p}request/?interest={o["slug"]}">Inquire</a>
<a class="btn btn-secondary" href="mailto:{CONTACT}?subject={name.replace(" ", "%20")}%20inquiry">Email {CONTACT}</a>
</div></div></section>
<section class="section"><div class="narrow prose">
<h2>{o["what_h"]}</h2>
<ul>{what_lis}</ul>
<h2>What it is not</h2>
<ul>{not_lis}</ul>
<h2>How it works</h2>
<ol class="steps">
{step_lis}
</ol>
<h2>Who it is for</h2>
<ul>{who_lis}</ul>
<h2>Who it is not for</h2>
<ul>{not_who_lis}</ul>
<div class="callout"><strong>Delivery model:</strong> {o["delivery"]}</div>
<h2>Same studio, different job</h2>
<p>These pages sit under Meridian, next to <a href="{p}vibe-code-rescue/">Vibe Code Rescue</a>. The sibling service is <a href="{p}{o["sibling_slug"]}/">{o["sibling_name"]}</a> — {o["sibling_blurb"]}. This inquire form is the same one used for a rescue diagnostic. Bookkeeping does not use it — start at the <a href="{p}{FIT_PATH}">bookkeeping fit check</a>. If the tool list does not apply, choose Mixed / other and describe the business.</p>
<h2>FAQ</h2>
{faq_html(faqs)}
</div></section>
<section class="cta-band">
  <div class="container">
    <h2>{o["cta_title"]}</h2>
    <p>{o["cta_sub"]}</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-primary btn-lg" href="{p}request/?interest={o["slug"]}">Inquire</a>
      <a class="btn btn-secondary btn-lg" href="mailto:{CONTACT}?subject={name.replace(" ", "%20")}%20inquiry">Email {CONTACT}</a>
    </div>
  </div>
</section>
</main>
{footer(path)}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)

CATCHUP_FAQS = [
 ("How do you count months behind?",
  "Open periods without a completed close and reconciliation. Partial months are scoped in the quote."),
 ("What if I only want catch-up, not monthly?",
  "That is fine. Catch-up is a project. Ongoing Starter or Standard is optional."),
 ("Is catch-up a flat $200 for every month?",
  "No. $200 per month behind is the public starting point. We quote after the fit check. Simple, clean books can be lower. Complex books — more entities, messy source data, a long backlog — are higher."),
 ("Will this fix my taxes?",
  "We organise the books. Your CPA files and advises. We coordinate the handoff."),
 ("What slows catch-up down?",
  "Missing statements, locked accounts, or unclear owner draws. We list blockers early so you can unblock them async."),
]

FOUNDER_FAQS = [
 ("Will you learn our product?",
  "Enough to categorise sensibly and ask sharp exception questions. We will not join roadmap reviews."),
 ("Can you work in our Notion, Linear, or email?",
  "Yes for admin triage and documentation on Standard. The books stay in accounting software."),
 ("Do you do R&D or startup tax-credit work?",
  "We organise books and supporting documents. Credits and filings go through your CPA or a specialist."),
 ("We are pre-revenue. Is it still worth it?",
  "Often yes if spend is real and you want clean habits before a raise or a tax filing. The fit check will say if volume is too light."),
 ("What does Standard cost?",
  "Standard is from $449 per month: the monthly close plus light admin capped at 3 hours a month. Starter is from $299 per month with no admin. Catch-up is quoted from $200 per month behind."),
]

ECOM_FAQS = [
 ("Do you file sales tax?",
  "No. We categorise and reconcile payouts, fees, and deposits. Sales tax filing stays with your CPA."),
 ("Which package fits a store?",
  "Starter from $299 per month if you only need the close. Standard from $449 per month if you also want light admin, capped at 3 hours a month. Catch-up from $200 per month behind if the store books are open."),
]

FIT_FAQS = [
 ("What happens after I submit the fit check?",
  "We review your answers and reply to your email within one business day. If you are a strong fit, we suggest next steps, including catch-up if the books are behind."),
 ("Is this the software diagnostic?",
  "No. This form is only for bookkeeping. It asks about the company, the software, how far behind the books are, and which package you want."),
 ("What if I am not sure which package?",
  "Choose Not sure. Starter is the close only, from $299 per month. Standard adds light admin capped at 3 hours a month, from $449 per month. Catch-up is a project from $200 per month behind, quoted after this form."),
]


def books_cta(title, sub, primary_label, primary_href, primary_track, secondary_label, secondary_href, secondary_track):
    return f"""<section class="cta-band">
  <div class="container">
    <h2>{title}</h2>
    <p>{sub}</p>
    <div class="btn-row" style="justify-content:center">
      <a class="btn btn-primary btn-lg" href="{primary_href}" data-track="bookkeeping_cta_click" data-track-label="{primary_track}">{primary_label}</a>
      <a class="btn btn-secondary btn-lg" href="{secondary_href}" data-track="bookkeeping_cta_click" data-track-label="{secondary_track}">{secondary_label}</a>
    </div>
  </div>
</section>
"""


def books_fit_form():
    return f"""<div id="books-form-success" class="form-success" role="status" tabindex="-1">
<p><strong>Thanks — we've got your fit check.</strong></p>
<p>We'll review your answers and reply to your email within one business day. If you're a strong fit for async monthly close, we'll suggest next steps, including catch-up if the books are behind.</p>
<p>What we don't do: CPA or tax filing, weekly stand-ups, or full executive assistant work. If you need those, we'll say so plainly.</p>
<p id="books-form-delivery" class="form-delivery-note" hidden></p>
</div>
<div class="form-card" id="books-form-card">
<!--
  Bookkeeping fit check only. Do not post this to /request/ or the rescue diagnostic.
  Endpoint is BOOKS_FORM in build.py. YOUR_BOOKKEEPING_FORM_ID does not deliver email.
  Until a real Formspree id is set, js/main.js opens a mailto draft to hello@meridian.dev.
-->
<form id="bookkeeping-fit-form" action="{BOOKS_FORM}" method="POST" data-formspree="{BOOKS_FORM}" novalidate>
<input type="hidden" name="_subject" value="Meridian bookkeeping fit check">
<input type="hidden" name="_replyto" id="bk-replyto" value="">
<input type="hidden" name="inquiry" id="bk-inquiry" value="Bookkeeping fit check">
<input type="hidden" name="source" id="bk-source" value="fit-check">
<input type="hidden" name="form_version" value="vb-fit-check-v1">
<input type="hidden" name="landing_page" id="bk-landing" value="">
<input type="hidden" name="submitted_at" id="bk-submitted" value="">
<input type="hidden" name="utm_source" id="bk-utm-source" value="">
<input type="hidden" name="utm_medium" id="bk-utm-medium" value="">
<input type="hidden" name="utm_campaign" id="bk-utm-campaign" value="">
<input type="hidden" name="utm_content" id="bk-utm-content" value="">
<div id="books-form-errors" class="form-errors" role="alert"></div>
<h2 class="form-section-title">About you</h2>
<div class="form-group">
<label for="bk-name">Full name</label>
<input id="bk-name" name="name" type="text" autocomplete="name" maxlength="120" required placeholder="Jane Founder" aria-describedby="bk-name-error">
<p class="field-error" id="bk-name-error"></p>
</div>
<div class="form-group">
<label for="bk-email">Work email</label>
<input id="bk-email" name="email" type="email" autocomplete="email" maxlength="160" required placeholder="you@company.com" aria-describedby="bk-email-error">
<p class="field-error" id="bk-email-error"></p>
</div>
<div class="form-group">
<label for="bk-company">Company name</label>
<input id="bk-company" name="company" type="text" autocomplete="organization" maxlength="160" required placeholder="Acme Labs" aria-describedby="bk-company-error">
<p class="field-error" id="bk-company-error"></p>
</div>
<div class="form-group">
<label for="bk-role">Role</label>
<select id="bk-role" name="role" required aria-describedby="bk-role-error">
<option value="">Select…</option>
<option>Founder / Co-founder</option>
<option>Operator / COO</option>
<option>Finance lead</option>
<option>Other</option>
</select>
<p class="field-error" id="bk-role-error"></p>
</div>
<div class="form-group">
<label for="bk-stage">Company stage</label>
<select id="bk-stage" name="stage" required aria-describedby="bk-stage-error">
<option value="">Select…</option>
<option>Pre-revenue</option>
<option>Revenue under $250k</option>
<option>$250k–$1M</option>
<option>$1M–$5M</option>
<option>$5M+</option>
</select>
<p class="field-error" id="bk-stage-error"></p>
</div>
<div class="form-group">
<label for="bk-team">Team size</label>
<select id="bk-team" name="team_size" required aria-describedby="bk-team-error">
<option value="">Select…</option>
<option>Just me</option>
<option>2–5</option>
<option>6–15</option>
<option>16–50</option>
<option>50+</option>
</select>
<p class="field-error" id="bk-team-error"></p>
</div>
<h2 class="form-section-title">Books and tools</h2>
<div class="form-group">
<label for="bk-software">Accounting software</label>
<select id="bk-software" name="software" required aria-describedby="bk-software-error">
<option value="">Select…</option>
<option>QuickBooks Online</option>
<option>Xero</option>
<option>Wave</option>
<option>Spreadsheet / none</option>
<option>Other</option>
</select>
<p class="field-error" id="bk-software-error"></p>
</div>
<div class="form-group" id="bk-software-other-wrap" hidden>
<label for="bk-software-other">Other software <span class="hint">(optional)</span></label>
<input id="bk-software-other" name="software_other" type="text" maxlength="120" placeholder="e.g. FreshBooks">
</div>
<div class="form-group">
<label for="bk-behind">How far behind are the books?</label>
<select id="bk-behind" name="behind" required aria-describedby="bk-behind-error">
<option value="">Select…</option>
<option>Current / up to 1 month</option>
<option>2–3 months</option>
<option>4–6 months</option>
<option>7–12 months</option>
<option>12+ months</option>
<option>Not sure</option>
</select>
<p class="field-error" id="bk-behind-error"></p>
</div>
<fieldset class="form-group" id="bk-needs-group">
<legend>Primary need</legend>
<p class="hint">Select all that apply.</p>
<div class="check-list">
<label><input type="checkbox" name="needs" value="Monthly close and reconciliation"> Monthly close and reconciliation</label>
<label><input type="checkbox" name="needs" value="Catch-up / backlog"> Catch-up / backlog</label>
<label><input type="checkbox" name="needs" value="Receipt and invoice capture"> Receipt and invoice capture</label>
<label><input type="checkbox" name="needs" value="Categorisation clean-up"> Categorisation clean-up</label>
<label><input type="checkbox" name="needs" value="Written monthly report"> Written monthly report</label>
<label><input type="checkbox" name="needs" value="Light admin" id="bk-need-admin"> Light admin (inbox triage, scheduling, documents)</label>
<label><input type="checkbox" name="needs" value="Something else" id="bk-need-else"> Something else</label>
</div>
<p class="field-error" id="bk-needs-error"></p>
</fieldset>
<div class="form-group" id="bk-else-wrap" hidden>
<label for="bk-else">Something else</label>
<textarea id="bk-else" name="needs_other" maxlength="500" placeholder="Brief description" aria-describedby="bk-else-error"></textarea>
<p class="field-error" id="bk-else-error"></p>
</div>
<div class="form-group">
<label for="bk-cpa">Do you already have a CPA / tax advisor?</label>
<select id="bk-cpa" name="cpa" required aria-describedby="bk-cpa-error">
<option value="">Select…</option>
<option>Yes</option>
<option>No</option>
<option>Looking for one</option>
</select>
<p class="field-error" id="bk-cpa-error"></p>
</div>
<h2 class="form-section-title">Fit signals</h2>
<div class="form-group">
<label for="bk-package">Package interest</label>
<select id="bk-package" name="package" required aria-describedby="bk-package-error">
<option value="">Select…</option>
<option value="Starter">Starter — from $299/mo</option>
<option value="Standard">Standard — from $449/mo</option>
<option value="Catch-up">Catch-up — from $200 per month behind</option>
<option value="Not sure">Not sure</option>
</select>
<p class="field-error" id="bk-package-error"></p>
</div>
<div class="form-group">
<label for="bk-done">What does “done” look like in 90 days?</label>
<textarea id="bk-done" name="done_90" required minlength="20" maxlength="2000" placeholder="e.g. Closed books by the 10th, clean categories, one written report I can send my CPA" aria-describedby="bk-done-error"></textarea>
<p class="field-error" id="bk-done-error"></p>
</div>
<div class="form-group">
<label for="bk-timing">Preferred start timing</label>
<select id="bk-timing" name="timing" required aria-describedby="bk-timing-error">
<option value="">Select…</option>
<option>ASAP</option>
<option>This month</option>
<option>Next 30–60 days</option>
<option>Just researching</option>
</select>
<p class="field-error" id="bk-timing-error"></p>
</div>
<div class="form-group">
<label for="bk-budget">Approx. monthly budget for books <span class="hint">(soft signal)</span></label>
<select id="bk-budget" name="budget" required aria-describedby="bk-budget-error">
<option value="">Select…</option>
<option>Under $299</option>
<option>$299–$448</option>
<option>$449–$699</option>
<option>$700+</option>
<option>Not sure yet</option>
</select>
<p class="field-error" id="bk-budget-error"></p>
</div>
<div class="form-group">
<label for="bk-hear">How did you hear about Meridian? <span class="hint">(optional)</span></label>
<select id="bk-hear" name="hear_about">
<option value="">Select…</option>
<option>Search</option>
<option>LinkedIn</option>
<option>Referral / CPA</option>
<option>Existing Meridian client</option>
<option>Other</option>
</select>
</div>
<div class="form-group">
<label for="bk-notes">Anything else we should know? <span class="hint">(optional)</span></label>
<textarea id="bk-notes" name="notes" maxlength="2000"></textarea>
</div>
<button class="btn btn-primary btn-lg" type="submit">Check fit — we'll reply within 1 business day</button>
<p class="form-endpoint-note">We'll only use this to assess fit and reply. No spam, no tax advice, no weekly meeting upsell.</p>
<p class="form-endpoint-note">Addressed to <a href="mailto:{CONTACT}">{CONTACT}</a>. A real Formspree id is still required for email delivery: replace <code>YOUR_BOOKKEEPING_FORM_ID</code> in <code>BOOKS_FORM</code> inside <code>build.py</code>. Until then, submit opens a draft in your email app. The draft is not sent until you send it.</p>
</form>
</div>
"""


def page_bookkeeping():
    path = "virtual-bookkeeping/"
    p = depth(path)
    title = "Virtual Bookkeeping — Async Monthly Close + Admin | Meridian"
    desc = "Receipt and invoice capture, categorisation, reconciliation, and a written monthly report. Standard from $449/mo, Starter from $299/mo. For technical founders and SaaS operators."
    extra = (
        crumbs_json([("Home", "/"), ("Virtual bookkeeping", "/virtual-bookkeeping/")])
        + service_schema(
            "Virtual bookkeeping",
            "/virtual-bookkeeping/",
            desc,
            "Starter from $299/month; Standard from $449/month; catch-up from $200 per month behind",
        )
        + faq_schema(BOOKS_FAQS)
        + ORG
    )
    crumbs = crumbs_html([("Home", p), ("Virtual bookkeeping", None)])
    fit = f"{p}{FIT_PATH}"
    catch = f"{p}catch-up-bookkeeping/"
    mail = f"mailto:{CONTACT}"
    body = f"""
{header(path, "books")}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<p class="hero-kicker">Virtual bookkeeping · Async by design</p>
<h1>Monthly close without the meeting treadmill</h1>
<p class="lede">Meridian handles receipt and invoice capture, categorisation, reconciliation, and a written monthly report — plus light admin for inbox triage, scheduling, and documents on Standard. You stay in the product. We keep the books current.</p>
<ul class="trust-bar">
<li>Standard from $449/mo</li>
<li>Starter from $299/mo</li>
<li>Catch-up from $200 per month behind</li>
<li>Not a CPA · not weekly meetings</li>
</ul>
<p class="meta-line">Last updated: {LAST}</p>
<div class="btn-row">
<a class="btn btn-primary btn-lg" href="{fit}" data-track="bookkeeping_cta_click" data-track-label="hero-fit-check">Start a fit check</a>
<a class="btn btn-secondary btn-lg" href="#included" data-track="bookkeeping_cta_click" data-track-label="hero-included">See what's included</a>
</div>
</div></section>
<section class="section"><div class="narrow prose">
<h2>Your books are somewhere between “fine” and “I’ll deal with it later”</h2>
<p>Receipts live in email. Invoices sit in Stripe, PayPal, or a folder named Finance-final-v3. Categories drift. Month-end never quite closes. When your CPA asks for numbers, you spend a weekend reconstructing reality.</p>
<p>You don’t need another weekly call. You need a reliable async close, and — if you choose Standard — someone who can also clear the admin that blocks shipping.</p>
</div></section>
<section class="section section-alt" id="included"><div class="container">
<h2 class="section-title">What’s in the monthly engagement</h2>
<div class="grid-2" style="margin-top:1.5rem">
<div class="card"><h3>Monthly close</h3>
<ul>
<li><strong>Receipt and invoice capture.</strong> From email, drives, and tools you already use. Gaps come back as a short checklist, not a meeting.</li>
<li><strong>Categorisation.</strong> A consistent chart of accounts. Edge cases flagged in writing.</li>
<li><strong>Reconciliation.</strong> Bank and key accounts matched each month.</li>
<li><strong>Written monthly report.</strong> What moved, what’s outstanding, what to decide. Ready to forward to your CPA.</li>
</ul></div>
<div class="card"><h3>Light admin — Standard only</h3>
<ul>
<li><strong>Inbox triage.</strong> Finance and operational mail sorted. Drafts or flags where you need to act.</li>
<li><strong>Scheduling.</strong> Holds and calendar coordination for the meetings that do matter.</li>
<li><strong>Document handling.</strong> Filing, naming, and routing contracts, statements, and vendor docs.</li>
</ul>
<p><strong>Hard cap:</strong> {ADMIN_CAP}. Hours past the cap are out of scope and quoted separately. Starter does not include admin.</p>
</div>
</div>
</div></section>
<section class="section"><div class="narrow prose">
<h2>Clear boundaries</h2>
<ul>
<li>We are not your CPA. We don’t file taxes or give tax advice.</li>
<li>We don’t default to weekly stand-ups. The work is async, with written updates.</li>
<li>We are not a full-time executive assistant.</li>
<li>We don’t replace your lawyer, payroll provider, or payment processor.</li>
</ul>
<p>If you need tax filing, we work cleanly with your CPA. If you need deep assistant cover, we will say so.</p>
<h2 id="how">Four steps. Mostly async.</h2>
<ol class="steps">
<li><strong>Fit check.</strong> Tools, how far behind you are, and what “done” looks like.</li>
<li><strong>Scope and kickoff.</strong> We confirm software, access, and whether catch-up comes first.</li>
<li><strong>Monthly rhythm.</strong> Capture, categorise, reconcile, written report. On Standard, admin runs against the same list, inside the hour cap.</li>
<li><strong>Handoff to your CPA.</strong> When tax season hits, the books are organised and documented.</li>
</ol>
</div></section>
<section class="section section-alt" id="pricing"><div class="container">
<h2 class="section-title">Pricing</h2>
<p class="lede">Standard is the main offer. Starter is the close without admin. Catch-up is a project, quoted after the fit check.</p>
<div class="grid-3" style="margin-top:1.5rem">
<div class="price-card"><span class="pill">Close only</span><h3>Starter</h3>
<div class="amount">$299 <span>/ month</span></div>
<p>From $299/mo. Async monthly close only.</p>
<ul>
<li>Capture, categorisation, reconciliation</li>
<li>Written monthly report</li>
<li>No admin</li>
</ul>
<a class="btn btn-secondary" href="{fit}?package=starter" data-track="bookkeeping_cta_click" data-track-label="pricing-starter">Start a fit check</a>
</div>
<div class="price-card featured"><span class="pill pill-ok">Main offer</span><h3>Standard</h3>
<div class="amount">$449 <span>/ month</span></div>
<p>From $449/mo. Starter, plus light admin.</p>
<ul>
<li>Everything in Starter</li>
<li>Inbox triage, scheduling, documents</li>
<li>Hard cap: {ADMIN_CAP}</li>
</ul>
<p class="price-note">Published price is $449/mo. Launch promo $399/mo on request.</p>
<a class="btn btn-primary" href="{fit}?package=standard" data-track="bookkeeping_cta_click" data-track-label="pricing-standard">Start a fit check</a>
</div>
<div class="price-card"><span class="pill">Project</span><h3>Catch-up</h3>
<div class="amount">$200 <span>/ month behind</span></div>
<p>From $200 per month behind. Quoted after the fit check.</p>
<ul>
<li>Simple, clean books can be lower</li>
<li>Complex books quote higher</li>
<li>Then Starter or Standard if you want it</li>
</ul>
<a class="btn btn-secondary" href="{catch}" data-track="bookkeeping_cta_click" data-track-label="pricing-catch-up">See catch-up</a>
</div>
</div>
<p class="meta-line" style="margin-top:1.25rem">No long contract is required to start a fit check. We quote before work begins. Tax stays with your CPA.</p>
</div></section>
<section class="section"><div class="narrow prose">
<h2>Built for people who ship product</h2>
<ul>
<li>Technical founders and co-founders</li>
<li>SaaS and product operators</li>
<li>Small teams that outgrew a spreadsheet and do not want a full-time bookkeeper on payroll yet</li>
</ul>
<p>Less of a fit: on-site staff, a weekly Zoom books meeting, or CPA and tax as the primary service. <a href="{p}virtual-bookkeeping/for-founders/">For founders</a> · <a href="{p}virtual-bookkeeping/for-ecommerce/">For ecommerce</a></p>
<div class="callout"><strong>Books behind?</strong> Start with a catch-up project. We clear the backlog month by month — from $200 per month behind, quoted after the fit check — then hand you a clean baseline. <a href="{catch}">See catch-up</a>.</div>
<h2>FAQ</h2>
{faq_html(BOOKS_FAQS)}
</div></section>
{books_cta(
    "Get the books off your plate — without adding another weekly meeting",
    "Tell us where the books stand and what done looks like. We'll reply within one business day.",
    "Start a fit check", fit, "bottom-fit-check",
    "Email hello@meridian.dev", mail, "bottom-email",
)}
</main>
{footer(path, "books")}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)


def page_catchup_bookkeeping():
    path = "catch-up-bookkeeping/"
    p = depth(path)
    title = "Catch-Up Bookkeeping — Clear the Backlog | Meridian"
    desc = "Bring months of receipts, invoices, and bank activity current. Catch-up from $200 per month behind, then optional Starter from $299/mo or Standard from $449/mo."
    extra = (
        crumbs_json([("Home", "/"), ("Catch-up bookkeeping", "/catch-up-bookkeeping/")])
        + service_schema(
            "Catch-up bookkeeping",
            "/catch-up-bookkeeping/",
            desc,
            "From $200 per month behind, quoted after the fit check",
        )
        + faq_schema(CATCHUP_FAQS)
        + ORG
    )
    crumbs = crumbs_html([("Home", p), ("Catch-up bookkeeping", None)])
    fit = f"{p}{FIT_PATH}?intent=catch-up"
    monthly = f"{p}virtual-bookkeeping/"
    mail = f"mailto:{CONTACT}"
    body = f"""
{header(path, "books")}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<p class="hero-kicker">Catch-up project · Then optional monthly close</p>
<h1>Clear the backlog. Start the next month clean.</h1>
<p class="lede">Meridian works through receipts, invoices, and statements month by month — categorisation, reconciliation, and a written summary of what is fixed and what is still open. From $200 per month behind. The quote comes after the fit check. Simple books can be lower; complex books higher.</p>
<p class="meta-line">Last updated: {LAST}</p>
<div class="btn-row">
<a class="btn btn-primary btn-lg" href="{fit}" data-track="bookkeeping_cta_click" data-track-label="catchup-hero-fit-check">Start a fit check</a>
<a class="btn btn-secondary btn-lg" href="{mail}" data-track="bookkeeping_cta_click" data-track-label="catchup-hero-email">Email hello@meridian.dev</a>
</div>
</div></section>
<section class="section"><div class="narrow prose">
<h2>You are looking for a finish line</h2>
<ul>
<li>Two to twelve months, or more, of uncategorised transactions</li>
<li>Receipts in email, Slack, or a drive folder with an unhelpful name</li>
<li>A CPA asking for numbers you cannot produce without a weekend</li>
<li>A founder who would rather ship than reconstruct last quarter by hand</li>
</ul>
<h2>Month by month, until you are current</h2>
<ul>
<li><strong>Capture.</strong> Invoices, receipts, and bank or export data for each open month.</li>
<li><strong>Categorisation.</strong> Consistent categories. Undocumented spend flagged in writing.</li>
<li><strong>Reconciliation.</strong> Accounts matched, so the backlog is not only sorted in name.</li>
<li><strong>Written catch-up summary.</strong> What closed, the exceptions, and a recommended ongoing rhythm.</li>
</ul>
<p>Not included: tax filing, tax advice, or an audit. We prepare books your CPA can use.</p>
<h2>Priced by how far behind you are</h2>
<ul>
<li><strong>Catch-up:</strong> from $200 per month behind. Quoted after the fit check. Simple, clean books can be lower. Complex books are higher.</li>
<li><strong>Then, if you want ongoing:</strong> <a href="{monthly}">Starter from $299/mo</a> (close only) or Standard from $449/mo (close plus light admin, capped at {ADMIN_CAP}).</li>
</ul>
<p>Example, illustrative only: six months behind starts from $1,200, then an optional monthly retainer. The final number waits until we see volume, entities, and software.</p>
<h2>How catch-up works</h2>
<ol class="steps">
<li><strong>Fit check.</strong> Software, approximate months behind, access constraints. Catch-up is noted on the form.</li>
<li><strong>Scoped quote.</strong> A project based on months and complexity, not an open clock.</li>
<li><strong>Access and batch work.</strong> We work async. You answer a short exception list when needed.</li>
<li><strong>Handoff.</strong> A clean baseline and a summary. Option to continue on Starter or Standard.</li>
</ol>
<p>Typical kickoff is within one to two weeks of approved access. Duration depends on the months behind and how complete the source data is.</p>
<h2>Don’t fall behind again</h2>
<p>Most teams move into async monthly close. Starter is the close only. Standard adds inbox triage, scheduling, and document handling inside a {ADMIN_CAP} cap. <a href="{monthly}">Monthly bookkeeping</a>.</p>
<h2>FAQ</h2>
{faq_html(CATCHUP_FAQS)}
</div></section>
{books_cta(
    "Tell us how many months are open",
    "The fit check takes a few minutes. We'll reply within one business day with whether we're a fit and a catch-up estimate.",
    "Start a fit check", fit, "catchup-bottom-fit-check",
    "See the monthly package", monthly, "catchup-bottom-monthly",
)}
</main>
{footer(path, "books")}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)


def page_bookkeeping_founders():
    path = "virtual-bookkeeping/for-founders/"
    p = depth(path)
    title = "Bookkeeping for Technical Founders &amp; SaaS | Meridian"
    desc = "Async monthly close for people who ship product. Standard from $449/mo, Starter from $299/mo. Catch-up from $200 per month behind."
    extra = (
        crumbs_json([
            ("Home", "/"),
            ("Virtual bookkeeping", "/virtual-bookkeeping/"),
            ("For founders", "/virtual-bookkeeping/for-founders/"),
        ])
        + service_schema(
            "Virtual bookkeeping for founders",
            "/virtual-bookkeeping/for-founders/",
            "Async monthly close for technical founders, SaaS, and product operators. Standard from $449/month.",
            "Standard from $449/month; Starter from $299/month; catch-up from $200 per month behind",
        )
        + faq_schema(FOUNDER_FAQS)
        + ORG
    )
    crumbs = crumbs_html([
        ("Home", p),
        ("Virtual bookkeeping", f"{p}virtual-bookkeeping/"),
        ("For founders", None),
    ])
    fit = f"{p}{FIT_PATH}?source=founders&amp;package=standard"
    monthly = f"{p}virtual-bookkeeping/"
    catch = f"{p}catch-up-bookkeeping/"
    mail = f"mailto:{CONTACT}"
    body = f"""
{header(path, "books")}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<p class="hero-kicker">For technical founders · SaaS · product operators</p>
<h1>Ship product. We'll close the month.</h1>
<p class="lede">Meridian runs an async monthly close — receipt and invoice capture, categorisation, reconciliation, and a written report you can send to your CPA — plus light admin on Standard so finance ops don’t eat the roadmap. Standard from $449/mo. Starter from $299/mo if you want the close only.</p>
<p class="niche-line">Built for technical founders and busy operators who want clean numbers without a weekly finance meeting.</p>
<p class="meta-line">Last updated: {LAST}</p>
<div class="btn-row">
<a class="btn btn-primary btn-lg" href="{fit}" data-track="bookkeeping_cta_click" data-track-label="founders-fit-check">Start a fit check</a>
<a class="btn btn-secondary btn-lg" href="{monthly}#how" data-track="bookkeeping_cta_click" data-track-label="founders-rhythm">See the monthly rhythm</a>
</div>
</div></section>
<section class="section"><div class="narrow prose">
<h2>The founder problem, said plainly</h2>
<p>You can read a P&amp;L. You should not have to assemble one from Stripe exports, Gmail attachments, and a bank CSV every month.</p>
<p>Meetings-as-bookkeeping don’t help. You need categories that stay consistent, reconciled accounts by a predictable date, a short written report, and — on Standard — someone who can triage the inbox and documents that stall decisions.</p>
<p>That is the retainer. Not a second co-founder. Not a CPA. Not a weekly Zoom.</p>
<h2>Async, documented, tool-friendly</h2>
<ul>
<li><strong>Your stack.</strong> QuickBooks Online or Xero, bank feeds, and Stripe or PayPal exports when needed.</li>
<li><strong>Your pace.</strong> Exception lists and written updates. A call only when a decision needs one.</li>
<li><strong>Your CPA.</strong> Books are handoff-ready. We don’t file taxes or replace advice.</li>
<li><strong>Your admin load.</strong> On Standard only: inbox triage, scheduling, and document handling, capped at {ADMIN_CAP}.</li>
</ul>
<h2>What’s included</h2>
<p><strong>Monthly close.</strong> Capture, categorise, reconcile, written monthly report. That is Starter, from $299/mo, and the base of Standard.</p>
<p><strong>Light admin.</strong> Inbox triage, scheduling, document handling. Standard only, from $449/mo, capped at {ADMIN_CAP}.</p>
<p><strong>If you are behind.</strong> <a href="{catch}">Catch-up</a> from $200 per month behind, quoted after the fit check, then optional ongoing monthly.</p>
<p>Full detail is on the <a href="{monthly}">monthly bookkeeping page</a>.</p>
<h2>Pricing anchors</h2>
<ul>
<li><strong>Starter</strong> — from $299/mo. Close only. No admin.</li>
<li><strong>Standard</strong> — from $449/mo. Close plus light admin, {ADMIN_CAP} cap. Published price. Launch promo $399/mo on request.</li>
<li><strong>Catch-up</strong> — from $200 per month behind. Quoted after the fit check.</li>
</ul>
<p>Scope is confirmed after the fit check. Async is the product. We will not switch you onto a weekly meeting after you sign.</p>
<h2>Who this page is for</h2>
<ul>
<li>Solo or small technical founding teams</li>
<li>SaaS with recurring revenue and messy categories</li>
<li>Product operators who inherited books that are not actually closed</li>
<li>Teams with a CPA who needs cleaner inputs, not more founder weekends</li>
</ul>
<p>Less ideal if you want tax filing in-house, daily chat babysitting, or full executive-assistant coverage.</p>
<h2>FAQ</h2>
{faq_html(FOUNDER_FAQS)}
</div></section>
{books_cta(
    "One fit check. A clear reply within a business day.",
    "Tell us your tools, how far behind you are, and what done looks like in 90 days.",
    "Start a fit check", fit, "founders-bottom-fit-check",
    "Email hello@meridian.dev", mail, "founders-bottom-email",
)}
</main>
{footer(path, "books")}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)


def page_bookkeeping_ecommerce():
    path = "virtual-bookkeeping/for-ecommerce/"
    p = depth(path)
    title = "Bookkeeping for ecommerce | Meridian"
    desc = "Monthly bookkeeping for ecommerce in QuickBooks Online or Xero. Standard from $449/mo, Starter from $299/mo. Sales tax stays with your CPA."
    extra = (
        crumbs_json([
            ("Home", "/"),
            ("Virtual bookkeeping", "/virtual-bookkeeping/"),
            ("For ecommerce", "/virtual-bookkeeping/for-ecommerce/"),
        ])
        + service_schema(
            "Virtual bookkeeping for ecommerce",
            "/virtual-bookkeeping/for-ecommerce/",
            desc,
            "Standard from $449/month; Starter from $299/month; catch-up from $200 per month behind",
        )
        + faq_schema(ECOM_FAQS)
        + ORG
    )
    crumbs = crumbs_html([
        ("Home", p),
        ("Virtual bookkeeping", f"{p}virtual-bookkeeping/"),
        ("For ecommerce", None),
    ])
    fit = f"{p}{FIT_PATH}?source=ecommerce"
    monthly = f"{p}virtual-bookkeeping/"
    catch = f"{p}catch-up-bookkeeping/"
    body = f"""
{header(path, "books")}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<p class="hero-kicker">Virtual bookkeeping · Ecommerce</p>
<h1>Ecommerce books, closed monthly.</h1>
<p class="lede">Payouts, processor fees, and sales-channel deposits categorised and reconciled in QuickBooks Online or Xero. A written close. Standard from $449/mo if you want light admin. Starter from $299/mo for the close only. Sales tax filing stays with your CPA.</p>
<p class="meta-line">Last updated: {LAST}</p>
<div class="btn-row">
<a class="btn btn-primary btn-lg" href="{fit}" data-track="bookkeeping_cta_click" data-track-label="ecommerce-fit-check">Start a fit check</a>
<a class="btn btn-secondary btn-lg" href="{monthly}" data-track="bookkeeping_cta_click" data-track-label="ecommerce-monthly">See the monthly package</a>
</div>
</div></section>
<section class="section"><div class="narrow prose">
<h2>What we close</h2>
<ul>
<li>Sales deposits, processor fees, and refunds categorised</li>
<li>Reconciliation against the bank and the payout reports you already export</li>
<li>A written month-end package</li>
<li><a href="{catch}">Catch-up</a> from $200 per month behind if the store books are open, then Starter or Standard</li>
</ul>
<h2>What we do not take on</h2>
<ul>
<li>Sales-tax filing, or a stand-in for your CPA</li>
<li>A weekly ecommerce meeting</li>
<li>Warehouse inventory accounting as the main job — say so on the fit check if that is what you actually need</li>
</ul>
<p>Standard light admin is capped at {ADMIN_CAP}. The full boundary of the work is on the <a href="{monthly}">monthly bookkeeping page</a>.</p>
<h2>FAQ</h2>
{faq_html(ECOM_FAQS)}
</div></section>
{books_cta(
    "Start a fit check",
    "Tell us the channel, the software, and how far behind the books are.",
    "Start a fit check", fit, "ecommerce-bottom-fit-check",
    "See the monthly package", monthly, "ecommerce-bottom-monthly",
)}
</main>
{footer(path, "books")}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)


def page_bookkeeping_fit_check():
    path = FIT_PATH
    p = depth(path)
    title = "Bookkeeping fit check | Meridian"
    desc = "Tell us your software, how far behind the books are, and whether you want Starter, Standard, or catch-up. We reply within one business day."
    extra = (
        crumbs_json([
            ("Home", "/"),
            ("Virtual bookkeeping", "/virtual-bookkeeping/"),
            ("Fit check", "/virtual-bookkeeping/fit-check/"),
        ])
        + faq_schema(FIT_FAQS)
        + ORG
    )
    crumbs = crumbs_html([
        ("Home", p),
        ("Virtual bookkeeping", f"{p}virtual-bookkeeping/"),
        ("Fit check", None),
    ])
    body = f"""
{header(path, "books")}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<p class="hero-kicker">Virtual bookkeeping · Fit check</p>
<h1>Start a fit check</h1>
<p class="lede">Tell us the company, the software, how far behind the books are, and which package you want. We reply within one business day. Standard is from $449/mo. Starter is from $299/mo. Catch-up is from $200 per month behind, quoted after this form.</p>
<p class="meta-line">Last updated: {LAST} · This is not a software diagnostic.</p>
</div></section>
<section class="section"><div class="container" style="max-width:640px">
<div id="catchup-note" class="callout" hidden>
<strong>Catch-up quote.</strong> This is the same fit check. We have noted that you want a project quote to get the books current, from $200 per month behind. Simple books can be lower; complex books higher. Say how far behind you are below.
</div>
{books_fit_form()}
<h2>Before you send it</h2>
{faq_html(FIT_FAQS)}
<p><a href="{p}virtual-bookkeeping/">Monthly package</a> · <a href="{p}catch-up-bookkeeping/">Catch-up bookkeeping</a> · <a href="{p}virtual-bookkeeping/for-founders/">For founders</a></p>
</div></section>
</main>
{footer(path, "books")}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)

def page_pricing():
    path = "pricing/"
    p = depth(path)
    title = "Pricing — Vibe Code Rescue ladder | Meridian"
    desc = "Transparent pricing for vibe code rescue: diagnostic free–$500, audit $299–$2,500, rescue $500–$12,500+, rebuild path higher. Clear not-for-you criteria."
    faqs = [
      ("How much does vibe code rescue cost?",
       "Typical 2026 bands: diagnostic free to $500; paid audit $299–$2,500; focused rescue $500–$12,500+; full rebuild paths are higher and scoped separately. Exact quotes follow the diagnostic."),
      ("Is the diagnostic free?",
       "Often free or credited toward rescue for a clear, bounded ask. Larger or rush reviews may be $299–$500. We say which before you send access."),
    ]
    extra = crumbs_json([("Home","/"),("Pricing","/pricing/")]) + faq_schema(faqs) + ORG
    crumbs = crumbs_html([("Home",p),("Pricing",None)])
    body = f"""
{header(path)}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<h1>Transparent pricing ladder</h1>
<p class="answer-first"><strong>Quick answer:</strong> Diagnostic typically free–$500 (48h written scorecard). Paid audit $299–$2,500. Focused rescue $500–$12,500+. Rebuild / production sprint paths are higher and quoted after the diagnostic. Fixed scope when we cut code. You own everything.</p>
<p class="meta-line">Last updated: {LAST} · Bands reflect common 2026 market ranges; your quote follows evidence from the audit.</p>
</div></section>
<section class="section"><div class="container">
<div class="grid-2">
<div class="price-card"><span class="pill">Step 1</span><h3>Diagnostic</h3><div class="amount">Free–$500 <span>USD</span></div>
<p>Written severity-ranked scorecard within ~48 hours. Keep / harden / rebuild recommendation.</p>
<ul><li>Repo or export review</li><li>Security &amp; money path scan</li><li>Often credited toward rescue</li></ul>
<a class="btn btn-primary" href="{p}request/">Request diagnostic</a></div>
<div class="price-card"><span class="pill">Step 2</span><h3>Paid audit</h3><div class="amount">$299–$2,500 <span>USD</span></div>
<p>Deeper written audit when the codebase is larger, regulated, or you need diligence-ready notes.</p>
<ul><li>Expanded findings &amp; priorities</li><li>Architecture notes</li><li>Remediation roadmap</li></ul>
<a class="btn btn-secondary" href="{p}request/">Ask about audit depth</a></div>
<div class="price-card featured"><span class="pill pill-ok">Most common</span><h3>Focused rescue</h3><div class="amount">$500–$12,500+ <span>USD</span></div>
<p>Fixed-scope salvage: secrets, auth, RLS/tenancy, payments, deploy blockers, and agreed hardening.</p>
<ul><li>Quote after diagnostic</li><li>Boundaries in writing</li><li>You own the repo</li></ul>
<a class="btn btn-primary" href="{p}vibe-code-rescue/">How rescue works</a></div>
<div class="price-card"><span class="pill pill-muted">When needed</span><h3>Rebuild / production sprint</h3><div class="amount">Higher <span>scoped</span></div>
<p>When salvage is uneconomical or diligence demands a clean foundation. Quoted only after honest diagnostic.</p>
<ul><li>Strangler or clean rebuild options</li><li>Still fixed-scope where possible</li><li>See <a href="{p}guides/rescue-vs-rewrite/">rescue vs rewrite</a></li></ul>
<a class="btn btn-secondary" href="{p}request/">Discuss rebuild path</a></div>
</div>
<div class="narrow prose" style="margin-top:2.5rem">
<h2>Virtual bookkeeping</h2>
<p>A separate package from software rescue. Flat monthly fee. No hourly surprises. Tax stays with your CPA.</p>
<ul>
<li><strong>Starter:</strong> from $299/month. Async monthly close only. No admin.</li>
<li><strong>Standard:</strong> from $449/month. Starter plus light admin, capped at 3 hours a month. Published price is $449. Launch promo $399 on request.</li>
<li><strong>Catch-up:</strong> from $200 per month behind, quoted after the fit check. Simple books can be lower; complex books higher.</li>
</ul>
<div class="btn-row">
<a class="btn btn-primary" href="{p}virtual-bookkeeping/" data-track="bookkeeping_cta_click" data-track-label="pricing-page-monthly">Monthly package</a>
<a class="btn btn-secondary" href="{p}catch-up-bookkeeping/" data-track="bookkeeping_cta_click" data-track-label="pricing-page-catch-up">Catch-up bookkeeping</a>
</div>
</div>
<div class="not-for-you">
<h3>Not for you (and that is OK)</h3>
<ul>
<li>You want unlimited hourly tinkering with no scope</li>
<li>You need us to invent the product idea — we salvage and harden; we do not replace your vision</li>
<li>You refuse to rotate exposed secrets or grant reasonable access</li>
<li>You need a same-day miracle on an unscoped enterprise estate</li>
<li>You only want someone to prompt harder with no engineering ownership</li>
</ul>
<p>If that is you, we will say so politely after the diagnostic — or sooner by email at <a href="mailto:{CONTACT}">{CONTACT}</a>.</p>
</div>
<div class="narrow" style="margin-top:2.5rem">
<h2>FAQ</h2>
{faq_html(faqs)}
<p>More answers on the <a href="{p}faq/">full FAQ</a> and <a href="{p}vibe-code-rescue/">service page</a>.</p>
</div>
</div></section>
{cta(path, "Start with the diagnostic", "No obligation beyond the agreed diagnostic fee (often free). Fixed quotes before rescue work.")}
</main>
{footer(path)}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)


def page_request(slug="request"):
    path = f"{slug}/"
    p = depth(path)
    title = "Request a 48-hour diagnostic | Meridian"
    desc = "Request a Meridian Vibe Code Rescue diagnostic. Name, email, tools used, problem brief. Do not paste secrets. Written scorecard in ~48 hours."
    extra = crumbs_json([("Home","/"),("Request diagnostic",f"/{slug}/")]) + ORG
    crumbs = crumbs_html([("Home",p),("Request diagnostic",None)])
    alias = (f'<p class="meta-line">This page is also available at <a href="{p}request/">/request/</a>.</p>'
             if slug == "diagnostic" else
             f'<p class="meta-line">Also at <a href="{p}diagnostic/">/diagnostic/</a>.</p>')
    body = f"""
{header(path)}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<h1>Request a 48-hour diagnostic</h1>
<p class="answer-first"><strong>Quick answer:</strong> Tell us what you built, which AI tools you used, and what is broken or scary. We reply with next steps and aim for a written diagnostic within 48 hours of access. Do not paste API keys, tokens, or passwords into this form.</p>
<p class="meta-line">Last updated: {LAST}</p>
{alias}
<p>This form is for a software diagnostic, and for <a href="{p}customer-growth/">Customer growth</a>. Bookkeeping has its own form: <a href="{p}{FIT_PATH}">check if the package fits</a>. Do not paste secrets.</p>
</div></section>
<section class="section"><div class="container" style="max-width:640px">
<div id="form-success" class="form-success" role="status">
<strong>Request captured.</strong> If your mail client opened, send the message to complete. Or we received it via Formspree. We will reply from {CONTACT}.
</div>
<div class="form-card">
<div class="form-warning"><strong>Do not paste secrets.</strong> No API keys, <code>.env</code> contents, private keys, access tokens, or passwords. Describe the problem; share the repo privately after we reply (NDA available).</div>
<form id="request-form" data-formspree="https://formspree.io/f/YOUR_FORM_ID" novalidate>
<input type="hidden" name="_subject" value="Meridian diagnostic request">
<input type="hidden" name="interest" id="interest" value="">
<div class="form-group"><label for="name">Name</label><input id="name" name="name" type="text" required autocomplete="name"></div>
<div class="form-group"><label for="email">Email</label><input id="email" name="email" type="email" required autocomplete="email"></div>
<div class="form-group"><label for="company">Company <span class="hint">(optional)</span></label><input id="company" name="company" type="text" autocomplete="organization"></div>
<div class="form-group"><label for="tools">Tools used</label>
<select id="tools" name="tools" required>
<option value="">Select primary tool…</option>
<option>Cursor</option><option>Lovable</option><option>Bolt</option><option>v0</option>
<option>Replit Agent</option><option>Claude Code</option><option>Windsurf</option><option>Mixed / other</option>
</select></div>
<div class="form-group"><label for="problem">What is broken or blocking launch?</label>
<textarea id="problem" name="problem" required placeholder="e.g. Stripe checkout fails in production; Supabase RLS off; deploy errors on Vercel; AI keeps breaking auth…"></textarea></div>
<div class="form-group"><label for="repo">Repo URL <span class="hint">(optional — public or invite later)</span></label>
<input id="repo" name="repo" type="url" placeholder="https://github.com/…"></div>
<div class="form-group checkbox-row">
<input id="secrets-ack" name="secrets_ack" type="checkbox" value="yes" required>
<label for="secrets-ack">I confirm I have not pasted secrets, credentials, or private keys into this form.</label>
</div>
<button class="btn btn-primary btn-lg" type="submit">Send diagnostic request</button>
</form>
<p class="meta-line" style="margin-top:1.25rem">Prefer email? <a href="mailto:{CONTACT}?subject=Vibe%20Code%20Rescue%20diagnostic">{CONTACT}</a>. Replace <code>YOUR_FORM_ID</code> in the form Formspree endpoint when you deploy.</p>
</div></div></section>
</main>
{footer(path)}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)

def page_tool(slug, name, answer, bullets):
    path = f"rescue/{slug}/"
    p = depth(path)
    title = f"{name} rescue — Vibe Code Rescue | Meridian"
    desc = (answer[:152] + "…") if len(answer) > 155 else answer
    faqs = [
      (f"Can you fix a {name}-built app without rewriting it?",
       f"Usually yes for a large portion of the product. We diagnose first, then propose fixed-scope salvage focused on security, auth, data, and payments."),
      (f"How much does {name} rescue cost?",
       "Same ladder as our general pricing: diagnostic free–$500, audit $299–$2,500, focused rescue $500–$12,500+. See /pricing/."),
    ]
    extra = (crumbs_json([("Home","/"),(f"{name} rescue",f"/rescue/{slug}/")])
             + service_schema(f"{name} vibe code rescue", f"/rescue/{slug}/", answer)
             + faq_schema(faqs))
    crumbs = crumbs_html([("Home",p),("Vibe Code Rescue",f"{p}vibe-code-rescue/"),(name,None)])
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    body = f"""
{header(path)}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<p class="hero-kicker">Rescue by tool</p>
<h1>{name} rescue</h1>
<p class="answer-first"><strong>Quick answer:</strong> {answer}</p>
<p class="meta-line">Last updated: {LAST}</p>
<div class="btn-row">
<a class="btn btn-primary" href="{p}request/">Request diagnostic</a>
<a class="btn btn-secondary" href="{p}pricing/">Pricing</a>
</div></div></section>
<section class="section"><div class="narrow prose">
<h2>Common {name} failure signatures</h2>
<ul>{lis}</ul>
<h2>Related problems</h2>
<div class="chip-row">
<a class="chip" href="{p}problems/secrets-exposed/">Secrets exposed</a>
<a class="chip" href="{p}problems/rls-tenancy/">RLS / tenancy</a>
<a class="chip" href="{p}problems/stripe-payments/">Stripe payments</a>
<a class="chip" href="{p}problems/wont-deploy/">Won't deploy</a>
<a class="chip" href="{p}problems/ai-fix-loop/">AI fix loop</a>
</div>
<h2>How Meridian helps</h2>
<p>We run the same <a href="{p}vibe-code-rescue/">Vibe Code Rescue</a> process: 48h diagnostic, severity ranking, fixed-scope salvage. Tool-specific experience means we recognise the patterns faster.</p>
<h2>FAQ</h2>
{faq_html(faqs)}
</div></section>
{cta(path, f"Rescue your {name} app", "48-hour diagnostic. Empathy, no shame. You own the code.")}
</main>
{footer(path)}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)

def page_problem(slug, name, answer, bullets, closer):
    path = f"problems/{slug}/"
    p = depth(path)
    title = f"{name} — Meridian Vibe Code Rescue"
    desc = (answer[:152] + "…") if len(answer) > 155 else answer
    faqs = [(f"Can Meridian help with {name.lower()}?",
             "Yes. This is a standard diagnostic and rescue focus area. Request a 48-hour diagnostic and we will rank severity and propose fixed scope.")]
    extra = crumbs_json([("Home","/"),(name,f"/problems/{slug}/")]) + faq_schema(faqs)
    crumbs = crumbs_html([("Home",p),("Problems",f"{p}problems/secrets-exposed/"),(name,None)])
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    body = f"""
{header(path)}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<p class="hero-kicker">Problem guide</p>
<h1>{name}</h1>
<p class="answer-first"><strong>Quick answer:</strong> {answer}</p>
<p class="meta-line">Last updated: {LAST}</p>
<div class="btn-row">
<a class="btn btn-primary" href="{p}request/">Request diagnostic</a>
<a class="btn btn-secondary" href="{p}vibe-code-rescue/">Vibe Code Rescue</a>
</div></div></section>
<section class="section"><div class="narrow prose">
<h2>What to do</h2>
<ul>{lis}</ul>
<p>{closer}</p>
<h2>Rescue by tool</h2>
<div class="chip-row">
<a class="chip" href="{p}rescue/lovable/">Lovable</a>
<a class="chip" href="{p}rescue/bolt/">Bolt</a>
<a class="chip" href="{p}rescue/cursor/">Cursor</a>
<a class="chip" href="{p}rescue/v0/">v0</a>
<a class="chip" href="{p}rescue/replit/">Replit</a>
<a class="chip" href="{p}rescue/claude-code/">Claude Code</a>
</div>
<h2>FAQ</h2>
{faq_html(faqs)}
<p>See also <a href="{p}pricing/">pricing</a> and <a href="{p}guides/rescue-vs-rewrite/">rescue vs rewrite</a>.</p>
</div></section>
{cta(path)}
</main>
{footer(path)}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)


SITE_FAQS = VCR_FAQS + [
 ("How much does vibe code rescue cost at Meridian?",
  "Diagnostic free–$500; audit $299–$2,500; focused rescue $500–$12,500+; rebuild paths higher. Details on the pricing page."),
 ("Where is Meridian based?",
  "We work remotely with clients in Canada, the US, and internationally. Correspondence: hello@meridian.dev."),
 ("Do you invent fake case studies?",
  "No. We do not publish invented client names or metrics. Ask us directly about fit for your stack."),
] + [q for q in GROWTH_FAQS + BOOKS_FAQS if q[0] != "How do I start?"]

def page_faq():
    path = "faq/"
    p = depth(path)
    title = "FAQ — Vibe Code Rescue | Meridian"
    desc = "Frequently asked questions about Meridian Vibe Code Rescue: process, pricing, tools, rescue vs rewrite, and ownership."
    extra = crumbs_json([("Home","/"),("FAQ","/faq/")]) + faq_schema(SITE_FAQS) + ORG
    crumbs = crumbs_html([("Home",p),("FAQ",None)])
    body = f"""
{header(path)}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<h1>Frequently asked questions</h1>
<p class="answer-first"><strong>Quick answer:</strong> Meridian Vibe Code Rescue salvages AI-built apps with a 48-hour diagnostic, security-first fixed-scope work, and clear ownership. Empathy, no shame. Pricing bands are public on the pricing page. Customer growth and virtual bookkeeping are separate packages: scoped growth work, and a monthly books and admin close.</p>
<p class="meta-line">Last updated: {LAST}</p>
</div></section>
<section class="section"><div class="narrow">
{faq_html(SITE_FAQS)}
<p>Deep dive: <a href="{p}vibe-code-rescue/">Vibe Code Rescue</a> · <a href="{p}customer-growth/">Customer growth</a> · <a href="{p}virtual-bookkeeping/">Virtual bookkeeping</a> · <a href="{p}catch-up-bookkeeping/">Catch-up bookkeeping</a> · <a href="{p}guides/what-is-vibe-code-rescue/">What is vibe code rescue?</a> · <a href="{p}request/">Request diagnostic</a></p>
</div></section>
</main>
{footer(path)}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)

def page_about():
    path = "about/"
    p = depth(path)
    title = "About Meridian — Senior software studio"
    desc = "Meridian is a senior software studio with 30+ years combined experience across video games, finance, and web. Home of Vibe Code Rescue."
    extra = crumbs_json([("Home","/"),("About","/about/")]) + ORG
    crumbs = crumbs_html([("Home",p),("About",None)])
    body = f"""
{header(path)}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<h1>About Meridian</h1>
<p class="answer-first"><strong>Quick answer:</strong> Meridian is a senior software studio — an abstract umbrella brand for product and rescue work. We bring 30+ years combined experience across video games, finance, and web development. Our flagship service is Vibe Code Rescue.</p>
<p class="meta-line">Last updated: {LAST}</p>
</div></section>
<section class="section"><div class="narrow prose">
<h2>Why we exist</h2>
<p>AI coding tools made it rational to ship prototypes in days. Production still demands senior judgement: security, tenancy, payments, deployability, and maintainability. Meridian sits in that gap — without shaming founders for moving fast.</p>
<h2>How we work</h2>
<ul>
<li>Evidence before ego — diagnose, then decide salvage vs rewrite</li>
<li>Fixed scope when we cut code</li>
<li>You own the repository and the outcomes</li>
<li>Optional guardrails so AI remains a tool, not a liability</li>
</ul>
<h2>Services under the studio</h2>
<p><a href="{p}vibe-code-rescue/">Vibe Code Rescue</a> is the flagship: salvage AI-built apps into production-ready software. Two sibling packages sit beside it:</p>
<ul>
<li><a href="{p}customer-growth/">Customer growth</a> — search, campaigns, landing pages, CRM, and follow-up through to booking. A defined package, not a weekly marketing meeting.</li>
<li><a href="{p}virtual-bookkeeping/">Virtual bookkeeping</a> — async monthly close. Standard from $449/month, Starter from $299/month. <a href="{p}catch-up-bookkeeping/">Catch-up</a> from $200 per month behind. Start at the <a href="{p}{FIT_PATH}">fit check</a>.</li>
</ul>
<p>Product engineering, security hardening, and fractional CTO remain inquire-only while those packages are scoped.</p>
<h2>Contact</h2>
<p>Email <a href="mailto:{CONTACT}">{CONTACT}</a>. Software diagnostic: <a href="{p}request/">request form</a>. Bookkeeping: <a href="{p}{FIT_PATH}">fit check</a>.</p>
<p>We do not invent fake case-study metrics or client names. Fit conversations happen one-to-one.</p>
</div></section>
{cta(path)}
</main>
{footer(path)}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)

def page_guide_what():
    path = "guides/what-is-vibe-code-rescue/"
    p = depth(path)
    title = "What is vibe code rescue? | Meridian"
    desc = "Vibe code rescue is a productized service that salvages AI-built apps into production-ready software without a full rewrite — diagnostic first, then fixed-scope hardening."
    faqs = [SITE_FAQS[0], SITE_FAQS[1]]
    extra = crumbs_json([("Home","/"),("What is vibe code rescue?","/guides/what-is-vibe-code-rescue/")]) + faq_schema(faqs)
    crumbs = crumbs_html([("Home",p),("Guides",f"{p}guides/what-is-vibe-code-rescue/"),("What is vibe code rescue?",None)])
    body = f"""
{header(path)}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<h1>What is vibe code rescue?</h1>
<p class="answer-first"><strong>Quick answer:</strong> Vibe code rescue is a productized engineering service that takes applications built primarily with AI coding tools (Cursor, Lovable, Bolt, v0, Replit Agent, Claude Code, Windsurf, and similar) and makes them production-ready — usually without a full rewrite. Typical flow: short diagnostic, severity-ranked findings, then fixed-scope hardening of security, auth, data, and payments.</p>
<p class="meta-line">Last updated: {LAST}</p>
</div></section>
<section class="section"><div class="narrow prose">
<h2>Why the category exists</h2>
<p>Vibe coding made prototypes cheap. Production still fails in predictable ways: exposed secrets, fake auth, disabled RLS, Stripe stubs, and deploys that only work in preview. Rescue shops productised the cleanup.</p>
<h2>What Meridian rescue includes</h2>
<p>See the full <a href="{p}vibe-code-rescue/">Vibe Code Rescue</a> page for process, tools, deliverables, and FAQ. Pricing bands are on <a href="{p}pricing/">/pricing/</a>.</p>
<h2>Rescue vs rewrite</h2>
<p>Not every app should be salvaged. Use our <a href="{p}guides/rescue-vs-rewrite/">rescue vs rewrite guide</a> for the decision frame we use in diagnostics.</p>
<h2>FAQ</h2>
{faq_html(faqs)}
</div></section>
{cta(path)}
</main>
{footer(path)}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)

def page_guide_vs():
    path = "guides/rescue-vs-rewrite/"
    p = depth(path)
    title = "Rescue vs rewrite — decision guide | Meridian"
    desc = "When to salvage an AI-built app versus rewrite: security risk, architecture debt, team ability to maintain, and economics. Meridian diagnoses before recommending."
    extra = crumbs_json([("Home","/"),("Rescue vs rewrite","/guides/rescue-vs-rewrite/")])
    crumbs = crumbs_html([("Home",p),("Guides",f"{p}guides/what-is-vibe-code-rescue/"),("Rescue vs rewrite",None)])
    body = f"""
{header(path)}
<main>
<section class="page-hero"><div class="container">
{crumbs}
<h1>Rescue vs rewrite</h1>
<p class="answer-first"><strong>Quick answer:</strong> Choose rescue when the product surface works and risk is concentrated in security, auth, data, payments, or deploy — salvageable with fixed scope. Choose rewrite when structure, tenancy model, or defect density makes patching slower and riskier than a clean foundation. Meridian always diagnoses before recommending either path.</p>
<p class="meta-line">Last updated: {LAST}</p>
</div></section>
<section class="section"><div class="narrow prose">
<h2>Lean rescue when</h2>
<ul>
<li>Users already validate the workflow or UI</li>
<li>Core domain logic is understandable</li>
<li>Failures cluster in secrets, auth, RLS, Stripe, deploy</li>
<li>A senior engineer can map a 1–3 week fixed scope</li>
</ul>
<h2>Lean rewrite when</h2>
<ul>
<li>Nobody can explain data flow or tenancy</li>
<li>Security issues are structural, not local</li>
<li>Every AI edit causes regressions across the tree</li>
<li>Diligence or regulation demands a clean provenance story</li>
</ul>
<h2>How we decide</h2>
<p>The <a href="{p}vibe-code-rescue/">48-hour diagnostic</a> produces a keep / harden / rebuild recommendation with severity-ranked evidence — not a sales script. Sample tone: <a href="{p}artifacts/sample-audit.md">sample-audit.md</a>.</p>
<div class="btn-row">
<a class="btn btn-primary" href="{p}request/">Request diagnostic</a>
<a class="btn btn-secondary" href="{p}pricing/">See pricing</a>
</div>
</div></section>
</main>
{footer(path)}
"""
    write(path + "index.html", head(path, title, desc, "/" + path, extra) + body)


def write_robots():
    write("robots.txt", f"""# Meridian — allow major search and AI crawlers
User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Googlebot
Allow: /

Sitemap: {BASE}/sitemap.xml
""")

def write_sitemap(urls):
    locs = "\n".join(
        f"  <url>\n    <loc>{BASE}{u}</loc>\n    <lastmod>2026-09-29</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>"
        for u in urls
    )
    write("sitemap.xml", f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{locs}
</urlset>
""")

def write_llms():
    write("llms.txt", f"""# Meridian
> Senior software studio. Flagship service: Vibe Code Rescue — salvage AI-built apps into production-ready software.

Site: {BASE}/
Contact: {CONTACT}
Last updated: {LAST}

## Primary
- [Home]({BASE}/): Studio overview, 30+ years combined experience (games, finance, web), services grid
- [Vibe Code Rescue]({BASE}/vibe-code-rescue/): Full product page — process, tools, deliverables, FAQ
- [Pricing]({BASE}/pricing/): Diagnostic free–$500; audit $299–$2,500; rescue $500–$12,500+; rebuild higher; not-for-you
- [Request diagnostic]({BASE}/request/): Lead form (also /diagnostic/)
- [FAQ]({BASE}/faq/)
- [About]({BASE}/about/)
- [What is vibe code rescue?]({BASE}/guides/what-is-vibe-code-rescue/)
- [Rescue vs rewrite]({BASE}/guides/rescue-vs-rewrite/)
- [Sample audit artifact]({BASE}/artifacts/sample-audit.md)

## Rescue by tool
- [Lovable]({BASE}/rescue/lovable/)
- [Bolt]({BASE}/rescue/bolt/)
- [Cursor]({BASE}/rescue/cursor/)
- [v0]({BASE}/rescue/v0/)
- [Replit Agent]({BASE}/rescue/replit/)
- [Claude Code]({BASE}/rescue/claude-code/)
- [Windsurf]({BASE}/rescue/windsurf/)

## Problems
- [Secrets exposed]({BASE}/problems/secrets-exposed/)
- [RLS / tenancy]({BASE}/problems/rls-tenancy/)
- [Stripe / payments]({BASE}/problems/stripe-payments/)
- [Won't deploy]({BASE}/problems/wont-deploy/)
- [AI fix loop]({BASE}/problems/ai-fix-loop/)

## Service packages
- [Customer growth]({BASE}/customer-growth/): Scoped package for search, paid campaigns, landing pages, CRM, and follow-up through to booking. Not a weekly marketing meeting.
- [Virtual bookkeeping]({BASE}/virtual-bookkeeping/): Async monthly close. Starter from $299/month (close only). Standard from $449/month (close plus light admin, capped at 3 hours a month; launch promo $399 on request). QuickBooks Online and Xero. Complements a CPA. Not a weekly meeting.
- [Catch-up bookkeeping]({BASE}/catch-up-bookkeeping/): Project to get books current, from $200 per month behind, quoted after the fit check. Simple books can be lower; complex books higher. Then optional monthly close.
- [Bookkeeping for founders]({BASE}/virtual-bookkeeping/for-founders/): Technical founders, SaaS, and product operators.
- [Bookkeeping for ecommerce]({BASE}/virtual-bookkeeping/for-ecommerce/): Payouts, fees, and sales-channel deposits. Sales tax stays with the CPA.
- [Bookkeeping fit check]({BASE}/virtual-bookkeeping/fit-check/): Intake for bookkeeping. Not the software diagnostic at /request/.

## Other services (inquire)
- [Product engineering]({BASE}/product-engineering/)
- [Security hardening]({BASE}/security-hardening/)
- [Fractional CTO]({BASE}/fractional-cto/)

## Full document
- [llms-full.txt]({BASE}/llms-full.txt)

## Positioning
Senior engineers who salvage AI-built apps into production-ready software. Audit in 48 hours. Fix security, auth, data, and payments first. Keep what works. Fixed scope. You own the code. Optional AI guardrails after rescue. Empathy, no shame.
""")
    write("llms-full.txt", f"""# Meridian — full AI/citation brief
Last updated: {LAST}
Contact: {CONTACT}
Canonical site: {BASE}/

## Entity
Meridian is a senior software studio (not "Vibe Code Rescue" as the company name). Vibe Code Rescue is the flagship service brand under Meridian, at {BASE}/vibe-code-rescue/.

Experience: 30+ years combined across video games, finance, and web development.

## One-paragraph summary
Meridian salvages AI-built applications into production-ready software. Founders and teams who shipped with Cursor, Lovable, Bolt, v0, Replit Agent, Claude Code, or Windsurf request a diagnostic; Meridian returns a written severity-ranked scorecard within about 48 hours, then offers fixed-scope rescue focused on secrets, auth, tenancy/RLS, and payments — keeping salvageable product surface rather than rewriting for ego. Clients own the code. Optional post-rescue AI guardrails are available. Tone: empathy, no shame.

## Pricing bands (USD, typical 2026)
- Diagnostic: free–$500 (often credited)
- Paid audit: $299–$2,500
- Focused rescue: $500–$12,500+
- Rebuild / production sprint: higher, quoted after diagnostic
- Not for: unlimited unscoped hourly, product-idea outsourcing, refusal to rotate secrets, same-day unscoped enterprise miracles

## Process
1. Intake (no secrets in forms)
2. 48h diagnostic — keep / harden / rebuild
3. Fixed-scope rescue quote
4. Harden and hand off (+ optional AI guardrails)

## Tools named on-site
Cursor, Lovable, Bolt, v0, Replit Agent, Claude Code, Windsurf

## FAQ answers (citeable)
Q: What is vibe code rescue?
A: A productized engineering service that takes apps built primarily with AI coding tools and makes them production-ready without a full rewrite — diagnostic first, then fixed-scope hardening of security, auth, data, and payments.

Q: How is rescue different from a rewrite?
A: Rescue keeps the product surface and salvageable code; rewrite is for when structure or risk makes salvage uneconomical. Meridian recommends with evidence from the diagnostic.

Q: How fast is the diagnostic?
A: About 48 hours after access and brief; larger monorepos may take longer with notice.

Q: Who owns the code?
A: The client. Work happens in their repo or a fork they control.

Q: Will you shame vibe coders?
A: No. Empathy, no shame.

Q: Does customer growth include a weekly marketing call?
A: No. It is a scoped package for search, paid campaigns, landing pages, CRM, and follow-up through to booking. Reporting is async. It is not a weekly account-management meeting, a caller roster, or a fractional CMO engagement.

Q: Does virtual bookkeeping include a weekly books call?
A: No. It is a monthly close package: receipt and invoice capture, categorisation, reconciliation, a written report, plus inbox triage, scheduling, and document handling. Questions are async. It is not a bookkeeper in your meetings, and it does not replace a CPA.

Q: How much does virtual bookkeeping cost?
A: Starter from $299 per month for the async monthly close only. Standard from $449 per month, which adds light admin capped at 3 hours a month. Launch promo $399 per month is available on request for Standard; $449 is the published price. Catch-up is quoted from $200 per month behind. Tax stays with the client's CPA.

## Virtual bookkeeping
Monthly close and a written report, without a standing meeting. Tools: QuickBooks Online and Xero. Bank feeds and an agreed portal or shared drive for documents. Exceptions flagged in writing.
- Monthly package: {BASE}/virtual-bookkeeping/
- Catch-up: {BASE}/catch-up-bookkeeping/
- For founders: {BASE}/virtual-bookkeeping/for-founders/
- For ecommerce: {BASE}/virtual-bookkeeping/for-ecommerce/
- Fit check (not the rescue diagnostic): {BASE}/virtual-bookkeeping/fit-check/
- Pricing: Starter from $299/month (close only); Standard from $449/month (close plus light admin, 3-hour cap); catch-up from $200 per month behind

## Sibling service packages
Customer growth: {BASE}/customer-growth/
Virtual bookkeeping: {BASE}/virtual-bookkeeping/

Both sit under the Meridian umbrella. They are scoped professional packages — growth, and books plus admin — delivered async or as a monthly close. They do not include a standing weekly meeting. Customer growth uses the inquire form at {BASE}/request/. Bookkeeping uses the fit check at {BASE}/virtual-bookkeeping/fit-check/ and does not use the rescue diagnostic.

## Key URLs
{BASE}/
{BASE}/vibe-code-rescue/
{BASE}/customer-growth/
{BASE}/virtual-bookkeeping/
{BASE}/virtual-bookkeeping/fit-check/
{BASE}/virtual-bookkeeping/for-founders/
{BASE}/virtual-bookkeeping/for-ecommerce/
{BASE}/catch-up-bookkeeping/
{BASE}/pricing/
{BASE}/request/
{BASE}/faq/
{BASE}/about/
{BASE}/guides/what-is-vibe-code-rescue/
{BASE}/guides/rescue-vs-rewrite/
{BASE}/artifacts/sample-audit.md
{BASE}/llms.txt
{BASE}/sitemap.xml
""")

def write_sample_audit():
    write("artifacts/sample-audit.md", f"""# Sample diagnostic (redacted)

**Service:** Meridian Vibe Code Rescue
**Date:** 27 September 2026
**Engagement ID:** SAMPLE-000
**Classification:** Illustrative — fictionalised findings; no real client data

---

## Executive summary

**Recommendation:** **Harden** (salvage), not full rewrite.

The product UI and primary workflow are salvageable. Blocking issues cluster in secrets handling, Supabase RLS, and Stripe webhook verification. Estimated fixed-scope rescue: **1.5–2.5 weeks** after approval (band aligned with focused rescue pricing).

---

## Severity legend

| Level | Meaning |
|-------|---------|
| P0 | Exploit or data-loss path; fix before traffic/diligence |
| P1 | Production correctness / money path |
| P2 | Maintainability / deploy reliability |
| P3 | Cleanup / nice-to-have |

---

## Findings (excerpt)

### P0 — Privileged API key referenced in client bundle
- **Evidence:** Key prefix pattern present in a client-shipped module (redacted).
- **Impact:** Anyone can extract and abuse the key.
- **Action:** Rotate immediately; move to server-only env; add secret scanning to CI.

### P0 — RLS disabled on `profiles` and `workspaces`
- **Evidence:** Policies absent / row level security not applied (redacted schema notes).
- **Impact:** Cross-tenant read/write of user data.
- **Action:** Enable RLS; policies keyed to verified auth UID; add cross-tenant denial tests.

### P1 — Stripe webhooks accept unsigned payloads
- **Evidence:** Handler trusts body without signature verification.
- **Impact:** Forged events can grant entitlements.
- **Action:** Verify signatures; reconcile subscription state server-side; remove client-trusted success flags.

### P1 — Authz checks only in React components
- **Evidence:** Sensitive routes gated by UI conditionals only.
- **Impact:** Direct API access bypasses UI.
- **Action:** Enforce authz on server/edge; treat UI checks as UX only.

### P2 — Production deploy fails on missing env
- **Evidence:** Preview host injects vars that production host does not.
- **Impact:** "Works in preview" false confidence.
- **Action:** Document required env; fail closed; smoke test post-deploy.

### P3 — Inconsistent folder patterns from agent sessions
- **Impact:** Onboarding and future AI edits drift.
- **Action:** Light structure pass after P0/P1; optional agent rule files.

---

## Keep / harden / rebuild

| Area | Decision |
|------|----------|
| Marketing + app shell UI | Keep |
| Core booking/workflow screens | Keep + harden validation |
| Supabase data layer | Harden (RLS + tenancy tests) |
| Stripe integration | Harden (rewrite webhook path) |
| Auth | Harden (server enforcement) |
| Full framework rewrite | Not recommended now |

---

## Proposed fixed scope (illustrative)

1. Secret rotation runbook + CI secret scan
2. RLS policies + two cross-tenant tests
3. Stripe webhook verification + entitlement reconcile
4. Server authz on sensitive routes
5. Deploy env checklist + smoke script
6. Optional: Cursor/Claude rule files to protect tenancy and secrets patterns

**Out of scope (example):** New feature development, mobile apps, SOC2 programme.

---

## Next step

Reply to approve scope or ask questions. Do **not** paste live secrets into email; share via your secret manager or a private channel after rotation.

— Meridian · {CONTACT}
""")


def remove_legacy_services_dir():
    """Drop the retired services directory. Offerings now live at the site root."""
    legacy = SITE / "services"
    if legacy.is_dir():
        shutil.rmtree(legacy)
        print("removed legacy services/")


def main():
    prepare_hashed_assets()
    page_home()
    page_vcr()
    for slug, name, blurb, text in STUBS:
        page_stub(slug, name, blurb, text)
    for offering in OFFERINGS:
        page_offering(offering)
    page_bookkeeping()
    page_catchup_bookkeeping()
    page_bookkeeping_founders()
    page_bookkeeping_ecommerce()
    page_bookkeeping_fit_check()
    page_pricing()
    page_request("request")
    page_request("diagnostic")
    for t in TOOLS:
        page_tool(*t)
    for pr in PROBLEMS:
        page_problem(*pr)
    page_faq()
    page_about()
    page_guide_what()
    page_guide_vs()
    write_robots()
    write_llms()
    write_sample_audit()
    urls = [
        "/",
        "/vibe-code-rescue/",
        "/product-engineering/",
        "/security-hardening/",
        "/fractional-cto/",
        "/customer-growth/",
        "/virtual-bookkeeping/",
        "/virtual-bookkeeping/fit-check/",
        "/virtual-bookkeeping/for-founders/",
        "/virtual-bookkeeping/for-ecommerce/",
        "/catch-up-bookkeeping/",
        "/pricing/",
        "/request/",
        "/diagnostic/",
        "/faq/",
        "/about/",
        "/guides/what-is-vibe-code-rescue/",
        "/guides/rescue-vs-rewrite/",
        "/artifacts/sample-audit.md",
        "/llms.txt",
        "/llms-full.txt",
    ]
    for slug, *_ in TOOLS:
        urls.append(f"/rescue/{slug}/")
    for slug, *_ in PROBLEMS:
        urls.append(f"/problems/{slug}/")
    write_sitemap(urls)
    remove_legacy_services_dir()
    print("DONE", len(urls), "urls")

if __name__ == "__main__":
    main()
