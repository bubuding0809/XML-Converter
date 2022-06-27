from distutils.command.clean import clean
from distutils.command.config import config
import xml.etree.ElementTree as ET
from utils import *
from openpyxl import load_workbook
import os

baseDir = os.path.dirname(__file__)

#********************************************************* Application functions ********************************************************#


def handleXlsx(xlsxFile):
    # Load excel file with openpyxl load_workbook
    workbook = load_workbook(filename=xlsxFile)
    sheet = workbook.active

    # Convert excel sheet into a list of dictionary with header:value pairs
    reader = ExcelDictReader(sheet)

    conversionMap = {}
    duplicateDescriptionkeys = []

    for rowCount, row in enumerate(reader):
        # Create mapping based on each row
        # Convert old description to lower case to ensure case insensitive matching
        keywords = [keyword for keyword in row['keywords'].split('\n') if keyword]
        oldDescriptions = [description for description in row['classic teststep description'].split('\n') if description]
        cleanedOldDescriptions = [removeWhiteSpace(description.lower()) for description in oldDescriptions]

        new_description = row['DD2 teststep description'].strip()
        new_function_library = row['DD2 function_library'].strip()
        new_function_name = row['DD2 function_name'].strip()
        new_function_parameters = []

        funcParams = [param.strip()
                      for param in row['DD2 function_parameters'].split('\n')]
        for param in funcParams:
            if len(param):
                param = param.split('=')
                new_function_parameters.append({
                    'name': param[0],
                    'text': param[1]
                })

        if not cleanedOldDescriptions:
            cleanedOldDescriptions.append(f"empty_description_key - [row: {rowCount+2}]")

        for cleanedOldDescription, oldDescription in zip(cleanedOldDescriptions, oldDescriptions):

            if cleanedOldDescription not in conversionMap:
                conversionMap[cleanedOldDescription] = {
                    'isMatched': False,
                    'configRowCount': rowCount + 2,
                    'oldDescription': oldDescription,
                    'description': new_description,
                    'function_library': new_function_library,
                    'function_name': new_function_name,
                    'function_parameters': new_function_parameters,
                }
            else:
                duplicateDescriptionkeys.append(f"{oldDescription} - [row: {rowCount+2}]")


    return conversionMap, duplicateDescriptionkeys


def getTeststepsWithEmptyFields(conversion_map):
    teststeps_with_empty_field = []

    for index, (cleandedOldDescription, mapping) in enumerate(conversion_map.items()):
        empty_fields = []

        # Check if there are any empty fields in the teststep
        for tag, value in mapping.items():

            if tag == 'isMatched':
                continue
            
            if not value:
                empty_fields.append(tag)

        # If there are empty fields for the teststep, create obj with description and empty fields then add to list
        if empty_fields:

            if cleandedOldDescription.startswith('empty_description_key'):
                description = cleandedOldDescription
            else:
                description = f"{mapping['oldDescription']} - [row: {mapping['configRowCount']}]"

            teststeps_with_empty_field.append({
                'description': description,
                'emptyFields': empty_fields
            })    
    
    return teststeps_with_empty_field


def handleXlsxUpdate(configData, xlsxInFile, xlsxOutFile):

    #* Load excel file with openpyxl load_workbook
    workbook = load_workbook(filename=xlsxInFile)
    sheet = workbook.active
    
    #* Update config excel with the new mapping data generated from the application UI
    for configRowCount, mapping in configData.items():
        #* Update config excel column B, C, D, E with new data
        cell = sheet['C' + str(configRowCount)]
        cell.value = mapping['description']

        cell = sheet['D' + str(configRowCount)]
        cell.value = mapping['function_library']

        cell = sheet['E' + str(configRowCount)]
        cell.value = mapping['function_name']

        cell = sheet['F' + str(configRowCount)]
        cell.value = '\n'.join(mapping['function_params'])

    workbook.save(xlsxOutFile)


def getTestStepData(xmlInFile, conversionMap):
    tree = ET.parse(xmlInFile)
    root = tree.getroot()
    childParentMap = {child: parent for parent in root.iter()
                      for child in parent}
    allTestSteps = root.iter('teststep')

    # Initialize xmlData list
    xmlData = []

    for index, teststep in enumerate(allTestSteps):

        # Get teststep description attribute from teststep
        oldDescription = teststep.get('desc')
        cleanedOldDescription = removeWhiteSpace(oldDescription.lower())

        if cleanedOldDescription in conversionMap:
            # If teststep description finds match in conversionMap - set isMatched to True
            conversionMap[cleanedOldDescription]['isMatched'] = True

            # Get all teststep children
            oldFunctionLibrary = teststep.find('function_library').text
            oldFunctionName = teststep.find('function_name').text
            oldFunctionParams = teststep.find(
                'function_parameters').iter('param')

            # Create old data object
            oldTestStepData = {
                'cleanedDescription': cleanedOldDescription,
                'description': oldDescription,
                'function_library': oldFunctionLibrary,
                'function_name': oldFunctionName,
                'function_parameters': [{
                    'name': param.get('name'),
                    'text': param.text.strip('\n ')
                } for param in oldFunctionParams]
            }

            # Create new data object
            newTestStepData = {
                'description': conversionMap[cleanedOldDescription]['description'],
                'function_library': conversionMap[cleanedOldDescription]['function_library'],
                'function_name': conversionMap[cleanedOldDescription]['function_name'],
                'function_parameters': [{
                    'name': param['name'].strip(),
                    'text': param['text'].strip('\n ')
                } for param in conversionMap[cleanedOldDescription]['function_parameters']]
            }

            # Append to teststep data list
            xmlData.append({
                'id': index + 1,
                'parentId': childParentMap[teststep].get('id'),
                'parentType': childParentMap[teststep].tag,
                'parentName': childParentMap[teststep].get('name'),
                'configRowCount': conversionMap[cleanedOldDescription]['configRowCount'],
                'old': oldTestStepData,
                'new': newTestStepData,
            })

    return xmlData, conversionMap


def convertXml(filteredIds, xmlInFile, xmlOutFile, conversionMap):
    tree = ET.parse(xmlInFile)
    root = tree.getroot()
    counter = 0

    # Create a teststep object for every teststep in the xml
    allTestSteps = [{'id': index + 1, 'teststep': teststep}
                    for index, teststep in enumerate(root.iter('teststep'))]

    print('Displaying converted teststeps')
    for index, teststep in enumerate(allTestSteps):

        # Get teststep description attribute from teststep
        oldtestStepDescription = teststep['teststep'].get('desc')
        oldtestStepDescription = f"ID: {index+1} - {oldtestStepDescription}"

        # If teststep description finds match in conversionMap - convert to new version
        if oldtestStepDescription in conversionMap and teststep['id'] in filteredIds:
            counter += 1
            matchedConfig = conversionMap[oldtestStepDescription]

            # Change old teststep description to new description
            teststep['teststep'].set('desc', matchedConfig['description'])

            # Change old function_library text to new function_library text
            oldFunctionLibrary = teststep['teststep'].find('function_library')
            oldFunctionLibrary.text = matchedConfig['function_library']

            # Change old function_name text to new function_name text
            oldFunctionName = teststep['teststep'].find('function_name')
            oldFunctionName.text = matchedConfig['function_name']

            # Delete old function parameters and replace with new ones from conversionMap
            oldFunctionParams = teststep['teststep'].find(
                'function_parameters')

            # remove existing param elements from function_parameters
            for param in list(oldFunctionParams.iter('param')):
                oldFunctionParams.remove(param)

            # create new param elements and append to function_parameters
            for param in matchedConfig['function_parameters']:
                newParam = ET.SubElement(oldFunctionParams, 'param')
                newParam.set('name', param['name'])
                newParam.text = param['text']

            # Debug print
            print(f'''
id: {teststep['id']}
{teststep['teststep'].get('desc')}
{oldFunctionLibrary.text}
{oldFunctionName.text}
{[f"{param.get('name')}={param.text}" for param in oldFunctionParams]}
            ''')

            print(
                f"Converted teststeps: {counter} ______________________________________________________________________________________________")

    # Write modified xml file to specificed file location
    tree.write(xmlOutFile)


#********************************************************* Test functions ********************************************************#
def testHandleXlsx():
    xlsxFile = os.path.join(baseDir, 'samples/config_v2.xlsx')

    conversionMap, duplicateKeys = handleXlsx(xlsxFile)



    for index, (key, value) in enumerate(conversionMap.items()):
        print(f"{index+1}: Classic key: {key}")
        print('------------------------------')
        for key, value in value.items():
            print(f'{key}: {value}')
        print()

    print()

    for item in duplicateKeys:
        print(item)




def testHandleConvertXML():
    xlsxFile = './testdata/config.xlsx'
    xmlFile = './testdata/input.xml'

    conversionMap = handleXlsx(xlsxFile)
    convertXml(xmlFile, './testdata/output.xml', conversionMap)


def testHandleGetTestStepData():
    xlsxFile = './testdata/config.xlsx'
    xmlFile = './testdata/input.xml'

    conversionMap = handleXlsx(xlsxFile)

    for item in getTestStepData(xmlFile, conversionMap):
        for key, value in item.items():
            print(f'{key}: {value}')
            print()
        print('___________________________________________________________________________________________')


if __name__ == '__main__':
    testHandleXlsx()