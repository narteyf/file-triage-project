# Author Daniel Quaynor
# Version 1.0
# 10/11/26

from pathlib import Path
from datetime import datetime
import hashlib
import csv


# Gets the SHA-256 hash of a file.
def get_file_hash(file_path):
    value_hash = hashlib.sha256()

    try:
        with open(file_path, "rb") as input_file:
            while True:
                part = input_file.read(4096)

                if not part:
                    break

                value_hash.update(part)

    except IOError as e:
        print("Could not read file:", e)
        return None

    return value_hash.hexdigest()


# Reads known hashes and labels from the CSV.
def read_hashes(hash_file):
    hash_list = {}

    try:
        with open(hash_file, "r", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            if reader.fieldnames is None:
                print("The reference CSV is empty.")
                return None

            if "sha256" not in reader.fieldnames or "label" not in reader.fieldnames:
                print("The CSV needs sha256 and label columns.")
                return None

            for entry in reader:
                if entry["sha256"] and entry["label"]:
                    file_hash = entry["sha256"].strip().lower()
                    label = entry["label"].strip()
                    hash_list[file_hash] = label
                else:
                    print("Skipping a reference row with missing information.")

    except IOError as e:
        print("Could not read the reference CSV:", e)
        return None

    if len(hash_list) == 0:
        print("No usable reference hashes were found.")
        return None

    return hash_list


# Writes the report lines to a text file.
def write_report(report_text, report_path):
    try:
        with open(report_path, "w", encoding="utf-8") as report_file:
            for line in report_text:
                report_file.write(line + "\n")

        print("\nReport saved to:", report_path)

    except IOError as e:
        print("Could not save the report:", e)


input_folder = input("Enter the path to the File Triage package folder: ")
folder_path = Path(input_folder)

if not folder_path.exists():
    print("That folder could not be found.")

else:
    hash_file = folder_path / "hashes_reference.csv"
    hash_list = read_hashes(hash_file)

    if hash_list is not None:
        report_text = []
        duplicates = {}

        for file_path in sorted(folder_path.rglob("*")):
            if (
                file_path.is_file()
                and file_path.name != "README.txt"
                and file_path.name != "hashes_reference.csv"
                and file_path.name != "triage_report.txt"
            ):
                file_hash = get_file_hash(file_path)

                if file_hash is not None:
                    try:
                        details = file_path.stat()
                        edited_time = datetime.fromtimestamp(details.st_mtime)
                        label = hash_list.get(file_hash, "UNKNOWN")

                        result = (
                            f"{file_path.name} | {file_path.suffix} | "
                            f"{details.st_size} bytes | {edited_time} | "
                            f"{file_hash} | {label}"
                        )

                        print(result)
                        report_text.append(result)

                        if file_hash not in duplicates:
                            duplicates[file_hash] = []

                        duplicates[file_hash].append(file_path.name)

                    except IOError as e:
                        error_text = (
                            f"Could not get information for {file_path.name}: {e}"
                        )
                        print(error_text)
                        report_text.append(error_text)

        print("\nDuplicate files:")
        report_text.append("")
        report_text.append("Duplicate files:")

        duplicates_found = False

        for filenames in duplicates.values():
            if len(filenames) > 1:
                duplicate_text = (
                    f"{', '.join(filenames)} have identical content."
                )
                print(duplicate_text)
                report_text.append(duplicate_text)
                duplicates_found = True

        if not duplicates_found:
            print("No duplicate files found.")
            report_text.append("No duplicate files found.")

        report_path = Path(__file__).parent / "triage_report.txt"
        write_report(report_text, report_path)