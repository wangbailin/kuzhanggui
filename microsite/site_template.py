#coding:utf8

class SiteTemplate(object):
    def __init__(self):
        self.site_template = ''
        self.template_dicts = {}
        self.name = ''


site_templates = {}
t = SiteTemplate()
t.site_template = 'default'
t.name = u"数码黑"
#t.template_dicts['microsite.homepage'] = 'homepage.html'
site_templates[1] = t

t2 = SiteTemplate()
t2.site_template = 'default_light'
t2.name = u"珍珠白"
#t2.template_dicts['microsite.homepage'] = 'homepage.html'
site_templates[2] = t2

