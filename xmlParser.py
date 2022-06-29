import xml.etree.ElementTree as ET
from utils import removeWhiteSpace, ExcelDictReader
from openpyxl import load_workbook
import os

baseDir = os.path.dirname(__file__)

# ********************************************************* Application functions ********************************************************#

def handleXlsx(xlsxFile):
    # Load excel file with openpyxl load_workbook
    workbook = load_workbook(filename=xlsxFile)
    sheet = workbook.active

    # Convert excel sheet into a list of dictionary with header:value pairs
    reader = ExcelDictReader(sheet)

    conversionMap = {}
    keywordMap = {}
    duplicateDescriptionkeys = []
    duplicateKeywords = []

    # * Create mapping based on each row
    for rowCount, row in enumerate(reader):

        # Get keywords from each row
        keywords = tuple(set([
            removeWhiteSpace(keyword.lower())
            for keyword in row["keywords"].split("\n")
            if keyword
        ]))

        # Get classic description from each row
        oldDescriptions = [
            description
            for description in row["classic teststep description"].split("\n")
            if description
        ]

        # Convert classic description to lower case to ensure case insensitive matching
        cleanedOldDescriptions = [
            removeWhiteSpace(description.lower()) for description in oldDescriptions
        ]

        # * Get DD2.0 translations
        new_description = row["DD2 teststep description"].strip()
        new_function_library = row["DD2 function_library"].strip()
        new_function_name = row["DD2 function_name"].strip()
        new_function_parameters = []
        funcParams = [
            param.strip()
            for param in row["DD2 function_parameters"].split("\n")
            if param
        ]
        for param in funcParams:
            param_name_text = [item.strip() for item in param.split("=")]
            if len(param_name_text) == 2:
                new_function_parameters.append({
                    "name": param_name_text[0],
                    "text": param_name_text[1]
                })

        # * If classic description field is empty, append a empty_description_key
        if not cleanedOldDescriptions:
            cleanedOldDescriptions.append(
                f"empty_description_key - [row: {rowCount+2}]"
            )
            # continue

        # * Iterate through cleanded and original description together, add first instance of mapping to conversionMap
        # * else append it to the duplicate description keys list
        for cleanedOldDescription, oldDescription in zip(
            cleanedOldDescriptions, oldDescriptions
        ):

            if cleanedOldDescription not in conversionMap:
                conversionMap[cleanedOldDescription] = {
                    "isMatched": False,  # matching flag to check if mapping has been matched in the xml input
                    "configRowCount": rowCount + 2,  # Store excel row number of mapping
                    "oldDescription": oldDescription,
                    "description": new_description,
                    "function_library": new_function_library,
                    "function_name": new_function_name,
                    "function_parameters": new_function_parameters,
                }
            else:
                duplicateDescriptionkeys.append(
                    f"{oldDescription} - [row: {rowCount+2}]"
                )

        if not keywords:
            continue

        if keywords not in keywordMap:
            keywordMap[keywords] = {
                "isMatched": False,  # matching flag to check if mapping has been matched in the xml input
                "configRowCount": rowCount + 2,  # Store excel row number of mapping
                "oldDescription": oldDescription,
                "description": new_description,
                "function_library": new_function_library,
                "function_name": new_function_name,
                "function_parameters": new_function_parameters,
            }
        else:
            duplicateKeywords.append(
                f"{keywords} - [row: {rowCount+2}]"
            )

    return (conversionMap, duplicateDescriptionkeys,
            keywordMap, duplicateKeywords)


def getTeststepsWithEmptyFields(conversion_map):
    teststeps_with_empty_field = []

    for cleandedOldDescription, mapping in conversion_map.items():
        empty_fields = []

        # * Check if there are any empty fields in the teststep
        for tag, value in mapping.items():

            if tag == "isMatched":
                continue

            if not value:
                empty_fields.append(tag)

        # * If there are empty fields for the teststep, create obj with description and empty fields then add to list
        if empty_fields:

            if cleandedOldDescription.startswith("empty_description_key"):
                description = cleandedOldDescription
            else:
                description = (
                    f"{mapping['oldDescription']} - [row: {mapping['configRowCount']}]"
                )

            teststeps_with_empty_field.append(
                {"description": description, "emptyFields": empty_fields}
            )

    return teststeps_with_empty_field


def handleXlsxUpdate(configData, xlsxInFile, xlsxOutFile):

    # * Load excel file with openpyxl load_workbook
    workbook = load_workbook(filename=xlsxInFile)
    sheet = workbook.active

    # * Update config excel with the new mapping data generated from the application UI
    for configRowCount, mapping in configData.items():
        # * Update config excel column B, C, D, E with new data
        cell = sheet["C" + str(configRowCount)]
        cell.value = mapping["description"]

        cell = sheet["D" + str(configRowCount)]
        cell.value = mapping["function_library"]

        cell = sheet["E" + str(configRowCount)]
        cell.value = mapping["function_name"]

        cell = sheet["F" + str(configRowCount)]
        cell.value = "\n".join(mapping["function_params"])

    workbook.save(xlsxOutFile)


def getTestStepData(xmlInFile, conversionMap, keywordMap):
    tree = ET.parse(xmlInFile)
    root = tree.getroot()
    childParentMap = {child: parent for parent in root.iter()
                      for child in parent}
    allTestSteps = root.iter("teststep")

    # Initialize xmlData list
    xmlData = []

    for index, teststep in enumerate(allTestSteps):

        # Get teststep description attribute from teststep
        oldDescription = teststep.get("desc")
        cleanedOldDescription = removeWhiteSpace(oldDescription.lower())

        # * If teststep description matches a mapping in conversionMap, generate data object and append to xmlData
        if cleanedOldDescription in conversionMap:
            # If teststep description finds match in conversionMap - set isMatched to True
            conversionMap[cleanedOldDescription]["isMatched"] = True

            # Get all teststep children
            oldFunctionLibrary = teststep.find("function_library").text
            oldFunctionName = teststep.find("function_name").text
            oldFunctionParams = teststep.find(
                "function_parameters").iter("param")

            # Create old data object
            oldTestStepData = {
                "cleanedDescription": cleanedOldDescription,
                "description": oldDescription,
                "function_library": oldFunctionLibrary,
                "function_name": oldFunctionName,
                "function_parameters": [
                    {"name": param.get("name"),
                     "text": param.text.strip("\n ")}
                    for param in oldFunctionParams
                ],
            }

            # Create new data object
            newTestStepData = {
                "description": conversionMap[cleanedOldDescription]["description"],
                "function_library": conversionMap[cleanedOldDescription][
                    "function_library"
                ],
                "function_name": conversionMap[cleanedOldDescription]["function_name"],
                "function_parameters": [
                    {"name": param["name"].strip(
                    ), "text": param["text"].strip("\n ")}
                    for param in conversionMap[cleanedOldDescription][
                        "function_parameters"
                    ]
                ],
            }

            # Append to teststep data list
            xmlData.append(
                {
                    "id": index + 1,
                    "parentId": childParentMap[teststep].get("id"),
                    "parentType": childParentMap[teststep].tag,
                    "parentName": childParentMap[teststep].get("name"),
                    "configRowCount": conversionMap[cleanedOldDescription][
                        "configRowCount"
                    ],
                    "old": oldTestStepData,
                    "new": newTestStepData,
                }
            )

        # * If a teststep description matches a particular set of keywords, generate data object and append to xmlData
        for keys, mapping in keywordMap.items():

            # if a key does not match the description skip generate data object for the mapping
            isAllMatched = True
            for key in keys:
                if key not in cleanedOldDescription:
                    isAllMatched = False

            if not isAllMatched: continue

            oldFunctionLibrary = teststep.find("function_library").text
            oldFunctionName = teststep.find("function_name").text
            oldFunctionParams = teststep.find(
                "function_parameters").iter("param")

            # Create old data object
            oldTestStepData = {
                "cleanedDescription": cleanedOldDescription,
                "description": oldDescription,
                "function_library": oldFunctionLibrary,
                "function_name": oldFunctionName,
                "function_parameters": [
                    {"name": param.get("name"),
                     "text": param.text.strip("\n ")}
                    for param in oldFunctionParams
                ],
            }

            # Create new data object
            newTestStepData = {
                "description": mapping["description"],
                "function_library": mapping["function_library"],
                "function_name": mapping["function_name"],
                "function_parameters": [
                    {"name": param["name"].strip(
                    ), "text": param["text"].strip("\n ")}
                    for param in mapping["function_parameters"]
                ],
            }

            # Append to teststep xmlData if teststep id has not been matched yet
            if next((item for item in xmlData if item['id'] == index+1), None) is None:
                
                xmlData.append({
                    "id": index + 1,
                    "parentId": childParentMap[teststep].get("id"),
                    "parentType": childParentMap[teststep].tag,
                    "parentName": childParentMap[teststep].get("name"),
                    "configRowCount": mapping["configRowCount"],
                    "old": oldTestStepData,
                    "new": newTestStepData,
                })

    return xmlData, conversionMap


def convertXml(filteredIds, xmlInFile, xmlOutFile, conversionMap):
    tree = ET.parse(xmlInFile)
    root = tree.getroot()
    counter = 0

    # Create a teststep object for every teststep in the xml
    allTestSteps = [
        {"id": index + 1, "teststep": teststep}
        for index, teststep in enumerate(root.iter("teststep"))
    ]

    print("Displaying converted teststeps")
    for index, teststep in enumerate(allTestSteps):

        # Get teststep description attribute from teststep
        oldtestStepDescription = teststep["teststep"].get("desc")
        oldtestStepDescription = f"ID: {index+1} - {oldtestStepDescription}"

        # If teststep description finds match in conversionMap - convert to new version
        if oldtestStepDescription in conversionMap and teststep["id"] in filteredIds:
            counter += 1
            matchedConfig = conversionMap[oldtestStepDescription]

            # Change old teststep description to new description
            teststep["teststep"].set("desc", matchedConfig["description"])

            # Change old function_library text to new function_library text
            oldFunctionLibrary = teststep["teststep"].find("function_library")
            oldFunctionLibrary.text = matchedConfig["function_library"]

            # Change old function_name text to new function_name text
            oldFunctionName = teststep["teststep"].find("function_name")
            oldFunctionName.text = matchedConfig["function_name"]

            # Delete old function parameters and replace with new ones from conversionMap
            oldFunctionParams = teststep["teststep"].find(
                "function_parameters")

            # remove existing param elements from function_parameters
            for param in list(oldFunctionParams.iter("param")):
                oldFunctionParams.remove(param)

            # create new param elements and append to function_parameters
            for param in matchedConfig["function_parameters"]:
                newParam = ET.SubElement(oldFunctionParams, "param")
                newParam.set("name", param["name"])
                newParam.text = param["text"]

            # Debug print
            print(
                f"""
id: {teststep['id']}
{teststep['teststep'].get('desc')}
{oldFunctionLibrary.text}
{oldFunctionName.text}
{[f"{param.get('name')}={param.text}" for param in oldFunctionParams]}
            """
            )

            print(
                f"Converted teststeps: {counter} ______________________________________________________________________________________________"
            )

    # Write modified xml file to specificed file location
    tree.write(xmlOutFile)


# ********************************************************* Test functions ********************************************************#

def testHandleXlsx():
    xlsxFile = os.path.join(baseDir, "samples/configTest_v2.xlsx")

    conversionMap, duplicateKeys, keywordMap, duplicateKeywords = handleXlsx(
        xlsxFile)

    print('_____________________Conversion map____________________')
    for index, (key, value) in enumerate(conversionMap.items()):
        print(f"{index+1}: Classic key: {key}")
        print("------------------------------")
        for key, value in value.items():
            print(f"{key}: {value}")
        print()
    print()

    print('_____________________Duplicate keys____________________')
    for item in duplicateKeys:
        print(item)
        print()
    print()

    print('_____________________Keyword map____________________')
    for index, (key, value) in enumerate(keywordMap.items()):
        print(f"{index+1}: Classic key: {key}")
        print("------------------------------")
        for key, value in value.items():
            print(f"{key}: {value}")
        print()
    print()

    print('_____________________Duplicate keywords____________________')
    for item in duplicateKeywords:
        print(item)
    print()


def testHandleConvertXML():
    xlsxFile = "./testdata/config.xlsx"
    xmlFile = "./testdata/input.xml"

    conversionMap = handleXlsx(xlsxFile)
    convertXml(xmlFile, "./testdata/output.xml", conversionMap)


def testHandleGetTestStepData():
    xlsxFile = "./samples/config.xlsx"
    xmlFile = "./samples/input.xml"

    conversionMap = handleXlsx(xlsxFile)

    for item in getTestStepData(xmlFile, conversionMap):
        for key, value in item.items():
            print(f"{key}: {value}")
            print()
        print(
            "___________________________________________________________________________________________"
        )


if __name__ == "__main__":
    #testHandleXlsx()
    pass
