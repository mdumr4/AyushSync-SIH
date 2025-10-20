# SIH Project: Edge-Native Terminology Service - Definitive Project Plan

This document outlines the definitive, step-by-step plan to build the production-ready Edge-Native Terminology Service. This plan is meticulously aligned with every requirement of the SIH problem statement and includes our winning-strategy features.

## 1. Core Objective

To design, build, and deliver a lightweight, secure, and robust microservice that harmonizes three key terminologies (NAMASTE, WHO International Ayurveda, and WHO ICD-11) and makes them easily accessible to EMR systems, in full compliance with India’s 2016 EHR Standards.

---

## 2. Phased Development Plan

### **Phase 1: The Data Foundation - Multi-Source Harmonization**

**Goal:** To create a single, clean, and structured SQLite database that contains all the harmonized data from the three required sources, respecting their distinct roles and the rules of the target systems.

*   **Task 1.1: Project Scaffolding**
    *   Create directory structure: `app/`, `scripts/`, `data/`, `tests/`.
    *   Initialize `requirements.txt` with all necessary libraries.
    *   Place placeholder data files in `data/`: `NAMASTE.csv`, `WHO_Ayurveda_Terms.csv`.

*   **Task 1.2: Build the Ingestion Script (`scripts/ingest.py`)**
    *   **Sub-Task 1.2.1 (Data Ingestion):** Implement logic to read `NAMASTE.csv`, `WHO_Ayurveda_Terms.csv`, and to fetch live data from the WHO ICD-11 API (TM2 & Biomedicine).
    *   **Sub-Task 1.2.2 (Generate `CodeSystem` Resources):** Use `fhir.resources` to create **two distinct `CodeSystem` resources**: one for NAMASTE and one for the "WHO Standardised International Terminologies for Ayurveda".
    *   **Sub-Task 1.2.3 (Generate Multi-Step `ConceptMap`):** Generate a sophisticated FHIR `ConceptMap` that models the full, three-step harmonization pathway: **NAMASTE -> WHO Ayurveda Term -> ICD-11 Code**.
    *   **Sub-Task 1.2.4 (Implement ICD-11 Coding Rules):** The `ConceptMap` generation logic will be enhanced to include rules for ICD-11 compliance, such as defining code clusters or post-coordination where necessary, ensuring the output is not just mapped, but correctly structured.

*   **Task 1.3: Database Persistence**
    *   Define the SQLite schema to store the concepts from all three sources and the multi-step mappings.
    *   The ingestion script will populate the `terminology.db` with this rich, harmonized data.

### **Phase 2: The Core FHIR API**

**Goal:** To expose the harmonized data through a set of secure, compliant, and high-performance API endpoints.

*   **Task 2.1: Basic API Setup (`app/main.py`)**
    *   Initialize the FastAPI application and database connection logic.

*   **Task 2.2: Implement Terminology Endpoints**
    *   **Auto-Complete (`/ValueSet/$lookup`):** The response for this endpoint will be enhanced to show the full mapping pathway (NAMASTE -> WHO Ayurveda -> ICD-11) and any relevant coding rules (e.g., "This code should be clustered with...").
    *   **Translation (`/ConceptMap/$translate`):** The translation endpoint will support multi-step translations.
    *   **Dedicated ICD-11 Lookup (`/icd11-lookup`):** Create a new, optimized endpoint for fast searching of only the ICD-11 Biomedicine codes.

### **Phase 3: Data Capture, Security, and Synchronization**

**Goal:** To implement the workflow for receiving data from EMRs and to build the robust, secure synchronization service.

*   **Task 3.1: Implement Encounter Upload Endpoint (`/Bundle`)**
    *   Create the POST endpoint to accept FHIR `Bundle` submissions.
    *   **Add Consent Validation:** The endpoint will inspect the bundle for a `Consent` resource and validate its status (e.g., `active`, `rejected`). Bundles with invalid or rejected consent will be flagged.
    *   The endpoint will save the entire valid bundle to the `upload_queue` table in the SQLite database.

*   **Task 3.2: Build the Synchronization Service (`sync_service.py`)**
    *   Create a background service to process the `upload_queue`.
    *   **Uploader Logic with Consent Check:** Before uploading, the service will re-verify the consent status within the stored bundle. Bundles without active consent will **not** be sent to the central server and will be moved to a local quarantine state for audit purposes.
    *   **OAuth 2.0 Client:** The service will read a stored ABHA token and use it in the `Authorization: Bearer` header for all outgoing requests to the central server.
    *   **Updater & Versioning Logic:** The service will periodically check for new terminology versions and trigger the ingestion script to keep the local database updated.

### **Phase 4: Demonstration and Verification**

**Goal:** To create a simple but effective user interface to demonstrate the service's advanced capabilities.

*   **Task 4.1: Build a Simple Web UI (`demo.py`)**
    *   Using `Streamlit`, create an interactive web application.

*   **Task 4.2: Implement Demonstration Features**
    *   **Showcase Multi-Step Mapping:** The search results will visually display the NAMASTE -> WHO Ayurveda -> ICD-11 harmonization chain.
    *   **Showcase Biomedicine Lookup:** The UI will have a separate search bar for the dedicated `/icd11-lookup` endpoint.
    *   **Showcase Consent:** The UI will include a sample checkbox for "Patient Consent Given" and will show how the `Consent` resource is constructed and added to the FHIR Bundle before submission, demonstrating the consent-aware workflow.