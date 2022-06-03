# ATPxml converter app (Project planning)

## Core Features:

- [ ] Receives xml file as input.
- [ ] Receives xlsx file with mapping requirements.
- [ ] Parse xml file and map over old data with new data as specified in the xlsx file.
- [ ] Outputs newly parsed xml file for user to use in ATP

## Core UI Features:

- [x] File Input field for xml file, via file-explorer
- [x] File Input field for xlsx file, via file-explorer
- [x] Convert button to trigger conversion
- [x] Filedialogue widget to save file to specified directory
- [ ] load data function to load filtered XML data
- [ ] Select all checkbox to toggle selection of testcase to be converted
- [ ] Group matched teststeps under respective testcases and functions
- [ ] Make this teststeps groups collapsable to aid focus on individual groups

## Additional Features:

- [ ] Data-grid to display xml file contents pre-conversion with conditonal highlighting
- [ ] Data-grid to display xml file contents post-conversion  
       with conditioanl highlighting
- [ ] Interative data-grid that allows for selection of test-steps filtered for conversion

## Software stack used:

- Python Programming language
- PyQT GUI framework
