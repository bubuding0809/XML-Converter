import xml.etree.ElementTree as ET

def ExcelDictReader(sheet):
    reader = []

    for values in sheet.iter_rows(min_row=2, values_only=True):
        dictReader = {}
        headers = list(sheet.iter_rows(min_row=1, max_row=1, values_only=True))

        for header, value in zip(headers[0], values):
            dictReader[header] = value if value else ''

        reader.append(dictReader)

    return reader

def getAllTestSteps(xmlInfile):
    tree = ET.parse(xmlInfile)
    root = tree.getroot()
    
    return root.iter('teststep')
