#!/usr/bin/env python

import argparse, os, re, subprocess, sys, time

from gps import *

from datetime    import datetime
from dateutil.tz import tzlocal

class parser(object):
    def __init__(self, device='wlan0'):
        self.device = device

    def reset(self):
        self.nets = []
        self.current = {}
        
    def dump_json(self):
        for n in self.nets:
            print n

    def location(self):
        lon, lat, gpstime = 0, 0, ''
        session = gps(mode=WATCH_ENABLE)
        for report in session:
            if report['class'] == 'DEVICE':
                # Clean up our current connection.
                session.close()
                # Tell gpsd we're ready to receive messages.
                session = gps(mode=WATCH_ENABLE)
                # Do more stuff
            elif report['class'] == 'TPV':
                if dict(report).has_key('lon') and dict(report).has_key('lat'):
                    lon     = float(report['lon'])
                    lat     = float(report['lat'])
                    gpstime = str(report['time'])
                    break
        session.close()

        return (lon,lat,gpstime)

    def timestamp(self):
        localtime = datetime.now(tzlocal()).replace(microsecond=0)
        return localtime.isoformat()
    
    def update(self):
        self.reset()
        self.gpsdata = self.location()
        self.time    = self.timestamp()
        try:
            output = self.execute()
            lines = output.split('\n')
            for line in lines:
                self.parse_line(line)
            if len(self.current):
                self.nets += [ self.current ]
        except subprocess.CalledProcessError, e:
            time.sleep(5)

class iwlist_parser(parser):
    def __init__(self, device='wlan0'):
        super(iwlist_parser,self).__init__(device)
    
    def execute(self):
        return subprocess.check_output( ['iwlist', self.device, 'scan'] )
    
    def parse_line(self,line):
        if line.startswith(self.device):
            return
        oldlen = len(line)
        line = line.strip()
        newlen = len(line)
        newindent = oldlen - newlen
        if not len(line):
            return
        if line.startswith('Cell'):
            if len(self.current):
                self.nets += [self.current]
                self.current = {}
            self.current.update({
                    'lon'    : self.gpsdata[0],
                    'lat'    : self.gpsdata[1],
                    'gpstime': self.gpsdata[2],
                    'time'   : self.time,
                    })
            line = ' '.join(line.split('-')[1:]).strip()
    
        colon = line.find(':')
        if colon != -1:
            key = line[:colon].strip().lower().replace(' ','_').replace('(','').replace(')','')
            if key in ['ie', 'extra']:
                return
            val = line[colon+1:].strip()
            if len(val) and val[0] == '"':
                val = val[1:-1]
            if key in ['address']:
                self.current[key] = val.lower()
            else:
                self.current[key] = val
        elif line.startswith('Quality'):
            tmp = line.split()
            quality, siglvl = (tmp[0], ''.join(tmp[1:]))
            self.current['quality']       = quality.split('=')[1].split('/')[0]
            self.current['signal_level']  = siglvl.split('=')[1].split('/')[0]
        else:
            pass

    def debug(self):
        #printkeys = ['ESSID', 'Address', 'Quality', 'Signal level', 'Encryption key']
        printkeys = [ k for k in self.nets[0].keys() if k not in ['IE', 'Extra']]
        #printkeys = ['Protocol', 'Pairwise Ciphers (1)', 'Encryption key', 'Bit Rates', 'Signal level', 'Frequency', 'Mode', 'Address', 'Authentication Suites (1)', 'Quality', 'Group Cipher', 'ESSID']
        maxlength = max([len(k) for k in printkeys])
        for i in self.nets:
            for k in printkeys:
                print k.ljust(maxlength), i[k]
            print

class wpacli_parser(parser):
    def __init__(self, device='wlan0'):
        super(wpacli_parser,self).__init__(device)

    def execute(self):
        subprocess.check_output(('wpa_cli -i %s scan' % self.device).split())
        return subprocess.check_output(('wpa_cli -i %s scan_results' % self.device).split())

    def parse_line(self, line):
        if not re.match( r'^[a-f0-9]{2}:.*', line):
            return
        bssid, freq, signal, flags, ssid = line.split()
        self.nets.append(
            { 'bssid'  : bssid,
              'freq'   : freq,
              'signal' : signal,
              'flags'  : flags,
              'ssid'   : ssid,
              'lon'    : self.gpsdata[0],
              'lat'    : self.gpsdata[1],
              'gpstime': self.gpsdata[2],
              'time'   : self.time
              })

def detach():
    stdin  = '/dev/null'
    stdout = '/dev/null'
    stderr = '/dev/null'
    
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)
        
    # decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)
    
    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent
            sys.exit(0)
    except OSError, e:
        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
        sys.exit(1)
       
    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def checkIfRunning(name, kill=False):
    pidfile = os.path.join(os.environ['HOME'],".%s.pid" % name)
    if not os.path.exists( pidfile):
        return False
    f = open(pidfile)
    oldpid = int(f.readline().strip())
    f.close()

    cmdlinefile = os.path.join('/proc',str(oldpid),'cmdline')
    if not os.path.exists( cmdlinefile):
        return False
    f = open(cmdlinefile)
    args = f.readline().strip().split('\0')
    f.close()
    if len(args) > 1 and not args[0].endswith(name):
        if not args[1].endswith(name):
            return False

    if kill:
        try:
            import signal, time
            os.kill(oldpid, signal.SIGTERM)
            time.sleep(1)
            os.kill(oldpid, signal.SIGKILL)
        except:
            pass
        return False
    
    return True
    
def createPIDFile(name):
    pidfile = os.path.join(os.environ['HOME'],".%s.pid" % name)
    f = open(pidfile, 'w')
    print>>f, os.getpid()
    f.close()
    import atexit
    atexit.register(lambda: os.path.exists(pidfile) and os.remove(pidfile))

def main():
    name = os.path.basename(__file__)
    parser = argparse.ArgumentParser(description=name)
    parser.add_argument( '-d', '--daemon',
                         help='run as daemon',   action="store_true")
    parser.add_argument( '-k', '--kill-running',
                         help='kill if running', action="store_true")
    parser.add_argument( '-n', '--interval', metavar='SECS', type=int, default=1,
                         help='log data every SECS seconds (default: %(default)s)')
    parser.add_argument( '-m', '--mode', metavar='MODE', type=str, default='iwlist',
                         help='use either iwlist or wpacli backend (default: %(default)s)')
    parser.add_argument( '-o', '--output', metavar='FILE', type=str, default='-',
                         help='select output file (or - for stdout) (default: %(default)s)')
    cmdargs = parser.parse_args()
    
    if checkIfRunning(name, kill=cmdargs.kill_running):
        print "Already running, exiting"
        sys.exit(0)

    if cmdargs.daemon: detach()
    createPIDFile(name)
    
    if cmdargs.output != '-':
        sys.stdout = open(cmdargs.output, 'w')
        
    if cmdargs.mode == 'iwlist':
        p = iwlist_parser()
    elif cmdargs.mode == 'wpacli':
        p = wpacli_parser()
    else:
        print "Unknown mode", cmdargs.mode
        return 1
    
    while True:
        p.update()
        p.dump_json()
        time.sleep(cmdargs.interval)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
