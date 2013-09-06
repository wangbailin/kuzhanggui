#coding:utf8

DEFAULT_JOIN_COVER = 'img/joinus_message.png'
DEFAULT_CONTACT_COVER = 'img/kefuphone_message.png'
DEFAULT_NEWS_COVER = 'img/news_message.png'
DEFAULT_PRODUCT_COVER = 'img/product_message.png'
DEFAULT_CASE_COVER = 'img/case_message.png'

DEFAULT_HOMEPAGE_MSG = u'点击查看%s微官网。'
DEFAULT_INTRO_MSG = u'点击查看公司介绍。'
DEFAULT_BUSINESS_MSG = u'点击查看公司业务。'
DEFAULT_NEWS_MSG = u'点击查看公司动态。'
DEFAULT_JOIN_MSG = u'点击查看公司最新招聘信息。'
DEFAULT_CONTACT_MSG = u'点击查看公司联系方式。'
DEFAULT_CASE_MSG = u'点击查看公司案例。'
DEFAULT_PRODUCT_MSG = u'点击查看公司产品。'
DEFAULT_WEIBO_MSG = u'点击查看公司官方微博。'
DEFAULT_HELP_MSG = u'点击查看新手指导。'
DEFAULT_MSG = "点击查看全部内容。"

def get_default_msg(page):
    if page.real_type == ContentType.objects.get_for_model(ContactApp):
        return DEFAULT_CONTACT_MSG
    elif page.real_type == ContentType.objects.get_for_model(TrendsApp):
        return DEFAULT_NEWS_MSG
    elif page.real_type == ContentType.objects.get_for_model(CaseApp):
        return DEFAULT_CASE_MSG
    elif page.real_type == ContentType.objects.get_for_model(ProductApp):
        return DEFAULT_PRODUCT_MSG
    elif page.real_type == ContentType.objects.get_for_model(HomePage):
        return DEFAULT_HOMEPAGE_MSG
    elif page.real_type == ContentType.objects.get_for_model(IntroPage):
        return DEFAULT_INTRO_MSG
    elif page.real_type == ContentType.objects.get_for_model(BusinessPage):
        return DEFAULT_BUSINESS_MSG
    elif page.real_type == ContentType.objects.get_for_model(JoinPage):
        return DEFAULT_JOIN_MSG
    elif page.real_type == ContentType.objects.get_for_model(WeiboPage):
        return DEFAULT_WEIBO_MSG
    elif page.real_type == ContentType.objects.get_for_model(ContentPage):
        return DEFAULT_MSG
    elif page.real_type == ContentType.objects.get_for_model(LinkPage):
        return DEFAULT_MSG