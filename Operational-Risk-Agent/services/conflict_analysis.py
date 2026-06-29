import requests


# ==========================================
# MARITIME CONFLICT ZONES
# ==========================================

CONFLICT_ZONES = {

    "Hormuz": {
        "risk": 15
    },

    "Gulf of Aden": {
        "risk": 20
    },

    "Red Sea": {
        "risk": 25
    },

    "Suez Canal": {
        "risk": 10
    },

    "Gulf of Guinea": {
        "risk": 20
    }
}


# ==========================================
# RELIEFWEB
# ==========================================

def get_reliefweb_reports():

    try:

        response = requests.get(
            "https://api.reliefweb.int/v1/reports",
            params={
                "appname":
                "marine-risk-agent",

                "limit":
                50
            },
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        reports = []

        for item in data.get(
            "data",
            []
        ):

            fields = item.get(
                "fields",
                {}
            )

            reports.append({

                "title":
                fields.get(
                    "title",
                    ""
                ),

                "body":
                fields.get(
                    "body-html",
                    ""
                )
            })

        return reports

    except Exception:

        return []


# ==========================================
# CONFLICT ANALYSIS
# ==========================================

async def conflict_analysis(state):

    try:

        route_text = (
            state.route_details.lower()
        )

        reports = (
            get_reliefweb_reports()
        )

        risk = 0

        detected = []

        report_hits = []

        # ==================================
        # ROUTE CHOKEPOINT RISK
        # ==================================

        if "hormuz" in route_text:

            risk += 15

            detected.append(
                "Strait of Hormuz"
            )

        if "gulf of aden" in route_text:

            risk += 20

            detected.append(
                "Gulf of Aden"
            )

        if "red sea" in route_text:

            risk += 25

            detected.append(
                "Red Sea"
            )

        if "suez canal" in route_text:

            risk += 10

            detected.append(
                "Suez Canal"
            )

        if "gulf of guinea" in route_text:

            risk += 20

            detected.append(
                "Gulf of Guinea"
            )

        # ==================================
        # LIVE CONFLICT EVENTS
        # ==================================

        conflict_keywords = [

            "war",
            "attack",
            "missile",
            "drone",
            "piracy",
            "houthi",
            "iran",
            "israel",
            "yemen",
            "somalia"
        ]

        event_count = 0

        for report in reports:

            text = (

                report["title"]

                +

                " "

                +

                report["body"]

            ).lower()

            for keyword in conflict_keywords:

                if keyword in text:

                    event_count += 1

                    report_hits.append(
                        report["title"]
                    )

                    break

        if event_count >= 20:

            risk += 15

        elif event_count >= 10:

            risk += 10

        elif event_count >= 5:

            risk += 5

        risk = min(
            risk,
            35
        )

        state.conflict_risk = (
            risk
        )

        state.conflict_details = f"""
Conflict Intelligence

Conflict Risk:
{risk}

Detected Conflict Zones:
{chr(10).join(detected)}

Recent Conflict Events:
{event_count}

Sample Reports:
{chr(10).join(report_hits[:10])}
"""

    except Exception as e:

        state.conflict_risk = 0

        state.conflict_details = (
            f"Conflict analysis failed: "
            f"{str(e)}"
        )

    return state