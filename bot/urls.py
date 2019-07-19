from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='bot.index'),
    url(r"^realestate/$", views.realestate, name="bot.realestate"),
]