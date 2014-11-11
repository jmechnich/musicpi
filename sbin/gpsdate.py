#!/usr/bin/env python

import gps, sys, time

import dateutil.parser
from   dateutil.tz import tzlocal

def _linux_set_time(sec,msec=0):
    import ctypes
    import ctypes.util

    # /usr/include/linux/time.h:
    #
    # define CLOCK_REALTIME                     0
    CLOCK_REALTIME = 0

    # /usr/include/time.h
    #
    # struct timespec
    #  {
    #    __time_t tv_sec;            /* Seconds.  */
    #    long int tv_nsec;           /* Nanoseconds.  */
    #  };
    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long),
                    ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec  = int(sec)
    ts.tv_nsec = int(msec) * 1000000 # Millisecond to nanosecond

    # http://linux.die.net/man/3/clock_settime
    status = librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))
    return status

def _linux_get_time():
    import ctypes
    import ctypes.util

    # /usr/include/linux/time.h:
    #
    # define CLOCK_REALTIME                     0
    CLOCK_REALTIME = 0

    # /usr/include/time.h
    #
    # struct timespec
    #  {
    #    __time_t tv_sec;            /* Seconds.  */
    #    long int tv_nsec;           /* Nanoseconds.  */
    #  };
    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long),
                    ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec  = 0
    ts.tv_nsec = 0

    # http://linux.die.net/man/3/clock_settime
    status = librt.clock_gettime(CLOCK_REALTIME, ctypes.byref(ts))
    return (status, ts.tv_sec,ts.tv_nsec)

def _get_gps_time():
    gpsinfo = None
    maxtries = 10
    
    session = gps.gps(mode=gps.WATCH_ENABLE)
    try:
        while not gpsinfo and maxtries:
            report = session.next()
            if report['class'] == 'TPV':
                gpsinfo = dict(report)
            maxtries -= 1
    except StopIteration:
        pass
    session.close()
    if gpsinfo and gpsinfo.has_key('time'):
        return dateutil.parser.parse(gpsinfo['time']).astimezone(tzlocal())
    return None

status, sys_sec, sys_nsec = _linux_get_time()
gpstime = _get_gps_time()

if gpstime:
    gps_sec = int(time.mktime(gpstime.timetuple()))
    print 'GPS time: %s, System time: %s' % (time.asctime(time.localtime(gps_sec)),time.asctime(time.localtime(sys_sec)))
    if abs(gps_sec-sys_sec) > 60:
        print 'Adjusting system time to gps'
        status = _linux_set_time(gps_sec)
        if status == 0:
            status, sys_sec, sys_nsec = _linux_get_time()
            print 'GPS time: %s, System time: %s' % (time.asctime(time.localtime(gps_sec)),time.asctime(time.localtime(sys_sec)))
            sys.exit(0)
        else:
            print "Could not set system time"
            sys.exit(1)
else:
    print "No GPS fix"
    sys.exit(1)

sys.exit(0)
