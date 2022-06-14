# ATPxml converter app (Project planning)

## Core Features:

- [x] Receives xml file as input.
- [x] Receives xlsx file with mapping requirements.
- [x] Parse xml file and map over old data with new data as specified in the xlsx file.
- [x] Outputs newly parsed xml file for user to use in ATP

## Core UI Features:

- [x] File Input field for xml file, via file-explorer
- [x] File Input field for xlsx file, via file-explorer
- [x] Convert button to trigger conversion
- [x] Filedialogue widget to save file to specified directory
- [x] load data function to load filtered XML data
- [x] Select all checkbox to toggle selection of testcase to be converted
- [x] Group matched teststeps under respective testcases and functions
- [x] Make this teststeps groups collapsable to aid focus on individual groups

## Additional Features:

- [x] Data-grid to display xml file contents pre-conversion
- [x] Data-grid to display xml file contents post-conversion  
       with conditioanl highlighting
- [x] Interative data-grid that allows for selection of test-steps filtered for conversion

## To-do implementations:

- [x] Add Error check for Xlsx config.
      For example: If user mistyped one of the old test step description, program will prompt user that that specific test step entered has no match. If a config file with the wrong structure has been submitted (wrong headers or extra columns) and error prompt will be shown.
- [ ] Implement direct configuration of conversion parameters in the data grid in case there are errors in the Xlsx.
- [ ] Conversion summary for an overview of the testcases that has been chosen to be converted.
- [ ] To be provided with more xml test files from the test team to check if conversion works on ATP.
- [ ] Implement batch conversion of xml files.
- [x] Release of Xlsx config format to the test team for them to start defining there conversion parameters.

## Software stack used:

- Python Programming language
- PyQT GUI framework
