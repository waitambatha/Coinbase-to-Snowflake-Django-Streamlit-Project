import requests
import csv
import json
import os
import snowflake.connector
from dotenv import load_dotenv



# Load environment variables from the .env file located in the project root
load_dotenv()

# Retrieve Snowflake credentials from the environment variables
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
# ----- STEP 1: Fetch JSON Data from the API -----
url = "https://api.exchange.coinbase.com/currencies"
response = requests.get(url)
if response.status_code != 200:
    raise Exception("Failed to fetch data from the API")
data = response.json()  # List of currency objects

# ----- STEP 2: Convert JSON Data to CSV File -----
# Collect the union of all keys
all_keys = set()
for record in data:
    all_keys.update(record.keys())
# For consistency, sort the keys
all_keys = sorted(all_keys)

csv_file = "../currencies.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=all_keys)
    writer.writeheader()
    for record in data:
        row = {}
        for key in all_keys:
            val = record.get(key)
            # For dicts or lists, dump as JSON string; otherwise, leave as is.
            if isinstance(val, (dict, list)):
                row[key] = json.dumps(val)
            else:
                row[key] = val
        writer.writerow(row)
print(f"CSV file written to {csv_file}")

# ----- STEP 3: Connect to Snowflake and (Re)Create the Table -----
conn = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA

)
cs = conn.cursor()

try:
    # Drop the table if it exists
    cs.execute("DROP TABLE IF EXISTS CURRENCIES")

    # Create the table using the CSV headers. We create columns as VARCHAR.
    # (For simplicity, we convert header names to uppercase.)
    cols = []
    for key in all_keys:
        cols.append(f'"{key.upper()}" VARCHAR')
    create_stmt = "CREATE TABLE CURRENCIES (" + ", ".join(cols) + ")"
    cs.execute(create_stmt)
    print("Table CURRENCIES created.")

    # ----- STEP 4: Upload CSV File and Load Data into Snowflake -----
    abs_csv_path = os.path.abspath(csv_file)
    # The @%CURRENCIES stage is an internal stage for the table.
    put_stmt = f"PUT file://{abs_csv_path} @%CURRENCIES auto_compress=true"
    cs.execute(put_stmt)
    print("CSV file uploaded to internal stage.")

    # Use COPY INTO to load the CSV data into the table.
    copy_stmt = """
        COPY INTO CURRENCIES
        FILE_FORMAT = (
            TYPE = 'CSV'
            FIELD_OPTIONALLY_ENCLOSED_BY = '\"'
            SKIP_HEADER = 1
        )
    """
    cs.execute(copy_stmt)
    print("Data loaded into table CURRENCIES.")

    conn.commit()
finally:
    cs.close()
    conn.close()
