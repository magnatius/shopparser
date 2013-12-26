# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Source, Category, ProxyServer,Product, Param
from django.conf import settings
from mptt.admin import MPTTModelAdmin

class SourcesAdmin(admin.ModelAdmin):
    model = Source

admin.site.register(Source, SourcesAdmin)
admin.site.register(Category, MPTTModelAdmin)
admin.site.register(Product, admin.ModelAdmin)
admin.site.register(Param, admin.ModelAdmin)
admin.site.register(ProxyServer, admin.ModelAdmin)