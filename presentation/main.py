"""
Author: Peiqi Wang
Course: CST8002 Practical Project 2
Professor: Tyler DeLay
Due Date: 2025-02-16
Description: This project follows a layered model structure
with business, model, persistence, and presentation layers.
This module serves as the entry point for the application.
It provides a user interface for interacting with the record system.
"""
"""
Author: Peiqi Wang
Course: CST8002 Practical Project 3
Professor: Tyler DeLay
Due Date: 2025-03-16
Description:
This is the entry point for the application. It provides a user interface for interacting
with the record system using a layered structure.
"""

import os
from persistence.file_handler import (
    create_table,
    load_data_from_csv,
    reset_database,
    display_records,
    display_records_by_id,
    add_record,
    edit_record,
    delete_record
)

def main():
    """
    Main function to handle user interaction and menu options.
    """
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Dwellingunitsdownload.csv")

    # Step 1: Ensure DB table exists
    create_table()

    # Step 2: Load initial data if not already loaded
    load_data_from_csv(file_path)

    #reset_database(file_path)

    while True:
        print("\n--- Full Name: Peiqi Wang ---")
        print("Options:")
        print("1. Display All Data")
        print("2. Display Selected Data")
        print("3. Add a Data")
        print("4. Edit a Data")
        print("5. Delete a Data")
        print("6. Reset Database to 100 Records")
        print("7. Visualize Data")
        print("8. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            display_records()

        elif choice == "2":
            try:
                ids = input("Enter record ID(s), separated by commas: ")
                ids = [int(i.strip()) for i in ids.split(",")]
                display_records_by_id(ids)
            except ValueError:
                print("Invalid input. Please enter numbers only.")

        elif choice == "3":
            csduid = input("Enter CSDUID: ")
            csd = input("Enter CSD: ")
            period = int(input("Enter Period: "))
            description = input("Enter Description: ")
            unit = input("Enter Unit: ")
            value = float(input("Enter Value: "))
            add_record(csduid, csd, period, description, unit, value)

        elif choice == "4":
            try:
                record_id = int(input("Enter Record ID to edit: "))
                csduid = input("Enter new CSDUID: ")
                csd = input("Enter new CSD: ")
                period = int(input("Enter new Period: "))
                description = input("Enter new Description: ")
                unit = input("Enter new Unit: ")
                value = float(input("Enter new Value: "))
                edit_record(record_id, csduid, csd, period, description, unit, value)
            except ValueError:
                print("Invalid input. Please enter numbers where required.")

        elif choice == "5":
            try:
                record_id = int(input("Enter Record ID to delete: "))
                delete_record(record_id)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "6":
            reset_database(file_path)

        elif choice == "7":
            print("Select chart type:")
            print("1. Vertical Bar Chart")
            print("2. Horizontal Bar Chart")
            print("3. Pie Chart")
            chart_choice = input("Enter chart type number: ")

            chart_map = {"1": "bar", "2": "hbar", "3": "pie"}
            chart_type = chart_map.get(chart_choice, "bar")

            print("Group data by:")
            print("1. CSD")
            print("2. Description")
            print("3. Period")
            print("4. Unit")
            print("5. CSDUID")
            print("6. Value")
            group_choice = input("Enter grouping column: ")

            group_map = {
                "1": "csd",
                "2": "description",
                "3": "period",
                "4": "unit",
                "5": "csduid",
                "6": "value"
            }

            group_by = group_map.get(group_choice, "csd")

            from persistence.file_handler import fetch_all_records
            from business.manager import visualize_data

            records = fetch_all_records()
            visualize_data(records, chart_type=chart_type, group_by=group_by)

        elif choice == "8":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")

if __name__ == "__main__":
    main()
