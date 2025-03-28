"""
Author: Peiqi Wang
Course: CST8002 Practical Project 3
Professor: Tyler DeLay
Due Date: 2025-03-16
Description:
This is a persistence layer that contains functions to handle database operations.
"""

#import mysql.connector
import csv
#from mysql.connector import Error

import pymysql
from pymysql.err import MySQLError

# Database Connection Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "shihuai",
    "database": "record_management"
}

# Connect to MySQL
def connect_db():
    print("Trying to connect to MySQL...")
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="shihuai",
            database="record_management",
            cursorclass=pymysql.cursors.Cursor  # Optional: can also use DictCursor
        )
        print("Connection successful.")
        return conn
    except MySQLError as e:
        print(f"Error connecting to database: {e}")
        return None

# Create Table
def create_table():
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INT AUTO_INCREMENT PRIMARY KEY,
                csduid VARCHAR(255),
                csd VARCHAR(255),
                period INT,
                description TEXT,
                unit VARCHAR(50),
                value FLOAT
            );
        ''')
        conn.commit()
        cursor.close()
        conn.close()

# Load CSV Data into MySQL Table with a Limit of 100
def load_data_from_csv(csv_file_path):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM records")
        record_count = cursor.fetchone()[0]
        if record_count >= 100:
            print("Database already populated with 100 records, skipping CSV load.")
            return

        try:
            with open(csv_file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                count = record_count
                for row in reader:
                    if count >= 100:
                        break
                    cursor.execute(
                        "INSERT INTO records (csduid, csd, period, description, unit, value) VALUES (%s, %s, %s, %s, %s, %s)",
                        (
                            row["CSDUID"],
                            row["CSD"],
                            int(row["Period"]),
                            row["IndicatorSummaryDescription"],
                            row["UnitOfMeasure"] if row["UnitOfMeasure"] else "N/A",
                            float(row["OriginalValue"]) if row["OriginalValue"] else 0.0,
                        ),
                    )
                    count += 1
            conn.commit()
            print("Database populated successfully!")
        except FileNotFoundError:
            print("Error: CSV file not found.")
        except Exception as e:
            print(f"Error inserting records: {e}")
        finally:
            cursor.close()
            conn.close()

# Reset the database and reload 100 records
def reset_database(csv_file_path):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM records")
            conn.commit()
            print("All records deleted. Reloading 100 records from CSV...")

            with open(csv_file_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                count = 0
                for row in reader:
                    if count >= 100:
                        break
                    cursor.execute(
                        "INSERT INTO records (csduid, csd, period, description, unit, value) VALUES (%s, %s, %s, %s, %s, %s)",
                        (
                            row["CSDUID"],
                            row["CSD"],
                            int(row["Period"]),
                            row["IndicatorSummaryDescription"],
                            row["UnitOfMeasure"] if row["UnitOfMeasure"] else "N/A",
                            float(row["OriginalValue"]) if row["OriginalValue"] else 0.0,
                        ),
                    )
                    count += 1
                conn.commit()
                print(f"Database successfully reset with {count} records.")
        except FileNotFoundError:
            print("CSV file not found.")
        except Exception as e:
            print(f"Error resetting database: {e}")
        finally:
            cursor.close()
            conn.close()

# Fetch and return top 100 records
def fetch_all_records(limit=100):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM records LIMIT %s", (limit,))
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records
    return []

# Display All Records
# Display All Records (showing actual DB record ID)
def display_records(indices=None):
    records = fetch_all_records()
    if not records:
        print("No records to display.")
        return

    print(f"\n --- Total Records: {len(records)} ---")
    print("\n--- Records ---")
    if indices is None:
        for record in records:
            print(f"[ID {record[0]}] CSDUID: {record[1]}, CSD: {record[2]}, Period: {record[3]}, "
                  f"Desc: {record[4]}, Unit: {record[5]}, Value: {record[6]}")
    else:
        for index in indices:
            if 1 <= index <= len(records):
                r = records[index - 1]
                print(f"[ID {r[0]}] CSDUID: {r[1]}, CSD: {r[2]}, Period: {r[3]}, "
                      f"Desc: {r[4]}, Unit: {r[5]}, Value: {r[6]}")
            else:
                print(f"Invalid index: {index}")
    print("\n--- Full Name: Peiqi Wang ---")


# Display Records by Database ID (not row index)
def display_records_by_id(record_ids):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        format_strings = ','.join(['%s'] * len(record_ids))
        query = f"SELECT * FROM records WHERE id IN ({format_strings})"
        cursor.execute(query, tuple(record_ids))
        records = cursor.fetchall()

        if records:
            print("\n--- Selected Records ---")
            for r in records:
                print(f"[ID {r[0]}] CSDUID: {r[1]}, CSD: {r[2]}, Period: {r[3]}, Desc: {r[4]}, Unit: {r[5]}, Value: {r[6]}")
        else:
            print("No records found with the given ID(s).")

        cursor.close()
        conn.close()

# Insert a New Record
def add_record(csduid, csd, period, description, unit, value):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO records (csduid, csd, period, description, unit, value) VALUES (%s, %s, %s, %s, %s, %s)",
            (csduid, csd, period, description, unit, value),
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Record added successfully!")

# Edit an Existing Record
def edit_record(record_id, csduid, csd, period, description, unit, value):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE records SET csduid=%s, csd=%s, period=%s, description=%s, unit=%s, value=%s WHERE id=%s",
            (csduid, csd, period, description, unit, value, record_id),
        )
        conn.commit()
        cursor.close()
        conn.close()
        print("Record updated successfully!")

# Delete a Record
def delete_record(record_id):
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM records WHERE id=%s", (record_id,))
        conn.commit()
        cursor.close()
        conn.close()
        print("Record deleted successfully!")
