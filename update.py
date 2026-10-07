#!/usr/bin/env python3

import sys
import os

applications_file = "job_applications.tsv"

def check_for_database():
	if os.path.isfile(applications_file):
		return
	else:
		print(f"{applications_file} doesn't exist. It seems like you haven't applied for any jobs yet :(")
		sys.exit(1)

def load_database():
	global database
	with open(applications_file, "r") as fin:
		database = [ line.split("\t") for line in fin]

def update_entry(idx, update):
	match update:
		case "r":
			new = "rejected"
		case "i":
			new = "interview"
		case "o":
			new = "offer"
		case "h":
			new = "hired"
		case _:
			new = update

	database[int(idx)][3] = new
	with open(applications_file, "w") as fout:
		for entry in database:
			fout.write("\t".join(entry))
	print("")
	print("Database has been updated!")
	
def ask_for_entry():
	Company = input("What Company did you apply at? ")
	if Company == "":
		Job_Title = input("What was the Job Title? ")
		if Job_Title == "":
			print("Couldn't identify entry. Exiting..")
			sys.exit(0)
		return Job_Title, 1
	return Company, 0
	
def find_entry(identifier, col):
	found_entries = []
	for entry_idx, entry in enumerate(database):
		if identifier.lower() in entry[col].lower():
			found_entries.append((entry_idx, entry))
	
	print("")	
	print(f"found {len(found_entries)} entries that match your identifier")
	print("---------------------------------------------------------------")
	if len(found_entries) == 0:
		sys.exit(0)
	for entry_idx, entry in found_entries:
		print(entry_idx, entry)
	print("")
	idx = input("Which entry would you like to update? idx: ")
	print("")
	update = input("What is the update? rejected(r)/interview(i)/offer(o)/hired(h): ")

	return idx, update

if __name__ == "__main__":
	check_for_database()

	load_database()

	entry, col = ask_for_entry()

	idx, update = find_entry(entry, col)

	update_entry(idx, update)
