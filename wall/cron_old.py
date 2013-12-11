 -*- coding: utf-8 -*-
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

class AccessTokenNull(Exception):
    print 'accesstoken is null'

class AccessTokenUnuseful(Exception):
    print 'accesstoken is unuseful'

@cronjobs.register
def info_get():

    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    while True:
        res = r.blpop('userList')
        if res == None:
            pass
        else:
            logger.info('a new user')
            openid = res[1]
            logger.info('openid is %s' % openid)
            #现在无法测试其他帐号，所以过滤掉其他帐号,回来补上
            walluser = WallUser.objects.get(openid=openid)
            wx_id = walluser.wx_id
            if wx_id == 37:
                wall_accesstoken = WallAccesstoken.objects.get(wx_id=wx_id)
                accesstoken = wall_accesstoken.access_token
                app_id = wall_accesstoken.app_id
                app_secret = wall_accesstoken.app_secret
                try: 
                    if accesstoken == "":
                        raise AccessTokenNull
                    else:
                        
                        userinfo = crawl(accesstoken, openid)
                        userinfo = json.loads(userinfo)
                        nickname = userinfo['nickname']
                        if nickname == "":
                            raise AccessTokenUnuseful
                        else:
                            logger.info('almost sucess')
                            pic = userinfo['headimgurl']
                            walluser.nickname = nickname
                            logger.info(nickname)
                            if pic == "":
                                walluser.pic = '/static/img/default_avatar.png'
                            else:
                                picUrl = pic
                                logger.info(pic)
                                path = '/data/media/avatar/%s.png' % openid
                                data = urllib.urlopen(picUrl).read()  
                                f = file(path,"wb")  
                                f.write(data)  
                                f.close()
                                # o = work_bucket.object('/1.png')
                                # o.put_file(path)
                                walluser.pic = '/media/avatar/%s.png' % openid
                            walluser.save()
                            logger.info('sucess')
                except:
                    try:
                        logger.info('get new accesstoken')
                        accesstoken = get_new_accesstoken(app_id, app_secret)
                        logger.info('accesstoken is %s' % accesstoken)
                        userinfo = crawl(accesstoken, openid)
                        userinfo = json.loads(userinfo)
                        nickname = userinfo['nickname']
                        pic = userinfo['headimgurl']
                        walluser.nickname = nickname
                        if pic == "":
                            walluser.pic = '/static/img/default_avatar.png'
                        else:
                            picUrl = pic
                            logger.info(pic)
                            path = '/data/media/avatar/%s.png' % openid
                            data = urllib.urlopen(picUrl).read()
                            f = file(path,"wb")
                            f.write(data)
                            f.close()
                           # o = work_bucket.object('/1.png')
                           # o.put_file(path)
                            walluser.pic = '/media/avatar/%s.png' % openid
                        walluser.save()
                        logger.info('sucess')
                        wall_accesstoken.access_token = accesstoken
                        wall_accesstoken.last_get_time = datetime.datetime.now()
                        wall_accesstoken.save()
                    except:
                        logger.info('wrong')
                        pass


def crawl(accesstoken, openid):
    c = pycurl.Curl()
    url =  "https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s" % (accesstoken, openid)
    url = str(url)
    c.setopt(c.URL, url)
    buffc = cStringIO.StringIO()
    hdrc = cStringIO.StringIO()
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(c.WRITEFUNCTION, buffc.write)
    c.setopt(c.HEADERFUNCTION, hdrc.write)
    c.perform()
    userinfo = buffc.getvalue()
    return userinfo

def get_new_accesstoken(app_id, app_secret):    
    b = pycurl.Curl()
    url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (app_id, app_secret)
    url = str(url)
    b.setopt(b.URL, url)
    buffb = cStringIO.StringIO()
    hdrb = cStringIO.StringIO()
    b.setopt(pycurl.SSL_VERIFYHOST, 0)
    b.setopt(pycurl.SSL_VERIFYPEER, 0)
    b.setopt(b.WRITEFUNCTION, buffb.write)
    b.setopt(b.HEADERFUNCTION, hdrb.write)
    b.perform()
    accesstoken = eval(buffb.getvalue())['access_token']
    return accesstoken

        

@cronjobs.register
def get_all_info():
    wx_accounts = WXAccount.objects.all()

    for account in wx_accounts:
        
            
        

        
