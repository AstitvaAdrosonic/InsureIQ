# Audit Agent

### Intelligent Document Intake & Submission Validation for Insurance Underwriting

**Part of the InsureIQ Multi-Agent Underwriting Platform**

---

# Overview

The Audit Agent is the entry point of the InsureIQ underwriting workflow and is responsible for initiating every underwriting case. Built using **UiPath Agent Builder**, it automates the intake, validation, and standardization of insurance submissions before any risk assessment begins.

Insurance submissions often arrive with multiple supporting documents such as proposal forms, financial statements, previous claim records, vessel information, and other underwriting documents. These files may differ in structure, format, and completeness, requiring significant manual effort before they can be reviewed by an underwriter.

The Audit Agent eliminates this manual process by reading incoming submissions, extracting relevant information, validating mandatory details, identifying missing information, and converting unstructured documents into a standardized format. This ensures that every downstream agent works with consistent, reliable, and validated underwriting data.

By acting as the gateway to the underwriting process, the Audit Agent establishes the foundation for accurate and efficient AI-assisted risk assessment.

---

# Purpose

The primary objective of the Audit Agent is to determine whether an insurance submission is complete, valid, and ready for underwriting.

Rather than allowing incomplete or inconsistent submissions to move through the underwriting workflow, the Audit Agent performs a comprehensive validation process and prepares a structured underwriting case for the Research Stage.

---

# Where the Agent Fits

The Audit Agent is the first AI agent executed within the InsureIQ workflow.

When a new underwriting submission is received, the Audit Agent processes the attached documents, validates the information, and stores the structured underwriting data in the UiPath Storage Bucket.

Only after successful validation are the Financial Risk Agent, Operational Risk Agent, and Claim History Agent triggered to begin their parallel assessments.

---

# Workflow

```
Insurance Submission Email
            │
            ▼

      Audit Agent

            │
            ▼

 Read Attached Documents

            │
            ▼

 Extract Underwriting Data

            │
            ▼

 Validate Submission

            │
            ▼

 Detect Missing Information

            │
            ▼

 Generate Structured JSON

            │
            ▼

 Store Data in UiPath Storage Bucket

            │
            ▼

 Trigger Research Stage
```

---

# Example Input

The Audit Agent receives an insurance submission through Microsoft Outlook.

### Example Email

**Subject**

```
Marine Cargo Insurance Submission – Navigator Holdings
```

**Body**

```
Dear Underwriting Team,

Please find attached our marine cargo insurance submission for
Navigator Holdings.

The submission includes the proposal form, financial statements,
previous claim records, vessel information, and supporting documents.

Kindly review and process the application.

Regards,

ABC Marine Brokers
```

---

# Example Supporting Documents

The Audit Agent can process multiple document types submitted as part of an underwriting request.

| Document | Purpose |
|-----------|---------|
| Proposal Form | Customer information |
| Financial Statements | Financial assessment |
| Previous Claims | Historical claims review |
| Vessel Information | Vessel details |
| Voyage Information | Operational assessment |
| Supporting Documents | Additional underwriting evidence |

---

# Information Extracted

After analysing the submitted documents, the Audit Agent prepares a structured underwriting record.

Example:

```json
{
  "company_name": "Navigator Holdings",
  "vessel_name": "Navigator Holdings",
  "origin_port": "Houston",
  "destination_port": "Singapore",
  "line_of_business": "Marine Cargo Insurance"
}
```

This standardized information becomes the common input for all research agents.

---

# Validation Performed

Before the submission proceeds further, the Audit Agent performs multiple validation checks.

## Mandatory Field Validation

The agent verifies that all required underwriting information is available.

Examples include:

- Company Name
- Vessel Name
- Origin Port
- Destination Port
- Line of Business

---

## Document Completeness

The agent confirms that all required supporting documents have been submitted.

Typical documents include:

- Proposal Form
- Financial Statements
- Previous Claims
- Vessel Information
- Supporting Documents

---

## Duplicate Submission Detection

To prevent redundant processing, the Audit Agent identifies duplicate submissions before creating a new underwriting case.

---

## Data Consistency

Information extracted from different documents is compared to identify inconsistencies.

Examples include:

- Company information
- Vessel details
- Voyage information
- Customer details

---

## Document Quality Assessment

The Audit Agent also checks for common document-related issues.

These include:

- Corrupted documents
- Password-protected files
- Unsupported formats
- Empty attachments
- Low-quality scans
- Missing pages

---

# Example Validation Result

```
Submission Validation Report

Company Name

Navigator Holdings

Submission Status

Validated

Documents Reviewed

✓ Proposal Form

✓ Financial Statements

✓ Previous Claims

✓ Vessel Information

✓ Voyage Information

Validation Summary

✓ All mandatory information available

✓ Required supporting documents received

✓ No duplicate submission detected

✓ Document consistency verified

Result

Submission approved for Research Stage.
```

---

# Agent Output

Once validation has been completed successfully, the Audit Agent generates a structured underwriting case.

```json
{
  "company_name": "Navigator Holdings",
  "vessel_name": "Navigator Holdings",
  "origin_port": "Houston",
  "destination_port": "Singapore",
  "line_of_business": "Marine Cargo Insurance",
  "submission_status": "Validated",
  "validation_result": "Success"
}
```

The generated information is stored in the UiPath Storage Bucket and becomes the shared input for all downstream research agents.

---

# Integration within InsureIQ

The Audit Agent is the first stage of the underwriting workflow.

```
              Microsoft Outlook
                      │
                      ▼

                Audit Agent

                      │
                      ▼

         UiPath Storage Bucket

                      │

      ┌───────────────┼───────────────┐

      ▼               ▼               ▼

Claim History   Financial Risk   Operational Risk
     Agent          Agent             Agent

      └───────────────┼───────────────┘
                      ▼

               Summary Agent
```

Unlike the Research Stage, which executes multiple agents in parallel, the Audit Agent completes its validation process before any risk assessment begins.

---

# Technology Stack

## UiPath Platform

- UiPath Agent Builder
- UiPath Orchestrator
- UiPath Storage Buckets
- UiPath Case Management
- UiPath Automation Cloud
- Microsoft Outlook Integration

## AI Capabilities

- Large Language Model (LLM)
- Intelligent Document Understanding
- Natural Language Processing
- Information Extraction
- Structured Data Generation

## Data Processing

- PDF Documents
- Microsoft Word Documents
- Excel Spreadsheets
- Images
- Structured JSON

---

# Key Features

- Automated email-based submission intake
- Intelligent document extraction
- Multi-format document support
- Mandatory field validation
- Missing information detection
- Duplicate submission detection
- Document consistency verification
- Structured underwriting case generation
- Integration with UiPath Storage Buckets
- Automatic initiation of the Research Stage

---

# Business Value

The Audit Agent removes one of the most time-consuming stages of the underwriting process by automatically validating insurance submissions before detailed risk analysis begins.

Rather than manually reviewing multiple documents for completeness and consistency, underwriters receive a standardized underwriting case that has already been verified for mandatory information, supporting documentation, and data quality.

By standardizing every submission at the point of entry, the Audit Agent reduces manual effort, improves data quality, minimizes processing delays, and enables downstream AI agents to perform reliable and consistent risk assessments.

---

# Future Enhancements

Future enhancements may include:

- Intelligent document classification
- Optical Character Recognition (OCR) for scanned documents
- Automatic broker identification
- Digital signature verification
- Fraud screening during submission
- Regulatory compliance validation
- Multi-language document processing
- Enterprise document management integration
- Confidence scoring for extracted information
- AI-assisted document quality assessment

---

# Part of InsureIQ

The Audit Agent serves as the gateway to the **InsureIQ Multi-Agent Underwriting Platform**. By transforming unstructured insurance submissions into validated and standardized underwriting data, it provides the foundation for efficient financial analysis, operational risk assessment, and historical claims evaluation. Its role ensures that every underwriting case begins with complete, consistent, and reliable information before progressing through the remainder of the workflow.