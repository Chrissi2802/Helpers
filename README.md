# Helpers

This repository contains several helper files for python. Help functions and classes are available in these files.


## Overview of the file structure
| Files                                                           | Description                                                   |
| --------------------------------------------------------------- | ------------------------------------------------------------- |
| [classifier_regressor_test.py](classifier_regressor_test.py)    | contains functions for testing all sklearn classifier and regressor   |
| [db_connection_template.yaml](db_connection_template.yaml)      | contains the login data for the SQL database                  |
| [db_connection.py](db_connection.py)                            | contains functions to communicate with a SQL database         |
| [emails_template.yaml](emails_template.yaml)                    | contains the login data to send emails                        |
| [emails.py](emails.py)                                          | contains functions to send emails                             |
| [helpers_ann.py](helpers_ann.py)                                | contains auxiliary functions for artificial neural network (ann)   |
| [helpers_general.py](helpers_general.py)                        | contains general help functions                               |
| [helpers_ml.py](helpers_ml.py)                                  | contains auxiliary functions for machine learning (ml)        |
| [selftest.py](selftest.py)                                      | contains a class for checking Python files                    |


### Checks during selftest
- check_pyflakes: checks Python source files for errors
- check_vulture: finds unused code
- check_file_imported_somewhere: checks if the files were imported into one of the other files
- check_asserts: checks if asserts are present in the main block `if (__name__ == "__main__"):`
- check_main_block: executes the code that is written at `if (__name__ == "__main__"):`

