# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from user_agents import parse
import logging

logger = logging.getLogger('wall')

def judge_os_br(user_agent):
    ua_string = user_agent
    user_agent = parse(ua_string)

    browser = user_agent.browser.family
    os = user_agent.os.family
    logger.info(browser)
    logger.info(os)


def judge_symbol(str):
    s = str[-1]
    if s == ',' or s == '.' or s == '!' or s == '?' or s == '，' or s =='。' or s == '！' or s == '？':
        return True
    else:
        return False
