import feedparser
from collections import defaultdict


# ==========================================
# NEWS FEEDS
# ==========================================

NEWS_FEEDS = [

    "https://maritime-executive.com/rss",

    "https://safety4sea.com/feed/",

    "https://gcaptain.com/feed/",

    "https://news.google.com/rss/search?q=maritime+shipping"
]


# ==========================================
# RISK KEYWORDS
# ==========================================

RISK_KEYWORDS = {

    "piracy": 20,

    "hijack": 25,

    "attack": 20,

    "missile": 25,

    "drone": 20,

    "war": 30,

    "conflict": 20,

    "houthi": 25,

    "iran": 15,

    "israel": 15,

    "yemen": 25,

    "somalia": 20,

    "sanctions": 15,

    "closure": 15,

    "closed": 15,

    "congestion": 10,

    "delay": 10,

    "strike": 10,

    "collision": 15,

    "grounding": 20,

    "detained": 15,

    "detention": 15,

    "storm": 15,

    "cyclone": 20,

    "hurricane": 20,

    "red sea": 25,

    "gulf of aden": 20,

    "suez": 15,

    "hormuz": 20
}


# ==========================================
# NEWS ANALYSIS
# ==========================================

async def news_analysis(state):

    try:

        headlines = []

        unique_titles = set()

        total_risk = 0

        matched_events = []

        route_text = (
            state.route_details.lower()
        )

        route_keywords = []

        if "red sea" in route_text:

            route_keywords.extend([
                "red sea",
                "houthi",
                "yemen"
            ])

        if "gulf of aden" in route_text:

            route_keywords.extend([
                "somalia",
                "piracy",
                "gulf of aden"
            ])

        if "suez canal" in route_text:

            route_keywords.append(
                "suez"
            )

        if "hormuz" in route_text:

            route_keywords.extend([
                "hormuz",
                "iran"
            ])

        for feed_url in NEWS_FEEDS:

            try:

                feed = feedparser.parse(
                    feed_url
                )

                for entry in feed.entries[:25]:

                    title = (
                        entry.title.strip()
                    )

                    if title in unique_titles:

                        continue

                    unique_titles.add(
                        title
                    )

                    headlines.append(
                        title
                    )

                    title_lower = (
                        title.lower()
                    )

                    local_risk = 0

                    for keyword, score in (
                        RISK_KEYWORDS.items()
                    ):

                        if keyword in title_lower:

                            local_risk += score

                    for route_keyword in (
                        route_keywords
                    ):

                        if route_keyword in title_lower:

                            local_risk += 10

                    if local_risk > 0:

                        matched_events.append(

                            f"{title}"
                            f" ({local_risk})"

                        )

                        total_risk += (
                            local_risk
                        )

            except Exception:

                continue

        if total_risk >= 300:

            news_risk = 35

        elif total_risk >= 200:

            news_risk = 30

        elif total_risk >= 120:

            news_risk = 25

        elif total_risk >= 60:

            news_risk = 15

        elif total_risk >= 20:

            news_risk = 10

        else:

            news_risk = 0

        state.news_risk = (
            news_risk
        )

        state.news_details = f"""
News Intelligence

Articles Analysed:
{len(headlines)}

Route Keywords:
{", ".join(route_keywords)}

Matched Risk Events:
{chr(10).join(matched_events[:15])}

Total News Score:
{total_risk}

News Risk:
{news_risk}
"""

    except Exception as e:

        state.news_risk = 0

        state.news_details = (
            f"News analysis failed: "
            f"{str(e)}"
        )

    return state