from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.api import EntryResource, testResource, UserResource, RedisResource
from tastypie.api import Api
#from django.conf.urls.defaults import *

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(EntryResource())
v1_api.register(RedisResource())
v1_api.register(testResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'apitest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^blog/', include('api.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
