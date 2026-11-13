"""Unique local copy for each market page (keeps the city pages from being
near-duplicates in Google's eyes).

Brand rules (GLL brand guide): Josh's voice, plain language, no rates or loan
terms, no superlatives, no office visits, soft CTAs. Only state local facts
that are public knowledge; never invent market stats or deal counts.
Plain text with "&" is fine here; build.py escapes it.
"""

CITY_COPY = {
    "hard-money-lenders-nebraska": {
        "intro": "Nebraska real estate isn't one market. Omaha, Lincoln and the towns along I-80 each have their own prices, buyers and rehab realities. Good Life Lending is a Nebraska-based direct lender funding fix-and-flip and rental deals statewide, in as little as 5 days from approval to funding.",
        "heading": "Investing in Nebraska Real Estate",
        "paragraphs": [
            "I've been in real estate since 2008: my first flip with no playbook, my first rental in 2010. I got into lending because I'd been on the other side of the table, turned down by a bank when my income didn't look right on paper.",
            "That's why we lend the way we do. We look at the deal and the person behind it, not just a credit score. We're selective. You'll need decent credit, real cash in the deal and a solid opportunity. When those are there, we move fast.",
            "Whether you're in the Omaha metro, Lincoln, or a smaller town in central or western Nebraska, the process is the same, and it's 100% digital.",
        ],
        "areas_heading": "Nebraska markets we lend in",
        "areas": ["Omaha", "Lincoln", "Bellevue", "Grand Island", "Kearney", "Fremont", "Hastings", "Norfolk", "Columbus", "North Platte", "Scottsbluff", "Lexington"],
        "fits": [
            "Fix-and-flip purchases with a rehab budget",
            "BRRRR and buy-and-hold rentals you plan to refinance",
            "Time-sensitive purchases where a quick close wins the deal",
        ],
        "faqs": [
            ("Do you lend everywhere in Nebraska?", "Yes. We fund deals across the state, from Omaha and Lincoln to Grand Island, Kearney, North Platte and Scottsbluff. We don't lend outside Nebraska right now."),
            ("What do I need to qualify?", "Decent credit, real cash in the deal and a solid opportunity. We look at the whole picture: who you are, what the deal looks like and whether the numbers make sense."),
            ("How is a hard money loan different from a bank loan?", "Speed and flexibility. Banks often take 25–40+ days and decide mostly on paperwork. We can fund in as little as 5 days from approval and weigh the deal and the borrower together."),
        ],
    },
    "omaha-hard-money-lenders": {
        "intro": "Omaha moves fast. Good houses in established neighborhoods don't sit long, and a seller who wants a quick close isn't going to wait 30-plus days on a bank. Good Life Lending funds Omaha fix-and-flip and rental deals in as little as 5 days from approval, so your offer can compete.",
        "heading": "Investing in Omaha Real Estate",
        "paragraphs": [
            "Omaha is Nebraska's largest metro, and it's really several markets stacked together. A 1920s two-story in Benson or Dundee is a different project than a 1970s ranch in Millard or a starter home in Bellevue or Papillion. Rehab budgets, buyers and timelines change from one part of town to the next.",
            "A lot of Omaha's older housing, especially in midtown, North Omaha and South Omaha, needs real work: electrical, plumbing, roofs, foundations. That's where fix-and-flip money earns its keep. You need a lender who funds the purchase and the rehab and doesn't flinch when the inspection report gets long.",
            "We look at the deal and the person behind it. Bring decent credit, real cash in the deal and a property that makes sense, and we'll move as fast as the deal needs.",
        ],
        "areas_heading": "Omaha-area neighborhoods and towns we lend in",
        "areas": ["Benson", "Dundee", "Midtown", "Florence", "North Omaha", "South Omaha", "Millard", "Elkhorn", "Ralston", "Bellevue", "Papillion", "La Vista", "Gretna", "Bennington"],
        "fits": [
            "Older homes in established neighborhoods that need a full rehab",
            "Buy-and-hold rentals you plan to refinance once the work is done",
            "Competitive purchases where closing fast wins the deal",
        ],
        "faqs": [
            ("Do you lend in Council Bluffs or elsewhere in Iowa?", "Not right now. We fund deals in Nebraska only, so that's Omaha, Bellevue, Papillion, La Vista and the rest of the metro on the Nebraska side of the river."),
            ("Can you fund an Omaha flip that needs a big rehab?", "Yes, as long as the numbers work. We finance the purchase and the renovation and fund rehab draws as the work gets done. What matters is the after-repair value, your budget and your plan."),
            ("How fast can you close in Omaha?", "As little as 5 days from approval to funding. Title and appraisal timing can move that a little, but we work hard not to be the holdup."),
        ],
    },
    "lincoln-hard-money-lenders": {
        "intro": "Lincoln is home base for Good Life Lending. We've funded deals across town, like a northeast Lincoln ranch our borrower closed on fast and turned into a long-term rental. If you're flipping or building a rental portfolio in Lincoln, you're working with a local, direct lender.",
        "heading": "Investing in Lincoln Real Estate",
        "paragraphs": [
            "Lincoln is a steady market. With the University of Nebraska and state government anchoring the city, there's consistent demand from renters and first-time buyers, which is good news whether you're flipping or holding.",
            "Much of the opportunity is in older neighborhoods near downtown and campus, like Near South, Clinton, Hartley, University Place, Havelock and College View, where solid houses need updates. Newer areas on the edges of town draw a different buyer, and your rehab plan should reflect that.",
            "Being local doesn't replace good numbers. But it does mean you're talking to someone who knows Lincoln and understands the deal you're describing.",
        ],
        "areas_heading": "Lincoln neighborhoods and nearby towns we lend in",
        "areas": ["Near South", "Clinton", "Hartley", "University Place", "Havelock", "College View", "Bethany", "Belmont", "Northeast Lincoln", "Waverly", "Hickman", "Crete"],
        "fits": [
            "Rentals near UNL and downtown",
            "Ranch and split-level homes ready for an update",
            "BRRRR deals: buy, rehab, rent, refinance",
        ],
        "faqs": [
            ("Are you a local Lincoln lender?", "Yes. Good Life Lending is based in Lincoln and lends directly, with no broker in the middle. Everything happens online and over the phone, so there's no office to come to."),
            ("Do you fund rental properties near UNL?", "We look at them like any other deal: the property, the rent numbers, your rehab plan and your experience. If it's a solid rental with real cash in it, let's talk."),
            ("Can a first-time investor get a fix-and-flip loan in Lincoln?", "Yes. We work with people on their first or second flip. We need to see decent credit, real cash in the deal and a property that makes sense."),
        ],
    },
    "grand-island-hard-money-lenders": {
        "intro": "Grand Island investors shouldn't have to wait on a big-city lender who doesn't know central Nebraska. Good Life Lending funds fix-and-flip and rental deals in Grand Island and the towns around it, in as little as 5 days from approval to funding.",
        "heading": "Investing in Grand Island Real Estate",
        "paragraphs": [
            "Grand Island is the hub of central Nebraska. It's home to the Nebraska State Fair and a big regional workforce, and that keeps demand steady for decent, affordable rentals.",
            "Prices here run lower than in Omaha or Lincoln, so the margin on a flip or rental comes down to buying right and keeping the rehab budget under control. Older homes around downtown and the established neighborhoods nearby are where most value-add deals show up.",
            "Smaller markets sometimes get passed over by lenders. We'd rather look at your deal on its merits.",
        ],
        "areas_heading": "Central Nebraska towns we lend in",
        "areas": ["Grand Island", "Alda", "Wood River", "Doniphan", "Cairo", "Central City", "Aurora", "St. Paul", "Hastings"],
        "fits": [
            "Affordable single-family rentals",
            "Older homes near downtown that need updating",
            "Quick purchases from motivated sellers",
        ],
        "faqs": [
            ("Do you lend outside Grand Island?", "Yes. We lend throughout Nebraska, including Hastings, Kearney, Central City, Aurora and the smaller towns in between."),
            ("Is a small-town deal too small for you?", "It depends on the deal, not the zip code. Tell us about the property and your numbers, and we'll give you a straight answer."),
            ("Do I need to meet with you in person?", "No. Our process is 100% digital, so it works the same in Grand Island as it does in Omaha."),
        ],
    },
    "kearney-hard-money-lenders": {
        "intro": "Kearney sits right on I-80 with the University of Nebraska at Kearney in town, and that combination keeps housing in demand. Good Life Lending funds fix-and-flip and rental deals in Kearney and across Buffalo County, in as little as 5 days from approval to funding.",
        "heading": "Investing in Kearney Real Estate",
        "paragraphs": [
            "UNK, healthcare and a regional retail and service economy give Kearney a steady base of renters and buyers. For investors, rentals near campus and well-located starter homes can both work, as long as the numbers do.",
            "Like a lot of Nebraska towns, Kearney has plenty of solid older homes that need a refresh. The opportunity is buying right, keeping the rehab tight and knowing who your end buyer or renter is.",
            "If you're flipping in Kearney, you shouldn't have to wait a month on a bank to close. We move as fast as the deal needs.",
        ],
        "areas_heading": "Kearney-area towns we lend in",
        "areas": ["Kearney", "Gibbon", "Elm Creek", "Shelton", "Ravenna", "Lexington", "Holdrege", "Minden"],
        "fits": [
            "Rentals near UNK",
            "Starter homes that need a cosmetic or full rehab",
            "Purchases where a fast close gets you the deal",
        ],
        "faqs": [
            ("Do you fund rentals near UNK?", "Yes, if the deal works. We look at the property, your rent numbers, your rehab plan and the cash you're bringing."),
            ("Do you lend in towns around Kearney?", "Yes. That includes Lexington, Holdrege, Minden, Gibbon and the rest of central and western Nebraska."),
            ("How do I get started?", "Fill out the quick quote form on this page or start a full application. We'll follow up within one business day."),
        ],
    },
}
