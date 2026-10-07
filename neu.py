#!/usr/bin/env python3

from datetime import datetime
from DEFAULT import DEFAULT_RESUME_PATH
import os.path

applications_file = "job_applications.tsv"

def add_to_database(
	Company,
	Job_Title,
	Date,
	Status,
	Link,
	CV,
	Cover_Letter,
	Location,
	Salary,
	Where
):
	with open(applications_file, "a") as file:
		file.write("\t".join([Company, Job_Title, Date, Status, Link, CV, Cover_Letter, Location, Salary, Where]) + "\n")

	print("")
	print("=======================")
	print("Added Entry: ")
	print(f"Company: {Company}")
	print(f"Job_Title: {Job_Title}")
	print(f"Date: {Date}")
	print(f"Status: {Status}")
	print(f"Link: {Link}")
	print(f"CV: {CV}")
	print(f"CL: {Cover_Letter}")
	print(f"Location: {Location}")
	print(f"Salary: {Salary}")
	print(f"Where: {Where}")

	

def check_for_database():
	if os.path.isfile(applications_file):
		return
	else:
		with open(applications_file, "w") as fout:
			fout.write("\t".join(["Company", "Job_Title", "Date", "Status", "Link", "CV", "CL", "Location", "Salary", "Where"]) + "\n")

def main():
	
	check_for_database()

	Company = input("Company: ")
	Job_Title = input("Job Title: ")
	Date = input("Date (YYYY-DD-MM): ")
	if Date == "":
		Date = datetime.today().strftime("%Y-%m-%d")
	Status = "applied"
	Link = input("Link to job position: ")
	CV = input("File path to CV(Lebenslauf): ")
	if CV == "":
		CV = DEFAULT_RESUME_PATH
	Cover_Letter = input("File path to Cover Letter(Anschreiben): ")
	Location = input("Job Location: ")
	Salary = input("Salary: ")
	Where = input("Where did you find this job? ")

	add_to_database(
		Company,
		Job_Title,
		Date,
		Status,
		Link,
		CV,
		Cover_Letter,
		Location,
		Salary,
		Where
	)
	

if __name__ == "__main__":
	main()
