# -*- coding: utf-8 -*-
from celery.decorators import task
from core.parser_base import GetParser

@task
def run_spider(source, threads, ptype, server_list):
    if not source.parser.split('.')[1] in globals():
            if True:
            #try:
                globals().update({source.parser.split('.')[1]:GetParser(source.parser)})
            #except:
                #return {'result':False, 'message':'parser %(pname)s not found for feeding data from %(stitle)s' % {'pname':source.parser.split('.')[1], 'stitle':source.title}}
    parser = globals()[source.parser.split('.')[1]](source=source)
    if ptype:
        parser.parse(threads=threads, ptype=ptype, proxies=server_list)
    else:
        parser.parse(threads=threads)