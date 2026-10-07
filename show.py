#!/usr/bin/env python3

# run using: streamlit run show.py

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from DEFAULT import DEFAULT_RESUME_PATH
from datetime import datetime

import tab0_overview
import tab1_database
import tab2_settings


page_title = "Job Application Tracker"
page_icon = ":+1:"
layout = "wide"

st.set_page_config(
	page_title = page_title,
	page_icon = page_icon,
	layout = layout
	)

st.title(page_title + " " + page_icon)

tabs = st.tabs([
	"Overview",
	"Database",
	"Settings"
])

with tabs[0]:
	tab0_overview.main()

with tabs[1]:
	tab1_database.main()
