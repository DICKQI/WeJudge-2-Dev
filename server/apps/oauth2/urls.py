
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^services/education/school/(?P<sid>\d+)/authorize$', authorize_education, name="oauth2.education.authorize"),
    url(r'^services/access_token$', access_token, name="oauth2.services.access.token"),
    url(r'^services/access_token/valid$', valid_access_token, name="oauth2.services.valid.access.token"),
    url(r'^services/refresh_token$', refresh_token, name="oauth2.services.refresh.token"),
]