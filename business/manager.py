"""
Author: Peiqi Wang
Course: CST8002 Practical Project 2
Professor: Tyler DeLay
Due Date: 2025-02-16
Description:
This is a business layer provides business logic for managing record
"""
from persistence.file_handler import load_records

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
    return load_records(file_path)

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