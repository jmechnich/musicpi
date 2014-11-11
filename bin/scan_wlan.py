#!/usr/bin/env python

import re, subprocess, sys, time

from datetime import datetime
from dateutil.tz import *

class parser(object):
    def __init__(self, device='wlan0'):
        self.device = device

    def reset(self):
        self.nets = []
        self.current = {}
        
    def dump_json(self):
        for n in self.nets:
            print n
    
    def timestamp(self):
        localtime = datetime.now(tzlocal()).replace(microsecond=0)
        return localtime.isoformat()
    
    def update(self):
        self.reset()
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
            self.current['time'] = self.timestamp()
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
            { 'bssid' : bssid,
              'freq'  : freq,
              'signal': signal,
              'flags' : flags,
              'ssid'  : ssid,
              'time'  : self.timestamp()
              })

def main():
    #p = iwlist_parser()
    p = wpacli_parser()
    while True:
        p.update()
        p.dump_json()
        time.sleep(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
