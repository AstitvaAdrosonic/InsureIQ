# ===============================================================
# Financial Risk Assessment Agent
# Enterprise Version - Part 1
# ===============================================================

import os
import re
import requests
import feedparser
import yfinance as yf
import json
from urllib.parse import quote_plus

from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from uipath_langchain.chat.models import UiPathAzureChatOpenAI

# ===============================================================
# Configuration
# ===============================================================

ALPHA_API_KEY = os.getenv(
    "ALPHA_VANTAGE_API_KEY",
    "IERTSSGFMI75NGN3"
)

REQUEST_TIMEOUT = 20

# ===============================================================
# Input Model
# ===============================================================

class Input(BaseModel):

    company_name: str = Field(
        description="Company Name"
    )

    country: str = Field(
        description="Country"
    )

# ===============================================================
# State Model
# ===============================================================

class State(BaseModel):

    company_name: str

    country: str

    registry_details: str = ""

    financial_details: str = ""

    director_details: str = ""

    litigation_details: str = ""

    news_details: str = ""

    risk_score: int = 0

    risk_category: str = ""

    summary: str = ""

# ===============================================================
# Output Model
# ===============================================================

class Output(BaseModel):

    company_name: str

    risk_score: int

    risk_category: str

    summary: str

# ===============================================================
# Alpha Vantage Symbol Search
# ===============================================================

async def get_symbol(company_name: str):

    try:

        url = (
            "https://www.alphavantage.co/query"
            "?function=SYMBOL_SEARCH"
            f"&keywords={quote_plus(company_name)}"
            f"&apikey={ALPHA_API_KEY}"
        )

        response = requests.get(url, timeout=20)

        data = response.json()

        matches = data.get("bestMatches", [])

        if not matches:
            return None

        candidates = []

        for item in matches[:10]:

            candidates.append(
                {
                    "symbol": item.get("1. symbol"),
                    "name": item.get("2. name"),
                    "region": item.get("4. region"),
                    "currency": item.get("8. currency"),
                }
            )

        llm = UiPathAzureChatOpenAI(
            model="gpt-4o-mini-2024-07-18"
        )

        prompt = f"""
You are a financial market expert.

The user wants information about this company:

{company_name}

Below are the possible stock symbols returned by Alpha Vantage.

{json.dumps(candidates, indent=2)}

Choose ONLY the company that best matches the requested company.

Rules:

1. Prefer the exact company.
2. Ignore ETFs.
3. Ignore REITs unless the user explicitly requested them.
4. Ignore Trusts.
5. Ignore Warrants.
6. Ignore Preferred Shares.
7. Prefer the main listed equity.
8. If Apple -> AAPL
9. If Microsoft -> MSFT
10. If Google -> GOOGL
11. If Alphabet -> GOOGL
12. If Tesla -> TSLA
13. If Amazon -> AMZN
14. If Meta -> META

Return ONLY the stock ticker.

Example:

AAPL

Nothing else.
"""

        result = await llm.ainvoke(prompt)

        symbol = result.content.strip()

        symbol = symbol.replace('"', "")

        symbol = symbol.replace("`", "")

        symbol = symbol.split()[0]

        return symbol

    except Exception as e:

        print(e)

        return None

# ===============================================================
# Alpha Vantage Company Overview
# ===============================================================

def get_company_overview(symbol: str):

    try:

        url = (
            "https://www.alphavantage.co/query"
            "?function=OVERVIEW"
            f"&symbol={symbol}"
            f"&apikey={ALPHA_API_KEY}"
        )

        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT
        )

        return response.json()

    except Exception:

        return {}

# ===============================================================
# Yahoo Finance
# ===============================================================

def get_yfinance_info(symbol: str):

    try:

        ticker = yf.Ticker(symbol)

        return ticker.info

    except Exception:

        return {}

# ===============================================================
# Google News RSS
# ===============================================================

def google_news(query: str):

    try:

        rss = (
            "https://news.google.com/rss/search?"
            f"q={quote_plus(query)}"
        )

        return feedparser.parse(rss)

    except Exception:

        return None

# ===============================================================
# Registry Lookup
# ===============================================================

def registry_lookup(company_name: str):

    try:

        url = (
            "https://api.opencorporates.com/v0.4/"
            f"companies/search?q={quote_plus(company_name)}"
        )

        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT
        )

        data = response.json()

        companies = (
            data.get("results", {})
            .get("companies", [])
        )

        if len(companies) == 0:

            return None

        return companies[0]["company"]

    except Exception:

        return None

# ===============================================================
# Sentiment
# ===============================================================

analyzer = SentimentIntensityAnalyzer()

def sentiment(text):

    try:

        return analyzer.polarity_scores(
            text
        )["compound"]

    except Exception:

        return 0

# ===============================================================
# Helper Functions
# ===============================================================

def safe(value):

    if value in (
        None,
        "",
        "None"
    ):
        return "N/A"

    return value

def format_currency(value):

    try:

        value = float(value)

        return f"${value:,.0f}"

    except Exception:

        return str(value)

def format_percentage(value):

    try:

        value = float(value)

        if value < 1:

            value *= 100

        return f"{value:.2f}%"

    except Exception:

        return str(value)
# ===============================================================
# Company Registry Analysis
# ===============================================================

async def company_registry_analysis(state: State):

    try:

        company = registry_lookup(state.company_name)

        if company:

            state.registry_details = f"""
Company Name      : {safe(company.get("name"))}
Company Number    : {safe(company.get("company_number"))}
Jurisdiction      : {safe(company.get("jurisdiction_code"))}
Status            : {safe(company.get("current_status"))}
Incorporated On   : {safe(company.get("incorporation_date"))}
Registry URL      : {safe(company.get("registry_url"))}
"""

        else:

            state.registry_details = (
                "No registry information available."
            )

    except Exception as e:

        state.registry_details = str(e)

    return state


# ===============================================================
# Financial Analysis
# ===============================================================

async def financial_analysis(state: State):

    try:

        symbol = await get_symbol(state.company_name)

        if symbol is None:

            state.financial_details = (
                "Unable to identify a listed company."
            )

            return state

        overview = get_company_overview(symbol)

        info = get_yfinance_info(symbol)

        state.financial_details = f"""
Ticker                : {symbol}

Exchange              : {safe(overview.get("Exchange"))}

Currency              : {safe(overview.get("Currency"))}

Sector                : {safe(overview.get("Sector"))}

Industry              : {safe(overview.get("Industry"))}

Country               : {safe(overview.get("Country"))}

Market Cap            : {format_currency(overview.get("MarketCapitalization"))}

Revenue TTM           : {format_currency(overview.get("RevenueTTM"))}

Gross Profit          : {format_currency(overview.get("GrossProfitTTM"))}

EBITDA                : {format_currency(overview.get("EBITDA"))}

EPS                   : {safe(overview.get("EPS"))}

Book Value            : {safe(overview.get("BookValue"))}

Dividend Per Share    : {safe(overview.get("DividendPerShare"))}

Dividend Yield        : {safe(info.get("dividendYield"))}

PE Ratio              : {safe(overview.get("PERatio"))}

PEG Ratio             : {safe(overview.get("PEGRatio"))}

Price To Book         : {safe(overview.get("PriceToBookRatio"))}

Profit Margin         : {format_percentage(overview.get("ProfitMargin"))}

Operating Margin      : {format_percentage(overview.get("OperatingMarginTTM"))}

ROA                   : {format_percentage(overview.get("ReturnOnAssetsTTM"))}

ROE                   : {format_percentage(overview.get("ReturnOnEquityTTM"))}

Current Ratio         : {safe(info.get("currentRatio"))}

Quick Ratio           : {safe(info.get("quickRatio"))}

Debt                  : {format_currency(info.get("totalDebt"))}

Cash                  : {format_currency(info.get("totalCash"))}

52 Week High          : {safe(info.get("fiftyTwoWeekHigh"))}

52 Week Low           : {safe(info.get("fiftyTwoWeekLow"))}

Analyst Recommendation: {safe(info.get("recommendationKey"))}
"""

    except Exception as e:

        state.financial_details = (
            f"Financial Analysis Failed : {e}"
        )

    return state


# ===============================================================
# Director Analysis
# ===============================================================

async def director_analysis(state: State):

    try:

        feed = google_news(
            f"{state.company_name} CEO director board management"
        )

        headlines = []

        if feed:

            for article in feed.entries[:10]:

                headlines.append(article.title)

        if len(headlines) == 0:

            state.director_details = (
                "No recent director related news found."
            )

        else:

            state.director_details = (
                "Director / Management News\n\n"
                + "\n".join(headlines)
            )

    except Exception as e:

        state.director_details = str(e)

    return state


# ===============================================================
# Litigation Analysis
# ===============================================================

async def litigation_analysis(state: State):

    try:

        feed = google_news(
            f"{state.company_name} lawsuit fraud investigation sec penalty court"
        )

        headlines = []

        if feed:

            for article in feed.entries[:10]:

                headlines.append(article.title)

        if len(headlines) == 0:

            state.litigation_details = (
                "No major litigation found."
            )

        else:

            state.litigation_details = (
                "Legal & Regulatory News\n\n"
                + "\n".join(headlines)
            )

    except Exception as e:

        state.litigation_details = str(e)

    return state


# ===============================================================
# News Analysis
# ===============================================================

async def news_analysis(state: State):

    try:

        feed = google_news(state.company_name)

        headlines = []

        scores = []

        if feed:

            for article in feed.entries[:20]:

                headlines.append(article.title)

                scores.append(
                    sentiment(article.title)
                )

        if len(scores):

            average = sum(scores) / len(scores)

        else:

            average = 0

        if average >= 0.25:

            overall = "Positive"

        elif average <= -0.25:

            overall = "Negative"

        else:

            overall = "Neutral"

        state.news_details = f"""
Average Sentiment Score

{average:.3f}

Overall Sentiment

{overall}

Recent Headlines

{'-'*70}

{chr(10).join(headlines)}
"""

    except Exception as e:

        state.news_details = str(e)

    return state
# ===============================================================
# Risk Scoring
# ===============================================================


async def risk_scoring(state: State) -> State:

    llm = UiPathAzureChatOpenAI(
        model="gpt-4o-mini-2024-07-18"
    )

    prompt = f"""
You are a Senior Commercial Underwriter.

Your job is to assess ONLY the company below.

==============================
COMPANY
==============================

Company:
{state.company_name}

Country:
{state.country}

==============================
REGISTRY
==============================

{state.registry_details}

==============================
FINANCIALS
==============================

{state.financial_details}

==============================
DIRECTORS
==============================

{state.director_details}

==============================
LITIGATION
==============================

{state.litigation_details}

==============================
NEWS
==============================

{state.news_details}

==============================

IMPORTANT

Only assess THIS company.

Ignore articles where another company is the main subject.

Ignore lawsuits involving other companies.

Ignore SEC news if it is unrelated to this company.

Ignore generic market news.

==============================

Score ONLY these categories.

Financial Risk (0-40)

0 = Excellent

40 = Extremely Poor

Litigation Risk (0-20)

0 = None

20 = Severe

News/Reputation Risk (0-20)

0 = Positive

20 = Extremely Negative

Governance Risk (0-10)

0 = Excellent

10 = Severe governance concerns

Registry Risk (0-10)

0 = Active company

10 = Dissolved / Suspended / Unknown

DO NOT calculate the risk category.

ONLY return JSON.

{{
    "financial_score":0,
    "litigation_score":0,
    "news_score":0,
    "governance_score":0,
    "registry_score":0,
    "reason":"Short explanation"
}}
"""

    response = await llm.ainvoke(prompt)

    try:

        text = response.content.strip()

        text = text.replace("```json", "")

        text = text.replace("```", "")

        result = json.loads(text)

        financial = int(result.get("financial_score", 20))
        litigation = int(result.get("litigation_score", 10))
        news = int(result.get("news_score", 10))
        governance = int(result.get("governance_score", 5))
        registry = int(result.get("registry_score", 5))

        score = (
            financial
            + litigation
            + news
            + governance
            + registry
        )

        score = max(0, min(score, 100))

        state.risk_score = score

        if score <= 20:
            state.risk_category = "LOW"

        elif score <= 40:
            state.risk_category = "MEDIUM"

        elif score <= 70:
            state.risk_category = "HIGH"

        else:
            state.risk_category = "CRITICAL"

        state.summary = f"""
Financial Risk : {financial}/40

Litigation Risk : {litigation}/20

News Risk : {news}/20

Governance Risk : {governance}/10

Registry Risk : {registry}/10

Reason

{result.get("reason","No explanation")}
"""

    except Exception as e:

        state.risk_score = 50

        state.risk_category = "MEDIUM"

        state.summary = f"Unable to calculate risk.\n\n{e}"

    return state

async def final_output(state: State) -> Output:

    llm = UiPathAzureChatOpenAI(
        model="gpt-4o-mini-2024-07-18"
    )

    prompt = f"""
Generate a professional underwriting report.

Company:
{state.company_name}

Country:
{state.country}

Registry:
{state.registry_details}

Financial:
{state.financial_details}

Director:
{state.director_details}

Litigation:
{state.litigation_details}

News:
{state.news_details}

Risk Score:
{state.risk_score}

Risk Category:
{state.risk_category}

Risk Summary:
{state.summary}

Write an enterprise-quality underwriting report.
"""

    response = await llm.ainvoke(prompt)

    return Output(
        company_name=state.company_name,
        risk_score=state.risk_score,
        risk_category=state.risk_category,
        summary=response.content
    )
# ===============================================================
# LangGraph
# ===============================================================

builder=StateGraph(
    State,
    input=Input,
    output=Output
)

builder.add_node(
    "company_registry_analysis",
    company_registry_analysis
)

builder.add_node(
    "financial_analysis",
    financial_analysis
)

builder.add_node(
    "director_analysis",
    director_analysis
)

builder.add_node(
    "litigation_analysis",
    litigation_analysis
)

builder.add_node(
    "news_analysis",
    news_analysis
)

builder.add_node(
    "risk_scoring",
    risk_scoring
)

builder.add_node(
    "final_output",
    final_output
)

builder.add_edge(
    START,
    "company_registry_analysis"
)

builder.add_edge(
    "company_registry_analysis",
    "financial_analysis"
)

builder.add_edge(
    "financial_analysis",
    "director_analysis"
)

builder.add_edge(
    "director_analysis",
    "litigation_analysis"
)

builder.add_edge(
    "litigation_analysis",
    "news_analysis"
)

builder.add_edge(
    "news_analysis",
    "risk_scoring"
)

builder.add_edge(
    "risk_scoring",
    "final_output"
)

builder.add_edge(
    "final_output",
    END
)

graph=builder.compile()    
    