Python Application Development - Core Library Classes

Developed over a period of time to address reoccurring requirements for most all applications.  It provides the following modules:

See Pydocs: http://crowfly.net/pydocs/vlib

## Modules

   * Configuration File Support

   * Database Support

   * DataTable Support (an ORM Lite)

   * Logging Support (with email Support)

   * Object-like (dot) syntax for Dictionaries

   * Utilities

## Details

### Configuration Module


The configuration module reads yaml files and provides a dot syntax for expressing nested data trees.  ie. self.conf.database.hostname.
    
       Usage:
       
          # To create a singleton instance of configuration data
          # found in a yaml file pointed to by an environment
          # variable called VCONF
          #
          # eq.:
          # $ export VCONF=$HOME/proj/conf/dev.yml

          from vlib import conf
          myconf = conf.getInstance()

          # Print configuration data, from a Yaml file that looks
          # like this:
          #
          # crew:
          #   captian: Kirk
          #   science_officer: Spock

          print myconf.crew.captian

          # Real world example with Objects
          
          from vlib import conf
          class Foo(object):
              def __init__(self):
                  self.conf = conf.getInstance()
                  self.webserver = self.conf.webserver
                  self.dbname    = self.conf.db.name
                  ...
### Database Module

The database modules provides a simple set of methods for talking to your database, like query(), startTransaction(), commit(), etc.

      Usage:

          # To setup the Db instance, you need to define the following
          # in your config file pointed to by the VCONF environement var.
          # The db module uses the conf module to read this information
          #
          # database:
          #    engine: mysql
          #    host: localhost
          #    db: vlibtests
          #    user: vlibtests
          #    passwd: bogangles
          
          from vlib import db
          mydb = db.getInstance()
          
          for row in mydb.query('select * from product_types'):
             print row['product_type_id']
             print row['name']
             
          # Without using config
          # --------------------
          
          from vlib import Db
          mydb = Db({'engine':'mysql', 
                     'host':'db1', 
                     'db':'books',                 
                     'user':'bookmgr', 
                     'passwd':'mepassword', 
                     'dictcursor':True })
                     
                     
         # Real world example with Objects
         # -------------------------------
         
         from vlib import db

         class Books(object):

             def __init__(self):
                 self.db = db.getInstance()

             def getBook(self, book_id):
                sql = 'select * from books where book_id = %s' % book_id
                results = self.db.query(sql)
                if results:
                   return results[0]
                return []
                
                
          # Connecting to multiple databases
          # --------------------------------

          # Define additional database connections in the config
          # ro_database:
          #    engine: mysql
          #    host: localhost
          #    db: vlibtests
          #    user: vlibtests_ro
          #    passwd: bogangles
          
          # __ ro/db.py __
          from vlib import conf
          from vlib.db import singletonFactory
          
          def getInstance():
            conf_ = conf.getInstance()
            return singletonFactory.create(**conf_.ro_database)
            
          # __ myprog.py __
          import ro.db as rodb
          my_rodb = rodb.getInstance()
          print my_rodb.query('select * from customers')

### DataTable Module

The DataTable module provides a simple abstraction for creating and executing SQL Statements.  It relies on the Database Module for connection.

      Usage:

          from vlib import db
          from vlib.datatable import DataTable

          mydb = db.getInstance()

          books = DataTable(mydb, 'books')
          books.setColumns(['book_id as book_id', 'title'])
          books.setFilters("created > '2015-05-01'");
          for book in books.getTable():
              print book

     Usage as a base class:

         from vlib import db
         from vlib.datatable import DataTable

         class Books(DataTable):

             def __init__(self):
                 sellf.db = db.getInstance()
                 DataTable.__init__(self, self.db, 'books')

             def report(self):
                 self.setColumns(['created',
                                  'count(*) as books'])
                 self.setFilters('created > "2000-01-01"')
                 self.setGroupBy(1)
                 return self.getTable()

     See, Also:
     [DataTable Pydocs](http://crowfly.net/pydocs/vlib/datatable.html)

### Logging Module

The logging module uses log4r to produce consistent log entries that include date, hostname, and class name.

     Usage:

          # To setup a Logging instance, you define the following in your
          # config file.  The logging module uses the conf module to read it.
          #
          # logging:
          #    filename: /var/log/myapp/myapp.log
          #    level: DEBUG
           
          # If you want the logger to email you on 'critical' you need 
          # define email server
          #
          # email:                                                                          
          #    server  : smtp.gmail.com:587                                                 
          #    username: mailerbot@mycompany.com                                   
          #    password: secret                                                    
          #    fromaddr: Myapp Admin mailerbot@mycompany.com                         
           
          from vlib import logger
                    
          class MyClass:
           
             def __init__(self):
                self.logger = logger.getLogger(self.__class__.__name__)
               
             def do_something(self):
                self.logger.debug('Started doing something')
                self.logger.info('Did Something')
                self.logger.warn('Warning')
                self.logger.error('Did not do something')
                 
                # The following we send email:                                          
                # self.logger.critical('Something bad happened')    
                 
          MyClass().do_something()

The above outputs to the log:

    2014-02-24 14:41:30	dev1.localdomain	DEBUG	MyClass	Started MyClass.do_something()
    2014-02-24 14:41:30	dev1.localdomain	INFO	MyClass	Did Something
    2014-02-24 14:41:30	dev1.localdomain	WARNING	MyClass	Warning
    2014-02-24 14:41:30	dev1.localdomain	ERROR	MyClass	Did not do something


### Object Dictionary

The **odict** class is syntactic sugar for dealing with dictionaries and nested dictionaries. It privides dot (.) sytax, as well as flower brace ({}) and square braces ([]) syntax

    attr['color'] = 'blue' # normal dict

    attr.color = 'blue'    # odict

Example 1: This code using dicts …

    picture  = {'name'    : 'The Card Players',
                'filename': 'cezanne2.jpg',
                'year'    : 1895}
    print img(src=picture['filename'])

Can be written like this:

    from vlib.odict import odict
    picture  = odict(name     = 'The Card Players',
                     filename = 'cezanne2.jpg',
                     year     = 1895)
    print img(src=picture.filename)


Nested Odicts Example:

    from vlib.odict import odict
    workflow = odict(processes=odict(max_processes=5, debug=False))
    for p in workflow.processes.max_processes:
        startHandler(workflow.processes.debug)

### Utilities

    pretty(X):
        Return X formated nicely for the console

    str2datetime(s, format="%Y-%m-%d %H:%M:%S"):
        Convert str in the form of "2010-11-11 17:39:52" or
                                   "2010-11-11"          to a
        datetime.datetime Object

    str2date(s):
        Convert str in the form of "2010-11-11" to a
        datetime.date Object

    format_datetime(d, with_seconds=False, format=None):
        Given a datetime object
        Return formated String as follows:

           Format: None   : 11/22/2013 01:46[:00] am
                   ISO8601: 2013-11-21T01:46:00-05:00 (EST)

    format_date(d):
        Given a datetime object
        Return a string in the form of "mm/dd/yyyy"

    table2csv(data):
        Give a LIST or TUPLE
        Return: A CSV table as STRING or the input data if not LIST or TUPLE

    list2csv(data):
        Given a Table of data as a LIST of LISTs
        Return in CSV format as a STR

    formatdict(d, width=console_width(), indent=0, keylen=0, color=False):
        Recursively format contents of dictionaries in sorted tabular order.
        Optionally a certain width, indented, and/or a specific key length.

        >>> utils.formatdict(batch_item)
                active: 1
              batch_id: 3250
              on_press: None
              order_id: 2007372
             page_list: None
                   qty: 2
          removed_date: None

    uniqueId(with_millisec=False):
        Return system time to the millisec as set of numbers

    shift(alist):
        shift the firt element off of an array and return it

    valid_email(email):
        Given an email address
        Return whether it is in valid format as BOOLEAN



## Installation

__Ubuntu__

Update apt-get to the latest libraries:

    apt-get update

Install pip, if you haven't done so already:

     apt-get install python-pip
     pip install -U pip

Install Mysql DB Connectorm, if you haven't done so already:

    apt-get install python-dev libmysqlclient-dev
    pip install MySQL-python

Install vweb:

    pip install vlib

__Red Hat__

    yum install MySQL-python
