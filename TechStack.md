# Tech Stack and Protocols

This document outlines the technology stack, protocols, and data models for the Edge-Native Terminology Service.

## Tech Stack

*   **Backend Framework:** FastAPI (Python)
*   **Database:** SQLite
*   **Data Harmonization Library:** `fhir.resources` (Python)
*   **Demonstration UI:** Streamlit (Python)

## Protocols

*   **FHIR (Fast Healthcare Interoperability Resources):** The core standard for structuring and exchanging healthcare data.
*   **HTTP/S:** Standard protocol for the API endpoints.
*   **OAuth 2.0:** For secure, authorized data synchronization with a central server.

## Data Models

### Terminology Models
*   **NAMASTE:** Source terminology.
*   **WHO International Ayurveda Terminology:** Intermediate standard terminology.
*   **WHO ICD-11 (TM2 & Biomedicine):** Target terminology for final mapping.

### FHIR Resource Models
*   **`CodeSystem`:** Represents the NAMASTE and WHO Ayurveda terminologies.
*   **`ConceptMap`:** Defines the multi-step harmonization pathway (NAMASTE -> WHO Ayurveda -> ICD-11).
*   **`Bundle`:** Packages encounter data for submission from EMRs.
*   **`Consent`:** Manages patient consent for data sharing, included within the `Bundle`.
