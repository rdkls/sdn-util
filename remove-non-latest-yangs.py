#!/usr/bin/env python3
# Remove non-newest yang files from official yang repo https://github.com/YangModels/yang
# Non-newest defined as:
#   - filename *@*.yang
#   - another file in same dir with same format, but newer date
#     (this should probably also apply to newer files without the @date, however there don't seem to be any atm)

import glob
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', default='/home/nick/ws/lab/telstra/yang')
parser.add_argument('-t', '--test-only', action='store_true')
args = parser.parse_args()

path = os.path.join(args.directory, '**', '*.yang')

for filepath in glob.iglob(path, recursive=True):
    (path, fn) = os.path.split(filepath)
    try:
        (prefix, date) = fn.split('@')

        # If there's a newer version, either prefix@date.yang
        # or prefix.yang,
        # delete current
        sibling_spec = os.path.join(path, '%s@*.yang' % prefix)
        for maybe_newer_fn in glob.iglob(sibling_spec):
            if maybe_newer_fn > filepath:
                print('-'*24)
                print('%s is newer file \n%s is old and will be deleted' % (os.path.split(maybe_newer_fn)[1], fn))
                if not args.test_only:
                    os.unlink(filepath)
    except ValueError:
        # No '@' to split on, ignore
        pass
