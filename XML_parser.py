import xml.etree.ElementTree as ET
from utils import ExcelDictReader
from openpyxl import load_workbook

def handleXlsx(xlsxFile):
    #Load excel file with openpyxl load_workbook
    workbook = load_workbook(filename=xlsxFile)
    sheet = workbook.active

    #Convert excel sheet into a list of dictionary with header:value pairs
    reader = ExcelDictReader(sheet)

    #Convert dictionary list into atpMap
    atpMap = {}
    for row in reader:

        funcParams = row['function_parameters'].split('\n')
        newfuncParamsPair = []

        for param in funcParams:
            param = param.split('=')
            paramNameText = {
                'name': param[0],
                'text': param[1]
            }
            newfuncParamsPair.append(paramNameText)

        atpMap[row['teststep.desc old']] = {
            'test_step.desc': row['test_step.desc new'],
            'function_library': row['function_library'],
            'function_name': row['function_name'],
            'function_parameters': newfuncParamsPair,
        }

    return atpMap

def convertXML(xmlInFile, xmlOutFile, atpMap):
    tree = ET.parse(xmlInFile)
    root = tree.getroot()
    teststeps = root.iter('teststep')

    for teststep in teststeps:
       
        # Get teststep description attribute from teststep
        testDesc = teststep.attrib['desc']

        # IF teststep description finds match in atpMap - convert to new version
        if testDesc in atpMap:
            oldtestStepDescription = teststep.attrib.get('desc')
            matchPairs = atpMap[oldtestStepDescription]

            #Change old teststep description to new description
            teststep.set('desc', matchPairs['test_step.desc'])

            #Change old function_library text to new function_library text
            oldFunctionLibrary = teststep.find('function_library')
            oldFunctionLibrary.text = matchPairs['function_library']

            #Change old function_name text to new function_name text
            oldFunctionName = teststep.find('function_name')
            oldFunctionName.text = matchPairs['function_name']

            #Delete old function parameters and replace with new ones from atpMap
            oldFunctionParams = teststep.find('function_parameters')

            #remove existing param elements from function_parameters
            for param in list(oldFunctionParams.iter('param')):
                oldFunctionParams.remove(param)
               
            #create new param elements and append to function_parameters
            for param in matchPairs['function_parameters']:
                newParam = ET.SubElement(oldFunctionParams, 'param')
                newParam.set('name', param['name'])
                newParam.text = param['text']


            #Format newly populated function_parameters with proper indents and next lines
            ET.indent(oldFunctionParams, space=''*4)

            print(f'''
{teststep.get('desc')}
{oldFunctionLibrary.text}
{oldFunctionName.text}
{[f"{param.get('name')}={param.text}" for param in oldFunctionParams]}
            ''')
    tree.write(xmlOutFile)


def main():
    xlsxFile = 'mapping.xlsx'
    xmlFile = 'input.xml'

    atpMap = handleXlsx(xlsxFile)
    convertXML(xmlFile, 'output.xml', atpMap)

if __name__ == '__main__':
    main()

