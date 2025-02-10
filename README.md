
# Coinbase-to-Snowflake-Django-Streamlit Project

## Overview

This project ingests cryptocurrency data from Coinbase’s currencies API, loads it into a Snowflake database, exposes the data via a Django REST API with three authorization levels, and visualizes the data through separate Streamlit applications. The three authorization levels are defined as follows:

- **Level 1 (Public):**  
  Minimal data (e.g. ID, status). No authentication required.

- **Level 2 (Authenticated):**  
  A moderate subset of fields (e.g. ID, name, min_size, status, default_network, display_name). Accessible after login via the custom login API endpoint.

- **Level 3 (Admin):**  
  All available data fields. Accessible only for admin users (those with `is_staff` or `is_superuser` set to True).

The project also includes a custom login API endpoint that allows users to log in using session-based authentication so that the Streamlit apps can simulate a login and then access protected endpoints.

---

## Project Structure

```
coinbaseapi/
├── api/
│   ├── __init__.py
│   ├── urls.py              # API URL configuration (includes endpoints for login, level1, level2, level3)
│   └── views.py             # Django API views for login and data endpoints
├── ingest_to_snowflake_csv.py  # Script to fetch Coinbase API data, convert it to CSV, and load it into Snowflake
├── README.md              # This file
├── manage.py              # Django project management file
├── requirements.txt       # Python package dependencies
├── streamlit_level1.py    # Streamlit app for Level 1 visualization (public)
├── streamlit_level2.py    # Streamlit app for Level 2 visualization (authenticated user)
└── streamlit_level3.py    # Streamlit app for Level 3 visualization (admin)
```

---

## Flow Diagram

Below is a Mermaid flow diagram that illustrates the overall project flow:

```mermaid
flowchart TD
    A[Coinbase API Data Source]
    B[Data Ingestion Script]
    C[CSV File]
    D[Snowflake: CURRENCIES Table]
    E[Django REST API]
    F[Login Endpoint<br/>(/api/login/)]
    G[Level 1 Endpoint<br/>(/api/level1/currencies/)]
    H[Level 2 Endpoint<br/>(/api/level2/currencies/)]
    I[Level 3 Endpoint<br/>(/api/level3/currencies/)]
    J[Streamlit App Level 1]
    K[Streamlit App Level 2]
    L[Streamlit App Level 3]

    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    E --> G
    E --> H
    E --> I
    G --> J
    H --> K
    I --> L
```

*How It Works:*  
1. The **Data Ingestion Script** (`ingest_to_snowflake_csv.py`) fetches JSON data from Coinbase, converts it to CSV (ensuring all keys appear as columns), drops any existing **CURRENCIES** table, creates a new one, and loads the CSV data into Snowflake.  
2. The **Django REST API** queries Snowflake and exposes endpoints:  
   - **Level 1:** Returns minimal fields.  
   - **Level 2:** Returns a moderate subset (requires login).  
   - **Level 3:** Returns all data (admin-only).  
3. The **Custom Login API Endpoint** (`/api/login/`) allows users to log in (and obtain a session cookie).  
4. The **Streamlit apps** use session-based login (or token-based authentication) to fetch and visualize the data at their respective levels.

---

## Installation and Setup

### Prerequisites

- **Python 3.8+** (with `pip`)  
- **Django** and **Django REST Framework**  
- **Streamlit**  
- **Snowflake Connector for Python**  
- A **Snowflake Account**  
- **SnowSQL** (for command‑line interactions with Snowflake; see installation instructions below)  
- An Arch-based Linux distribution (e.g., Garuda Linux) for SnowSQL installation

### 1. Clone the Repository and Install Dependencies

```bash
git clone https://github.com/yourusername/coinbaseapi.git
cd coinbaseapi
pip install -r requirements.txt
```

*Example `requirements.txt` might include:*
```
Django>=3.2
djangorestframework
requests
snowflake-connector-python
streamlit
```

### 2. Configure Your Django Project

- Update your Django settings with your Snowflake credentials.
- Make sure the apps `api` and `rest_framework` (plus `rest_framework.authtoken` if using token auth) are added to `INSTALLED_APPS`.

### 3. Load Data into Snowflake

Run the ingestion script to fetch data from Coinbase, convert it to CSV, drop/recreate the table, and load data:

```bash
python ingest_to_snowflake_csv.py
```

### 4. Run the Django Server

Start the Django development server:

```bash
python manage.py runserver
```

Your API endpoints will be available at:  
- Public: [http://127.0.0.1:8000/api/level1/currencies/](http://127.0.0.1:8000/api/level1/currencies/)  
- Login: [http://127.0.0.1:8000/api/login/](http://127.0.0.1:8000/api/login/)  
- Level 2: [http://127.0.0.1:8000/api/level2/currencies/](http://127.0.0.1:8000/api/level2/currencies/)  
- Level 3: [http://127.0.0.1:8000/api/level3/currencies/](http://127.0.0.1:8000/api/level3/currencies/)

### 5. Run the Streamlit Applications

Open three separate terminals (or tabs) and run:

- **Level 1 (Public):**

  ```bash
  streamlit run streamlit_level1.py --server.port 8501
  ```

- **Level 2 (Authenticated):**

  ```bash
  streamlit run streamlit_level2.py --server.port 8502
  ```

- **Level 3 (Admin):**

  ```bash
  streamlit run streamlit_level3.py --server.port 8503
  ```

---

## Installing SnowSQL on Garuda Linux

Garuda Linux is an Arch-based distribution. The recommended way to install SnowSQL on Arch-based systems is to use an AUR helper (like `yay`) to install the AUR package.

### Steps to Install SnowSQL on Garuda Linux



## Summary

1. **Data Flow:**  
   - Data is ingested from Coinbase, converted to CSV, and loaded into Snowflake.
   - Django REST API queries Snowflake and serves data via endpoints protected at three levels.
   - Custom login API enables session-based authentication.
   - Separate Streamlit apps visualize data at each authorization level.

