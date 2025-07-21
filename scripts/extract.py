#To do all the operating system related operations like reading writing the file or creating directory etc
import os
#To work with json file
import json
#Using python default logging module to create the log files
import logging
from datetime import datetime, timedelta,date
#To load the data from the env file
from dotenv import load_dotenv
import time
import csv

#Plaid SDK integrated with python
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.sandbox_public_token_create_request import SandboxPublicTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid import ApiClient, Configuration
from plaid.exceptions import ApiException

#convert  date fucntion to convert the date in the response to string as JSON doesn't support datetime
def convert_dates(obj):
    if isinstance(obj, dict):
        return {k: convert_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_dates(item) for item in obj]
    elif isinstance(obj, (date, datetime)):
        return obj.isoformat()
    else:
        return obj
    
def write_metadata_log(metadata, log_path='logs/audit/control_log.csv'):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    file_exists = os.path.exists(log_path)

    with open(log_path, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=metadata.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(metadata)

# Step 1: Setup Logging
def setup_logger():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = "logs/extract"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"extract_{timestamp}.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)

    logging.info("Extracting data from Plaid Sandbox")
    return timestamp

# Step 2: Load API credentials from the env file by using dotenv module of python
def load_credentials():
    load_dotenv()
    return {
        "client_id": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
        "env": os.getenv("PLAID_ENV", "sandbox")
    }

# Step 3: Connect to Plaid creating a client object steup that can help us for further endpoints call
def get_plaid_client(creds):
    configuration = Configuration(
        host="https://sandbox.plaid.com",
        api_key={
            "clientId": creds["client_id"],
            "secret": creds["secret"],
        }
    )
    api_client = ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)

# Step 4: Get transactions from Plaid
def fetch_transactions(client):
    # Create public token using the https://sandbox.plaid.com/sandbox/public_token/create endpoint
    public_token_response = client.sandbox_public_token_create(
        SandboxPublicTokenCreateRequest(
            institution_id="ins_109508",
            initial_products=[Products("transactions")],
        )
    )
    public_token = public_token_response.public_token
    logging.info("Created sandbox public token")

    # Exchange for access token givng the public token to this endpoint to get access token https://sandbox.plaid.com/item/public_token/exchange
    exchange_response = client.item_public_token_exchange(
        ItemPublicTokenExchangeRequest(public_token=public_token)
    )
    access_token = exchange_response.access_token
    logging.info("Exchanged public token for access token")

    # Request transactions using https://sandbox.plaid.com/transactions/get endpoint
    start_date = (datetime.now() - timedelta(days=30)).date()
    end_date = datetime.now().date()
    #request = TransactionsGetRequest(
    #    access_token=access_token,
    #    start_date=start_date,
    #    end_date=end_date,
    #    options=TransactionsGetRequestOptions(count=100, offset=0)
    #)

    #response = client.transactions_get(request)

    max_retries = 5
    for attempt in range(max_retries):
        try:
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date,
                end_date=end_date,
                options=TransactionsGetRequestOptions(count=100, offset=0)
            )
            response = client.transactions_get(request)
            logging.info("Pulled transaction data from Plaid")
            #print("Pulled transaction data from Plaid")
            break  # exit loop on success

        except ApiException as e:
            if "PRODUCT_NOT_READY" in str(e):
                print(f"🔄 Transaction data not ready, retrying... ({attempt+1}/{max_retries})")
                time.sleep(5)  # wait 5 seconds
            else:
                raise e

    return convert_dates(response.to_dict())

# Step 5: Save raw data to Bronze Layer
def save_to_bronze(data, timestamp):
    bronze_dir = "data/bronze"
    os.makedirs(bronze_dir, exist_ok=True)
    filename = os.path.join(bronze_dir, f"transactions_{timestamp}.json")

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    logging.info(f"Raw transaction data saved to: {filename}")

# === Main ETL Flow ===
if __name__ == "__main__":
    metadata = {
        "run_id": None,
        "start_time": None,
        "end_time": None,
        "status": "FAILED",
        "records_extracted": 0,
        "file_written_to": None,
        "error_message": None
    }

    try:
        ts = setup_logger()
        metadata["run_id"] = ts
        metadata["start_time"] = datetime.now().isoformat()

        creds = load_credentials()
        client = get_plaid_client(creds)
        transactions = fetch_transactions(client)

        metadata["records_extracted"] = len(transactions.get("transactions", []))

        save_to_bronze(transactions, ts)
        metadata["file_written_to"] = f"data/bronze/transactions_{ts}.json"
        metadata["status"] = "SUCCESS"
        logging.info("Data successfully extracted and stored to bronze layer.")

    except Exception as e:
        logging.error("Extraction failed", exc_info=True)
        metadata["error_message"] = str(e)

    finally:
        metadata["end_time"] = datetime.now().isoformat()
        write_metadata_log(metadata)
        logging.info("Control metadata logged.")
