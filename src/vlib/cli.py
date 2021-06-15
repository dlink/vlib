#!/usr/bin/env python

# Command Line Interface

import sys
import os
import copy

class CLI_Error(Exception): pass

class CLI(object):
    '''Command Line Interface

       Usage:
          from cli import CLI, CLI_Error

          class MyClass(object):
             def run(self):
                 commands = [<list of commands>]
                 self.cli = CLI(self.process, commands)
                 print self.cli.process()

             def process(self, *args):
                args = list(args)
                do something with args

          if __name__ == '__main__':
             MyClass().run()

       See Test Class below for example
    '''
    def __init__(self, process_method, commands, options={}):
        self.process_method = process_method
        self.commands = commands
        self.options = options
        self.hasoption = {}
        self.return_not_exit = 0
        if 'v' not in self.options:
            self.options['v'] = 'Verbose'
        if 'q' not in self.options:
            self.options['q'] = 'Quite'

        self.verbose = False

    def process(self, return_not_exit=0):
        '''Process Command Line Arguments
           
           call process_method(**args)

           sets self.verbose
           
           Exists with status
                0 - success
                1 - syntax displayed and not action taken
              100 - fail
        '''
        args = copy.copy(sys.argv[1:])

        # options
        #   set things like self.hasoption['v'], etc

        for opt in self.options:
            cmdopt = '-' + opt
            if cmdopt in args:
                self.hasoption[opt] = True
                p = args.index(cmdopt)
                args = args[0:p]+args[p+1:]
            else:
                self.hasoption[opt] = False

        if not args:
            self.syntax(return_not_exit=return_not_exit)

        retcode = 0
        try:
            results = self.process_method(*args)
        except Exception as e:
            if self.hasoption.get('v'):
                raise
            results = "Error: %s: %s" % (e.__class__.__name__, str(e))
            retcode = 100

        if not self.hasoption.get('q'):
            print_pretty(results)

        if return_not_exit:
            return retcode

        sys.exit(retcode)

    def syntax(self, emsg=None, return_not_exit=0):
        prog = os.path.basename(sys.argv[0])
        if emsg:
            print(emsg)
        ws = ' '*len(prog)

        options = '[OPTIONS]'

        print()
        for i, command in enumerate(self.commands):
            a = prog if i == 0 else ' '*len(prog)
            b = options if i == 0 else ' '*len(options)
            print(' %s %s %s' % (a, b, command))
        print()
        for o, desc in list(self.options.items()):
            print('%s -%s: %s' % (' '*len(prog), o, desc))
        print()
        if return_not_exit:
            return 1
        sys.exit(1)

    def are_you_sure(self, msg=None):
        if msg:
            print(msg)
            print()
        print('Are you sure? ', end=' ')

        yn = sys.stdin.readline().strip().lower()
        if yn not in ('y', 'yes', 'yea', 'yeah', 'sure', 'si'):
            print('Existing')
            sys.exit(1)
        print()

def print_pretty(results):
    if not results:
        return

    if isinstance(results, (list, tuple)):
        if isinstance(results[0], (list, tuple)):
            for row in results:
                print(",".join(map(str, row)), end=' ')
                print()
        else:
            print("\n".join(map(str, results)))
    elif isinstance(results, dict):
        keys = sorted(results.keys())
        for k in keys:
            print("%s: %s" % (k, results[k]))
    else:
        print(results)

class Test(object):
        
    def run(self):
        commands = ['say <greeting>',
                    'add <n> <m>',
                    'time']
        self.cli = CLI(self.process, commands)
        return self.cli.process()

    def process(self, *args):
        '''Process incoming requests'''
        args = list(args)
        if len(args) < 1:
            self.cli.syntax('missing args')

        cmd = args.pop(0)
        if cmd == 'say':
            opt = args[0]
            return opt
        elif cmd == 'add':
            n = args[0]
            m = args[1]
            return int(n) + int(m)

        elif cmd == 'time':
            import datetime
            return datetime.datetime.now()
        else:
            raise CLI_Error('Unrecognized Command: %s' % cmd)

if __name__ == '__main__':
    Test().run()
