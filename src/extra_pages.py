"""Extra pages: portal login, Nebraska fix & flip guide, recently funded deals.

Brand rules: Josh's voice, no rates or loan terms, no superlatives, no em dashes,
no office visits, no borrower names or addresses.
"""
import json, os, datetime, html as H

SRC = os.path.dirname(os.path.abspath(__file__))


def _read(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return f.read()


def _hero(h1, sub, eyebrow=""):
    eb = f'<p class="hero-eyebrow">{eyebrow}</p>' if eyebrow else ""
    return f"""  <header class="page-hero">
    <div class="container">
      {eb}
      <h1>{h1}</h1>
      <p>{sub}</p>
    </div>
  </header>"""


def _crumbs(domain, slug, name):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{domain}/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{domain}/{slug}"}]}


def _faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def _faq_html(faqs):
    return "\n".join(f'          <details class="faq-item"><summary><h3>{H.escape(q)}</h3></summary><p>{H.escape(a)}</p></details>'
                     for q, a in faqs)


# ---------------------------------------------------------------------------
def portal_login(ctx):
    page, write, D = ctx["page"], ctx["write"], ctx["DOMAIN"]
    body = _hero("Borrower &amp; Investor Portal Login",
                 "Good Life Lending borrowers and investors manage loans, draws, documents and payments in our secure online portal.",
                 "Good Life Lending Portal") + f"""
  <main>
    <section>
      <div class="container" style="max-width:760px;">
        <div class="card center" style="padding:40px 28px;">
          <h2 class="section-title" style="font-size:26px;">Log in to your portal</h2>
          <p style="color:var(--muted);margin-bottom:24px;">Use the same email you applied with. If you've forgotten your password, use the reset link on the login screen.</p>
          <a href="{ctx['PORTAL_URL']}" class="btn btn-primary">Go to the Portal Login <span class="btn-arrow" aria-hidden="true">→</span></a>
        </div>
        <div class="review-grid" style="margin-top:28px;">
          <article class="review-card"><h3>New borrower?</h3><p>Start a full loan application in the portal, or get a quick quote first.</p><p><a href="{ctx['APPLY_URL']}"><strong>Apply for a loan →</strong></a><br /><a href="/#contact"><strong>Get an instant quote →</strong></a></p></article>
          <article class="review-card"><h3>Need a proof of funds letter?</h3><p>Request a POF letter so you can make cash offers and stay ahead of the competition.</p><p><a href="{ctx['POF_URL']}"><strong>Request a POF letter →</strong></a></p></article>
          <article class="review-card"><h3>Trouble logging in?</h3><p>Call or email and we'll get you sorted out.</p><p><a href="tel:+14027707950"><strong>(402) 770-7950</strong></a><br /><a href="mailto:{ctx['EMAIL']}"><strong>{ctx['EMAIL']}</strong></a></p></article>
        </div>
        <p class="map-note" style="margin-top:24px;">This portal is for Good Life Lending, a private lender in Lincoln, Nebraska. It isn't affiliated with other companies that use the GoodLife name.</p>
      </div>
    </section>
  </main>"""
    write("portal-login.html", page("portal-login", "Borrower & Investor Portal Login | Good Life Lending",
                                    "Log in to the Good Life Lending borrower and investor portal to manage your loan, draws, documents and payments.",
                                    body, ld=[_crumbs(D, "portal-login", "Portal Login")]))


# ---------------------------------------------------------------------------
GUIDE_FAQS = [
    ("Can I get a fix and flip loan with no experience?", "Yes. We work with investors on their first or second flip. We look closely at the deal, your rehab plan, your contractor and the cash you're bringing, along with your credit."),
    ("How much cash do I need for a fix and flip loan?", "It depends on the deal. We require real cash in every deal, and we'll tell you exactly what yours needs up front, before you're committed."),
    ("Do you lend outside Omaha and Lincoln?", "Yes. We fund deals across Nebraska, from Omaha and Lincoln to Columbus, Norfolk, Beatrice, Kearney, Grand Island and Scottsbluff."),
    ("Do you lend outside Nebraska?", "Not right now. We fund deals in Nebraska only."),
]


def guide(ctx):
    page, write, D = ctx["page"], ctx["write"], ctx["DOMAIN"]
    slug = "nebraska-fix-and-flip-loan-guide"
    title = "Nebraska Fix and Flip Loan Guide | Good Life Lending"
    desc = "How fix and flip loans work in Nebraska: what lenders look for, what to have ready, the process from offer to payoff, and mistakes to avoid."
    body = _hero("Nebraska Fix &amp; Flip Loan Guide",
                 "How hard money works in Nebraska, what lenders look for, what to have ready, and how the process runs from offer to payoff. Written by a lender who's been on the borrower side.",
                 "Investor Guide") + f"""
  <main>
    <section>
      <div class="container guide">
        <nav class="guide-toc" aria-label="In this guide">
          <strong>In this guide</strong>
          <a href="#what">What a fix and flip loan is</a>
          <a href="#vs-bank">Hard money vs. a bank loan</a>
          <a href="#look-for">What we look for</a>
          <a href="#ready">What to have ready</a>
          <a href="#process">How the process works</a>
          <a href="#nebraska">Nebraska-specific tips</a>
          <a href="#mistakes">Mistakes to avoid</a>
          <a href="#faq">FAQs</a>
        </nav>
        <article class="prose guide-body">
          <h2 id="what">What is a fix and flip loan?</h2>
          <p>A fix and flip loan is short-term financing for buying a property that needs work, renovating it, and then selling it or refinancing it into a rental. Instead of a 30-year mortgage, it's built for a project that lasts months, not decades.</p>
          <p>Most fix and flip loans cover two things: the purchase and the renovation. The purchase money funds at closing. The renovation money is usually held back and released in draws as the work gets done and verified.</p>

          <h2 id="vs-bank">Hard money vs. a bank loan</h2>
          <ul>
            <li><strong>Speed.</strong> Banks often take 25–40+ days to close. We can fund in as little as 5 days from approval. When a seller wants a fast close, that's the difference between getting the deal and losing it.</li>
            <li><strong>Underwriting.</strong> Banks lean on tax returns and debt-to-income ratios. A hard money lender focuses on the deal itself: the property, the after-repair value and your plan, along with your credit and the cash you're bringing.</li>
            <li><strong>Property condition.</strong> Banks often won't lend on a house that needs major work. Fix and flip lenders will, because that's the whole point.</li>
            <li><strong>Term.</strong> Hard money loans are short term and built to be paid off when you sell or refinance.</li>
            <li><strong>Cost.</strong> Hard money costs more than a bank loan. You're paying for speed and convenience, so the deal has to have enough margin to cover it.</li>
          </ul>
          <p>I got cut off by my bank once when my income didn't look right on paper. That's a big part of why Good Life Lending looks at the person and the deal together.</p>

          <h2 id="look-for">What we look for</h2>
          <p>We're selective. That isn't gatekeeping; it's how we make sure our borrowers succeed. Every deal we fund has these:</p>
          <ul>
            <li><strong>Decent credit.</strong> Not perfect, but a history of handling what you owe.</li>
            <li><strong>Real cash in the deal.</strong> You need skin in the game, plus reserves for surprises.</li>
            <li><strong>A solid opportunity.</strong> The purchase price plus renovation needs to leave room under the after-repair value.</li>
            <li><strong>A realistic scope of work.</strong> A line-by-line rehab budget that matches the house.</li>
            <li><strong>Experience or a plan.</strong> If it's your first flip, show us your contractor and your plan.</li>
          </ul>

          <h2 id="ready">What to have ready when you apply</h2>
          <ul>
            <li>The property address and your purchase contract (or the price you plan to offer)</li>
            <li>A scope of work and rehab budget, broken out line by line</li>
            <li>Your after-repair value estimate, with comparable sales if you have them</li>
            <li>Your exit plan: sell, or refinance and rent</li>
            <li>The LLC or other entity you'll buy in. Most investors use one; if you don't have one yet, tell us</li>
            <li>Recent bank statements showing the cash you're bringing</li>
            <li>Insurance for a vacant or under-renovation property, with the lender named on the policy</li>
          </ul>

          <h2 id="process">How the process works</h2>
          <ol class="steps-list">
            <li>Get a quick quote online or by phone</li>
            <li>Submit your full application in our portal</li>
            <li>We review the property, your numbers and you</li>
            <li>Title, insurance and closing documents come together</li>
            <li>Funding, in as little as 5 days from approval</li>
            <li>Request rehab draws as work is completed</li>
            <li>Pay off the loan when you sell or refinance</li>
          </ol>
          <p>Closings run through a title company. In Nebraska, the loan is secured by a deed of trust on the property, and it's released once the loan is paid off. Everything else happens online and over the phone, so there's no office to drive to.</p>

          <h2 id="nebraska">Nebraska-specific tips</h2>
          <ul>
            <li><strong>Every market is different.</strong> Omaha and Lincoln have the most buyers and the most competition for good houses. Smaller towns often have lower purchase prices but fewer buyers, so be conservative with your after-repair value and timeline.</li>
            <li><strong>Plan for older houses.</strong> Many of the best value-add homes in established Nebraska neighborhoods are decades old. Budget for foundations, electrical, plumbing and sewer lines, not just finishes.</li>
            <li><strong>Winter changes your timeline.</strong> Exterior work, concrete and roofing slow down in the cold months. Build that into your schedule and your holding costs.</li>
            <li><strong>Know your end buyer.</strong> A finish level that sells in west Omaha may be overkill in a small town, and the reverse is true too.</li>
          </ul>

          <h2 id="mistakes">Mistakes to avoid</h2>
          <ul>
            <li>Underestimating the rehab. Add a contingency, because something always comes up.</li>
            <li>Stretching the after-repair value to make the numbers work.</li>
            <li>Overpaying because the deal feels exciting.</li>
            <li>Having no backup plan if the house doesn't sell as fast as you hoped.</li>
            <li>Waiting to line up financing until after you're under contract. Get pre-qualified first so you can close fast.</li>
          </ul>
          <p>See what real deals look like on our <a href="/recently-funded">recently funded page</a>, or check where you stand with our <a href="/pre-qualify">60-second qualification check</a>.</p>

          <h2 id="faq">Fix and flip loan FAQs</h2>
          <div class="faq-list" style="margin:16px 0 0;">
{_faq_html(GUIDE_FAQS)}
          </div>
        </article>
      </div>
    </section>

    <section id="cta">
      <div class="container">
        <h2>Have a Nebraska Flip in Mind?</h2>
        <p>Tell us about the deal. If it works, we'll move fast. If it doesn't, we'll tell you why.</p>
        <div class="cta-group">
          <a href="{ctx['APPLY_URL']}" class="btn btn-gold">Apply for a Loan</a>
          <a href="/#contact" class="btn btn-outline" style="color:#fff;border-color:rgba(255,255,255,0.4);">Get a Quote</a>
        </div>
      </div>
    </section>
  </main>"""
    article = {"@context": "https://schema.org", "@type": "Article", "headline": "Nebraska Fix & Flip Loan Guide",
               "description": desc, "url": f"{D}/{slug}", "author": {"@type": "Person", "name": "Josh Nix"},
               "publisher": {"@type": "Organization", "name": "Good Life Lending", "logo": {"@type": "ImageObject", "url": f"{D}/assets/img/logo.png"}},
               "datePublished": "2026-11-12", "dateModified": "2026-11-12", "image": f"{D}/assets/img/og-image.jpg"}
    write(f"{slug}.html", page(slug, title, desc, body, ld=[article, _faq_ld(GUIDE_FAQS), _crumbs(D, slug, "Nebraska Fix & Flip Loan Guide")]))


# ---------------------------------------------------------------------------
def _months(a, b):
    d = (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days / 30.44
    m = round(d * 2) / 2
    return f"{int(m)}" if m == int(m) else f"{m:.1f}".replace(".5", "½")


def recently_funded(ctx):
    page, write, D = ctx["page"], ctx["write"], ctx["DOMAIN"]
    slug = "recently-funded"
    deals = sorted(json.loads(_read("funded_deals.json"))["deals"], key=lambda x: x["sold"], reverse=True)
    def money(v): return f"${v:,.0f}"
    cards = []
    for d in deals:
        sold = datetime.date.fromisoformat(d["sold"]).strftime("%b %Y")
        scale = d["sale"]
        cards.append(f"""          <article class="deal-snap">
            <div class="deal-snap-head"><strong>{H.escape(d['town'])}, NE</strong><span class="deal-sold">Sold {sold}</span></div>
            <div class="tl-row"><div class="tl-top"><span>Purchase price</span><span class="tl-val">{money(d['purchase'])}</span></div><div class="tl-bar"><i style="width:{d['purchase'] / scale * 100:.0f}%;background:var(--navy);"></i></div></div>
            <div class="tl-row"><div class="tl-top"><span>Renovation</span><span class="tl-val">{money(d['renovation'])}</span></div><div class="tl-bar"><i style="width:{max(d['renovation'] / scale * 100, 3):.0f}%;background:var(--blue);"></i></div></div>
            <div class="tl-row"><div class="tl-top"><span>Sale price</span><span class="tl-val tl-tag-accent">{money(d['sale'])}</span></div><div class="tl-bar"><i style="width:100%;background:var(--orange);"></i></div></div>
            <p class="deal-foot">Fix &amp; flip · Funded to sold in about {_months(d['funded'], d['sold'])} months</p>
          </article>""")
    towns = sorted({d["town"] for d in deals})
    body = _hero("Recently Funded Fix &amp; Flip Deals",
                 "Here's what real deals look like. These are Nebraska flips we funded that have since sold. We share the town and the numbers, never the borrower or the address.",
                 "Real Deals") + f"""
  <main>
    <section>
      <div class="container">
        <div class="deal-snap-grid">
{chr(10).join(cards)}
        </div>
        <p class="map-note" style="margin-top:24px;">Purchase and renovation figures come from our loan records; sale prices as recorded at payoff. Every deal is different, and past results don't guarantee future ones.</p>
        <p style="margin-top:20px;">Flipping in {", ".join(towns[:-1])} or {towns[-1]}? See our <a href="/nebraska-fix-and-flip-loan-guide"><strong>Nebraska fix and flip loan guide</strong></a> or <a href="/hard-money-lenders-nebraska"><strong>Nebraska fix and flip loans</strong></a>.</p>
      </div>
    </section>

    <section id="cta">
      <div class="container">
        <h2>Your Deal Could Be Next</h2>
        <p>Working on a flip in Nebraska? Tell us about it. We fund in as little as 5 days from approval.</p>
        <div class="cta-group">
          <a href="{ctx['APPLY_URL']}" class="btn btn-gold">Apply for a Loan</a>
          <a href="/#contact" class="btn btn-outline" style="color:#fff;border-color:rgba(255,255,255,0.4);">Get a Quote</a>
        </div>
      </div>
    </section>
  </main>"""
    write(f"{slug}.html", page(slug, "Recently Funded Fix & Flip Deals in Nebraska | Good Life Lending",
                               "Real Nebraska fix and flip deals funded by Good Life Lending: purchase price, renovation and sale price. Towns only, no borrower details.",
                               body, ld=[_crumbs(D, slug, "Recently Funded")]))


def build_extra(ctx):
    portal_login(ctx)
    guide(ctx)
    recently_funded(ctx)
