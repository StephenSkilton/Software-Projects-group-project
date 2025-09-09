import csv
import sys
from datetime import datetime
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

def show_info_alert():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window
    messagebox.showinfo("Warning", "Incorrect File Type Selected")
    root.destroy()
def select_file():
    # Hide the main Tkinter window
    root = tk.Tk()
    root.withdraw()

    # Open the file dialog and get the selected file path
    file_path = filedialog.askopenfilename(
        title="Select a file",
        filetypes=(("CSV and Excel files", "*.csv *.xls *.xlsx"),("All files", "*.*"))
    )

    if file_path:
        print(f"Selected file: {file_path}")
        return file_path

    else:
        print("No file selected.")
        return None

def get_valid_file():
    while True:
        file_path = select_file()
        if file_path is None:
            print("No file selected. Exiting program.")
            sys.exit()
        elif file_path.endswith((".csv", ".xls", ".xlsx")):
            return file_path
        else:
            show_info_alert("Please select a valid CSV or Excel file.")


# file_path = ("sample_usage_data_month.csv")
# file_path = ("sample_usage_data_month.xlsx")


def file_reader(file_path):
    data_dict = {}
    if file_path.endswith(".csv"):
        with open(file_path, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Parse timestamp string into datetime object
                timestamp = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                kwh = float(row["kWh"])  # convert to float
                data_dict[timestamp] = kwh
    else:

        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            timestamp = datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
            kwh = float(row["kWh"])
            data_dict[timestamp] = kwh





    return data_dict


def flat_calculation(data):
    usage=0
    for value in data.values():
        usage += value
    total=usage*0.25+10
    total = round(total, 2)
    return total

def tier_calculation(data):
    usage=0
    total=0
    for value in data.values():
        usage += value
    if usage<=100:
        total=usage*0.2+10
    elif usage>=101 and usage<=300:
        tier1 = 100*0.2
        tier2=usage-100
        total=tier2 * 0.3 + tier1 + 10
    else:
        tier1 = 100 * 0.2
        tier2 = 200*0.3
        tier3= usage-300
        total=tier3 * 0.4 + tier1 + tier2 + 10

    total = round(total, 2)
    return total

def time_calculation(data):
    peak=0
    off=0
    shoulder=0
    peak_start = 18
    peak_end = 22
    off_start = 22
    off_end = 7
    for key in data.keys():
        if key.hour >= peak_start and key.hour <= peak_end:
            peak += data[key]
        elif key.hour >= off_start and key.hour <= off_end:
            off += data[key]
        else:
            shoulder += data[key]
    total=(peak * 0.4) + (off*0.15) +(shoulder*0.25) + 10

    total = round(total, 2)

    return total


file_path = get_valid_file()
data_dict = file_reader(file_path)
print("Flat rate total: $" + str(flat_calculation(data_dict)))
print ("Tiered tariff total: $" + str(tier_calculation(data_dict)))
print ("TOU Tariff total: $"+ str(time_calculation(data_dict)))