# Job-Application-Tracker

A Python application built with Streamlit to help you manage and track your job applications in one place. It lets you record new applications and update their status as you progress through the hiring process.

## Features
- Add new job application with relevant details such as:
  - Company name, Job title, Job location, etc.
- Track application process through stages:
  - applied
  - rejected
  - interview
  - offer
  - hired
- Add and update applications directly in the app or via the commandline
- Store data in a simple TSV file
- Keep local reference to CV and cover letter files

## Tech Stack
- Python
- Streamlit
- Pandas

## Requirements
- streamlit
- pandas

## Running the app
Either use ```python3 run.py show | add | new```
or directly use ```neu.py``` to add a new job application or ```update.py``` to update an existing job application

## License
This project does not currently include a license file. Feel free to do whatever :)

## Coming Soon
- Custom setting tab for things like font-size and color
- Salary visualization
