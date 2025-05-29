import sqlite3
import json
from datetime import datetime

DB_PATH = "remediation.db"


def fetch_all_errors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, error_hash, timestamp, message, level, remediation FROM errors ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def format_timestamp(timestamp):
    """Format the timestamp to be more readable."""
    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp


def main():
    rows = fetch_all_errors()
    if not rows:
        print("No records found in the errors table.")
        return

    print("\n" + "=" * 100)
    print("REMEDIATION DATABASE CONTENTS")
    print("=" * 100)

    for row in rows:
        id, error_hash, timestamp, message, level, remediation = row
        remediation_data = json.loads(remediation)

        print("\n" + "-" * 100)
        print(f"Record ID: {id}")
        print(f"Timestamp: {format_timestamp(timestamp)}")
        print(f"Error Hash: {error_hash}")
        print(f"Message: {message}")
        print(f"Level: {level}")
        print("\nREMEDIATION:")
        print(json.dumps(remediation_data, indent=2))
        print("-" * 100)


if __name__ == "__main__":
    main() 