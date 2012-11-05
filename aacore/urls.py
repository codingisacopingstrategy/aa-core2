from django.conf.urls.defaults import (patterns, url)


urlpatterns = patterns('aacore.views',
    url(r'^$', 'browse', {}, name='aa-browse'),
    url(r'^namespaces.css/$', 'namespaces_css', {}, name='aa-namespaces-css'),
)
