from datetime import date
from django import template
from django.conf import settings

from services.models import ServicePage

register = template.Library()



# Services feed for home page
@register.inclusion_tag('services/tags/service_listing_homepage.html',takes_context=True)
def service_listing_homepage(context, count=3):
    posts = ServicePage.objects.live().order_by('first_published_at')
    return {
        'posts': posts[:count],
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }