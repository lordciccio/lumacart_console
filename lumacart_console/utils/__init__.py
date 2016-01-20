import re
import sys
import traceback

def safe_get(sequence, default = None):
    return sequence[0] if sequence else default

def get_exception_trace():
    t, v, tb = sys.exc_info()
    s = traceback.format_exception(t, v, tb)
    return "".join(s)

def snake_string(s):
     # Remove all non-word characters (everything except numbers and letters)
     s = re.sub(r"[^\w\s]", '', s)

     # Replace all runs of whitespace with a single dash
     return re.sub(r"\s+", '_', s).lower()

def blank_if_none(s):
    if not s:
        return ''
    return s