#!/bin/usr/env python3

# not finished
# needs cleaning up

import pandas as pd
import shutil

application_file = "job_applications.tsv"

def load_data(data_file):
	df = pd.read_csv(data_file, delimiter = "\t")
	return df

applications_df = load_data(application_file)

dates = applications_df["Date"].value_counts().sort_index()
dates_formatted = []

for date, count in dates.items():
    year,month,day = date.split("-")

    match month:
        case "01":
            month_name = "Jan"
        case "02":
            month_name = "Feb"
        case "03":
            month_name = "Mar"
        case "04":
            month_name = "Apr"
        case "05":
            month_name = "May"
        case "06":
            month_name = "Jun"
        case "07":
            month_name = "Jul"
        case "08":
            month_name = "Aug"
        case "09":
            month_name = "Sep"
        case "10":
            month_name = "Okt"
        case "11":
            month_name = "Nov"
        case "12":
            month_name = "Dec"
        case _:
            month_name = "?"

    dates_formatted.append(month_name + " " + day)


plot_width = min(len(dates_formatted)*4, shutil.get_terminal_size().columns - 3)
print(plot_width)

normalized_values = [ round(x / max(dates.values) * 20) for x in dates.values ]


# column width = 4 chars, y axis = 3 chars
num_cols = int(plot_width / 4)


selected_values = dates.values[-num_cols:]

selected_dates = dates_formatted[-num_cols:]

months = [ x.split(" ")[0] for x in selected_dates ]
selected_months = months[-num_cols:]

months_set = set([ x.split(" ")[0] for x in selected_dates ])

months_width = int(plot_width / len(months_set) - 4*(len(months_set)-1))

dates_stuff = {
    month: 0 for month in months_set
}

for month in months:
    dates_stuff[month] += 1

month_string = "--+"

all_months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"]

for month in all_months:
    if month in dates_stuff:
        space = dates_stuff[month]*4 - 3
        space_left = int(space/2) + 1 if space % 2 != 0 else int(space/2)
        space_right = int(space/2)
        
        month_string += "-"*space_left
        month_string += month
        month_string += "-"*space_right
        month_string += "|"
print(month_string)

date_labels = [
    f" {d.split(" ")[1]}." for d in dates_formatted
]

# print(date_labels)

y_axis = [
    [" 1"," 2"," 3"," 4"," 5"],
    [" 2"," 4"," 6"," 8","10"],
    [" 1"," 5","10","15","20"],
    ["10","20","30","40","50"],
    ["20","40","60","80","99"],
]

x = max(selected_values)
if x <= 5:
    idx = 0
elif x > 5 and x <= 10:
    idx = 1
elif x > 10 and x <= 20:
    idx = 2
elif x > 20 and x <= 50:
    idx = 3
else:
    idx = 4
selected_axis = y_axis[idx]

cols = []
for val in selected_values:
    spacer_column = ""
    column_pre = ""
    column = ""
    column_post = ""
    is_first = True
    for step in selected_axis:
        if val >= int(step):
            spacer_column += " "
            column_pre += " "
            column += "\u2588"
            column_post += " "
        else:
            if is_first:
                spacer_column += " "
                if len(str(val)) == 2:
                    column_pre += str(val)[0]
                else:
                    column_pre += " "
                column += str(val)[-1]
                column_post += " "
                is_first = False
            else:
                spacer_column += " "
                column_pre += " "
                column += " "
                column_post += " "
    if is_first:
        spacer_column += " "
        if len(str(val)) == 2:
            column_pre += str(val)[0]
        else:
            column_pre += " "
        column += str(val)[-1]
        column_post += " "
    else:
        spacer_column += " "
        column_pre += " "
        column += " "
        column_post += " "
    cols.append((spacer_column, column_pre, column, column_post))


plot = [
    (" 1"," 5","10","15","20"),
    
]
selected_axis.append("  ")
plot = [
    selected_axis,
    ( "|", "|", "|", "|", "|", "|",)
]
for col in cols:
    for c in col:
        plot.append(c)



counter = 5
while counter >= 0:
    line = ""
    for i in plot:
        line += i[counter]
    print(line)
    counter -= 1
    
print("--+" + "-"*(len(month_string)-3))


days = [ i.split(" ")[1]+"." for i in selected_dates]

days_string = "  |"
for day in days:
    days_string += " "
    days_string += day
days_string += "  "

print(days_string)

# new_days_string = ""
# for i,c in enumerate(month_string):
#     if c == "|":
#         new_days_string += "|"
#     else:
#         new_days_string += days_string[i]

# print(new_days_string)