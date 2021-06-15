from datetime import datetime
from email.utils import formatdate
import logging, logging.handlers
import os
import os.path
import smtplib
import socket

from . import conf

HOSTNAME=socket.gethostname()

class CustomFormatter(logging.Formatter):
    def format(self, record):
        newmsg = "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            HOSTNAME,
            record.levelname,
                record.name,
            record.msg,
            record.exc_info if record.exc_info else '',
            record.exc_text if record.exc_text else ''
            )
        return newmsg

class TlsSMTPHandler(logging.handlers.SMTPHandler):
    def emit(self, record):
        '''Override SMTPHandler, in order to use gmail
        '''
        smtp = smtplib.SMTP(self.mailhost, self.mailport)
        msg = self.format(record)
        msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\n\n%s" % (
            self.fromaddr,
            ','.join(self.toaddrs),
            self.getSubject(record),
            formatdate(), 
            msg)
        smtp.ehlo() 
        smtp.starttls() 
        smtp.ehlo() 
        smtp.login(self.username, self.password)
        smtp.sendmail(self.fromaddr, self.toaddrs, msg)
        smtp.quit()

def getLogger(name, logfile=None):
    '''A Factory mentod.
       Returns: An instance of Python Logger
    '''
    _conf = conf.Factory.create().data
    level   = _conf['logging']['level']
    if not logfile:
        logfile = _conf['logging']['filename']

    formatter = CustomFormatter()

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create dir if nec.
    dirname = os.path.dirname(logfile)
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    # file handler
    fh = logging.FileHandler(logfile)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    # email hander
    if 'email' in _conf:
        server, port = _conf['email']['server'].split(':')
        username = _conf['email']['username']
        password = _conf['email']['password']
        fromaddr = _conf['email']['fromaddr']
        notify   = _conf['notify']
        subject = '%s - BIEngine Error' % _conf['environment']
        gm = TlsSMTPHandler( (server, port),
                             username,
                             notify,
                             subject,
                             (username, password) )
        gm.setLevel(logging.CRITICAL)
        logger.addHandler(gm)

    return logger

def test():
    l=getLogger('cleaner')
    import datetime
    l.info('time is %s' % datetime.datetime.now())
    l.debug('time is %s' % datetime.datetime.now())
    l.error('time is %s' % datetime.datetime.now())
    l.critical('time is %s' % datetime.datetime.now())
