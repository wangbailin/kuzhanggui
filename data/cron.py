#encoding=utf-8
#! usr/local/bin/python
import cronjobs
import datetime
import logging
import sys
import os, os.path, re

sys.path.append("..")

from django.core.management import setup_environ
from rocket import settings
setup_environ(settings)

logger = logging.getLogger("cron")

from data.models import WSiteDailyData

@cronjobs.register
def sts_log_analyse():
    log_file = file("./logs/sts.log")
    user_extract = re.compile("wx (\w+) user (\w+)")
    pv = 0
    uv = 0
    wx = {}
    while True:
        line = log_file.readline()
        if len(line) <= 0:
            break
        match = user_extract.search(line)
        if match:
            logger.debug("match line")
            wx_id = int(match.group(1))
            if wx_id not in wx:
                wx[wx_id] = [0, 0, {}] #uv, pv, hash
            user = match.group(2)
            if user not in wx[wx_id][2]:
                wx[wx_id][0] += 1
                wx[wx_id][2][user] = 1
            wx[wx_id][1] += 1

    log_file.close()
    logger.debug(str(wx))
    for wx_id, v in wx.iteritems():
        WSiteDailyData.today(wx_id, v[1], v[0])

