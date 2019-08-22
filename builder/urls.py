from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', login_required(views.index), name='builder.index'),
    url(r'^(?P<name>[\w-]+)/$', login_required(views.edit), name='builder.edit'),
    url(r'^profile/$', login_required(views.profile), name='builder.profile'),
    # url(r"^register/$", views.register, name="home.register"),
]