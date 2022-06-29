import re

# ******************************************** xmlParser helper functions ********************************************

# * Parse the excel file and return a list of dictionaries
def ExcelDictReader(sheet):
    reader = []

    for values in sheet.iter_rows(min_row=2, values_only=True):
        dictReader = {}
        headers = list(sheet.iter_rows(min_row=1, max_row=1, values_only=True))

        for header, value in zip(headers[0], values):
            dictReader[header] = value if value else ""

        reader.append(dictReader)

    return reader


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
