# ==========================================
# ENTERPRISE OPERATIONAL RISK SCORING ENGINE
# ==========================================

MAX_ROUTE_RISK = 50
MAX_WEATHER_RISK = 25
MAX_NEWS_RISK = 35
MAX_SENTIMENT_RISK = 20
MAX_CONFLICT_RISK = 35

MAX_TOTAL_SCORE = (
    MAX_ROUTE_RISK +
    MAX_WEATHER_RISK +
    MAX_NEWS_RISK +
    MAX_SENTIMENT_RISK +
    MAX_CONFLICT_RISK
)


# ==========================================
# ENTERPRISE RISK SCORING
# ==========================================

async def risk_scoring(state):

    try:

        # ==================================
        # VALIDATE COMPONENT SCORES
        # ==================================

        route_score = max(
            0,
            min(state.route_risk, MAX_ROUTE_RISK)
        )

        weather_score = max(
            0,
            min(state.weather_risk, MAX_WEATHER_RISK)
        )

        news_score = max(
            0,
            min(state.news_risk, MAX_NEWS_RISK)
        )

        sentiment_score = max(
            0,
            min(state.sentiment_risk, MAX_SENTIMENT_RISK)
        )

        conflict_score = max(
            0,
            min(state.conflict_risk, MAX_CONFLICT_RISK)
        )

        # ==================================
        # RAW SCORE
        # ==================================

        raw_score = (
            route_score +
            weather_score +
            news_score +
            sentiment_score +
            conflict_score
        )

        # ==================================
        # NORMALIZED SCORE (0-100)
        # ==================================

        normalized_score = int(
            round(
                   (raw_score / MAX_TOTAL_SCORE) * 100
                 )
        )

        normalized_score = max(
            0,
            min(normalized_score, 100)
        )

        state.risk_score = normalized_score

        # ==================================
        # RISK CATEGORY
        # ==================================

        if normalized_score < 20:

            category = "LOW"

        elif normalized_score < 40:

            category = "MEDIUM"

        elif normalized_score < 70:

            category = "HIGH"

        else:

            category = "CRITICAL"

        state.risk_category = category

        # ==================================
        # PRIMARY RISK DRIVERS
        # ==================================

        drivers = []

        if route_score >= 35:
            drivers.append(
                "High-Risk Maritime Route"
            )

        if weather_score >= 15:
            drivers.append(
                "Severe Weather Conditions"
            )

        if news_score >= 20:
            drivers.append(
                "Major Operational Disruptions"
            )

        if sentiment_score >= 10:
            drivers.append(
                "Negative Maritime Intelligence"
            )

        if conflict_score >= 20:
            drivers.append(
                "Conflict Zone Exposure"
            )

        if not drivers:
            drivers.append(
                "No Significant Operational Threats"
            )

        # ==================================
        # CONTRIBUTION (%)
        # ==================================

        route_percent = round(
            route_score / MAX_TOTAL_SCORE * 100,
            1
        )

        weather_percent = round(
            weather_score / MAX_TOTAL_SCORE * 100,
            1
        )

        news_percent = round(
            news_score / MAX_TOTAL_SCORE * 100,
            1
        )

        sentiment_percent = round(
            sentiment_score / MAX_TOTAL_SCORE * 100,
            1
        )

        conflict_percent = round(
            conflict_score / MAX_TOTAL_SCORE * 100,
            1
        )

        # ==================================
        # DATA CONFIDENCE
        # ==================================

        confidence = 100

        if route_score == 0:
            confidence -= 25

        if weather_score == 0:
            confidence -= 15

        if news_score == 0:
            confidence -= 15

        if conflict_score == 0:
            confidence -= 15

        confidence = max(confidence, 40)

        # ==================================
        # SUMMARY
        # ==================================

        state.summary = f"""
============================================================
MARINE OPERATIONAL RISK ASSESSMENT
============================================================

OVERALL RISK SCORE

{normalized_score}/100

Risk Category

{category}

Assessment Confidence

{confidence}%

------------------------------------------------------------

Component Scores

Route Risk:
{route_score}/{MAX_ROUTE_RISK}

Weather Risk:
{weather_score}/{MAX_WEATHER_RISK}

News Risk:
{news_score}/{MAX_NEWS_RISK}

Sentiment Risk:
{sentiment_score}/{MAX_SENTIMENT_RISK}

Conflict Risk:
{conflict_score}/{MAX_CONFLICT_RISK}

------------------------------------------------------------

Raw Operational Score

{raw_score}/{MAX_TOTAL_SCORE}

------------------------------------------------------------

Contribution to Overall Risk

Route:
{route_percent}%

Weather:
{weather_percent}%

News:
{news_percent}%

Sentiment:
{sentiment_percent}%

Conflict:
{conflict_percent}%

------------------------------------------------------------

Primary Risk Drivers

{chr(10).join("- " + d for d in drivers)}

------------------------------------------------------------

Enterprise Interpretation

LOW
Routine voyage with minimal operational concerns.

MEDIUM
Moderate operational exposure requiring periodic monitoring.

HIGH
Significant operational exposure requiring mitigation
before voyage execution.

CRITICAL
Very high operational exposure involving geopolitical,
security or severe environmental threats. Senior
underwriter approval is recommended before policy issuance.

============================================================
"""

    except Exception as e:

        state.risk_score = 0

        state.risk_category = "UNKNOWN"

        state.summary = (
            f"Risk scoring failed: {str(e)}"
        )

    return state