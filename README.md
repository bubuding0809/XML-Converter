# ATPxml converter app (Project planning)

## Core Features:

- [x] Receives xml file as input.
- [x] Receives xlsx file with mapping requirements.
- [x] Parse xml file and map over old data with new data as specified in the xlsx file.
- [x] Outputs newly parsed xml file for user to use in ATP

---

## Core UI Features:

- [x] File Input field for xml file, via file-explorer
- [x] File Input field for xlsx file, via file-explorer
- [x] Convert button to trigger conversion
- [x] Filedialogue widget to save file to specified directory
- [x] load data function to load filtered XML data
- [x] Select all checkbox to toggle selection of testcase to be converted
- [x] Group matched teststeps under respective testcases and functions
- [x] Make this teststeps groups collapsable to aid focus on individual groups

---

## Additional Features:

- [x] Data-grid to display xml file contents pre-conversion
- [x] Data-grid to display xml file contents post-conversion  
       with conditioanl highlighting
- [x] Interative data-grid that allows for selection of test-steps filtered for conversion

---

## To-do implementations: Feature Alignment and Progress 10/6/2022

- [x] Add Error check for Xlsx config.
      For example: If user mistyped one of the old test step description, program will prompt user that that specific test step entered has no match. If a config file with the wrong structure has been submitted (wrong headers or extra columns) and error prompt will be shown.
- [x] Implement direct configuration of conversion parameters in the data grid in case there are errors in the Xlsx.
- [x] Conversion summary for an overview of the testcases that has been chosen to be converted.
- [x] Release of Xlsx config format to the test team for them to start defining there conversion parameters.
- [ ] To be provided with more xml test files from the test team to check if conversion works on ATP.
- [ ] Implement batch conversion of xml files.
- [ ]

---

## To-do implementations: First build release and additional feature implementation 20/6/2022

<details open>
  <summary>UI implementations</summary>
  <br>

- [x] Prevent user from selecting temp excel files which starts with ~$
- [x] Remove load button and implement loading of data directly after both config and xml file has been uploaded
- [x] Implement filter feature to allow user to choose to show testcase/functions/all
- [x] Implement right click context menu for old parameter list with the following features
  - Append parameters to new parameter list
  - Replace new parameter list with old parameters
- [x] Change direct editing of DD2 mapping in the UI data grid to propagate to all similar teststeps instead of only for the particular teststep.
- [x] Add option to output updated config file based on the changes in the UI data grid
</details>

<details>
  <summary>Config parser implementations</summary>
  <br>

- [x] Add multiple classic ATP test step description mapping for a single teststep.
  - ![config image](media\images\config_classicATP.png "config image")
- [x] Add keyword column in excel config file for users to define must have keywords for match. keywords are seperated by a newline(\n) which indicates an AND relation.
  - ![config image](media\images\config_keywords.png "config image")
- [x] Catch multiple classic description key error
- [ ] Implement parameter referencing in the config excel
  - ![config image](media\images\config_at_reference.PNG "config image")
  - ![config image](media\images\config_sharp_reference.PNG "config image")
- [ ] Add integrity check for function library, function name and function parameters at column C,D and E of excel config. To be provided with a list of valid info to check against.
</details>

---

## Software stack used:

- Python Programming language
- PyQT GUI framework
