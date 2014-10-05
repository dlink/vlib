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

   * Database Module

      Usage:

          # To setup the Db instance, you need to define the following
          # in your config file:
          #
          # database:
          #    engine: mysql
          #    host: localhost
          #    db: vlibtests
          #    user: vlibtests
          #    passwd: bogangles
          
          from vlib import db
          db_ = db.getInstance()
          
          for row in db_.query('select * from product_types'):
             print row['product_type_id']
             print row['name']
             
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
