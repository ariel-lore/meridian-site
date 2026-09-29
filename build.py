#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import shutil

SITE = Path(__file__).resolve().parent
BASE = "https://meridian.dev"
LAST = "27 September 2026"
CONTACT = "hello@meridian.dev"
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

def header(path):
    p = depth(path)
    return f"""<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{p}">{BRAND}<span>Meridian</span></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">Menu</button>
    <nav class="nav" id="site-nav">
      <a href="{p}vibe-code-rescue/">Vibe Code Rescue</a>
      <a href="{p}pricing/">Pricing</a>
      <a href="{p}guides/what-is-vibe-code-rescue/">Guides</a>
      <a href="{p}faq/">FAQ</a>
      <a href="{p}about/">About</a>
      <a class="nav-cta" href="{p}request/">Request diagnostic</a>
    </nav>
  </div>
</header>
"""

def footer(path):
    p = depth(path)
    return f"""<footer class="site-footer">
  <div class="container footer-grid">
    <div>
      <div class="footer-brand">{BRAND}<span>Meridian</span></div>
      <p>Senior software studio. We salvage AI-built apps into production-ready software.</p>
      <p><a href="mailto:{CONTACT}">{CONTACT}</a></p>
    </div>
    <div>
      <h4>Services</h4>
      <ul>
        <li><a href="{p}vibe-code-rescue/">Vibe Code Rescue</a></li>
        <li><a href="{p}product-engineering/">Product engineering</a></li>
        <li><a href="{p}security-hardening/">Security hardening</a></li>
        <li><a href="{p}fractional-cto/">Fractional CTO</a></li>
      </ul>
    </div>
    <div>
      <h4>Rescue by tool</h4>
      <ul>
        <li><a href="{p}rescue/lovable/">Lovable</a></li>
        <li><a href="{p}rescue/bolt/">Bolt</a></li>
        <li><a href="{p}rescue/cursor/">Cursor</a></li>
        <li><a href="{p}rescue/v0/">v0</a></li>
        <li><a href="{p}rescue/replit/">Replit Agent</a></li>
        <li><a href="{p}rescue/claude-code/">Claude Code</a></li>
      </ul>
    </div>
    <div>
      <h4>Resources</h4>
      <ul>
        <li><a href="{p}pricing/">Pricing</a></li>
        <li><a href="{p}problems/secrets-exposed/">Common problems</a></li>
        <li><a href="{p}guides/rescue-vs-rewrite/">Rescue vs rewrite</a></li>
        <li><a href="{p}faq/">FAQ</a></li>
        <li><a href="{p}request/">Request diagnostic</a></li>
        <li><a href="{p}llms.txt">llms.txt</a></li>
      </ul>
    </div>
  </div>
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
  '"knowsAbout":["Vibe Code Rescue","AI-generated code","Software security","Product engineering","Fractional CTO"]}'
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
<div class="grid-2" style="margin-top:1.5rem">
<div class="card"><span class="pill pill-ok">Flagship</span><h3>Vibe Code Rescue</h3><p>Salvage AI-built apps (Cursor, Lovable, Bolt, v0, Replit Agent, Claude Code, Windsurf) into production-ready software. 48h diagnostic. Fixed scope.</p><a class="card-link" href="{p}vibe-code-rescue/">View service →</a></div>
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
<div class="btn-row">
<a class="btn btn-primary" href="{p}request/?interest={slug}">Inquire</a>
<a class="btn btn-secondary" href="mailto:{CONTACT}?subject={name}%20inquiry">Email {CONTACT}</a>
</div>
</div></section>
</main>
{footer(path)}
"""
    write(path + "index.html", head(path, title, blurb, "/" + path, extra) + body)

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
</div></section>
<section class="section"><div class="container" style="max-width:640px">
<div id="form-success" class="form-success" role="status">
<strong>Request captured.</strong> If your mail client opened, send the message to complete. Or we received it via Formspree. We will reply from {CONTACT}.
</div>
<div class="form-card">
<div class="form-warning"><strong>Do not paste secrets.</strong> No API keys, <code>.env</code> contents, private keys, access tokens, or passwords. Describe the problem; share the repo privately after we reply (NDA available).</div>
<form id="request-form" data-formspree="https://formspree.io/f/YOUR_FORM_ID" novalidate>
<input type="hidden" name="_subject" value="Meridian diagnostic request">
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
]

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
<p class="answer-first"><strong>Quick answer:</strong> Meridian Vibe Code Rescue salvages AI-built apps with a 48-hour diagnostic, security-first fixed-scope work, and clear ownership. Empathy, no shame. Pricing bands are public on the pricing page.</p>
<p class="meta-line">Last updated: {LAST}</p>
</div></section>
<section class="section"><div class="narrow">
{faq_html(SITE_FAQS)}
<p>Deep dive: <a href="{p}vibe-code-rescue/">service page</a> · <a href="{p}guides/what-is-vibe-code-rescue/">What is vibe code rescue?</a> · <a href="{p}request/">Request diagnostic</a></p>
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
<h2>Contact</h2>
<p>Email <a href="mailto:{CONTACT}">{CONTACT}</a> or use the <a href="{p}request/">diagnostic request form</a>.</p>
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
        f"  <url>\n    <loc>{BASE}{u}</loc>\n    <lastmod>2026-09-27</lastmod>\n    <changefreq>weekly</changefreq>\n  </url>"
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

## Key URLs
{BASE}/
{BASE}/vibe-code-rescue/
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
