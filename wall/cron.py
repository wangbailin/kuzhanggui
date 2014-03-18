# -*- coding: utf-8 -*-
import cronjobs
import pycurl
import cStringIO
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import redis
import json
import datetime
import urllib
import logging

sys.path.append("..")
from django.core.management import setup_environ
from rocket import settings
setup_environ(settings)

from wall.models import *
from framework.models import WXAccount
#from baidu_yun import pybcs
logger = logging.getLogger('wall')

#AK = '0PpOPCsMLi3iZ1IXjjsL5QA7'
#SK = 'kNuLSKl23B9PlQa54VSdmZBDQInUP1tH'
#BUCKET = 'nan-0610'
#bcs = pybcs.BCS('http://bcs.duapp.com/', AK, SK, pybcs.HttplibHTTPC)
#work_bucket = bcs.bucket(BUCKET)


def check_wx_id(wx_id):
    try:
        wx_account = WXAccount.objects.get(id=wx_id)
        logger.info('wx_id is valid')
        return True
    except:
        logger.info('wx_id is invalid')
        return False

def get_wall_accesstoken(wx_id):#有就得，没有就建 
    if check_wx_id(wx_id):
        wx_account = WXAccount.objects.get(id=wx_id)
        try:
            wall_accesstoken = WallAccesstoken.objects.get(wx=wx_account)
            logger.info('get_wall_accesstoken success')
            return wall_accesstoken
        except:
            wall_accesstoken = WallAccesstoken.objects.create(wx=wx_account, app_id=wx_account.app_id, app_secret=wx_account.app_secret)
            logger.info('new wall_accesstoken success')
            return wall_accesstoken

def get_new_accesstoken(app_id, app_secret):
    try:
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (app_id, app_secret)
        url = str(url)
        info = crawl(url)
        if info['access_token']:
            accesstoken = info['access_token']
            logger.info('get new accesstoken success')
            return accesstoken
        else:
            logger.info(info['errocode'])
    except:
        logger.info('get new accesstoken fail')

def crawl(url):
    try:
        c = pycurl.Curl()
        c.setopt(c.URL,url)
        buff = cStringIO.StringIO()
        hdr = cStringIO.StringIO()
        c.setopt(pycurl.SSL_VERIFYHOST, 0)
        c.setopt(pycurl.SSL_VERIFYPEER, 0)
        c.setopt(c.WRITEFUNCTION, buff.write)
        c.setopt(c.HEADERFUNCTION, hdr.write)
        c.perform()
        info = buff.getvalue()
        info = json.loads(info) 
        logger.info('crawl success')
        return info
    except:
        logger.info('crawl fail')

def download_pic(pic, openid):
    try:
        path = '/data/media/avatar/%s.png' % openid
        data = urllib.urlopen(pic).read()
        f = file(path,"wb")
        f.write(data)
        f.close()
        logger.info('download pic success')
        return True
    except:
        logger.info('download pic fail')
        return False

def fetch_info(accesstoken, openid):
    try:
        url =  "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s" % (accesstoken, openid)
        url = str(url)
        userinfo = crawl(url)
        nickname = userinfo['nickname']
        pic = userinfo['headimgurl']
        if pic == "":
            pic ='/static/img/default_avatar.png'
        else:
            if download_pic(pic, openid):
                pic = '/media/avatar/%s.png' % openid
            else:
                pic ='/static/img/default_avatar.png'
        logger.info('fetch info success')
        return [nickname, pic]
    except:
        logger.info('fetch info fail')

def fetch_one_info(wx_id, openid):
    walluser, created = WallUser.objects.get_or_create(wx_id=wx_id, openid=openid, wall_item_id=0)
    wx_id = walluser.wx_id
    wall_accesstoken = get_wall_accesstoken(wx_id)
    accesstoken = wall_accesstoken.access_token
    app_id = wall_accesstoken.app_id
    app_secret = wall_accesstoken.app_secret
    try:
        logger.info('accesstoken is %s and openid is %s'% (accesstoken, openid))
        userinfo = fetch_info(accesstoken, openid)
        walluser.nickname = userinfo[0]
        walluser.pic = userinfo[1]
        walluser.save()
        wall_accesstoken.access_token=accesstoken
        wall_accesstoken.save()
        logger.info('success')
    except:
        try:
            accesstoken = get_new_accesstoken(app_id, app_secret)
            userinfo = fetch_info(accesstoken, openid)
            logger.info(userinfo)
            walluser.nickname = userinfo[0]
            walluser.pic = userinfo[1]
            walluser.save()
            wall_accesstoken.access_token=accesstoken
            wall_accesstoken.save()
            logger.info('success')
        except:
            logger.info('fail')

@cronjobs.register
def get_one_info():
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    while True:
        res = r.blpop('userList')
        if res == None:
            logger.info('muyou new user')
            pass
        else:
            openid = res[1]
            logger.info('a new user openid is %s' % openid)
            walluser = WallUser.objects.get(openid=openid)
            wx_id = walluser.wx_id
            wall_accesstoken = get_wall_accesstoken(wx_id) 
            accesstoken = wall_accesstoken.access_token
            app_id = wall_accesstoken.app_id
            app_secret = wall_accesstoken.app_secret
            try:
                if accesstoken == "":
                    accesstoken = get_new_accesstoken(app_id, app_secret)
                logger.info('accesstoken is %s and openid is %s'% (accesstoken, openid))
                userinfo = fetch_info(accesstoken, openid)
                walluser.nickname = userinfo[0]
                walluser.pic = userinfo[1]
                walluser.save()
                wall_accesstoken.access_token=accesstoken
                wall_accesstoken.save()
                logger.info('success')
            except:
                try:
                    accesstoken = get_new_accesstoken(app_id, app_secret)
                    userinfo = fetch_info(accesstoken, openid)
                    logger.info(userinfo)
                    walluser.nickname = userinfo[0]
                    walluser.pic = userinfo[1]
                    walluser.save()
                    wall_accesstoken.access_token=accesstoken
                    wall_accesstoken.save()
                    logger.info('success')
                except:
                    logger.info('fail')
                    pass

@cronjobs.register
def get_all_info(wx_id):
    try:
        wall_accesstoken = get_wall_accesstoken(wx_id)
        accesstoken = wall_accesstoken.access_token
        app_id = wall_accesstoken.app_id
        app_secret = wall_accesstoken.app_secret
        if accesstoken == "":
            accesstoken = get_new_accesstoken(app_id, app_secret)
            wall_accesstoken.access_token=accesstoken
            wall_accesstoken.save()
        #用用户分组管理接口测试accesstoken
        url_test = "https://api.weixin.qq.com/cgi-bin/groups/get?access_token=%s"  % accesstoken
        url_test = str(url_test)
        info = crawl(url_test)
        try:
            if info['groups']:
                logger.info('accesstoken is useful')
            else:
                logger.info('accesstoken is not useful')
                accesstoken = get_new_accesstoken(app_id, app_secret)
                wall_accesstoken.access_token=accesstoken
                wall_accesstoken.save()
        except:
            accesstoken = get_new_accesstoken(app_id, app_secret)
            wall_accesstoken.access_token=accesstoken
            wall_accesstoken.save()
            logger.info('get a new  accesstoken')
        url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s" % accesstoken
        url = str(url)
        userlist = crawl(url)
        logger.info(userlist)
        total = userlist['total']
        logger.info('接口已被授权')
        #最多一万，以后可以补上
        if total:
            total = int(total)
            count = int(userlist['count'])
            logger.info('total is %d' % total)
            data = userlist['data']  
            openids = data['openid']
            num = 0 
            for openid in openids:
                try:
                    fetch_one_info(wx_id, openid)
                    num = num + 1
                    logger.info('sucess %s' % openid)
                    logger.info('total is %d ,doing %d and success %d' % (count, num, num ))
                except:
                    logger.info('fail %s' % openid)
                    num = num + 1
                    logger.info('total is %d ,doing %d and fail %d' % (count, num, num ))
                    pass
    except:
        logger.info('fail')
