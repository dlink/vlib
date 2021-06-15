#!/usr/bin/env python
#
# Usage:
#   from vlib.shell import Shell
#
#   class MyClass(object):
#
#      def __init__(self):
#         self.shell = Shell()
#         self.shell.echo_cmd = True
#
#      def do(self):
#         result = self.shell.cmd(cmd)

from subprocess import Popen, PIPE

ECHO_CMD = False
DRY_RUN = False

class ShellError(Exception): pass

class Shell(object):
    def __init__(self):
        self.echo_cmd = ECHO_CMD
        self.dry_run = DRY_RUN
        self.stderr_okay = False
        self.returncode_okay = False

    def cmd(self, cmd):
        if self.echo_cmd:
            print("Shell.cmd: %s" % cmd)
        if self.dry_run:
            return ''

        # process
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        (stdout, stderr) = process.communicate()

        # raise error on stderr if nec.
        if stderr and not self.stderr_okay:
            raise ShellError(stderr)
            
        # raise error on retcode
        if process.returncode and not self.returncode_okay:
            raise ShellError('Command failed:\n%s\nreturncode: %s\n' 
                             '%s%s' % 
                             (cmd, process.returncode, stdout.strip(), 
                              stderr.strip()))

        return stdout + stderr

