#encoding=utf-8
#! usr/local/bin/python
import cronjobs
import datetime
import logging
import sys
import os, os.path, re, time

sys.path.append("..")

from django.core.management import setup_environ
from rocket import settings
setup_environ(settings)

logger = logging.getLogger("cron")

from data.models import WSiteDailyData, WeixinDailyData
from framework.models import WXAccount

@cronjobs.register
def sts_log_analyse():
    log_update_time = os.path.getmtime("./logs/sts.log")
    today_begin_time = int((time.time() + 8 * 3600) / (24 * 3600)) * 24 * 3600 - 8 * 3600
    for wx in WXAccount.objects.filter(state=WXAccount.STATE_BOUND):
        try:
            data = WSiteDailyData.objects.get(weixin=wx, date=datetime.date.today())
            logger.debug("already have one")
        except:
            logger.error(traceback.format_exc())
            data = WSiteDailyData()
            data.weixin = wx
            data.date = datetime.date.today()
            data.visitor_count = 0
            data.visit_count = 0
            data.save()
    if log_update_time > today_begin_time:
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


@cronjobs.register
def weixin_daily_analyse():
    for wx in WXAccount.objects.filter(state=WXAccount.STATE_BOUND):
        try:
            data = WeixinDailyData.objects.get(weixin=wx, date=datetime.date.today())
            logger.debug("already have one")
        except:
            data = WeixinDailyData()
            data.weixin = wx
            data.date = datetime.date.today()
            data.save()


    
