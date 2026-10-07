#!/usr/bin/env python3

import streamlit as st
import pandas as pd
from DEFAULT import DEFAULT_RESUME_PATH
from datetime import datetime
from neu import add_to_database

applications_file = "job_applications.tsv"

def load_data(data_file):
	df = pd.read_csv(data_file, delimiter = "\t")
	return df

# def enter_application( Company, Job_Title, Date, Status, Link, CV, Cover_Letter, Location, Salary, Where):
#     add_to_database(
#         Company,
#         Job_Title,
#         Date,
#         Status,
#         Link,
#         CV,
#         Cover_Letter,
#         Location,
#         Salary,
#         Where
#     )

def update_entry(database, idx, update):
    database.loc[int(idx), "Status"] = update
    database.to_csv(applications_file, sep = "\t", index = False)

    st.session_state["search_company"] = None
    st.session_state["search_title"] = None
    st.session_state["selected_job"] = None
    st.session_state["update_status"] = None
    st.session_state["update_message"] = "Entry has been updated!"

def main():
    
    st.markdown("## Enter a new Job Application")
    col1, col2 = st.columns([1,1])

    Company = col1.text_input(label = "Company Name", required = True)
    CV = col1.text_input(label = "CV", placeholder = DEFAULT_RESUME_PATH)
    Date = col1.date_input(label = "When did you apply?")
    Location = col1.text_input(label = "Job Location", required = True)


    Job_Title = col2.text_input(label = "Job Title", required = True)
    Cover_Letter = col2.text_input(label = "CL file path", required = False)
    Link = col2.text_input(label = "Link to the Job Position")
    Where = col2.text_input(label = "Where did you find the job?", required = True)

    with st.container(horizontal = True, horizontal_alignment = "center"):
        enter_btn = st.button(
            "Enter Application", type = "primary",
            on_click = add_to_database,
            args = (
                Company,
                Job_Title,
                str(Date),
                "applied",
                Link,
                CV,
                Cover_Letter,
                Location,
                "-",
                Where
            )
        )
    
    with st.container(horizontal = True, horizontal_alignment = "center"):
        if enter_btn:
            st.markdown("""
                <span>Entry successfully added!</span>
                """, unsafe_allow_html = True
            )
        else:
            st.markdown("""
                <span style="
                    color: transparent;
                    user-select: none;
                ">
                you found the placeholder :)
                </span>
                """, unsafe_allow_html = True
            )

    st.markdown("## Update a Job Application")
    
    df = load_data("job_applications.tsv")
    
    col1, col2 = st.columns([1,1])
    
    search_company = col1.selectbox(label = "Company Name", options = df["Company"].sort_values(na_position = "last", key = lambda x : x.str.lower()).unique(), index = None, placeholder = "Select Company Name", key = "search_company")
    
    search_title = col2.selectbox(label = "Job Title", options = df["Job_Title"].sort_values(na_position = "last", key = lambda x : x.str.lower()), index = None, placeholder = "Select Job Title", key = "search_title")

    selected_job = None
    if search_company is not None:
        filtered_df = df.loc[df["Company"] == search_company]
        display_cols = [ col for col in df.columns if col != "Salary"]
        
        selected_job = st.selectbox(
            label = "Company\tJob_Title\tDate\tStatus\tLink\tCV\tCL\tLocation\tWhere",
            options = filtered_df.index.tolist(),
            index = None,
            key = "selected_job",
            format_func = lambda idx : " : ".join(
                filtered_df.loc[idx, display_cols].astype(str)
            )
        )
    elif search_title is not None:
        filtered_df = df.loc[df["Job_Title"] == search_title]
        display_cols = [ col for col in df.columns if col != "Salary"]
        
        selected_job = st.selectbox(
            label = "Company\tJob_Title\tDate\tStatus\tLink\tCV\tCL\tLocation\tWhere",
            options = filtered_df.index.tolist(),
            index = None,
            key = "selected_job",
            format_func = lambda idx : " : ".join(
                filtered_df.loc[idx, display_cols].astype(str)
            )
        )

    if selected_job is not None:
        update = st.selectbox(label = "Update Status", options = ["applied", "rejected", "interview", "offer", "hired"], index = None, key = "update_status")
        
        with st.container(horizontal = True, horizontal_alignment = "center"):
            update_btn = st.button(
                "Update Entry", type = "primary",
                on_click = update_entry, args = (df, selected_job, update)
            )
        
    update_placeholder = st.session_state.pop("update_message", "")
    with st.container(horizontal = True, horizontal_alignment = "center"):
        st.markdown(update_placeholder)
        