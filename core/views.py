# -*- coding: utf-8 -*-

from django.http import HttpResponse, Http404
from core.parser_base import GetParser
from core.models import Source

def ParseAjax(request, sid):
    if request.is_ajax():
        threads = request.GET.get('threads', 1)
        source = Source.objects.get(id=sid)
        if not source.parser.split('.')[1] in globals():
            try:
                globals().update({source.parser.split('.')[1]:GetParser(source.parser)})
            except:
                return {'result':False, 'message':'parser %(pname)s not found for feeding data from %(stitle)s' % {'pname':source.parser.split('.')[1], 'stitle':source.title}}
        parser = globals()[source.parser.split('.')[1]](source=source)
        parser.parse(threads=threads)
        return HttpResponse('ok')

    else:
        raise Http404
    
