LOGFILE = '/tmp/robots.log'

def log(msg):
    with open(LOGFILE, 'a') as f:
        f.write(str(msg)+'\n')
