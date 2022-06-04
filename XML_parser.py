import xml.etree.ElementTree as ET
from utils import *
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

    
def getTestStepData(xmlInFile, atpMap):
    tree = ET.parse(xmlInFile)
    root = tree.getroot()
    childParentMap = {c: p for p in root.iter() for c in p}
    allTestSteps = root.iter('teststep')
    
    xmlData = []
    idCounter = 0
    
    for teststep in allTestSteps:
        
        #Initialize counter to create id for each test step
        
        # Get teststep description attribute from teststep
        teststepDesc = teststep.get('desc')
        
        if teststepDesc in atpMap:
            idCounter += 1
            testStepData = {
                'id': idCounter,
                'parentId': childParentMap[teststep].get('id'),
                'description': teststepDesc,
                'function_library': teststep.find('function_library').text,
                'function_name': teststep.find('function_name').text,
                'function_parameters': [{
                    'name': param.get('name'),
                    'text': param.text.strip('\n ')
                    } for param in teststep.find('function_parameters').iter('param')]
            }
            
            xmlData.append(testStepData)
        
    return xmlData


def convertXML(xmlInFile, xmlOutFile, atpMap):
    tree = ET.parse(xmlInFile)
    root = tree.getroot()
    allTestSteps = root.iter('teststep')

    for teststep in allTestSteps:
       
        # Get teststep description attribute from teststep
        oldtestStepDescription = teststep.attrib['desc']

        # IF teststep description finds match in atpMap - convert to new version
        if oldtestStepDescription in atpMap:
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
            print(f'''
                {teststep.get('desc')}
                {oldFunctionLibrary.text}
                {oldFunctionName.text}
                {[f"{param.get('name')}={param.text}" for param in oldFunctionParams]}
            ''')
            
    tree.write(xmlOutFile)


def testHandleXlsx():
    xlsxFile = './testdata/mapping.xlsx'
    xmlFile = './testdata/input.xml'
    
    atpMap = handleXlsx(xlsxFile)
    print(atpMap['[CAN] Check TMU Mute Signal'])

def testHandleConvertXML():
    xlsxFile = './testdata/mapping.xlsx'
    xmlFile = './testdata/input.xml'

    atpMap = handleXlsx(xlsxFile)
    convertXML(xmlFile, './testdata/output.xml', atpMap)
    
def testHandleGetTestStepData():
    xlsxFile = './testdata/mapping.xlsx'
    xmlFile = './testdata/input.xml'
    
    atpMap = handleXlsx(xlsxFile)
    
    for item in getTestStepData(xmlFile, atpMap):
        print(item)
        break
    
    
if __name__ == '__main__':
    testHandleGetTestStepData()
