"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import xadmin
import apps.wejudge.urls
import apps.account.urls
import apps.problem.urls
import apps.education.urls
import apps.contest.urls
import apps.helper.urls
import apps.oauth2.urls

urlpatterns = [
    url(r'', include(apps.wejudge.urls)),
    url(r'^account/', include(apps.account.urls)),
    url(r'^problem', include(apps.problem.urls)),
    url(r'^education/', include(apps.education.urls)),
    url(r'^contest/', include(apps.contest.urls)),
    url(r'^helper/', include(apps.helper.urls)),
    url(r'^oauth2/', include(apps.oauth2.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
]