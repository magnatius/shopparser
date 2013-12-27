# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from core.parser_base import GetParser
from core.models import Source, ProxyServer
import json, urllib

def ParseAjax(request, sid):
    if request.is_ajax():
        threads = request.GET.get('threads', 1)
        ptype = request.GET.get('ptype')
        if ptype:
            proxies = json.loads(urllib.unquote(request.GET.get('proxies')))
            server_list=[]
            for proxy_id in proxies:
                server = ProxyServer.objects.get(id=proxy_id)
                server_str =':'.join([server.server,str(server.port)])
                if server.username:
                    server_str = ":".join([server_str, server.username, server.password])
                server_list.append(server_str)
        source = Source.objects.get(id=sid)
        if not source.parser.split('.')[1] in globals():
            try:
                globals().update({source.parser.split('.')[1]:GetParser(source.parser)})
            except:
                return {'result':False, 'message':'parser %(pname)s not found for feeding data from %(stitle)s' % {'pname':source.parser.split('.')[1], 'stitle':source.title}}
        parser = globals()[source.parser.split('.')[1]](source=source)
        if ptype:
            parser.parse(threads=threads, ptype=ptype, proxies=server_list)
        else:
            parser.parse(threads=threads)
        return HttpResponse('ok')

    else:
        raise Http404
    
