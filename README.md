Python Application Development - Core Library Classes

Developed over a period of time to address reoccurring requirements for most all applications.  It provides the following modules:

__Modules__

   * Configuration File Support

   * Database Support

   * Logging Support

   * Emailing Support

   * Object-like (dot) syntax for Dictionaries

__Details__

*Configuration Module*

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
*Database Module*

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
          
          from vlib import Db
          mydb = Db({'engine':'mysql', 
                     'host':'db1', 
                     'db':'books',                 
                     'user':'bookmgr', 
                     'passwd':'mepassword', 
                     'dictcursor':True })
                     
         # Real world example with Objects
         
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

*Logging Module*

The logging module uses log4r to produce consistent log entries that include date, hostname, and class name.

     Usage:

          # To setup a Logging instance, you define the following in yuor
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


Installation
------------

__Ubuntu__

If you haven't installed pip yet:

     apt-get install python-pip
     pip install -U pip

If you havent installed Mysql DB Connectorm, yet:

    apt-get install python-dev libmysqlclient-dev
    pip install MySQL-python

Install vlib:

    pip install vlib
