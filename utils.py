import re

# ******************************************** xmlParser helper functions ********************************************

# * Parse the excel file and return a list of dictionaries
def ExcelDictReader(sheet):
    for values in sheet.iter_rows(min_row=2, values_only=True):
        row = {}
        headers = list(sheet.iter_rows(min_row=1, max_row=1, values_only=True))[0]

        for header, value in zip(headers, values):
            row[header] = value if value else ""

        yield row

def removeWhiteSpace(string):
    pattern = re.compile(r"\s+")

    return re.sub(pattern, "", string)


# *********************************************** PyQt helper functions ***********************************************


def iterLayout(layout):  # Unsued
    return [layout.itemAt(i) for i in range(layout.count())]


def getLayoutWidgets(layout):  # Unsued
    items = iterLayout(layout)
    return [item.widget() for item in items if item.widget()]


if __name__ == "__main__":
    pass
