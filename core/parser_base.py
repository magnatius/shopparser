# -*- coding: utf-8 -*-
import os,sys, importlib, inspect
from core.models import Source, Category, Product, Param
from core.ext_fn import get_or_none
from shopparser.settings import BASE_DIR

class Parser(object):
    Name = 'undefined'
    Link = 'undefined'
    
    def __init__(self, *args, **kwargs):
        if 'source' in kwargs:
            self.source=kwargs['source']
        super(Parser, self).__init__()
    
    
    def parse(self, *args, **kwargs):
        pass
    
    def ResetUpdateFlag(self):
        categories=Category.objects.filter(source=self.source)
        categories.update(updated=False)
        for category in categories:
            products = category.products.all()
            products.update(updated=False)
            for product in products:
                product.params.update(updated=False)
    
    def CleanDeleted(self):
        categories = Category.objects.filter(source=self.source).filter(updated=False)
        categories.delete()
        products = Product.objects.select_related().filter(category__source=self.source).filter(updated=False)
        products.delete()
    
    def GetCategory(self, category):
        if category['parent']:
            parent = Category.objects.get(external_id=category['parent'])
        else: 
            parent = None
        cat_in_base, created = Category.objects.get_or_create(parent=parent, external_id=category['id'], source=category['src'], defaults={'name':category['name']})
        if not created:
            cat_in_base.updated=True
            cat_in_base.save()
        return created
    
    def GetProduct(self, product):
        category = Category.objects.get(external_id=product['category'])
        prod_in_base, created = Product.objects.get_or_create(external_id=product['id'], defaults={'name':product['name']})
        if not created:
            prod_in_base.updated = True
            prod_in_base.save()
        prod_in_base.category.add(category)
        return created
    
    def UpdateParam(self, param):
        product = Product.objects.get(external_id=param['product'])
        param_in_base, created = Param.objects.get_or_create(product=product, name=param['name'], defaults={'value':param['value']})
        if not created:
            param_in_base.value = param['value']
            param_in_base.updated = True
            param_in_base.save()
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
    