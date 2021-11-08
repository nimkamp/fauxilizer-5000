import json
import csv
from os.path import exists


def solution(X):
    # We assume X is a csv file
    categories = {"real", "fake", "ambiguous"}
    rows = []

    path = exists(X)

    # check if X is actually a file, if not return an error
    if path == False:
        raise ValueError("File does not exist")

    with open(X, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        row_values = list(map(tuple, csv_reader))

    # Must have 4 columns
    if len(row_values[0]) != 4:
        raise ValueError("Number of columns must equal 4")

    (experiment_name, sample_id, fauxness, category_guess) = row_values[0]

    # Check to see if headers match
    if experiment_name == 'experiment_name' and sample_id == 'sample_id' and fauxness == 'fauxness' and category_guess == 'category_guess':
        headers = row_values[0]
        del row_values[0]
        for row in row_values:
            # Check to make sure we still have 4 columns per row.
            if len(row) != 4:
                raise ValueError("Number of columns must equal 4")

            (experiment_name, sample_id, fauxness, category_guess) = row

            # validation

            if experiment_name == "":
                raise ValueError("experiment_name cannot be empty")
            elif is_valid_sample_id(sample_id) == False:
                raise ValueError(
                    "sample_id must be a positive integer and must be whole numbers.")
            elif is_valid_fauxness(fauxness) == False:
                raise ValueError(
                    "fauxness is not in the range of 0.0 and 1.0 inclusive.")
            elif category_guess not in categories:
                raise ValueError(
                    "category_guess must be either real, fake, or ambigious.")
            else:
                rows.append(row)

            # function calls to test below

            summaryData = display_summary_data(row_values)
            print("Summary Data: ", summaryData)

            print("JSON: ", display_json(row_values, headers, 0))

            print("CSV: ", display_csv(row_values, 0))
            print("In Memory: ", display_in_memory(row_values, 0))
    else:
        raise ValueError("Column headers are invalid.")

# int -> bool


def is_valid_sample_id(sample_id):
    if sample_id.isdigit() == False or int(sample_id) <= 0:
        return False
    else:
        return True

# float -> bool


def is_valid_fauxness(fauxness):
    if float(fauxness) > 1.0 or float(fauxness) < 0.0:
        return False

    potentialFloat = fauxness.replace('.', '', 1).isdigit()
    return potentialFloat

# return json representation of values


def display_json(list_of_tuple, headers, row_number):
    output = dict()
    for idx, key in enumerate(headers):
        output[key] = list_of_tuple[row_number][idx]
    jsonObj = json.dumps(output)
    return jsonObj

# return csv representation of values


def display_csv(rows, row_number):
    csv_representation = ""
    for value in rows[row_number]:
        csv_representation += value + ","
    return csv_representation

# return in memory representation of values


def display_in_memory(rows, row_number):
    return rows[row_number]

# return summary data is json format


def display_summary_data(rows):
    return json.dumps(rows)


solution('path/to/fauxfile')
