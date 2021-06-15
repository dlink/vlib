#!/usr/bin/env python

# $Id$

'''

ElapsedTime

This little class is just a nice way to get elapsed time
values in various formats. It's based on the system
clock so it's accuracy is limited to that at best.

Revision:
Modified the initialization code so an additional parameter <firstrun> value
of True will cause the timeout method to return True even if the timeout
has not in fact passed. The default behavior of the parameter is False, same
as existing code.
'''

__author__  = "Doug Farrell"
__date__    = "11/29/2006"
__version__ = "$Rev: 6175 $"


import time


class ElapseTime(object):
    '''This is the elapsed time class definition and defines the behavior 
    of the class. As soon as an object of this Class is created the clock is
    running and elapsed time values can be taken at any time from that point.
    '''
    def __init__(self, timeout=0.0, firstrun=False):
        '''The constructor for the class. Essentially create an object of this
        class starts the timer running by taking a snapshot of the current
        time value from the system clock'''
        self._starttime = time.time()
        self._timeoutStarttime = self._starttime
        self._timeout = float(timeout)
        self._firstrun = firstrun
        
    def reset(self):
        '''This method just resets the internal starttime to right now.'''
        self._starttime = time.time()
        
    @property
    def starttime(self): 
        return self._starttime

    @property
    def seconds(self): 
        return time.time() - self._starttime

    @property
    def ms(self): 
        return (time.time() - self._starttime) * 1000
    
    @property
    def timeout(self):
        retval = False
        now = time.time()
        if self._firstrun or now - self._timeoutStarttime > self._timeout:
            self._firstrun = False
            self._timeoutStarttime = now
            retval = True
        return retval

    def timeit(self, stmt, context, tries=1):
        '''Like the timeit module but easier to work with local vars.
        
            (I wish locals() could be included automatically) '''
        s = self.seconds
        for t in range(tries):
            exec(stmt, context)
        return self.seconds - s
    
    
def test():
    e = ElapseTime()
    e = ElapseTime(2)
    print(e.seconds)
    print(e.ms)
    time.sleep(2)
    print(e.seconds)
    print(e.ms)
    while True:
        if e.timeout:
            print("hit timeout")
            print(e.seconds)
            break
    def fib(n): return 1 if n < 3 else fib(n - 1) + fib(n - 2)
    print(e.timeit('fib(24)', locals()))
    print("done")

    
if __name__ == "__main__":
    test()
