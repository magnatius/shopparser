from django.conf.urls import patterns, include, url
from adminex.views import LoadSourcesView, ProxyList
from core.views import ParseAjax
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shopparser.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^parse/(?P<sid>(\d+))/', ParseAjax),
    url(r'^admin/load_sources/', LoadSourcesView),
    url(r'^admin/proxy_list/', ProxyList),
    url(r'^admin/', include(admin.site.urls)),
    
)
