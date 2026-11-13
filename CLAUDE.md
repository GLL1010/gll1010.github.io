# Good Life Lending website (goodlife-lending.com)

Static site for Good Life Lending, a Lincoln, Nebraska hard money lender. Hosted free on
GitHub Pages from the `docs/` folder of this repo (GLL1010/gll1010.github.io). Moved off
GoHighLevel (GHL) in November 2026; lead capture still runs through GHL embeds.

**This repo is public.** Never commit passwords, API keys, borrower names, addresses or
personal email addresses here.

## How to make a change

1. Edit files in `src/` (never edit `docs/` by hand: the build overwrites it).
2. Build: `python3 src/build.py`
3. Check (see "Before you deploy").
4. Deploy: `git add -A && git commit -m "..." && git push`. GitHub Pages republishes in about a minute.
5. Verify on the live site, e.g. `curl -s "https://goodlife-lending.com/<page>?v=$RANDOM" | grep -c "<new text>"`,
   and look at it in the browser on desktop and phone widths.

The stylesheet URL gets an automatic cache-buster (`site.css?v=<hash>`), so CSS changes show immediately.
Local preview: `python3 -m http.server 8765 --directory docs` (extensionless URLs like `/apply` only work on the live site).

## What each file controls

| File | Controls |
|---|---|
| `src/build.py` | Everything shared: tracking code, nav, footer, page layout, city-page template, legal page text, redirects, sitemap list, constants (apply/POF/portal URLs, Google rating) |
| `src/home.html` | Homepage body (hero, deal card, why-us band, how it works, FAQs, reviews, contact). `{{...}}` placeholders are filled by build.py |
| `src/site.css` | All styles (later rules override earlier ones) |
| `src/city_copy.py` | Unique local copy + FAQs for each market page (Nebraska, Omaha, Lincoln, Grand Island, Kearney, Columbus, Norfolk, Beatrice) |
| `src/seo.json` | Titles, descriptions and structured data for the original market pages |
| `src/home-schema.json` | Homepage structured data (FAQ schema is rebuilt from the visible FAQs) |
| `src/extra_pages.py` | `/portal-login`, `/nebraska-fix-and-flip-loan-guide`, `/recently-funded` |
| `src/funded_deals.json` | Deals shown on /recently-funded |
| `src/lending_map.json` | Towns + loan counts on the homepage "Where We Lend" map |
| `src/nebraska_paths.json` | Nebraska/county outlines for the map (generated from US Census data; don't hand-edit) |
| `src/scorecard.html` | The "Do You Qualify?" 60-second check on /pre-qualify (copied from GHL) |
| `docs/assets/img/` | Images (logo, photos, share image) |

Adding a city page: add an entry to `CITY_COPY` (unique copy, not a template swap), add it to
`NEW_CITIES` and the `urls` sitemap list in build.py, and link it from the footer, the map chips
and `AREAS`. Only build pages for towns with real deals or real search demand.

## Copy and brand rules (must follow)

- Josh's voice: plain, conversational, honest, low-pressure. Short paragraphs.
- **No em dashes** anywhere. Use commas, colons, periods or parentheses. (En dashes in ranges like "25–40+" are fine.)
- Speed claim is **"as little as 5 days"** from approval to funding. Never "7–10 days" or an average.
- **No rates, loan terms, LTV/ARV percentages, minimum loan amounts or "competitive rates."**
- No superlatives ("best," "go-to," "fastest," "most competitive").
- Requirements are always: decent credit, real cash in the deal, a solid opportunity. Never imply GLL funds everyone; never say "no credit checks."
- No office visits ("stop by," "come in"). The process is 100% digital.
- Deal data: towns and numbers only. **Never borrower names or street addresses.**
- Don't publish total loan counts (e.g. "100+ loans").
- Don't use the word "scorecard" in visible copy (it's "60-second check").
- Legal pages (privacy, terms, EULA) are copied from the old site; change wording only when Josh asks.
- Only state local facts that are public knowledge; never invent market stats.

## GoHighLevel embeds (don't break these)

- **Instant Quote survey** `T2gbIv97b8rukjUzvRkV`: homepage contact section + every market page. Submissions fire the GHL workflow "Landing Page Survey Automation (Google ads)" (alert to Josh, `google ads` tag, nurture emails). It redirects to `https://goodlife-lending.com/thank-you`, so **keep the `/thank-you` page**.
- **Loan Request form** `XGMTCOitb0seEcEmT0dB`: on `/apply`. No workflow attached.
- On the homepage the survey is injected by a scroll-triggered loader (`DEFERRED_SURVEY` in build.py). **Never put `loading="lazy"` on a GHL iframe**: GHL's `form_embed.js` hides it off-screen until it loads, so it never loads and the card goes blank.
- Survey look (fonts, colors, padding) is set inside GHL's survey builder, separately for desktop and mobile.

## Tracking (on every real page via build.py)

GA4 `G-235FJNCR9P`, GTM `GTM-KV8DJBX7`, Meta Pixel `669608049332732`, Search Console verification meta tag,
and GHL external tracking. Redirect stubs intentionally have none.

## Data refreshes (from Lendr)

- **Map** (`lending_map.json`): Lendr `list-loans` with filter `active` and `completed`, Nebraska only, excluding loans
  where the borrower is "Good Life Lending" (internal). Count by town; add lat/lon for new towns.
  Scottsbluff was added at Josh's request (not in Lendr).
- **Recently Funded** (`funded_deals.json`): completed loans with a "Sale Price" custom field, purchase loans only,
  sold above purchase + renovation. Purchase = Lendr purchase price (`current_value`), renovation = larger of
  `construction_costs` and `holdback`, sold = Sale Price.
- **Google rating**: `GOOGLE_RATING`, `GOOGLE_REVIEW_COUNT` in build.py, and `aggregateRating` in `seo.json`.

## SEO setup

- Homepage targets "Nebraska hard money lender"; `/hard-money-lenders-nebraska` targets "Nebraska fix and flip loans".
  Keep them from competing.
- After adding or changing pages: bump `LASTMOD` in build.py, then in Google Search Console resubmit
  `https://goodlife-lending.com/sitemap.xml` and use URL Inspection → Request indexing on the new/changed URLs.
- Old GHL URLs are redirect stubs (`/home`, `/blog`, `/watch-party`, `/kearny-...`, `/real-estate-generic-005-12w/*` via 404.html).

## DNS (GoDaddy)

Apex A records → GitHub Pages (185.199.108–111.153); `www` CNAME → `gll1010.github.io`.
**Don't touch** MX (Google Workspace), TXT/SPF/DKIM (`ml._domainkey`), `mail`, or `portal` (that's Lendr).
The domain is also connected in GHL for email sending; don't remove it there.

## Before you deploy

- Zero em dashes in `docs/` (`grep -c "—" docs/*.html`)
- All JSON-LD blocks parse; no leftover `{{` placeholders in `docs/`
- New pages are in the sitemap and linked from somewhere
- Check desktop and ~375px phone width (no sideways scrolling)

## Open to-dos

- Google Business Profile: add recent deal photos, post funded/sold deals, add opening date.
- Consider city pages for Fremont, Hastings, North Platte once there are deals there.
- Optional: GHL notification workflow for Loan Request form submissions.
