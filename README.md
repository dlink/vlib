Python Application Development - Core Classes 

 Modules:

   * Configuration File Support

   * Database Support

   * Logging Support

   * Emailing Support

   * Object-like syntax for Dictionaries (odict)

 Details:

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