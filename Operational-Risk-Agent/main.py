from pydantic import BaseModel, Field

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langchain_core.messages import (
    HumanMessage,
    SystemMessage
)

from uipath_langchain.chat.models import (
    UiPathAzureChatOpenAI
)

# ==========================================
# IMPORT ANALYSIS NODES
# ==========================================

from services.route_analysis import (
    route_analysis
)

from services.weather_analysis import (
    weather_analysis
)

from services.news_analysis import (
    news_analysis
)

from services.sentiment_analysis import (
    sentiment_analysis
)

from services.conflict_analysis import (
    conflict_analysis
)

from services.risk_scoring import (
    risk_scoring
)

# ==========================================
# INPUT
# ==========================================

class Input(BaseModel):

    vessel_name: str = Field(
        description="Name of vessel"
    )

    origin_port: str = Field(
        description="Origin port"
    )

    destination_port: str = Field(
        description="Destination port"
    )


# ==========================================
# STATE
# ==========================================

class State(BaseModel):

    vessel_name: str

    origin_port: str

    destination_port: str

    # Route Intelligence

    # Route Intelligence

    route_details: str = ""

    route_distance_km: float = 0

    route_coordinates: list = Field(
        default_factory=list
    )

    route_risk: int = 0
    route_chokepoints: list = Field(
        default_factory=list
    )
    # Weather

    weather_details: str = ""

    weather_risk: int = 0

    # News

    news_details: str = ""

    news_risk: int = 0

    # Sentiment

    # Sentiment

    sentiment_score: float = 0

    sentiment_risk: int = 0

    sentiment_details: str = ""

    # Conflict Intelligence

    conflict_details: str = ""

    conflict_risk: int = 0

    # Final

    risk_score: int = 0

    risk_category: str = ""

    summary: str = ""


# ==========================================
# OUTPUT
# ==========================================

class Output(BaseModel):

    vessel_name: str

    risk_score: int

    risk_category: str

    route_risk: int

    weather_risk: int

    news_risk: int

    sentiment_risk: int

    conflict_risk: int

    summary: str


# ==========================================
# REPORT GENERATION
# ==========================================

async def generate_report(
    state: State
) -> Output:

    llm = UiPathAzureChatOpenAI(
    model="gpt-4.1-mini-2025-04-14",
    temperature=0.2
    )

    prompt = f"""
Generate a professional Marine Cargo
Operational Risk Assessment Report.

VESSEL
------
{state.vessel_name}

ROUTE
------
Origin: {state.origin_port}

Destination: {state.destination_port}

Route Information:
{state.route_details}

Distance:
{state.route_distance_km} km

Route Points:
{len(state.route_coordinates)}
WEATHER INTELLIGENCE
--------------------
{state.weather_details}


NEWS INTELLIGENCE
-----------------
{state.news_details}


CONFLICT INTELLIGENCE
---------------------
{state.conflict_details}


RISK COMPONENTS
---------------
Route Risk: {state.route_risk}

Weather Risk: {state.weather_risk}

News Risk: {state.news_risk}

Sentiment Risk: {state.sentiment_risk}

Conflict Risk: {state.conflict_risk}


FINAL RISK SCORE
----------------
{state.risk_score}

RISK CATEGORY
-------------
{state.risk_category}

CRITICAL FACTORS
----------------
Route Chokepoints:
{state.route_chokepoints}

Explain operational risks arising from these maritime chokepoints.

Assess:
- Piracy risk
- Geopolitical risk
- Port disruption risk
- Cargo delay risk
Provide:

1. Executive Summary

2. Route Assessment

3. Weather Assessment

4. News & Geopolitical Risks

5. Operational Concerns

6. Recommended Mitigation Actions

7. Insurance Considerations

Keep report concise but professional.
"""

    response = await llm.ainvoke(
        [
            SystemMessage(
                content=(
                    "You are a senior marine "
                    "cargo risk analyst."
                )
            ),
            HumanMessage(
                content=prompt
            )
        ]
    )

    return Output(

    vessel_name=state.vessel_name,

    risk_score=state.risk_score,

    risk_category=state.risk_category,

    route_risk=state.route_risk,

    weather_risk=state.weather_risk,

    news_risk=state.news_risk,

    sentiment_risk=state.sentiment_risk,

    conflict_risk=state.conflict_risk,

    summary=response.content
    )


# ==========================================
# GRAPH
# ==========================================

builder = StateGraph(
    State,
    input=Input,
    output=Output
)

# ==========================================
# NODES
# ==========================================

builder.add_node(
    "route_analysis",
    route_analysis
)

builder.add_node(
    "weather_analysis",
    weather_analysis
)

builder.add_node(
    "news_analysis",
    news_analysis
)

builder.add_node(
    "sentiment_analysis",
    sentiment_analysis
)

builder.add_node(
    "conflict_analysis",
    conflict_analysis
)

builder.add_node(
    "risk_scoring",
    risk_scoring
)

builder.add_node(
    "generate_report",
    generate_report
)

# ==========================================
# FLOW
# ==========================================

builder.add_edge(
    START,
    "route_analysis"
)

builder.add_edge(
    "route_analysis",
    "weather_analysis"
)

builder.add_edge(
    "weather_analysis",
    "news_analysis"
)

builder.add_edge(
    "news_analysis",
    "sentiment_analysis"
)

builder.add_edge(
    "sentiment_analysis",
    "conflict_analysis"
)

builder.add_edge(
    "conflict_analysis",
    "risk_scoring"
)

builder.add_edge(
    "risk_scoring",
    "generate_report"
)

builder.add_edge(
    "generate_report",
    END
)

# ==========================================
# COMPILE
# ==========================================

graph = builder.compile()