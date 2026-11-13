#!/usr/bin/env python3
"""Builds the Good Life Lending static site into ../docs (served by GitHub Pages).

Run:  python3 src/build.py
Edit page content here or in src/*.html, then rebuild and commit docs/.
"""
import json, os, re, sys, shutil, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from city_copy import CITY_COPY

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(SRC), "docs")
DOMAIN = "https://goodlife-lending.com"

APPLY_URL = "https://portal.goodlife-lending.com/goodlifelending/application"
POF_URL = "https://portal.goodlife-lending.com/goodlifelending/proof-of-funds"
PORTAL_URL = "https://portal.goodlife-lending.com"
PHONE = "402-770-7950"
EMAIL = "josh@goodlife-lending.com"
LASTMOD = "2026-11-12"
import hashlib
CSS_VERSION = hashlib.md5(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "site.css"), "rb").read()).hexdigest()[:8]  # cache-buster  # bump when content changes

# ---------------------------------------------------------------------------
# Tracking: copied verbatim from GHL > GLL Basic Site > Settings > Tracking code
# ---------------------------------------------------------------------------
HEAD_TRACKING = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-235FJNCR9P"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-235FJNCR9P');
</script>

<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-KV8DJBX7');</script>
<!-- End Google Tag Manager -->
<meta name="google-site-verification" content="Uqiuovt0kWRSX8nOMvMJW5FwQ706-2cWfcC6vaF-BWc" />

<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '669608049332732');
fbq('track', 'PageView');
</script>"""

BODY_OPEN_TRACKING = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KV8DJBX7"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""

# GHL Settings > External Tracking: page views + attribution for a non-GHL site
BODY_CLOSE_TRACKING = """<script
src="https://link.msgsndr.com/js/external-tracking.js"
data-tracking-id="tk_0595e86fcd384fb7b19104d3b74e73a8">
</script>"""

# ---------------------------------------------------------------------------
# GHL embeds (standard inline embed codes). These submit straight into GHL, so
# the existing workflows keep firing exactly as before.
# ---------------------------------------------------------------------------
FORM_EMBED_JS = '<script src="https://link.msgsndr.com/js/form_embed.js"></script>'

# Survey "Get an Instant Quote" -> triggers "Landing Page Survey Automation(Google ads)"
SURVEY_EMBED = """<iframe src="https://api.leadconnectorhq.com/widget/survey/T2gbIv97b8rukjUzvRkV" class="ghl-embed" style="border:none;width:100%;" scrolling="no" id="T2gbIv97b8rukjUzvRkV" title="Get an Instant Quote"></iframe>"""

# Homepage: the survey sits far down the page, so inject it (and GHL's
# form_embed.js) only when the visitor scrolls near it. Don't use
# loading="lazy" on the iframe: form_embed.js parks it off-screen until it
# loads, so a lazy iframe never loads and the card stays blank.
DEFERRED_SURVEY = """<div class="survey-slot" data-survey style="min-height:520px;"></div>
<script>
(function () {
  var slot = document.querySelector('[data-survey]');
  function load() {
    if (slot.getAttribute('data-loaded')) return;
    slot.setAttribute('data-loaded', '1');
    slot.innerHTML = '""" + SURVEY_EMBED.replace("'", "\\'") + """';
    var s = document.createElement('script');
    s.src = 'https://link.msgsndr.com/js/form_embed.js';
    document.body.appendChild(s);
  }
  if (location.hash === '#contact') load();
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href$="#contact"]');
    if (a) load();
  });
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting) { load(); io.disconnect(); }
    }, { rootMargin: '1500px 0px' });
    io.observe(slot);
  } else { load(); }
})();
</script>"""

# Form "Loan Request" (used on /apply)
LOAN_FORM_EMBED = """<iframe
    src="https://api.leadconnectorhq.com/widget/form/XGMTCOitb0seEcEmT0dB"
    class="ghl-embed"
    style="width:100%;height:100%;border:none;border-radius:3px;min-height:1150px"
    id="inline-XGMTCOitb0seEcEmT0dB"
    data-layout="{'id':'INLINE'}"
    data-trigger-type="alwaysShow"
    data-trigger-value=""
    data-activation-type="alwaysActivated"
    data-activation-value=""
    data-deactivation-type="neverDeactivate"
    data-deactivation-value=""
    data-form-name="Loan Request"
    data-height="1150"
    data-layout-iframe-id="inline-XGMTCOitb0seEcEmT0dB"
    data-form-id="XGMTCOitb0seEcEmT0dB"
    title="Loan Request"></iframe>"""

# ---------------------------------------------------------------------------
# Shared layout
# ---------------------------------------------------------------------------
NAV = f"""  <nav aria-label="Main navigation">
    <div class="container nav-inner">
      <a href="/" class="nav-logo">
        <img src="/assets/img/logo-header.png" alt="Good Life Lending" width="315" height="120" />
      </a>
      <ul class="nav-links" role="list">
        <li><a href="/#why-gll">Why GLL</a></li>
        <li><a href="/#how-it-works">How It Works</a></li>
        <li><a href="/pre-qualify">Do You Qualify?</a></li>
        <li><a href="{PORTAL_URL}">Borrower/Investor Portal</a></li>
        <li><a href="{APPLY_URL}" class="btn btn-primary nav-cta">Apply Now</a></li>
      </ul>
      <a href="{APPLY_URL}" class="btn btn-primary nav-mobile-cta">Apply Now</a>
    </div>
  </nav>"""

FOOTER = f"""  <footer role="contentinfo">
    <div class="container">
      <div class="footer-grid">
        <div>
          <div class="footer-brand-name"><img src="/assets/img/logo-white.png" alt="Good Life Lending" width="315" height="120" loading="lazy" /></div>
          <p class="footer-tagline">
            Helping real estate entrepreneurs experience opportunity through fast, character-based private financing.
          </p>
          <div class="footer-social" aria-label="Social media links">
            <a href="https://www.instagram.com/good_life_lending" target="_blank" rel="noopener noreferrer" title="Instagram"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 4.7a5.1 5.1 0 1 0 0 10.2 5.1 5.1 0 0 0 0-10.2zm0 8.4a3.3 3.3 0 1 1 0-6.6 3.3 3.3 0 0 1 0 6.6zm5.3-9.8a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4z"/></svg><span class="sr-only">Instagram</span></a>
            <a href="https://www.facebook.com/goodlifelending" target="_blank" rel="noopener noreferrer" title="Facebook"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M13.5 21.9v-8.1h2.7l.4-3.2h-3.1V8.6c0-.9.3-1.5 1.6-1.5h1.7V4.2c-.3 0-1.3-.1-2.5-.1-2.4 0-4.1 1.5-4.1 4.2v2.3H7.5v3.2h2.7v8.1h3.3z"/></svg><span class="sr-only">Facebook</span></a>
            <a href="https://www.linkedin.com/company/goodlifelending" target="_blank" rel="noopener noreferrer" title="LinkedIn"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9.5h4v11H3v-11zm7 0h3.8v1.6h.1c.5-1 1.8-2 3.8-2 4 0 4.8 2.7 4.8 6.1v5.3h-4v-4.7c0-1.1 0-2.6-1.6-2.6s-1.8 1.2-1.8 2.5v4.8h-4v-11z"/></svg><span class="sr-only">LinkedIn</span></a>
          </div>
          <p class="footer-contact">
            <a href="tel:+14027707950">{PHONE}</a><br />
            <a href="mailto:{EMAIL}">{EMAIL}</a><br />
            PO Box 5206, Lincoln, NE 68505
          </p>
        </div>
        <div class="footer-col">
          <p class="footer-heading">Company</p>
          <ul>
            <li><a href="/#about">Our Story</a></li>
            <li><a href="/#values">Our Values</a></li>
            <li><a href="/#faq">FAQ</a></li>
            <li><a href="/#contact">Contact</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <p class="footer-heading">Borrowers</p>
          <ul>
            <li><a href="{APPLY_URL}">Apply Now</a></li>
            <li><a href="/#contact">Get an Instant Quote</a></li>
            <li><a href="/pre-qualify">Do You Qualify?</a></li>
            <li><a href="{POF_URL}">Proof of Funds Letter</a></li>
            <li><a href="{PORTAL_URL}">Borrower/Investor Portal</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <p class="footer-heading">Service Areas</p>
          <ul>
            <li><a href="/hard-money-lenders-nebraska">Nebraska</a></li>
            <li><a href="/omaha-hard-money-lenders">Omaha</a></li>
            <li><a href="/lincoln-hard-money-lenders">Lincoln</a></li>
            <li><a href="/grand-island-hard-money-lenders">Grand Island</a></li>
            <li><a href="/kearney-hard-money-lenders">Kearney</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p>© 2026 Good Life Lending. All rights reserved. &nbsp;·&nbsp; <span class="footer-legal"><a href="/privacy-policy">Privacy Policy</a> | <a href="/terms">Terms &amp; Conditions</a></span></p>
        <p>
          Good Life Lending is a private lender. Loans are subject to credit approval, cash requirements, and deal quality review. This website does not constitute a commitment to lend. Terms and conditions apply.
        </p>
      </div>
    </div>
  </footer>"""


def page(path, title, description, body, *, canonical=None, extra_head="", ld=None,
         embeds=False, noindex=False, og_title=None, og_description=None):
    canonical = canonical if canonical is not None else f"{DOMAIN}/{path}".rstrip("/")
    if path == "":
        canonical = f"{DOMAIN}/"
    ld_block = ""
    for item in (ld if isinstance(ld, list) else [ld] if ld is not None else []):
        ld_txt = item if isinstance(item, str) else json.dumps(item, indent=2, ensure_ascii=False)
        ld_block += f'  <script type="application/ld+json">\n{ld_txt}\n  </script>\n'
    og = ""
    if not noindex:
        ot = H.escape(og_title or title); od = H.escape(og_description or description)
        og = f"""  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Good Life Lending" />
  <meta property="og:locale" content="en_US" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:title" content="{ot}" />
  <meta property="og:description" content="{od}" />
  <meta property="og:image" content="{DOMAIN}/assets/img/og-image.jpg" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{ot}" />
  <meta name="twitter:description" content="{od}" />
  <meta name="twitter:image" content="{DOMAIN}/assets/img/og-image.jpg" />
"""
    robots = '  <meta name="robots" content="noindex" />\n' if noindex else ""
    desc = f'  <meta name="description" content="{H.escape(description)}" />\n' if description else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{H.escape(title)}</title>
{desc}{robots}  <link rel="canonical" href="{canonical}" />
  <link rel="icon" type="image/png" href="/assets/img/favicon.png" />
  <link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png" />
{og}{extra_head}{ld_block}
{HEAD_TRACKING}

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/assets/site.css?v={CSS_VERSION}" />
</head>

<body>
{BODY_OPEN_TRACKING}

{NAV}

{body}

{FOOTER}

{FORM_EMBED_JS if embeds else ''}
{BODY_CLOSE_TRACKING}
</body>
</html>
"""


def write(name, content):
    p = os.path.join(OUT, name)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)


def redirect(name, target):
    """GitHub Pages can't send 301s; this is an instant meta/JS redirect that
    keeps query strings (UTMs, gclid, fbclid)."""
    write(name, f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8" />
<title>Redirecting…</title>
<link rel="canonical" href="{DOMAIN}{target}" />
<meta name="robots" content="noindex" />
<meta http-equiv="refresh" content="0; url={target}" />
<script>location.replace("{target}" + location.search + location.hash);</script>
</head><body><p>This page has moved to <a href="{target}">{DOMAIN}{target}</a>.</p></body></html>
""")


def read(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def lending_map_section():
    """Nebraska map of towns we've funded loans in (town-level only, never addresses)."""
    import math
    geo = json.loads(read("nebraska_paths.json"))
    data = json.loads(read("lending_map.json"))
    towns = sorted(data["towns"], key=lambda t: t["loans"])  # big dots drawn last
    total = sum(t["loans"] for t in towns)
    def xy(t):
        return ((t["lon"] - geo["lon0"]) * geo["cos"] * geo["k"], (geo["lat0"] - t["lat"]) * geo["k"])
    dots, labels = [], []
    for t in towns:
        x, y = xy(t); r = 4 + 2.6 * math.sqrt(t["loans"])
        n = f'{t["loans"]} loan' + ("" if t["loans"] == 1 else "s")
        dots.append(f'<circle class="ne-dot" cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"><title>{H.escape(t["name"])}: {n}</title></circle>')
        if t.get("label"):
            left = t.get("label_left")
            lx = x - r - 6 if left else x + r + 6
            labels.append(f'<text class="ne-label" x="{lx:.1f}" y="{y + 6:.1f}" text-anchor="{"end" if left else "start"}">{H.escape(t["name"])}</text>')
    svg = (f'<svg class="ne-map" viewBox="{geo["viewBox"]}" role="img" aria-labelledby="ne-map-title" preserveAspectRatio="xMidYMid meet">'
           f'<title id="ne-map-title">Map of Nebraska showing the {len(towns)} communities where Good Life Lending has funded loans</title>'
           f'<path class="ne-counties" d="{geo["counties"]}"/><path class="ne-state" d="{geo["state"]}"/>'
           + "".join(dots) + "".join(labels) + '</svg>')
    town_list = " · ".join(H.escape(t["name"]) for t in sorted(data["towns"], key=lambda t: (-t["loans"], t["name"])))
    loans_display = f"{(total // 10) * 10}+" if total >= 20 else str(total)
    return f"""    <!-- LENDING MAP -->
    <section id="areas" aria-labelledby="areas-heading">
      <div class="container">
        <p class="section-eyebrow center">Where We Lend</p>
        <h2 id="areas-heading" class="section-title center">Hard Money Loans Across Nebraska</h2>
        <p class="section-lead center" style="margin-left:auto;margin-right:auto;">Good Life Lending is a direct private lender based in Lincoln. Every dot below is a Nebraska town where we've funded a fix-and-flip, bridge or rental loan. The bigger the dot, the more deals we've done there.</p>
        <div class="map-stats">
          <div><strong>{loans_display}</strong><span>Loans funded</span></div>
          <div><strong>{len(towns)}</strong><span>Nebraska communities</span></div>
          <div><strong>Omaha to Gering</strong><span>Statewide reach</span></div>
        </div>
        <div class="map-card">
          {svg}
          <p class="map-towns"><strong>Communities we've funded in:</strong> {town_list}</p>
          <p class="map-note">Funded loans from our records, updated {H.escape(data["updated"])}. Towns only, never borrower addresses.</p>
        </div>
        <ul class="areas map-links">
          <li><a href="/hard-money-lenders-nebraska">Nebraska Hard Money Loans</a></li>
          <li><a href="/omaha-hard-money-lenders">Omaha Hard Money Lenders</a></li>
          <li><a href="/lincoln-hard-money-lenders">Lincoln Hard Money Lenders</a></li>
          <li><a href="/grand-island-hard-money-lenders">Grand Island Hard Money Lenders</a></li>
          <li><a href="/kearney-hard-money-lenders">Kearney Hard Money Lenders</a></li>
        </ul>
      </div>
    </section>
"""


def build_home():
    body = read("home.html")
    body = (body.replace("{{APPLY_URL}}", APPLY_URL)
                .replace("{{POF_URL}}", POF_URL)
                .replace("{{SURVEY_EMBED}}", DEFERRED_SURVEY)
                .replace("{{LENDING_MAP}}", lending_map_section()))
    schema = json.loads(read("home-schema.json"))
    faqs = re.findall(r'<details class="faq-item"><summary><h3>(.*?)</h3></summary><p>(.*?)</p></details>', body, re.S)
    for node in schema["@graph"]:
        if node["@type"] == "FinancialService":
            node["image"] = f"{DOMAIN}/assets/img/og-image.jpg"
            node["areaServed"] = [{"@type": "State", "name": "Nebraska"}] + [
                {"@type": "City", "name": f"{c}, NE"} for c in
                ["Omaha", "Lincoln", "Bellevue", "Grand Island", "Kearney", "Fremont", "Hastings", "Norfolk"]]
        if node["@type"] == "FAQPage":  # must match the FAQs visitors actually see
            node["mainEntity"] = [{"@type": "Question", "name": H.unescape(q.strip()),
                                   "acceptedAnswer": {"@type": "Answer", "text": H.unescape(" ".join(a.split()))}}
                                  for q, a in faqs]
    write("index.html", page(
        "", "Nebraska Hard Money Lender & Fix and Flip Loans | Good Life Lending",
        "Direct Nebraska hard money lender. Fix-and-flip, bridge and rental loans in Omaha, Lincoln and statewide, funded in as little as 5 days.",
        body, ld=schema, embeds=False,
        og_title="Good Life Lending | Hard Money Loans That Close in as Little as 5 Days",
        og_description="Fast, character-based hard money lending for Nebraska real estate investors. We've been on the borrower side, and we know how to say yes to the right deals."))


REVIEWS = [
    ("Awesome to work with", "My wife and I have worked with Josh on several projects over the past 5 years. He and the team at Good Life Lending have been great to work with. Always willing to meet our scheduled closing timeline even if it has been short notice. Photo is just one of the more recent houses Josh helped us with. Definitely would recommend Good Life Lending for any real estate transaction!", "Ryan Omel - Google Review"),
    ("Extremely knowledgeable and experienced", "Josh and his team at Good Life Lending have been great to work with. It has been amazing watching the real estate projects evolve and grow over the years. Josh is extremely knowledgeable and experienced about the market, ranging from residential to commercial investments.Look forward in making future investments.", "Christie Lebsack - Google Review"),
    ("Great insight on the market", "Josh at Good Life Lending has been awesome to work with. Experience investor with great insight on the market. I look forward to furthering the relationship with Josh and his team. My vision is to create affordable housing for the Omaha metro and to have a lending partner that understands that goal is mutually beneficial.", "Clemson Nwinye - Google Review"),
]

AREAS = [("Omaha", "/omaha-hard-money-lenders"), ("Lincoln", "/lincoln-hard-money-lenders"), ("Bellevue", None),
         ("Grand Island", "/grand-island-hard-money-lenders"), ("Kearney", "/kearney-hard-money-lenders"),
         ("Fremont", None), ("Hastings", None), ("Norfolk", None), ("All surrounding areas", None)]


def market_page(slug, place, seo):
    cc = CITY_COPY[slug]
    e = H.escape
    local_paras = "\n".join(f'          <p style="color:var(--muted);margin-bottom:16px;">{e(t)}</p>' for t in cc["paragraphs"])
    local_areas = "\n".join(f"            <li>{e(a)}</li>" for a in cc["areas"])
    local_fits = "\n".join(f"            <li>{e(f)}</li>" for f in cc["fits"])
    local_faqs = "\n".join(f'          <details class="faq-item"><summary><h3>{e(q)}</h3></summary><p>{e(a)}</p></details>' for q, a in cc["faqs"])
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in cc["faqs"]]}
    """Content ported from the GHL market pages (same copy; city name swapped)."""
    reviews = "\n".join(
        f'          <article class="review-card"><h3>"{t}"</h3><p>{H.escape(b)}</p><p class="who">{w}</p></article>'
        for t, b, w in REVIEWS)
    areas = "\n".join(
        f'          <li><a href="{u}">{n}</a></li>' if u else f"          <li>{n}</li>" for n, u in AREAS)
    body = f"""  <header class="page-hero">
    <div class="container">
      <p class="hero-eyebrow">Fix and Flip Loan Experts</p>
      <h1>Hard Money Lenders {"Nebraska" if place == "Nebraska" else place}</h1>
      <p>{e(cc["intro"])}</p>
    </div>
  </header>

  <main>
    <section id="quote">
      <div class="container split">
        <div>
          <p class="section-eyebrow">Fast, Flexible, and Investor-Friendly Funding from Good Life Lending</p>
          <h2 class="section-title">Your Trusted Hard Money Lender in {place}</h2>
          <p class="section-lead" style="margin-bottom:20px;">Good Life Lending is committed to helping real estate investors succeed. We offer reliable hard money loans throughout {place}, providing the flexibility traditional banks don't offer.</p>
          <p class="section-lead" style="margin-bottom:20px;">Josh has been investing in real estate since 2008, so we understand the urgency behind a good deal, and we’re here to help you act quickly.</p>
          <p class="section-lead" style="margin-bottom:20px;">Whether you're targeting Omaha, Lincoln, Grand Island, or any surrounding Nebraska markets, we fund deals fast, with a simple approval process and no unnecessary hurdles.</p>
          <p><strong>Or call us: <a href="tel:+14027707950">(402) 770-7950</a></strong></p>
        </div>
        <div class="card">
          {SURVEY_EMBED}
        </div>
      </div>
    </section>

    <section id="local" style="background:var(--bg-light);">
      <div class="container split">
        <div>
          <p class="section-eyebrow">Local Market</p>
          <h2 class="section-title">{e(cc["heading"])}</h2>
{local_paras}
        </div>
        <div class="card">
          <h3 style="margin-bottom:12px;">{e(cc["areas_heading"])}</h3>
          <ul class="areas">
{local_areas}
          </ul>
          <h3 style="margin:20px 0 4px;">Deals that tend to fit</h3>
          <ul class="checklist">
{local_fits}
          </ul>
        </div>
      </div>
    </section>

    <section>
      <div class="container">
        <p class="section-eyebrow">Reviews</p>
        <h2 class="section-title">What Investors Say</h2>
        <div class="review-grid">
{reviews}
        </div>
      </div>
    </section>

    <section style="background:var(--bg-light);">
      <div class="container split">
        <div>
          <h2 class="section-title">Why Investors Choose Good Life Lending</h2>
          <ul class="checklist">
            <li>Fast approvals &amp; fast closings</li>
            <li>Straight answers about your deal, no runaround</li>
            <li>A simple, 100% digital process</li>
            <li>Flexible underwriting that focuses on the property and your strategy</li>
            <li>Local expertise in {place} real estate markets</li>
            <li>Direct private lenders: no brokers, no delays</li>
          </ul>
          <p class="section-lead" style="margin-bottom:0;"><strong>When you need a {place} hard money lender who can deliver, Good Life Lending is the partner you can count on.</strong></p>
          <a href="#quote" class="btn btn-gold mt-24">Get An Instant Quote</a>
        </div>
        <div class="card">
          <h3 style="margin-bottom:12px;">Proof of Funds</h3>
          <p style="color:var(--muted);margin-bottom:20px;">We can provide a proof of funds letter so you are able to make cash offers and stay ahead of the competition. Click the button to request your POF letter now.</p>
          <a href="{POF_URL}" class="btn btn-primary">Proof of Funds</a>
        </div>
      </div>
    </section>

    <section>
      <div class="container split">
        <div>
          <p class="section-eyebrow">Funding for Your Next Investment Property</p>
          <h2 class="section-title">Fix &amp; Flip Loans {place}</h2>
          <p class="section-lead" style="margin-bottom:12px;">Good Life Lending specializes in providing Fix &amp; Flip Loans in {place} designed for both new and seasoned investors.</p>
          <p><strong>Our loans offer:</strong></p>
          <ul class="checklist">
            <li>Financing for acquisition + renovation</li>
            <li>Character-based underwriting that looks at you and the deal</li>
            <li>Quick draws for renovation</li>
            <li>Support from a team that understands the {place} investment landscape</li>
          </ul>
          <p style="color:var(--muted);">Whether you’re flipping a home in Omaha, updating a rental in Lincoln, or renovating a distressed property anywhere in the state, we fund projects of all sizes.</p>
        </div>
        <div>
          <h2 class="section-title">What We Look For in Every {place} Deal</h2>
          <p style="color:var(--muted);">Every deal is different, so we don't publish one-size-fits-all terms. Here's what we look at instead:</p>
          <ul class="checklist">
            <li>Decent credit</li>
            <li>Real cash in the deal</li>
            <li>A solid property with numbers that make sense</li>
            <li>Your rehab plan and budget</li>
            <li>Your experience, or your plan if this is your first flip</li>
          </ul>
          <p style="color:var(--muted);">Tell us about your deal and we'll give you a straight answer, and clear terms, quickly.</p>
        </div>
      </div>
    </section>

    <section style="background:var(--bg-light);">
      <div class="container">
        <h2 class="section-title">Simple &amp; Streamlined Loan Process</h2>
        <p class="section-lead" style="margin-bottom:12px;">Real estate opportunities move fast, and so do we. Our {place} hard money loan process is quick, investor-friendly, and designed to help you close without delays.</p>
        <ol class="steps-list">
          <li>Submit your property &amp; project details</li>
          <li>Get a quick quote</li>
          <li>Complete a quick underwriting review</li>
          <li>Sign final documents</li>
          <li>Get funded fast, often in under a week</li>
        </ol>
        <p><strong>Ready to get started?</strong> No complicated approvals. No endless paperwork. Just the capital you need, when you need it.</p>
        <a href="#quote" class="btn btn-gold mt-24">Get an Instant Quote Today</a>
      </div>
    </section>

    <section>
      <div class="container">
        <h2 class="section-title">Recently Closed Deals</h2>
        <div class="deal-grid">
          <article class="deal-card"><img src="/assets/img/deal-brrrr.jpg" width="843" height="524" alt="Rental property funded by Good Life Lending" loading="lazy" /><p>We don't only fund fix and flips. We also help people acquire rentals. This borrower is going to BRRR this property, ideal leaving no cash into the deal.</p></article>
          <article class="deal-card"><img src="/assets/img/deal-facelift.jpg" width="750" height="1000" alt="Vacant house being renovated with Good Life Lending financing" loading="lazy" /><p>This poor house was a vacant, outdated disaster. But this borrower's a design whiz and is going to give it a serious facelift, dragging it out of the dark ages and into the present.</p></article>
          <article class="deal-card"><img src="/assets/img/deal-lincoln-ranch.jpg" width="514" height="540" alt="Ranch home in northeast Lincoln funded by Good Life Lending" loading="lazy" /><p>Just funded this NE Lincoln ranch! Our borrower used our private funds to close fast, and now they’re gearing up to refinance and turn it into a long-term rental. Smart move!</p></article>
        </div>
      </div>
    </section>

    <section style="background:var(--bg-light);">
      <div class="container split">
        <div>
          <h2 class="section-title">What Makes Good Life Lending Different?</h2>
          <p style="color:var(--muted);">As a direct lender, Good Life Lending has complete control over the loan process. That means faster approvals, flexible underwriting, and a team dedicated solely to investor success.</p>
          <p class="mt-24"><strong>Benefits of Working With Good Life Lending</strong></p>
          <ul class="checklist">
            <li>A Nebraska-based, direct hard money lender</li>
            <li>Quick and responsive communication</li>
            <li>Loans built specifically for fix &amp; flip investors</li>
            <li>Local market insights</li>
            <li>Dedicated support from application to final sale</li>
          </ul>
          <p style="color:var(--muted);">We’re not just lenders. We’re long-term partners in your investment journey.</p>
        </div>
        <div>
          <h2 class="section-title">Areas We Serve in Nebraska</h2>
          <p style="color:var(--muted);">We lend throughout the entire state, including:</p>
          <ul class="areas">
{areas}
          </ul>
          <p style="color:var(--muted);">If you’re investing in {place} real estate, we’re prepared to help you fund your next project.</p>
        </div>
      </div>
    </section>

    <section id="faq">
      <div class="container">
        <p class="section-eyebrow">Common Questions</p>
        <h2 class="section-title">{place} Hard Money Loan FAQs</h2>
        <div class="faq-list">
{local_faqs}
        </div>
      </div>
    </section>

    <section id="cta">
      <div class="container">
        <h2>Apply for a {place} Hard Money Loan Today</h2>
        <p>Ready to secure fast funding for your next fix &amp; flip project? Good Life Lending makes it easy to get approved and get funded quickly. Get started today and we’ll follow up within one business day.</p>
        <div class="cta-group">
          <a href="#quote" class="btn btn-gold">Get Quote Now</a>
          <a href="{APPLY_URL}" class="btn btn-outline" style="color:#fff;border-color:rgba(255,255,255,0.4);">Apply for Your {place} Hard Money Loan</a>
        </div>
      </div>
    </section>

    <section>
      <div class="container founder">
        <img src="/assets/img/josh-nix.jpg" width="1000" height="1000" alt="Josh Nix, founder of Good Life Lending" loading="lazy" />
        <div>
          <p class="section-eyebrow">Here to Help</p>
          <h2 class="section-title">Josh Nix - Founder</h2>
          <p style="color:var(--muted);margin-bottom:16px;">At GoodLife Lending, we know real estate investing moves fast, and so do we. Whether you’re flipping, building, or scaling your portfolio, our team is here to make sure funding isn’t the holdup. With local roots, common-sense underwriting, and a commitment to quick answers, we’re here to help you get deals done and grow your business with confidence.</p>
          <p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a><br /><strong>Address:</strong> PO Box 5206 Lincoln, NE 68505<br /><strong>Phone:</strong> <a href="tel:+14027707950">{PHONE}</a></p>
          <a href="{APPLY_URL}" class="btn btn-primary mt-24">Apply Now</a>
        </div>
      </div>
    </section>
  </main>"""
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{DOMAIN}/"},
        {"@type": "ListItem", "position": 2, "name": f"Hard Money Lenders {place}", "item": f"{DOMAIN}/{slug}"}]}
    ld = seo["ld"]
    if ld is None:  # the GHL Nebraska page had no schema; reuse the city schema scoped to Nebraska
        txt = json.dumps(json.loads(read("seo.json"))["omaha-hard-money-lenders"]["ld"], ensure_ascii=False)
        for old, new in [("omaha-hard-money-lenders", slug), ("Hard Money Lenders Omaha, NE", "Hard Money Lenders Nebraska"),
                         ("Hard Money Lenders Omaha", "Hard Money Lenders Nebraska"),
                         ("in Omaha", "in Nebraska"), ("the Omaha investment", "the Nebraska investment"),
                         ('"areaServed": "Omaha, NE"', '"areaServed": "Nebraska"'), ("across Omaha and Nebraska", "across Nebraska")]:
            txt = txt.replace(old, new)
        ld = json.loads(txt)
    write(f"{slug}.html", page(slug, seo["title"], seo["description"], body, ld=[ld, crumbs, faq_ld], embeds=True))


def simple_page(slug, title, description, h1, inner, *, eyebrow="", embeds=False, noindex=False):
    eb = f'<p class="hero-eyebrow">{eyebrow}</p>' if eyebrow else ""
    body = f"""  <header class="page-hero">
    <div class="container">
      {eb}
      <h1>{h1}</h1>
    </div>
  </header>
  <main>
    <section>
      <div class="container">
{inner}
      </div>
    </section>
  </main>"""
    write(f"{slug}.html", page(slug, title, description, body, embeds=embeds, noindex=noindex))


def build_pages():
    seo = json.loads(read("seo.json"))
    market_page("hard-money-lenders-nebraska", "Nebraska", seo["hard-money-lenders-nebraska"])
    for slug, city in [("omaha-hard-money-lenders", "Omaha"), ("lincoln-hard-money-lenders", "Lincoln"),
                       ("grand-island-hard-money-lenders", "Grand Island"), ("kearney-hard-money-lenders", "Kearney")]:
        market_page(slug, city, seo[slug])

    # /thank-you: the Instant Quote survey redirects here (hard-coded in GHL)
    simple_page("thank-you", "Thank You", "", "Thank You", f"""        <div class="prose">
          <p>Thank you for submitting your information for a hard money loan quote.</p>
          <p>One of our team representatives will be in contact with you soon.</p>
          <p class="mt-24"><a href="{APPLY_URL}" class="btn btn-gold">Start Your Full Application</a> &nbsp; <a href="/" class="btn btn-outline">Back to Home</a></p>
        </div>""", noindex=True)

    # /apply: GHL "Loan Request" form (the Borrower Scorecard links here)
    simple_page("apply", "Apply for a Hard Money Loan | Good Life Lending", "Request a fix-and-flip or hard money loan from Good Life Lending. Share the property, purchase price, loan amount and closing date.", "Apply Now",
                f"""        <div class="card" style="max-width:760px;margin:0 auto;">
          {LOAN_FORM_EMBED}
        </div>""", embeds=True)

    # /pre-qualify: Borrower Scorecard, verbatim from the GHL custom code element
    simple_page("pre-qualify", "Do You Qualify for a Hard Money Loan? | Good Life Lending",
                "Take the 60-second Good Life Lending Borrower Scorecard and see how you stack up.",
                "Do You Qualify?", read("scorecard.html").replace('<meta charset="UTF-8">\n', ""), eyebrow="60-Second Check")

    simple_page("privacy-policy", "Privacy Policy | Good Life Lending", "How Good Life Lending collects, uses and protects your information, including text message privacy and how to opt out.", "Privacy Policy", PRIVACY)
    simple_page("terms", "Terms & Conditions | Good Life Lending", "Terms and conditions for using the Good Life Lending website and applying for a hard money or fix-and-flip loan.", "Terms &amp; Conditions", TERMS)
    simple_page("eula", "End-User License Agreement | Good Life Lending", seo["eula"]["description"], "End-User License Agreement", EULA)

    # Old GHL URLs -> new homes
    redirect("home.html", "/")
    redirect("blog.html", "/hard-money-lenders-nebraska")
    redirect("watch-party.html", "/")
    redirect("watch_party_110626.html", "/")
    redirect("thanks.html", "/")
    redirect("kearny-hard-money-lenders.html", "/kearney-hard-money-lenders")
    redirect("real-estate-generic-005-12w.html", "/")
    redirect("real-estate-generic-005-12w/index.html", "/")

    write("404.html", page("404", "Page Not Found | Good Life Lending", "", """  <script>
    // Old GHL path prefix: /real-estate-generic-005-12w/<page> -> /<page>
    (function(){var p=location.pathname, pre='/real-estate-generic-005-12w/';
      if(p.indexOf(pre)===0){location.replace('/'+p.slice(pre.length)+location.search+location.hash);}
      else if(p.length>1 && p.slice(-1)==='/'){location.replace(p.slice(0,-1)+location.search+location.hash);}
    })();
  </script>
  <header class="page-hero"><div class="container"><h1>Page not found</h1><p>That page has moved or no longer exists.</p></div></header>
  <main><section><div class="container"><a href="/" class="btn btn-primary">Go to the homepage</a> &nbsp; <a href="/#contact" class="btn btn-outline">Get an Instant Quote</a></div></section></main>""",
        canonical=f"{DOMAIN}/", noindex=True))

    urls = ["", "hard-money-lenders-nebraska", "omaha-hard-money-lenders", "lincoln-hard-money-lenders",
            "grand-island-hard-money-lenders", "kearney-hard-money-lenders", "pre-qualify", "apply",
            "privacy-policy", "terms", "eula"]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "".join(f"  <url><loc>{DOMAIN}/{u}</loc><lastmod>{LASTMOD}</lastmod></url>\n" for u in urls) + "</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    write("CNAME", "goodlife-lending.com\n")
    write(".nojekyll", "")


# ---------------------------------------------------------------------------
# Legal copy: verbatim from the live GHL pages (do not edit casually: the SMS
# consent language on the forms points to these for A2P/10DLC compliance)
# ---------------------------------------------------------------------------
PRIVACY = f"""        <div class="prose">
          <p class="meta">Effective Date: 07/01/2025</p>
          <p>At GoodLife Lending, your privacy is important to us. This Privacy Policy outlines how we collect, use, and protect your information when you interact with our website, services, and communications.</p>
          <h2>1. Information We Collect</h2>
          <p>We may collect the following types of information:</p>
          <ul>
            <li>Personal Information: Name, email address, phone number, and physical address when you contact us, schedule a service, or sign up for offers.</li>
            <li>Mobile Information: If you opt-in to receive text messages, we may collect your mobile number.</li>
            <li>Website Usage Data: Information about how you use our website, such as pages viewed and time spent.</li>
          </ul>
          <h2>2. How We Use Your Information</h2>
          <p>We use the collected information to:</p>
          <ul>
            <li>Respond to inquiries or service requests.</li>
            <li>Communicate with you about appointments, promotions, and important updates.</li>
            <li>Improve our website and services.</li>
          </ul>
          <h2>3. Text Messaging Privacy</h2>
          <p>We respect your privacy when it comes to mobile communications.</p>
          <p>No mobile information will be shared with third parties/affiliates for marketing/promotional purposes.</p>
          <p>This includes your text messaging originator opt-in data and consent; this information will not be shared with any third parties.</p>
          <p>Message and data rates may apply. Frequency of messages may vary. You may opt out at any time by replying “STOP.”</p>
          <h2>4. Sharing Your Information</h2>
          <p>We do not sell, rent, or trade your personal information with third parties for marketing purposes. We may share your information only in the following situations:</p>
          <ul>
            <li>To comply with legal obligations.</li>
            <li>With service providers who assist us in operating our website or conducting our business, under strict confidentiality agreements.</li>
          </ul>
          <h2>5. Data Security</h2>
          <p>We implement appropriate technical and organizational measures to protect your personal data against unauthorized access, disclosure, alteration, or destruction.</p>
          <h2>6. Your Rights and Choices</h2>
          <p>You may:</p>
          <ul>
            <li>Request a copy of your personal information.</li>
            <li>Request corrections or deletions.</li>
            <li>Opt-out of marketing communications at any time.</li>
          </ul>
          <h2>7. Updates to This Policy</h2>
          <p>We may update this policy periodically. When we do, we will revise the “Effective Date” at the top. Continued use of our services indicates acceptance of the updated policy.</p>
          <h2>8. Contact Us</h2>
          <p>If you have any questions or concerns about this Privacy Policy, please contact us at:</p>
          <p>Email: <a href="mailto:{EMAIL}">{EMAIL}</a><br />Phone: {PHONE}</p>
        </div>"""

TERMS = """        <div class="prose">
          <p class="meta">Effective Date: September 8, 2025</p>
          <h2>1. Introduction</h2>
          <p>Welcome to Good Life Lending (“we,” “us,” or “our”). By accessing or using our website at <a href="https://goodlife-lending.com">goodlife-lending.com</a> (“Site”), you agree to be bound by these Terms &amp; Conditions (“Terms”). We offer financing solutions, especially designed for fix-and-flip real estate investors, with quick decisions and simple paperwork.</p>
          <h2>2. Eligibility</h2>
          <p>Use of the Site is restricted to individuals or business entities that are legally capable of entering into contracts. You affirm that you are at least 18 years old (or the applicable age in your jurisdiction) and meet any other eligibility criteria we may set.</p>
          <h2>3. Use of the Site</h2>
          <p>You agree to use the Site for lawful purposes only and not for any fraudulent, malicious, or infringing activities.</p>
          <p>You promise not to interrupt or tamper with the Site’s operations or bypass its security systems.</p>
          <p>You’re responsible for maintaining the security of your login credentials (if any) and notifying us of any unauthorized use.</p>
          <h2>4. Loan Applications &amp; Financing Terms</h2>
          <p>Loan decisions and terms (such as interest rates, repayment schedule, fees) are determined case-by-case and at our sole discretion.</p>
          <p>While we strive to keep things fast and simple with minimal bureaucracy, all final loan agreements must be signed and are legally binding.</p>
          <p>For transparency and fairness, our financing complies with applicable consumer protection laws like the Truth in Lending Act (TILA), which mandates clear disclosure of credit terms, APR, and borrower rights, including, where applicable, the right to rescind certain loans within three business days.</p>
          <p>We do not engage in predatory lending practices. Fees and pricing are justified by risk-based evaluation, and we do not mislead or exploit borrowers.</p>
          <h2>5. Disclosures &amp; Reserve Rights</h2>
          <p>We retain the right to change loan application protocols, documentation requirements, underwriting criteria, or interest rates at our discretion. Check back, just like you’d inspect a job site, before applying.</p>
          <p>You shall receive any required disclosures at or before the time of application or loan consummation.</p>
          <h2>6. Intellectual Property</h2>
          <p>All content on the Site (text, graphics, logos, images, software) is owned by or licensed to Good Life Lending and protected under U.S. and international intellectual property laws.</p>
          <p>You may not reproduce, distribute, or create derivative works without our express permission.</p>
          <h2>7. Limitation of Liability</h2>
          <p>Our Site and services are provided “as is.” We disclaim all warranties, whether express or implied, related to functionality, accuracy, or uptime. If your site times out, you'll still have to come back (no warranties there either).</p>
          <p>To the fullest extent permitted by law, in no event will we be liable for any direct, indirect, incidental, punitive, or consequential damages arising out of or in connection with your use of the Site or your borrowing decisions.</p>
          <h2>8. Indemnification</h2>
          <p>You agree to indemnify, defend, and hold harmless Good Life Lending and its affiliates, officers, and employees from any claims, damages, liabilities, or expenses (including legal costs) arising from your violation of these Terms or your misuse of the Site.</p>
          <h2>9. Modifications</h2>
          <p>We may revise or update these Terms at any time, and such changes are effective immediately upon posting. Continued use of the Site after changes constitutes your acceptance, so check in now and then, right alongside your tool belt.</p>
          <h2>10. Governing Law &amp; Jurisdiction</h2>
          <p>These Terms are governed by Nebraska law, without respect to conflict of laws principles. Any legal disputes will be resolved in the state or federal courts located in Nebraska, preferably in Lincoln, where craftsmanship and lending align.</p>
          <h2>11. Miscellaneous</h2>
          <p>Severability: If a provision is deemed invalid, the remaining provisions remain in full force.</p>
          <p>Waiver: No waiver of any breach of these Terms shall be deemed a waiver of any subsequent breach.</p>
          <p>Assignment: You may not transfer your rights under these Terms without our written consent. We may freely assign or transfer these Terms or our rights hereunder.</p>
        </div>"""

EULA = """        <div class="prose">
          <p class="meta">Last Updated: March 31, 2026</p>
          <p>This End-User License Agreement ("Agreement") is a legal agreement between you and the owner of this application ("Company," "we," or "us") for the use of the KPI Dashboard application ("Application").</p>
          <h2>1. License Grant</h2>
          <p>We grant you a limited, non-exclusive, non-transferable license to use the Application for your internal business purposes, subject to the terms of this Agreement.</p>
          <h2>2. QuickBooks Integration</h2>
          <p>This Application integrates with QuickBooks Online using Intuit's API. By using this Application, you authorize us to access your QuickBooks data as necessary to provide the Application's functionality. Your use of QuickBooks is also subject to Intuit's terms of service.</p>
          <h2>3. Data Use</h2>
          <p>We access your QuickBooks data solely to display financial metrics and reports within the Application. We do not sell, share, or distribute your financial data to third parties.</p>
          <h2>4. Restrictions</h2>
          <p>You may not: (a) copy, modify, or distribute the Application; (b) reverse engineer or attempt to extract the source code; (c) use the Application for any unlawful purpose; or (d) share access credentials with unauthorized users.</p>
          <h2>5. Disclaimer of Warranties</h2>
          <p>THE APPLICATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. WE DISCLAIM ALL WARRANTIES, EXPRESS OR IMPLIED, INCLUDING WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT.</p>
          <h2>6. Limitation of Liability</h2>
          <p>IN NO EVENT SHALL WE BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES ARISING FROM YOUR USE OF THE APPLICATION.</p>
          <h2>7. Termination</h2>
          <p>This Agreement is effective until terminated. We may terminate your access at any time if you breach these terms. Upon termination, you must cease all use of the Application.</p>
          <h2>8. Changes to This Agreement</h2>
          <p>We reserve the right to modify this Agreement at any time. Continued use of the Application after changes constitutes acceptance of the modified terms.</p>
          <h2>9. Contact</h2>
          <p>If you have questions about this Agreement, please contact us through our website.</p>
        </div>"""


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    shutil.copy(os.path.join(SRC, "site.css"), os.path.join(OUT, "assets", "site.css"))
    build_home()
    build_pages()
    print("Built:", sorted(f for f in os.listdir(OUT) if f.endswith(".html")))
