import re

# ******************************************** helper functions ********************************************

# * Parse the excel file and return a list of dictionaries each dictionary containing header mapped to cell value
def ExcelDictReader(sheet):
    for values in sheet.iter_rows(min_row=2, values_only=True):
        row = {}
        headers = list(sheet.iter_rows(min_row=1, max_row=1, values_only=True))[0]

        for header, value in zip(headers, values):
            row[header] = value if value else ""

        yield row

# * function to strip all white space from a string
def removeWhiteSpace(string):
    pattern = re.compile(r"\s+")

    return re.sub(pattern, "", string)

