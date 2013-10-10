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
try: 
    from PIL import Image, ImageOps 
except ImportError: 
    import Image 
    import ImageOps 



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
        baidu_name = self._generate_name(name)
        o = work_bucket.object('/%s' % baidu_name)
        real_content = content.read()
        o.put(real_content)
        o.make_public()
        return baidu_name


    def _open(self, name, mode="rb"):
        logger.debug("open %s" % name)
        filename = '/tmp/icon.png'
        t = files.File(open(filename, 'rb'))
        t.name = name
        return t

    def ckeditor_upload(self, name, uid, thumb_size):
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        baidu_name = "baidu_yun-ckeditor-%d-%s-%d%s" % (uid, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"), random.randint(10000, 100000), file_ext)
        o = work_bucket.object('/%s' % baidu_name)
        o.put_file(name)
        o.make_public()

        thumb_name = '%s_thumb%s' % os.path.splitext(name)
        thumb_baidu_name = '%s_thumb%s' % os.path.splitext(baidu_name)
        image = Image.open(name)
        # Convert to RGB if necessary
        # Thanks to Limodou on DjangoSnippets.org
        # http://www.djangosnippets.org/snippets/20/
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')

        # scale and crop to thumbnail
        imagefit = ImageOps.fit(image, thumb_size, Image.ANTIALIAS)
        imagefit.save(thumb_name)
        o = work_bucket.object('/%s' % thumb_baidu_name)
        o.put_file(thumb_name)
        o.make_public()

        return baidu_name

        
    def url(self, name):
        if name.startswith('baidu_yun'):
            return "http://bcs.duapp.com/%s/" % BUCKET + name
        else:
            return settings.SITE_URL + settings.MEDIA_URL + name

    def ckeditor_thumb_url(self, baidu_name):
        thumb_baidu_name = '%s_thumb%s' % os.path.splitext(baidu_name)
        return self.url(thumb_baidu_name)

    def ckeditor_list(self, uid):
        objs = work_bucket.list_objects(prefix="/baidu_yun-ckeditor-%d" % uid)
        names = []
        for o in objs:
            name = os.path.splitext(o.object_name)[0]
            if name.endswith('_thumb'):
                continue
            names.append(o.object_name[1:])
        return names
        
    def exists(self, name):
        return False
        
