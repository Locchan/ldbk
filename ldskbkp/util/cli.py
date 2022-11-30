from ldskbkp.conf.config import CLI_YN_ANSWERS, LDBK_DATABASE_FILENAME
import os


def ask_yn(message):
    while True:
        r = input(message + "? [y/n]: ")
        if r.lower() in CLI_YN_ANSWERS["positive"]:
            return True
        elif r.lower() in CLI_YN_ANSWERS["negative"]:
            return False
