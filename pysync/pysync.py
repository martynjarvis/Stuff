#!/usr/bin/env python
"""Wrapper for rsync"""
import os
import subprocess
import optparse

SYNCFILE = '.sync'
IGNOREFILE = '.syncignore'
RSYNC = 'rsync'

def suffix(string, sfx):
    """Ensure that string endswith sfx"""
    if not string.endswith(sfx):
        return string+sfx
    return string

def main():
    """Parse command line options"""
    parser = optparse.OptionParser()
    # TODO add some options here

    (options, args) = parser.parse_args()

    cwd = os.getcwd()
    with open(os.path.join(cwd, SYNCFILE)) as sync_file:
        if 'push' in args:
            source = suffix(cwd, os.sep)
            for line in sync_file:
                dest = line.strip()
                ret = subprocess.call([RSYNC, '-avz', '--exclude-from',
                                       IGNOREFILE, source, dest])
            return ret
        elif 'pull' in args:
            # Just pull from first destination (Think about this)
            dest = cwd
            source = suffix(sync_file.readline().strip(), os.sep)
            ret = subprocess.call([RSYNC, '-avz', '--exclude-from',
                                   IGNOREFILE, source, dest])
            return ret
        else :
            return

if __name__ == '__main__':
    main()
