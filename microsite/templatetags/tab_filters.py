from django import template
from django.contrib.contenttypes.models import ContentType

from microsite.models import HomePage

register = template.Library()

@register.filter
def sortable_tabs(tabs):
    homepage_type = ContentType.objects.get_for_model(HomePage)
    return filter(lambda t: t[0].real_type != homepage_type and t[0].enable, tabs)

