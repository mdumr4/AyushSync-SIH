# Edge-Native Terminology Service

This project is a lightweight, secure, and robust microservice that harmonizes three key terminologies (NAMASTE, WHO International Ayurveda, and WHO ICD-11) and makes them easily accessible to EMR systems, in full compliance with India’s 2016 EHR Standards.

## Core Objective

To design, build, and deliver a lightweight, secure, and robust microservice that harmonizes three key terminologies (NAMASTE, WHO International Ayurveda, and WHO ICD-11) and makes them easily accessible to EMR systems, in full compliance with India’s 2016 EHR Standards.

## Features

*   **Data Harmonization:** Harmonizes NAMASTE, WHO International Ayurveda, and WHO ICD-11 terminologies.
*   **FHIR Compliant API:** Exposes the harmonized data through a secure and compliant FHIR API.
*   **Data Capture:** Implements a workflow for receiving data from EMRs.
*   **Security:** Includes consent validation and OAuth 2.0 authentication.
*   **Synchronization:** Keeps the local database updated with the latest terminology versions.
*   **Demonstration UI:** A Streamlit-based web UI to demonstrate the service's capabilities.

## Getting Started

### Prerequisites

*   Python 3.10+
*   Pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd SIH
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r prototype/requirements.txt
    ```

### Running the Application

1.  Run the ingestion script to populate the database:
    ```bash
    python prototype/scripts/ingest.py
    ```
2.  Run the application:
    ```bash
    python prototype/app.py
    ```

## Project Structure

```
.
├── app/
│   └── main.py
├── scripts/
│   └── ingest.py
├── data/
│   ├── NAMASTE.csv
│   └── WHO_Ayurveda_Terms.csv
├── tests/
├── .gitignore
├── gemini.md
├── install_and_run.bat
├── README.md
├── requirements.txt
└── run_prototype.bat
```
