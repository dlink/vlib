Python Application Development - Core Classes 

 __Modules:__

   * Configuration File Support

   * Database Support

   * Logging Support

   * Emailing Support

   * Object-like syntax for Dictionaries (odict)

__Details:__


   * Configuration Module
    
       Usage:
       
          # To create a singleton instance of configuration data
          # found in a yaml file pointed to by an environment
          # variable called VCONF
          
          from vlib import conf
          conf_ = conf.getInstance()

          # Print configuration data, from a Yaml file that looks
          # like this:
          #
          # mojo:
          #   color: read
          #   size: 15

          print conf_.mojo.color

          # Real world example with Objects
          
          from vlib import conf
          class Foo(object):
              def __init__(self):
                  self.conf = conf.getInstance()
                  webserver = self.conf.webserver
                  dbname    = self.conf.db.name
                  

   * Database Module

      Usage:

          # To setup the Db instance, you need to define the following
          # in your config file pointed to by the VCONF environement var
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
         # Set VCONF env var (conf module above)
         # $ export VCONF=$HOME/proj/conf/dev.yml
         
         from vlib import db
         class Foo(object):
             def __init__(self):
                 self.db   = db.getInstance()
             def getBook(self, book_id):
                sql = 'select * from books where book_id = %s' % book_id
                results = self.db.query(sql)
                if results:
                   return results[0]
                return []
             
   * Logging Module

     Usage:

          # To setup a Logging instance, you need to define the following
          # in your config file:
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
                self.logger.debug('Started MyClass.do_something()')
                self.logger.info('Did Something')
                self.logger.warn('Warning')
                self.logger.error('Did not do something')
                 
                # The following we send email:                                          
                # self.logger.critical('Something bad happened')    
                 
          MyClass().do_something()
             
          # Outputs the following in the log:
          2014-02-24 14:41:30	dev1.localdomain	DEBUG	MyClass	Started MyClass.do_something()		
          2014-02-24 14:41:30	dev1.localdomain	INFO	MyClass	Did Something		
          2014-02-24 14:41:30	dev1.localdomain	WARNING	MyClass	Warning		
          2014-02-24 14:41:30	dev1.localdomain	ERROR	MyClass	Did not do something	
