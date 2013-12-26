# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Source, Category, ProxyServer,Product, Param
from django.conf import settings
from feincms.admin import tree_editor
from django.http import HttpResponse

class SourcesAdmin(admin.ModelAdmin):
    model = Source

class ParentFilter(admin.SimpleListFilter):
    title = u'Родительская категория'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'parent'

    def lookups(self, request, model_admin):
        parent_categories = Category.objects.root_nodes().order_by("name")
        root_nodes = ((category.pk, category.name) for category in parent_categories)
        return root_nodes

    def queryset(self, request, queryset):
        if self.value():
            category = Category.objects.get(pk=self.value())
            return category.get_descendants(include_self=True)
        else:
            return queryset

class CategoryAdmin(tree_editor.TreeEditor):
    model=Category
    list_display = ("name", "parent", "external_id")
    search_fields = ("name", "external_id")
    ordering = ("-parent",)
    actions = ['export_xls', 'export_csv']
    list_filter = (ParentFilter,)
    list_per_page = Category.objects.count()
    
    def export_xls(self, request, queryset):
        from export_xls.views import export_xlwt
        fields = ["id", "parent", "name", "external_id"]
        filename = "category_list"
        return export_xlwt(filename, fields, queryset.values_list(*fields))        
    export_xls.short_description = u"Экспорт в Excel"
    
    def export_csv(self, request, queryset):
        import csv
        fields = ["id", "parent", "name", "external_id"]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="category_list.csv"'
        writer = csv.writer(response)
        writer.writerow(fields)
        for values in queryset.values_list(*fields):
        	writer.writerow(values)
        return response
    export_csv.short_description = u"Экспорт в CSV"

admin.site.register(Source, SourcesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, admin.ModelAdmin)
admin.site.register(Param, admin.ModelAdmin)
admin.site.register(ProxyServer, admin.ModelAdmin)