# Marine Operational Risk Assessment Agent

> **UiPath AgentHack 2026 Submission**

## Overview

Marine cargo insurance is becoming increasingly complex due to geopolitical instability, climate-related disruptions, piracy, congested shipping lanes, and changing operational conditions. Underwriters often need to consolidate information from multiple sources before making a decision, a process that is both time-consuming and difficult to standardize.

The **Marine Operational Risk Assessment Agent** was developed to automate this process by collecting operational intelligence, analysing maritime routes, assessing environmental and geopolitical risks, and generating a structured underwriting report using AI.

The solution is built using **UiPath Coded Agents**, **LangGraph**, and **Python**, demonstrating how AI agents can assist marine insurance professionals with faster and more consistent operational risk evaluation.

---

# Problem Statement

Marine underwriters and brokers regularly face questions such as:

* Does the voyage pass through high-risk conflict zones?
* Are there severe weather conditions expected along the route?
* Are there recent piracy or maritime security incidents?
* Is the route operationally safe?
* How should all these factors influence underwriting decisions?

Gathering this information manually requires consulting several independent sources, making the process inefficient and inconsistent.

---

# Solution

The Marine Operational Risk Assessment Agent automates operational risk assessment by combining multiple intelligence sources into a single underwriting workflow.

The agent performs the following sequence:

1. Receives vessel information and voyage details.
2. Generates the complete sea route.
3. Detects strategic maritime choke points.
4. Evaluates weather conditions across the voyage.
5. Collects and analyses maritime news.
6. Assesses geopolitical conflict exposure.
7. Performs sentiment analysis on current maritime events.
8. Calculates an overall operational risk score.
9. Generates an AI-assisted underwriting report.

---

# Risk Assessment Components

## Route Intelligence

* Sea route generation
* Voyage distance calculation
* Chokepoint detection
* Operational route risk

Examples include:

* Strait of Hormuz
* Gulf of Aden
* Red Sea
* Suez Canal
* Gulf of Guinea

---

## Weather Intelligence

Weather conditions are evaluated across multiple points along the voyage using marine weather services.

Parameters include:

* Wave height
* Average sea state
* Maximum sea state
* Severe weather locations

---

## Maritime News Intelligence

The agent continuously analyses maritime news feeds to detect operational events such as:

* Piracy
* Missile attacks
* Port congestion
* Vessel collisions
* Labour strikes
* Sanctions
* Route closures
* Security incidents

---

## Conflict Intelligence

Conflict monitoring focuses on major global shipping corridors including:

* Red Sea
* Gulf of Aden
* Persian Gulf
* Suez Canal

Current humanitarian and geopolitical reports are analysed to estimate operational exposure.

---

## Sentiment Intelligence

Natural language processing is used to measure the overall sentiment of maritime intelligence.

This helps identify periods of elevated operational concern where negative reporting significantly increases voyage uncertainty.

---

# Enterprise Risk Scoring

Each intelligence module contributes independently to the overall operational assessment.

The scoring engine evaluates:

* Route Risk
* Weather Risk
* News Risk
* Conflict Risk
* Sentiment Risk

These scores are combined into a normalized enterprise risk score and classified as:

* LOW
* MEDIUM
* HIGH
* CRITICAL

---

# AI Generated Underwriting Report

The final output is a professional report summarising:

* Executive Summary
* Route Assessment
* Weather Analysis
* Operational Concerns
* Conflict Exposure
* News Intelligence
* Recommended Mitigation Measures
* Insurance Considerations
* Overall Risk Classification

---

# Technology Stack

* UiPath Coded Agents
* UiPath Agent Builder
* LangGraph
* Python
* Pydantic
* Open-Meteo Marine API
* ReliefWeb API
* RSS Maritime Intelligence
* VADER Sentiment Analysis

---

# Project Structure

```
OperationalRiskAgent
│
├── main.py
├── services
│   ├── route_analysis.py
│   ├── weather_analysis.py
│   ├── news_analysis.py
│   ├── conflict_analysis.py
│   ├── sentiment_analysis.py
│   └── risk_scoring.py
│
├── data
│   └── ports.json
│
├── input.json
└── README.md
```

---

# Example Input

```json
{
  "vessel_name": "Navigator Holdings",
  "origin_port": "Houston",
  "destination_port": "Singapore"
}
```

---

# Example Output

```
Operational Risk Score : 91 / 100

Category : CRITICAL

Primary Risk Drivers

• High-risk maritime route
• Conflict zone exposure
• Operational disruptions
• Negative maritime intelligence
```

---

# Future Enhancements

* AIS vessel tracking integration
* Live piracy databases
* Port congestion prediction
* Marine catastrophe forecasting
* Cargo-specific underwriting recommendations
* Historical voyage benchmarking
* Insurance premium estimation
* Fleet-wide operational monitoring

---

# Why This Matters

Operational risk is one of the most significant factors affecting marine insurance decisions.

By combining route intelligence, weather analytics, geopolitical monitoring, maritime news, and AI-generated reporting into a single workflow, this project demonstrates how autonomous AI agents can support faster, more informed, and more consistent underwriting decisions.

---

### Developed for UiPath AgentHack 2026
