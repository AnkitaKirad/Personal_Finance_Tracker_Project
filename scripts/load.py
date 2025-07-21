import os
import logging
import pyodbc
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# === Setup Logging ===
def setup_logger():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_dir = "logs/gold"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"gold_{timestamp}.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(console)
    logging.info("Gold Layer processing started.")
    return timestamp

# === Load DB Credentials ===
def load_db_credentials():
    load_dotenv()
    return {
        "server": os.getenv("SQL_SERVER"),
        "database": os.getenv("SQL_DATABASE"),
        "username": os.getenv("SQL_USERNAME"),
        "password": os.getenv("SQL_PASSWORD")
    }

# === Log Metadata ===
def update_metadata_log(proc_name, status, timestamp):
    metadata_file = "logs/gold/metadata_log.csv"
    os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
    log_entry = {
        "procedure": proc_name,
        "timestamp": timestamp,
        "status": status,
        "layer": "Gold"
    }
    df = pd.DataFrame([log_entry])
    if os.path.exists(metadata_file):
        df.to_csv(metadata_file, mode='a', header=False, index=False)
    else:
        df.to_csv(metadata_file, index=False)
    logging.info(f"Metadata logged for procedure: {proc_name}")

# === Call Stored Procedure ===
def call_stored_procedure(procedure_name, creds, timestamp):
    conn_str = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={creds['server']};"
        f"DATABASE={creds['database']};"
        f"UID={creds['username']};"
        f"PWD={creds['password']}"
    )
    try:
        with pyodbc.connect(conn_str) as conn:
            cursor = conn.cursor()
            logging.info(f"Executing: {procedure_name}")
            cursor.execute(f"EXEC {procedure_name}")
            conn.commit()
            logging.info(f"Successfully executed: {procedure_name}")
            update_metadata_log(procedure_name, "Success", timestamp)
    except Exception as e:
        logging.error(f"Failed to execute {procedure_name}: {e}", exc_info=True)
        update_metadata_log(procedure_name, "Failed", timestamp)

# === Main ===
if __name__ == "__main__":
    try:
        ts = setup_logger()
        creds = load_db_credentials()

        procedures = [
            "Gold.sp_upsert_dim_account",
            "Gold.sp_load_dim_category",
            "Gold.sp_load_fact_transactions"
        ]

        for proc in procedures:
            call_stored_procedure(proc, creds, ts)

        logging.info("Gold Layer completed successfully!")

    except Exception as e:
        logging.error("Gold layer failed.", exc_info=True)
