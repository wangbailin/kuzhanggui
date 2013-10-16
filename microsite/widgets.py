#coding: utf-8
from django import forms

def _append_class(attrs, cls):
    classnames = attrs.get('class')
    if classnames is None:
        classnames = cls
    else:
        classnames += ' ' + cls
    attrs['class'] = classnames

class LongTextInput(forms.TextInput):
    def __init__(self, attrs=None):
        if attrs is None:
            forms.TextInput.__init__(self, attrs={'class': 'input-xxlarge'})
            return;

        _append_class(attrs, 'input-xxlarge')
        forms.TextInput.__init__(self, attrs=attrs)


class LongTextarea(forms.Textarea):
    def __init__(self, attrs=None):
        if attrs is None:
            forms.Textarea.__init__(self, attrs={'class': 'input-xxlarge'})
            return;

        _append_class(attrs, 'input-xxlarge')
        forms.Textarea.__init__(self, attrs=attrs)


