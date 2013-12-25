# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse, Http404
from core.parser_base import LoadParsers
from core.models import ProxyServer
from django.core import serializers

def LoadSourcesView(request):
    LoadParsers()
    return HttpResponseRedirect('/admin/core/source/')

def ProxyList(request):
    if request.is_ajax():
        type=request.GET.get('type', 0)
        proxies = ProxyServer.objects.filter(type=int(type))
        return HttpResponse(serializers.serialize("json", proxies))
    else:
        raise Http404