from vaderSentiment.vaderSentiment import (
    SentimentIntensityAnalyzer
)


# ==========================================
# RISK WORDS
# ==========================================

NEGATIVE_KEYWORDS = [

    "attack",

    "missile",

    "drone",

    "war",

    "conflict",

    "piracy",

    "hijack",

    "detained",

    "detention",

    "collision",

    "grounding",

    "storm",

    "cyclone",

    "hurricane",

    "closure",

    "closed",

    "delay",

    "strike",

    "sanctions",

    "red sea",

    "houthi",

    "somalia",

    "iran",

    "yemen"
]


# ==========================================
# SENTIMENT ANALYSIS
# ==========================================

async def sentiment_analysis(state):

    try:

        analyzer = (
            SentimentIntensityAnalyzer()
        )

        text = (
            state.news_details
        )

        if not text:

            state.sentiment_score = 0

            state.sentiment_risk = 0

            return state

        scores = analyzer.polarity_scores(
            text
        )

        compound = scores["compound"]

        state.sentiment_score = round(
            compound,
            3
        )

        # ==================================
        # COUNT NEGATIVE MARITIME EVENTS
        # ==================================

        text_lower = text.lower()

        keyword_hits = 0

        for keyword in NEGATIVE_KEYWORDS:

            if keyword in text_lower:

                keyword_hits += 1

        # ==================================
        # RISK SCORING
        # ==================================

        risk = 0

        if compound <= -0.70:

            risk += 15

        elif compound <= -0.50:

            risk += 10

        elif compound <= -0.20:

            risk += 5

        # Maritime incident boost

        if keyword_hits >= 10:

            risk += 15

        elif keyword_hits >= 5:

            risk += 10

        elif keyword_hits >= 3:

            risk += 5

        risk = min(
            risk,
            20
        )

        state.sentiment_risk = risk

        state.sentiment_details = f"""
Sentiment Intelligence

Compound Score:
{compound}

Negative Maritime Keywords:
{keyword_hits}

Sentiment Risk:
{risk}
"""

    except Exception as e:

        state.sentiment_score = 0

        state.sentiment_risk = 0

        state.sentiment_details = (
            f"Sentiment analysis failed: "
            f"{str(e)}"
        )

    return state