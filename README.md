

---

```markdown
# Coinbase-to-Snowflake-Django-Streamlit Project

## Overview

This project ingests cryptocurrency data from Coinbase’s currencies API, loads it into a Snowflake database, exposes the data via a Django REST API with three authorization levels, and visualizes the data using separate Streamlit applications. A custom login API endpoint is provided so that users can log in via session-based authentication. The three authorization levels are:

- **Level 1 (Public):** Minimal data (e.g. ID, status). No authentication required.
- **Level 2 (Authenticated):** A moderate subset of fields (e.g. ID, name, min_size, status, default_network, display_name). Requires login.
- **Level 3 (Admin):** All available fields. Accessible only to admin users (users with `is_staff` or `is_superuser` set to true).

---

## Project Structure

```
coinbaseapi/
├── .env                     # Environment variables file (contains Snowflake credentials)
├── .gitignore               # Git ignore file (excludes .env and other sensitive files)
├── ingest_to_snowflake_csv.py   # Script to ingest data: fetch JSON from Coinbase, convert to CSV, load into Snowflake
├── manage.py                # Django project management file
├── api/                     # Django app containing API views and URL configuration
│   ├── __init__.py
│   ├── urls.py              # API endpoints: login, level1, level2, level3
│   └── views.py             # API views implementation (custom login, data endpoints)
├── requirements.txt         # Python package dependencies
├── streamlit_level1.py      # Streamlit app for Level 1 (public) visualization
├── streamlit_level2.py      # Streamlit app for Level 2 (authenticated) visualization
└── streamlit_level3.py      # Streamlit app for Level 3 (admin) visualization
```

---

You can paste this snippet into your `README.md` file. Make sure your project’s root directory (where `manage.py` resides) contains the `.env` and `.gitignore` files as indicated, ensuring your sensitive configuration remains secure.
