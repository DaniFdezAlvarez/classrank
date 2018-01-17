from __future__ import print_function
import sys

def log_to_error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
