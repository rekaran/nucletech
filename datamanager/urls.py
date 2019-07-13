from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', login_required(views.index), name='datamanager.index'),
    url(r'^(?P<name>[a-zA-Z0-9_$]+)/$', login_required(views.getdata), name='datamanager.getdata'),
    url(r'^(?P<name>[a-zA-Z0-9_$]+)/savedata/$', login_required(views.savedata), name='datamanager.savedata'),
]