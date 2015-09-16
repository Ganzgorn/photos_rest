from django.conf.urls import url
from piston3.resource import Resource

from images_rest.handlers import *

user_resource = Resource(UserHandler)


urlpatterns = [
    url(r'^user/(?P<username>\w+)/$', user_resource, {'emitter_format': 'json'}),
    url(r'^user/$', user_resource, {'emitter_format': 'json'}),
    url(r'^user/(?P<username>\w+)/photo/upload\.json$', photo_upload),
    url(r'^user/(?P<username>\w+)/photo/info\.json$', photo_info),
    url(r'^user/(?P<username>\w+)/photo/edit\.json$', photo_edit),
    url(r'^user/(?P<username>\w+)/photo/delete\.json$', photo_delete),
    url(r'^user/(?P<username>\w+)/photo/list\.json$', photo_list),
    url(r'^user/(?P<username>\w+)/photo/search\.json$', photo_search),
    url(r'^user/(?P<username>\w+)/photo/archive\.json$', photo_archive),
    url(r'^user/(?P<username>\w+)/photo/upload\.xml$', photo_upload),
    url(r'^user/(?P<username>\w+)/photo/info\.xml$', photo_info),
    url(r'^user/(?P<username>\w+)/photo/edit\.xml$', photo_edit),
    url(r'^user/(?P<username>\w+)/photo/delete\.xml$', photo_delete),
    url(r'^user/(?P<username>\w+)/photo/list\.xml$', photo_list),
    url(r'^user/(?P<username>\w+)/photo/search\.xml$', photo_search),
    url(r'^user/(?P<username>\w+)/photo/archive\.xml$', photo_archive),
    url(r'^media/archives/(?P<archive_name>\w+)\.zip$', download_archive),
]
