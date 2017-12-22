
from django.conf.urls import url
from .views import wejudge
from .views import ckeditor


urlpatterns = [
    url(r'^$', wejudge.index, name='wejudge.index.index'),
    url(r'^index.html$', wejudge.index, name='wejudge.index.index.html'),
    url(r'^debug/on$', wejudge.sys_open_debug),
    url(r'^debug/off$', wejudge.sys_close_debug),
    url(r'^debug/status$', wejudge.sys_debug_status),

    url(r'^api/ckeditor/imgupload.do$', ckeditor.imgupload, name='api.wejudge.ckeditor.imgupload'),
    url(r'^api/ckeditor/fileupload.do$', ckeditor.fileupload, name='api.wejudge.ckeditor.fileupload'),
    url(r'^api/system/urls.json', wejudge.system_urls, name='api.wejudge.system.urls')
]
