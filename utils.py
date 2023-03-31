import time
from operator import itemgetter


def sorter(to_sort, keyname, reverse=False):
    newlist = sorted(to_sort, key=itemgetter(keyname), reverse=reverse)
    return newlist


def convertTime(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(seconds))


def timeLeft(seconds):
    timeleft = seconds - time.time()
    return timeleft
