#File triage and hash analysis

## Overview

This python script analyses the supplied teaching files. It records the file details and calculates SHA-256 hashes then compares them with the reference list. It identifies any duplicate files and saves a report.

## Requirements

Python 3
Standard pyton library modules, "Pathlib", "datetime", "hashlib and "csv"
No extra packages or API accounts are required 

## Project files

"file_triage.py" is the analysis script
"data/" is the supplied sample files
"hashes_refernce.csv" is the supplied hashes
"triage_report.txt" is the report created when the script is run

## How to run

Open terminal in the script folder and run, "python file_triage.py", it will ask you to enter the path to the file triage pack folder, enter the folder.