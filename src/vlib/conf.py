#!/usr/bin/env python

import os
import re
import yaml

from .odict import odict

# Set this to whatever you want.
CONF_ENV_VAR = 'VCONF'

class ConfElement(odict): pass
class ConfError(Exception): pass

class Conf(object):
    '''Configuration Module
    
       Usage:
       
          # To create a single instance of configuration data
          # found in a yaml file pointed to by an environment
          # variable called VCONF
          
          from vlib import conf
          myconf = conf.Factory.create().data

          # Print configuration data, from a Yaml file that looks
          # like this:
          #
          # database:
          #    engine: mysql
          #    host: localhost
          #    db: vlibtests
          #    user: vlibtests
          #    passwd: bogangles

          print myconf.database.hostname
          
    '''
    def __init__(self, filename=None):
        if not filename:
            try:
                filename = os.environ[CONF_ENV_VAR]
            except KeyError as e:
                raise ConfError('Environment variable %s not defined.'
                                  % CONF_ENV_VAR)

        try:
            self.data = expandEnvVars(yaml.load(open(filename),
                                                Loader=yaml.Loader))
        except Exception as e:
            raise ConfError('Unable to parse yaml: %s\n%s: %s' 
                            % (filename, e.__class__.__name__, e))

    def toStr(self):
        o = []
        for k, v in list(self.data.items()):
            if isinstance(v, dict):
                o2 = []
                for k2, v2 in list(v.items()):
                    o2.append('   %s: %s' % (k2, v2))
                v = '\n' + '\n'.join(o2)
            o.append('%s: %s' % (k, v))
        return '\n'.join(o)

def expandEnvVars(data):
    '''Expand OS Environement Variables
       Also returns data as a ConfElement
    '''
    data2 = ConfElement()
    for k, v in list(data.items()):
        if isinstance(v, dict):
            v = expandEnvVars(v)
        elif isinstance(v, str):
            if '\$' in v: # unescape \$
                v = v.replace('\$', '$')
            elif '$' in v:
                envvar = re.sub(r'.*\$([^/.]*).*', r'\1', v)
                envvar_val = os.getenv(envvar, 'Unknown_env_var:%s' % envvar)
                v = re.sub('\$[^/.]*', envvar_val, v)
        data2[k] = v
    return data2

class Factory(object):
    '''Single instance factory Class
       
       To Use:
           import conf
           c = conf.Factory.create()
           c2 = conf.Factory.create()
    '''

    def __init__(self):
        self.instance = None

    def create(self):
        if not self.instance:
            self.instance = Conf()
        return self.instance

Factory = Factory()

def getInstance():
    return Factory.create().data

if __name__ == '__main__':
    conf = Conf()
    print(conf.toStr())


