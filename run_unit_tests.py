#!/usr/bin/env python
# encoding: utf-8
import os
from subprocess import call
import argparse

dontstop = False

def runtest(testfilesubdir, testfile):
    global dontstop
    dir = os.path.realpath(testfilesubdir)
    test = os.path.join(dir, testfile)
    print " "
    print ("========================================== Running test %s in directory %s" % (test, dir))
    print " "
    status = call(test, cwd=dir)
    print " "
    print ("========================================== Completed test %s" % test)
    print " "
    if status != 0:
        print "Test %s failed." % testfile
        if not dontstop:
            quit(status)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run all TAP Unit Tests')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Force completion mode.  Continue testing even if errors occur.')
    args = parser.parse_args()
    dontstop = args.force
    if dontstop:
        print "Running tests in force completion mode."

    runtest('./tests', 'test_db_sqlite.py')
    runtest('./tests', 'test_multiple.py')
    runtest('./tests', 'test_rt_feeds.py')
