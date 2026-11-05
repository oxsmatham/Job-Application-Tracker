#!/usr/bin/env python3

import streamlit as st
import plotly.graph_objects as go
import pandas as pd

applications_file = "job_applications.tsv"

def load_data(data_file):
	df = pd.read_csv(data_file, delimiter = "\t")
	return df

def main():
    df = load_data(applications_file)
    
    st.dataframe(df)