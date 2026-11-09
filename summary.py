#!/bin/usr/env python3

import pandas as pd
import shutil
from datetime import datetime

APPLICATIONS_FILE = "job_applications.tsv"
APPLICATIONS_DF = pd.read_csv(APPLICATIONS_FILE, delimiter = "\t")

WINDOW_SIZE = shutil.get_terminal_size().columns

def count_entries(df, status):
    count = df["Status"].value_counts().get(status, 0)
    return count

def sankey_view():
    total_applications = len(APPLICATIONS_DF)
    
    applied_applications = count_entries(APPLICATIONS_DF, "applied")
    rejected_applications = count_entries(APPLICATIONS_DF, "rejected")
    hired_applications = count_entries(APPLICATIONS_DF, "hired")
    offer_applications = count_entries(APPLICATIONS_DF, "offer") + hired_applications
    interview_applications = count_entries(APPLICATIONS_DF, "interview") + hired_applications + offer_applications
    
    other_applications = total_applications - (applied_applications + rejected_applications + interview_applications + offer_applications + hired_applications)
    
    Date = datetime.today().strftime("%Y-%m-%d")
    today = APPLICATIONS_DF["Date"].value_counts().get(Date, 0)
    
    print(f"Total: {total_applications}\tOffer: {offer_applications}")
    print(f"Applied: {applied_applications}\tHired: {hired_applications}")
    print(f"Rejected: {rejected_applications}\tOther: {other_applications}")
    print(f"Interview: {interview_applications}\tApplications today: {today}")

def cover_letter():
    cl_no = (APPLICATIONS_DF["CL"] == "-").sum()
    cl_yes = (APPLICATIONS_DF["CL"] != "-").sum()
    total = cl_no + cl_yes
    
    cl_yes_percent = cl_yes / total * 100
    
    size = WINDOW_SIZE - 2 - 7
    
    bar_size = int(size / cl_yes_percent)
    bar = "\u25A0"*bar_size
    empty_size = size - bar_size
    empty = "\u25A1"*empty_size
    
    print(f"[{bar}{empty}] {cl_yes_percent:.2f}%")

def barplot():
    MONTH_NAMES = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"
    ]

    AXES = [
        [ 1, 2, 3, 4, 5],
        [ 2, 4, 6, 8,10],
        [ 1, 5,10,15,20],
        [10,20,30,40,50],
        [20,40,60,80,99],
    ]


    # Get data --
    dates = APPLICATIONS_DF["Date"].value_counts().sort_index()
    dates_formatted = []
    for date in dates.index:
        year, month, day = date.split("-")
        dates_formatted.append(f"{MONTH_NAMES[int(month) - 1]} {day}")



    # Get parameters --
    ''' column width = 4 chars, y axis = 3 chars '''
    plot_width = WINDOW_SIZE - 3
    col_width = 4
    num_cols = min(
        len(dates),
        plot_width // col_width
    )



    # Header line with months --
    selected_dates = dates_formatted[-num_cols:]

    months = [ x.split(" ")[0] for x in selected_dates ]

    months_set = set([ x.split(" ")[0] for x in selected_dates ])

    date_counts = {
        month: 0 for month in months_set
    }
    for month in months:
        date_counts[month] += 1
    month_string = "--+"

    for month in MONTH_NAMES:
        if month in date_counts:
            space = date_counts[month]*4 - 4
            space_left = int(space/2)
            space_right = int(space/2)
            
            month_string += "".join([
                "-"*space_left,
                month,
                "-"*space_right,
                "|"
            ])



    # Select y-axis --
    selected_values = dates.values[-num_cols:]

    maximum = max(selected_values)
    thresholds = next(
        (axis for axis in AXES if maximum <= axis[-1]),
        AXES[-1]
    )
    y_labels = [f"{threshold:2}" for threshold in thresholds] + ["  "]



    # Create barplot rows --
    cols = []
    for value in selected_values:
        height = sum(value >= step for step in thresholds)
        
        cells = (
            ["  \u2588 "] * height
            + [f" {value:2} "]
            + ["    "] * (len(thresholds) - height)
        )
        
        cols.append(cells)
    rows = list(zip(*cols))



    # Footer row with days --
    days = [ i.split(" ")[1]+"." for i in selected_dates]

    days_string = "  |" + "".join(f" {day}" for day in days)



    # Print barplot --
    print(month_string)
    for label, row in zip(reversed(y_labels), reversed(rows)):
        print(f"{label}|{''.join(row)}")
    print("--+" + "-"*(col_width*len(cols)))
    print(days_string)


# 
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"

print()
print(f"{BOLD}{UNDERLINE}Overview{RESET}")
sankey_view()
print()
print(f"{BOLD}{UNDERLINE}Cover Letter Usage{RESET}")
cover_letter()
print()
print(f"{BOLD}{UNDERLINE}Applications per Day{RESET}")
print()
barplot()
print()