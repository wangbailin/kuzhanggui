#coding:utf8

class SiteTemplate(object):
    def __init__(self):
        self.site_template = ''
        self.template_dicts = {}
        self.name = ''


site_templates = {}
t = SiteTemplate()
t.site_template = 'a'
t.name = u"标准模板"
t.template_dicts['microsite.homepage'] = 'homepage.html'
site_templates[1] = t

