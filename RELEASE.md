Release Notes - vlib
====================
v1.3.1
------

* Logger: allow passing in log file name

v1.3.0
------
07/17/2016

* Cli: Command Line Interface module

v1.2.3
------
02/05/2016

* Conf: Support passing in yaml files
* Db: new __repr__ string

v1.2.2
-------
01/19/2016

* DB: Support environment vars for passwd

v.1.2.1
-------

* Tests: Db: New tests for startTransaction/Rollback/Commit

v.1.2.0
-------
11/15/2015

* New Model Class: Attribute

v.1.1.0
-------
09/15/2015

* Microsoft SQL Server Support
  * DB: begin transaction/rollback

v.1.0.0
-------
8/07/2015

* Microsoft SQL Server Support
  * config.database.engine: mssql
  * Db: conditionally introduce pymsql.connection
  * DataTable changes
  * New Tests added
* DataRecord: changed data to odict

v.0.13
------
7/22/2015

* Doc: added link to pydocs housed on crowfly.net

v.0.12
------
7/19/2015

* DataRecord added
* DataRecord Tests added

v.0.11
------
5/31/2015

* Logger: removed dependency on config.email

v.0.10
------
12/18/2014
 
* Conf and odict: improved error messaging

v.0.9
-----
11/26/2016

* DataTable: New tests for table_columns, and describe 
* Config, rewording "Singleton", for "Single Instance", symantecs
* Tests: DB Create commented out creation and grants - that part moved to README 

v.0.8
-----
11/03/2014

* Get pip install vlib to work properly
* Setup: Added GNU General Pubic License (GPL)
* MANIFEST.in added
* README: Installation info added
* README: Reference guide added
* utils.pretty: stripping off final \n so we can print it

v.0.7
-----
10/11/2014

* DataTable: Bug fix debug_sql for updateRows
* DataTable: Big fix for setFilters
* Datatable: Debug: Show insert values  
* DataTable: New Method: get() which takes optional filter= param.  Short cutto setting Columns and Filters then calling getTable()
* Logger: create logfile's subdirectory if nec.
* utils.str2datetime: now accepts dates as well as datetime strings
* utils.format_datetime: changed iso8601 to be EST and not UTC time
* utils.pretty: bug fix: for empty lists
* sqlutils.pretty_sql: Improve formating of subqueries
* sqlutils.pretty_sql: handle left joins 
* Tests: added set_env.sh script to help run tests
* Tests: added tests for date conversion methods

v.0.4
-----
8/29/2013

* entities module added

v.0.3
-----
7/03/2013

* Db: Optional config param for setting session timezone

v.0.2
-----
6/22/2013

* Python package structure for use with easy_install and pip
* sqlutils.pretty_sql added

v.0.1
-----
5/09/2013

* setup.py added
* requirements.txt added
* README.md added
* Conf: data now stores odicts
* Conf: support for escaping $ with \$ 
* Db: Bugfix in db.py relating to parameter binding
* Db: Added property: rowcount, set by insert statements
* DataTable: Refactor for efficiency and clarity
* DataTable: setFilters: Allow kwargs
* DataTable: setFilters: kwargs support: map '= None' to 'is null'
* utils.list2csv() added
* utils.str2date() added
* utils.any_in() added
* utils.str2datetime: allow override default format
* utils.pretty() added
* utils.valid_email() added
* utils.formatdict() added
* utils.wordwrap() added
* odict added delete function

the begining 
------------
1/07/2013

Initial Check in of code.  In the process of refactoring out of existing Application 

* README added
* colors module added
* config module added
* datatable module added
* db module added
* logger module added
* odict module added
* unit tests added:
   * vlib_tests
   * create_vlibtests Database
* utils module added:
   * console_width() added
   * echoized added
   * format_date added
   * format_datetime added
   * newf added
   * str2datetime added
   * uniqueId added
   * validate_num_args() added
