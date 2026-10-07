#!/usr/bin/env python3

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from DEFAULT import DEFAULT_RESUME_PATH
from datetime import datetime

def load_data(data_file):
	df = pd.read_csv(data_file, delimiter = "\t")
	return df

def count_entries(df, status):
    count = df["Status"].value_counts().get(status, 0)
    return count

def draw_sankey(df):
    total_applications = len(df)
    
    applied_applications = count_entries(df, "applied")
    rejected_applications = count_entries(df, "rejected")
    hired_applications = count_entries(df, "hired")
    offer_applications = count_entries(df, "offer") + hired_applications
    interview_applications = count_entries(df, "interview") + hired_applications + offer_applications
    
    other_applications = total_applications - (applied_applications + rejected_applications + interview_applications + offer_applications + hired_applications)

    label = [
        f"Total Applications ({total_applications})", 
        f"Applied ({applied_applications})",
        f"Rejected ({rejected_applications})", 
        f"Interview ({interview_applications})", 
        f"Offer ({offer_applications})", 
        f"Hired ({hired_applications})", 
        f"Other ({other_applications})"
    ]

    source = [
        0, # total -> applied
        0, # total -> rejected
        0, # total -> interview
        3, # interview -> offer
        4, # offer -> hired
        0  # total -> other
    ]

    target = [
        1, # total -> applied
        2, # total -> rejected
        3, # total -> interview
        4, # interview -> offer
        5, # offer -> hired
        6  # total -> other
    ]

    value = [
        applied_applications,
        rejected_applications,
        interview_applications,
        offer_applications,
        hired_applications,
        other_applications
    ]

    fig = go.Figure(
        go.Sankey(
            node = dict(
                label = label, 
                pad = 40, 
                thickness = 14
            ),
            link = dict(
                source = source,
                target = target,
                value = value
            )
        )
    )
    
    return fig

def draw_pie(labels, values):
    fig = go.Figure(
        go.Pie(
            labels = labels,
            values = values,
            hole = 0.2,
            textinfo = "label+percent",
            hovertemplate = "%{label}: <b>%{value:.2f}</b><extra></extra>"
        )
    )
    
    return fig

def row(name, count):
    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: space-between;
            width: 100%;
        ">
            <span>{name}</span>
            <span>{count}</span>
        </div>
        """,
        unsafe_allow_html = True
    )

def main():
    
    # Sankey Diagram
    st.markdown("# Job Application Performance Overview")

    applications_df = load_data("job_applications.tsv")

    sankey_fig = draw_sankey(applications_df)

    st.plotly_chart(sankey_fig)


    # Pie charts
    
    col1, col2 = st.columns([1,1])

    ## Where did you find the Job?
    value_counter = applications_df["Where"].value_counts()
    labels = [ i for i in value_counter.index ]
    values = [ i for i in value_counter]

    pie_where = draw_pie(labels, values)

    container1 = col1.container(border = True)
    container1.markdown("## Where did you find the Job?")
    container1.plotly_chart(pie_where, width = "content", key = "pie_where")


    ## Did you attach a Cover Letter?
    cl_yes = 0
    cl_no = 0

    for i in applications_df["CL"]:
        if i == "-":
            cl_no += 1
        else:
            cl_yes += 1


    labels = ["Yes", "No"]
    values = [cl_yes, cl_no]

    pie_cl = draw_pie(labels, values)

    container2 = col2.container(border = True)
    container2.markdown("## Did you attach a Cover Letter?")
    container2.plotly_chart(pie_cl, width = "content", key = "pie_cl")


    # Company Summary
    st.markdown("# What Companies did you apply to?")

    companies = applications_df["Company"].value_counts()
    top5 = companies.head(5)
    rest = companies.iloc[5:]

    for name, count in top5.items():
        row(name, count)

    with st.expander("View more:", expanded = False, type = "compact"):
        for name, count in rest.items():
            row(name, count)


    # Location Summary
    st.markdown("# Where are the Jobs based at?")
    
    locations = applications_df["Location"].value_counts()
    top5 = locations.head(5)
    rest = locations.iloc[5:]

    for loc, count in top5.items():
        row(loc, count)

    with st.expander("View more:", expanded = False, type = "compact"):
        for loc, count in rest.items():
            row(loc, count)

    # Daily Summary
    st.markdown("# What Day did you apply?")

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

    hist = go.Figure(
        go.Bar(
            x = dates_formatted,
            y = dates.values
        )
    )

    st.plotly_chart(hist, key = "hist")