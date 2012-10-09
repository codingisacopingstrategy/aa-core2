from django.conf.urls.defaults import (patterns, url)


urlpatterns = patterns('aacore.views',
    url(r'^$', 'browse', {}, name='aa-browse'),
)
