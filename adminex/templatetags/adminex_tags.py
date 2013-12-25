# -*- coding: utf-8 -*-
from django import template
from core.models import Source, ProxyServer

register = template.Library()

@register.inclusion_tag('adminex/source_admin.html')
def display_parsers():
    sources = Source.objects.all()
    proxies = ProxyServer.objects.filter(type=0)
    return { 'sources': sources, 'proxies': proxies }
