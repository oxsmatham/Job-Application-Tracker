#!/bin/usr/env python3

import pandas as pd
import shutil

APPLICATIONS_FILE = "job_applications.tsv"

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
applications_df = pd.read_csv(APPLICATIONS_FILE, delimiter = "\t")

dates = applications_df["Date"].value_counts().sort_index()
dates_formatted = []
for date in dates.index:
    year, month, day = date.split("-")
    dates_formatted.append(f"{MONTH_NAMES[int(month) - 1]} {day}")



# Get parameters --
''' column width = 4 chars, y axis = 3 chars '''
plot_width = shutil.get_terminal_size().columns - 3
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
