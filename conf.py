#!/usr/bin/env python

import os
import re
import yaml

# Set this to whatever you want.
CONF_ENV_VAR = 'VLIBCONF'

class ConfError(Exception): pass

class Conf(object):
    
    def __init__(self):
        try:
            filename = os.environ[CONF_ENV_VAR]
        except KeyError, e:
            raise ConfError('Environment variable %s not defined.' 
                              % CONF_ENV_VAR)

        try:
            self.data = expandEnvVars(yaml.load(open(filename)))
        except Exception, e:
            raise ConfError('Unable to parse yaml: %s\n%s: %s' 
                            % (filename, e.__class__.__name__, e))

    def toStr(self):
        o = []
        for k, v in self.data.items():
            if isinstance(v, dict):
                o2 = []
                for k2, v2 in v.items():
                    o2.append('   %s: %s' % (k2, v2))
                v = '\n' + '\n'.join(o2)
            o.append('%s: %s' % (k, v))
        return '\n'.join(o)

def expandEnvVars(data):
    '''Expand OS Environement Variables'''
    data2 = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = expandEnvVars(v)
        elif isinstance(v, str):
            if '$' in v:
                envvar = re.sub(r'.*\$([^/.]*).*', r'\1', v)
                envvar_val = os.getenv(envvar, 'Uknown_env_var:%s' % envvar)
                v = re.sub('\$[^/.]*', envvar_val, v)
        data2[k] = v
    return data2

class Factory(object):
    '''Singleton factory Class
       
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

if __name__ == '__main__':
    conf = Conf()
    print conf.toStr()


