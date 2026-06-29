Financial Risk Agent 

An enterprise AI underwriting agent built using **UiPath Coded Agents**, **LangGraph**, and trusted public data sources to automate the financial due diligence of companies involved in marine cargo shipments.

---

# Overview

Marine cargo insurance underwriting involves much more than assessing a vessel or shipment. One of the most critical aspects of underwriting is understanding the financial strength and credibility of the companies involved throughout the supply chain.

Before issuing a policy, underwriters often need to evaluate:

* Exporters
* Importers
* Freight Forwarders
* Logistics Providers
* Ship Owners
* Charterers
* Trading Companies

This process typically requires collecting financial information from multiple sources, reviewing corporate records, checking recent legal developments, and analysing market sentiment.

The Financial Risk Assessment Agent automates this workflow and produces a structured underwriting report within minutes.

---

# Problem Statement

Financial due diligence is one of the most time-consuming activities during marine cargo underwriting.

Underwriters often spend hours searching multiple platforms to answer questions such as:

* Is the company financially stable?
* Has the company been involved in recent litigation?
* Are there any governance concerns?
* Has the company recently experienced financial distress?
* Is there any adverse media coverage?
* Does the company's financial position increase the probability of claim or default?

Manual research is inconsistent, expensive, and difficult to scale across thousands of submissions.

---

# Solution

The Financial Risk Assessment Agent acts as an AI underwriting assistant that automatically gathers and analyses publicly available information about the insured company.

The agent:

* Identifies the correct listed company
* Retrieves financial metrics
* Verifies corporate registration
* Analyses executive and management updates
* Reviews litigation and regulatory news
* Evaluates recent market sentiment
* Performs an AI-based underwriting assessment
* Generates a professional underwriting report

The final output provides underwriters with a consolidated view of the company's financial health before making underwriting decisions.

---

# Marine Cargo Insurance Workflow

```text
Cargo Insurance Submission
            │
            ▼
Extract Company Information
            │
            ▼
Financial Risk Assessment Agent
            │
            ├── Company Registry Verification
            ├── Financial Analysis
            ├── Director & Governance Review
            ├── Litigation Assessment
            ├── News & Reputation Analysis
            ▼
AI Underwriting Risk Evaluation
            │
            ▼
Professional Underwriting Report
            │
            ▼
Supports Marine Cargo Underwriter
```

---

# Key Features

* Automated company identification
* Intelligent stock ticker selection using AI
* Financial statement analysis
* Revenue and profitability assessment
* Corporate registry verification
* Director and executive analysis
* Litigation monitoring
* News sentiment analysis
* AI-driven underwriting risk evaluation
* Professional underwriting report generation

---

# Technology Stack

### AI & Agent Framework

* UiPath Coded Agents
* LangGraph
* UiPath Azure OpenAI

### Programming

* Python
* Pydantic

### Public Data Sources

* Alpha Vantage
* Yahoo Finance
* OpenCorporates
* Google News RSS

### Analysis Libraries

* Feedparser
* Requests
* VADER Sentiment

---

# Public Data Sources

The project intentionally relies on publicly available services to demonstrate a scalable and cost-effective underwriting workflow.

| Source          | Purpose                                            |
| --------------- | -------------------------------------------------- |
| Alpha Vantage   | Company discovery and financial market information |
| Yahoo Finance   | Financial ratios and company fundamentals          |
| OpenCorporates  | Corporate registration verification                |
| Google News RSS | Litigation and market news                         |
| VADER Sentiment | News sentiment analysis                            |

---

# Example Input

```json
{
    "company_name": "Navigator Holdings",
    "country": "USA"
}
```

---

# Example Output

The generated underwriting report includes:

* Company Overview
* Financial Health
* Revenue Analysis
* Liquidity Assessment
* Profitability Assessment
* Corporate Registry Details
* Director & Governance Review
* Litigation Summary
* News Sentiment
* Overall Financial Risk Score
* Underwriting Recommendation

---

# Business Value

The Financial Risk Assessment Agent enables marine cargo insurers to:

* Reduce manual underwriting effort
* Improve consistency in financial due diligence
* Detect financially distressed companies early
* Identify emerging legal or governance risks
* Support faster policy issuance
* Improve underwriting quality using explainable AI

---

# Running the Project

Install dependencies

```bash
pip install -r requirements.txt
```

Run the agent

```bash
uip codedagent run agent --file input.json
```

Deploy to UiPath

```bash
uip codedagent deploy --my-workspace
```

---

# Future Roadmap

This Financial Risk Agent is designed as one component of the broader **AdroForge AI Underwriting Platform**.

Planned agents include:

* Marine Route Risk Assessment Agent
* Weather & Natural Catastrophe Risk Agent
* Piracy & Geopolitical Risk Agent
* Operational Risk Assessment Agent
* Cargo Classification Agent
* OCR & Document Intelligence Agent
* Underwriting Decision Support Agent
* Portfolio Risk Monitoring Agent

Together, these agents provide an end-to-end AI-powered underwriting ecosystem for marine cargo insurance.

---

# About AdroForge

Financial Risk Assesment Agent  is an AI-powered agent designed to modernize marine cargo insurance by combining intelligent agents, public data sources, and enterprise AI to support faster, more informed, and more consistent underwriting decisions.

---

# Author

**Astitva Singh**

Developed for the **UiPath AI Agent Hackathon 2026**
