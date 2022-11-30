import os
import sys

from ldskbkp.conf.config import LDBK_DATABASE_FILENAME


def get_ldbk_database(apath):
    if os.path.isdir(apath):
        path = os.path.join(apath, LDBK_DATABASE_FILENAME)
    else:
        path = apath
    if os.path.exists(path):
        return True, path
    else:
        return False, path


def does_terminal_support_color():
    platform = sys.platform
    supported_platform = platform != 'Pocket PC' and (platform != 'win32' or 'ANSICON' in os.environ)
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return supported_platform and is_a_tty
