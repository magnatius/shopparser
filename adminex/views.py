# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from core.parser_base import LoadParsers

def LoadSourcesView(request):
    LoadParsers()
    return HttpResponseRedirect('/admin/core/source/')