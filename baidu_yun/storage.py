#coding:utf8
from django.core.files.storage import Storage
from django.core import files
import datetime, random, logging, os, os.path
import StringIO

logger = logging.getLogger('default')

import pybcs
pybcs.init_logging(logging.INFO)
AK = 'asaAuvEeFMOwyFMPcGe80uKz'
SK = 'EVX9MurfG2eGfTaBbp1bLCGwX4wK0D2G'
BUCKET = 'jianfei-baidu'
bcs = pybcs.BCS('http://bcs.duapp.com/', AK, SK, pybcs.HttplibHTTPC)

work_bucket = bcs.bucket(BUCKET)

from rocket import settings

class BaiduYunStorage(Storage):
    def _generate_name(self, name):
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        return "baidu_yun-%s-%d%s" % (datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), random.randint(10000, 100000), file_ext)

    def _save(self, name, content):
        logger.debug("save %s" % name)
        dir_name, file_name = os.path.split(name)
        if file_name.startswith("baidu_yun"):
            return file_name
        file_name = self._generate_name(name)
        o = work_bucket.object('/%s' % file_name)
        logger.debug("url %s %s" % (o.put_url, str(type(o.put_url))))
        real_content = content.read()
        o.put(real_content)
        o.make_public()
        return file_name


    def _open(self, name, mode="rb"):
        logger.debug("open %s" % name)
        filename = '/tmp/icon.png'
        t = files.File(open(filename, 'rb'))
        t.name = name
        return t

    def url(self, name):
        if name.startswith('baidu_yun'):
            return "http://bcs.duapp.com/jianfei-baidu/" + name
        else:
            return settings.SITE_URL + settings.MEDIA_URL + name

    def exists(self, name):
        return False
        
