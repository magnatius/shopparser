# -*- coding: utf-8 -*-
import os,sys, importlib, inspect
from core.models import Source, Category, Product, Param
from core.ext_fn import get_or_none
from shopparser.settings import BASE_DIR

class Parser(object):
    Name = 'undefined'
    Link = 'undefined'
    Source = None
    
    def parse(self, *args, **kwargs):
        pass
    
    def GetCategory(self, category):
        cat_in_base, created = Category.objects.get_or_create(parent=category.parent, external_id=category.id, source=category.src, defaults={'name':category.name})
        return created

def LoadParsers():
    files = os.listdir(BASE_DIR+'/core/parsers')
    sys.path.append(BASE_DIR+'/core')
    sys.path.append(BASE_DIR+'/core/parsers')
    for file in files:
        if os.path.splitext(file)[1]=='.py':
            mod = importlib.import_module(os.path.splitext(file)[0])
            globals().update({name: getattr(mod, name) for name, obj in inspect.getmembers(mod)})
    for parser in Parser.__subclasses__():
        p = parser()
        src = Source.objects.get_or_create(title=p.Name, url=p.Link, parser = p.__module__+'.'+p.__class__.__name__)
        p.Source=src
        
def GetParser(name):
    sys.path.append(BASE_DIR+'/core')
    sys.path.append(BASE_DIR+'/core/parsers')
    mod_name = name.split('.')[0]
    parser_name = name.split('.')[1]
    mod = importlib.import_module(mod_name)
    return getattr(mod, parser_name)
    