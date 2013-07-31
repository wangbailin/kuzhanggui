# -*- coding: utf-8 -*-
from inspect import isfunction
from pyweixin import WeiXin
from datetime import datetime
import logging

from django.core.cache import cache
logger = logging.getLogger("default")

class BuildConfig:
    def __init__(self, type, platform, data):
        self.type = type
        self.platform = platform
        self.data = data

    type = None
    platform = None
    data = None

def _build_weixin_raw_text(context, data):
    return WeiXin.to_text_xml(to_user_name=context.get('FromUserName', None),
            from_user_name=context.get('ToUserName', None),
            content=data,
            func_flag=0)

class MessageBuilder:
    # message types
    TYPE_RAW_TEXT = 'type_raw_text'
    TYPE_NO_RESPONSE = 'no_response'

    # platforms
    PLATFORM_WEIXIN = 'weixin'

    @classmethod
    def build(self,  context = None, build_config = None):
        return self._call_build_method(context, build_config.type, build_config.platform, build_config.data)

    _build_methods = {
        TYPE_RAW_TEXT : {
            PLATFORM_WEIXIN : _build_weixin_raw_text
        },
    }

    @classmethod
    def _call_build_method(self, context, type, platform, data):
        if self._build_methods[type] is not None:
            if isfunction(self._build_methods[type]):
                return self._build_methods[type](context, data)
            elif self._build_methods[type][platform] is not None and isfunction(self._build_methods[type][platform]):
                return self._build_methods[type][platform](context, data)
        raise 'do not support type: %s and platform: %s' % (type, platform)
