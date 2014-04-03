# -*- coding: utf-8 -*-
import sys 
import logging;
reload(sys) 
sys.setdefaultencoding('utf8')

import urllib  
import urllib2
import json


logger = logging.getLogger("default")

def get_wx_access_token(app_id, app_secret):
    req = urllib2.Request('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (app_id, app_secret))
    data = urllib.urlencode({})
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    resp = opener.open(req, data)
    
    data = resp.read()
    p = data.find('\r\n\r\n')
    if p >= 0:
        data = data[p:]
    logger.debug(data)

    jsonObj = json.loads(data)
    if jsonObj.has_key('access_token'):
        return jsonObj.get('access_token')
    else:
        return None

        
def create_wx_menu(access_token, menus):
    if not delete_wx_menu(access_token):
        return False

    req = urllib2.Request('https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % (access_token))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    resp = opener.open(req, str(menus))
    
    jsonObj = json.loads(resp.read())
    print jsonObj
    if jsonObj.get('errcode') == 0:
        return True
    else:
        return False

def delete_wx_menu(access_token):
    req = urllib2.Request('https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s' % (access_token))
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    resp = opener.open(req, {})
    
    jsonObj = json.loads(resp.read())
    print jsonObj
    if jsonObj.get('errcode') == 0:
        return True
    else:
        return False