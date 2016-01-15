
import sys
import traceback

def safe_get(sequence, default = None):
    return sequence[0] if sequence else default

def get_exception_trace():
    t, v, tb = sys.exc_info()
    s = traceback.format_exception(t, v, tb)
    return "".join(s)