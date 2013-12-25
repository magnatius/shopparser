# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Source, Category, ProxyServer

class SourcesAdmin(admin.ModelAdmin):
    model = Source
    
    

admin.site.register(Source, SourcesAdmin)
admin.site.register(Category, admin.ModelAdmin)
admin.site.register(ProxyServer, admin.ModelAdmin)