import smtplib
import email.utils
from email.mime.text import MIMEText
import functools
SUPPORT = 'support@alancer.ml'

def makes(s):
    if type(s)==unicode:
        return s.encode('utf8','ignore')
    else:
        return s

def makeu(s):
    if type(s)==str:
        return s.decode('utf8','ignore')
    else:
        return s

def ex(func):
    @functools.wraps(func)
    def foo(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception, e:
            print '===================send email ex================', e
    return foo

@ex
def send_email(title, content, addr_to, addr_fr=None):
    """
    a local postfix service is presumed
    """
    # Create the message
    if not addr_fr:
        addr_fr = SUPPORT   
    msg = MIMEText(makes(content), 'html')
    msg['To'] = email.utils.formataddr(('Recipient', addr_to))
    msg['From'] = email.utils.formataddr(('Sandbox', addr_fr))
    msg['Subject'] = title
    try:
        server = smtplib.SMTP('localhost')
    except Exception, e:
        print 'no SMTP service available', e
        return
    
    #server.set_debuglevel(True) # show communication with the server
    try:
        server.sendmail(addr_fr, [addr_to], msg.as_string())
    finally:
        server.quit()
