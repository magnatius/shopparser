# -*- coding: utf-8 -*-
from django import template
from core.models import Source

register = template.Library()

@register.inclusion_tag('adminex/source_admin.html')
def display_parsers():
    sources = Source.objects.all()
    return { 'sources': sources }