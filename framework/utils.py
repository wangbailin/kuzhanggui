# -*- coding: utf-8 -*-
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

import requests, urllib2

def send_sms(phone, content):
    url = "http://utf8.sms.webchinese.cn/?Uid=limijiaoyin&Key=66a7deba837e2f0630dc&smsMob=%s&smsText=%s" % (phone, content.encode('utf-8'))
    resp = urllib2.urlopen(url)
    return resp.read()