"""
Author: Peiqi Wang
Course: CST8002 Practical Project 2
Professor: Tyler DeLay
Due Date: 2025-02-16
Description:
This is a business layer provides business logic for managing record
"""
from persistence.file_handler import load_data_from_csv
import matplotlib.pyplot as plt


def display_records(records, indices=None):
    """
    Displays all records or selected records based on record number.
    """
    print(f"\n --- Total Records Loaded: {len(records)}---")
    print("\n--- Records ---")
    if indices is None:
        for record in records:
            print(record)
    else:
        for index in indices:
            if 1 <= index <= len(records):
                print(f"[{index}] {records[index-1]}")
            else:
                print(f"Invalid index: {index}")
    print("\n--- Full Name: Peiqi Wang ---")

def reload_data(file_path):
    """
    Reloads the dataset from disk.
    """
    return load_data_from_csv(file_path)

def add_record(records, record):
    """
    add a record data from memory.
    """
    records.append(record)
    print("Record added successfully.")
    return records

def edit_record(records, index, new_record):
    """
    edit a record data.
    """
    if 1 <= index <= len(records):
        records[index - 1] = new_record
        print("Record updated successfully.")
    else:
        print("Invalid index.")
        return records

def delete_record(records, index):
    """
     delete a record data.
    """
    if 1 <= index <= len(records):
        del records[index - 1]
        print("Record deleted successfully.")
    else:
        print("Invalid index.")
        return records

def visualize_data(records, chart_type="bar", group_by="csd"):
    """
    Generates a bar, horizontal bar, or pie chart grouped by a selected field.
    Also prints original values grouped by the selected column.
    """
    if not records:
        print("No data available to visualize.")
        return

    print(f"\n Visualizing data grouped by '{group_by}' using chart type: {chart_type}\n")

    # Field name to index mapping (for tuple records)
    field_map = {
        "csduid": 1,
        "csd": 2,
        "period": 3,
        "description": 4,
        "unit": 5,
        "value": 6
    }

    group_index = field_map.get(group_by, 2)  # Default to CSD
    value_index = 6  # Always value column

    grouped_data = {}
    totals = {}

    # Group raw records
    for record in records:
        key = str(record[group_index])
        grouped_data.setdefault(key, []).append(record)
        totals[key] = totals.get(key, 0) + float(record[value_index])

    # Print original values grouped by selected field
    for group_key, group_records in grouped_data.items():
        print(f"\n🔹 {group_by.upper()}: {group_key} — {len(group_records)} records")
        for rec in group_records:
            print(f"   [ID {rec[0]}] {rec[1]}, {rec[2]}, Period: {rec[3]}, Desc: {rec[4]}, Unit: {rec[5]}, Value: {rec[6]}")

    # Prepare chart data
    labels = list(totals.keys())
    values = list(totals.values())

    # Plot chart
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))
    if chart_type == "bar":
        plt.bar(labels, values)
        plt.title(f"{group_by.upper()} - Total Value")
        plt.xlabel(group_by.upper())
        plt.ylabel("Value")
    elif chart_type == "hbar":
        plt.barh(labels, values)
        plt.title(f"{group_by.upper()} - Total Value")
        plt.xlabel("Value")
        plt.ylabel(group_by.upper())
    elif chart_type == "pie":
        plt.pie(values, labels=labels, autopct='%1.1f%%')
        plt.title(f"{group_by.upper()} - Value Distribution")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    print("\n Chart displayed successfully.")
