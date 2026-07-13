# ATR (Automated Test Reconciliation) Engine - Project Specification



## Project Overview



Design and develop a reusable Python-based **ATR (Automated Test Reconciliation) Engine** that compares two datasets (**Source** and **Target**) and generates a comprehensive reconciliation report.



The engine should support datasets from both **files** and **databases**.



### Supported Data Sources



#### File Sources



* CSV

* Excel

* TSV

* Any future tabular file formats



#### Database Sources



* Oracle Database

* Snowflake

* PostgreSQL

* Any future supported databases



### Reconciliation Results



Every record must be classified into exactly one of the following categories:



* Matched Records

* Mismatched Records

* Source Only Records

* Target Only Records



The engine must support executing multiple reconciliation test cases in a single run.



---



# Supported Input Sources



## Source and Target Data



### File Sources



If the source or target type is **File**, the datasets are stored in:



* `resources/source`

* `resources/target`



### Database Sources



If the source or target type is **Database**, the database connection details are stored in:



* `utilityconfig.ini`



---



# Driver Configuration Specification



`driverconfig.xlsx` acts as the master execution and mapping document.



It defines:



* `run_flag`

* `testcase_name`

* `source_name`

* `source_type`

* `source_file` / database configuration

* `target_name`

* `target_type`

* `target_file` / database configuration

* `compare_key`

* `ignore_case`

* `ignore_whitespace`



The engine reads this file and executes every test case where `run_flag = Y`.



---



# Validation Rules



The engine shall perform all validations before starting reconciliation.



## Driver Configuration Validation



* All mandatory fields must be populated.

* Invalid or missing configuration should fail the current test case.



## Source Validation



Validate:



* Source exists.

* Source is accessible.

* File can be opened.

* Database connection is successful.

* Table exists.

* Data is available.



## Target Validation



Validate:



* Target exists.

* Target is accessible.

* File can be opened.

* Database connection is successful.

* Table exists.

* Data is available.



## Dataset Validation



After loading:



* Dataset loaded successfully.

* Dataset contains headers.

* Dataset is not corrupted.



If a dataset is empty:



* Do not treat it as an application error.

* Display that the dataset is empty.

* Display dataset metadata.



## File Validation



Perform validations such as:



* File exists.

* File is readable.

* Supported file format.



## Database Validation



Perform validations such as:



* Database connection successful.

* Credentials valid.

* Table exists.

* Query executed successfully.



---



# Comparison Rules



## 1. Record Matching Rule



If `compare_key` is provided:



* Match records using the configured key(s).



If `compare_key` is empty:



* Compare records row-by-row using their original order.



---



## 2. Key Comparison Rule



After matching records:



* Key exists in both datasets → Continue with column comparison.

* Key exists only in Source → Source Only.

* Key exists only in Target → Target Only.



---



## 3. Column Comparison Rule



For matched records:



* Compare every comparable column.



If every compared column matches:



* Status = Matched



If one or more columns differ:



* Status = Mismatched



---



## 4. Ignore Case Rule



If `ignore_case = True`:



* Character case differences are ignored.



If `ignore_case = False`:



* Values are compared exactly.



---



## 5. Ignore Whitespace Rule



If `ignore_whitespace = True`:



* Leading and trailing whitespaces are ignored.



If `ignore_whitespace = False`:



* Whitespaces are considered during comparison.



---



## 6. Record Classification Rule



Every record must belong to exactly one category:



* Matched

* Mismatched

* Source Only

* Target Only



A record must never belong to more than one category.



---



## 7. Column Order Rule



Column order does not matter.



Columns are mapped using their names.



---



## 8. Comparison Scope



Every comparable column is compared.



The compare key is used only for matching records.



---



## 9. Mismatch Identification Rule



For mismatched records, identify every differing column.



The report should display:



* Compare Key

* Column Name

* Source Value

* Target Value



instead of simply indicating that a record is mismatched.



---



# Report Specification



## Execution Log



During execution, display the following information in the terminal:



* Test Case

* Source Name

* Target Name

* Source Type

* Target Type

* Execution Date

* Start Time

* End Time

* Execution Duration

* Status (PASS / FAIL)



The same information should also be written to:



* Execution Log

* Summary Report



---



## HTML Report



Generate an interactive `Report.html`.



### Dataset Summary



Include:



* Source Record Count

* Target Record Count

* Source Column Count

* Target Column Count

* Compare Key

* Ignore Case

* Ignore Whitespace



### Comparison Summary



Display:



* Matched Count

* Mismatched Count

* Source Only Count

* Target Only Count



Include graphical representations wherever appropriate.



---



## Detailed Results



### Matched Records



* Display matched records only once.

* Do not duplicate source and target data.



### Mismatched Records



Display values side-by-side.



Example:



| Compare Key | Source Value | Target Value |

| ----------- | ------------ | ------------ |



Matching values should be highlighted in **Green**.



Differing values should be highlighted in **Red**.



### Source Only Records



Display complete records available only in the source dataset.



### Target Only Records



Display complete records available only in the target dataset.



---



# Output Files



For every executed test case, create a dedicated output folder containing:



* Summary.xlsx

* Matched.csv

* Mismatched.csv

* SourceOnly.csv

* TargetOnly.csv

* Report.html

* Summary_report.txt

* driverconfig.xlsx (only the current test case configuration)

* utilityconfig.ini (only the required database configuration)

* source_original_data.csv

* target_original_data.csv



---



# Error Handling



## Objective



* Handle all errors gracefully.

* Provide meaningful error messages.

* Continue executing the remaining test cases whenever possible.



## Error Categories



* Configuration Errors

* Input Errors

* Validation Errors

* Comparison Errors

* Report Generation Errors

* System Errors



## Error Handling Strategy



### Test Case Level



If a fatal error occurs:



* Mark the current test case as **FAILED**.

* Record the error.

* Continue with the next test case.



### Engine Level



Stop the entire engine only when execution cannot continue.



Examples:



* Application crash

* Out of memory

* Unrecoverable system failure



---



# Batch Execution



Execute every test case where `run_flag = Y`.



For each test case:



1. Start execution.

2. Perform validations.

3. Load datasets.

4. Execute reconciliation.

5. Generate reports.

6. Mark the test case as **PASSED** or **FAILED**.

7. Continue with the next eligible test case.



If `run_flag = N`:



* Skip execution.



---



# Batch Summary



After all test cases complete, generate an overall execution summary containing:



* Total Test Cases

* Passed

* Failed

* Skipped

* Overall Execution Status



The failure of one test case must not prevent the execution of the remaining independent test cases.



---



# Future Enhancements



Integrate **Great Expectations** as an optional data validation framework to perform configurable dataset quality checks before the reconciliation process.