# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Source

class SourcesAdmin(admin.ModelAdmin):
    model = Source

admin.site.register(Source, SourcesAdmin)