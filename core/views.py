# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from core.parser_base import GetParser
from core.models import Source, ProxyServer
import json, urllib
from core.tasks import run_spider

def ParseAjax(request, sid):
    if request.is_ajax():
        threads = request.GET.get('threads', 1)
        ptype = request.GET.get('ptype')
        server_list=[]
        if ptype:
            proxies = json.loads(urllib.unquote(request.GET.get('proxies')))
            for proxy_id in proxies:
                server = ProxyServer.objects.get(id=proxy_id)
                server_str =':'.join([server.server,str(server.port)])
                if server.username:
                    server_str = ":".join([server_str, server.username, server.password])
                server_list.append(server_str)
        source = Source.objects.get(id=sid)
        run_spider.delay(source, threads, ptype, server_list)
        return HttpResponse('ok')

    else:
        raise Http404
    
