# * This file holds all the warnings messages shown in the application

DUP_DESCRIPTION_KEYS_WARNING = 'There are duplicate classic teststep descriptions found in your config file. \
Only the DD2.0 translations from the first occurence of the descripton will be used, the rest will be ignored.'

DUP_KEYWORD_SETS_WARNING = 'There are duplicate keyword sets found in your config file. \
Only the DD2.0 translations from the first occurence of the keyword set will be used, the rest will be ignored.'

DUP_REFERENCE_KEYS_WARNINGS = 'There are duplicate reference keys found in your config file. \
Only the reference values from the first occurence of the reference key will be used, the rest will be ignored.'

INVALID_REFERENCE_KEYS_WARNING = 'There are invalid reference keys found in your config file. \
Ensure that all reference keys used are defined in the function parameter sheet.'

EMPTY_MAPPING_FIELDS_WARNINGS = 'There are empty mappings fields found in your config file. \
If the classic description key is left empty, it will not match and teststeps. Any empty DD2.0 fields will be translated to a empty string.'

DUP_FUNCTION_NAMES_WARNINGS = 'There are duplicate function name definitions in the function definition database. \
This could have been caused by and error in the database which can be solved by pulling the original version from git.\
Only the function_parameters from the first occurence of the function_name will be used, the rest will be ignored.'

INVALID_DD2_TRANSLATIONS = 'There are invalid DD2.0 translations found in your config file. \
Ensure that all DD2.0 function library, name and parameters used valid'