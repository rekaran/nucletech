from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.conf.urls import url, include
from . import views

login_forbidden = user_passes_test(lambda u: u.is_anonymous, 'builder.index', redirect_field_name=None)

urlpatterns = [
    url(r'^$', login_forbidden(views.index), name='home.index'),
    url(r"^contact/$", login_forbidden(views.contact), name="home.cotact"),
    url(r"^about/$", login_forbidden(views.about), name="home.about"),
    url(r"^careers/$", login_forbidden(views.commingsoon), name="home.careers"),
    url(r"^faq/$", login_forbidden(views.commingsoon), name="home.faq"),
    url(r"^casestudy/$", login_forbidden(views.commingsoon), name="home.casestudy"),
    url(r"^blogs/$", login_forbidden(views.commingsoon), name="home.blogs"),
    url(r"^sitemap /$", login_forbidden(views.commingsoon), name="home.sitemap"),
    url(r"^termsofuse/$", login_forbidden(views.termsofuse), name="home.termsofuse"),
    url(r"^privacy/$", login_forbidden(views.commingsoon), name="home.privacy"),
    url(r"^press/$", login_forbidden(views.commingsoon), name="home.press"),
    url(r"^login/$", login_forbidden(auth_views.LoginView.as_view(template_name='home/login.html', redirect_authenticated_user=True)), name='home.login'),
    url(r"^register/$", login_forbidden(views.register), name="home.register"),
    url(r"^logout/$", login_required(auth_views.LogoutView.as_view(next_page="home.login")), name="home.logout"),
    url(r'^oauth/', include('social_django.urls', namespace='home.social')),
    url(r"^passwordreset/$", login_forbidden(auth_views.PasswordResetView.as_view(template_name="home/pwdreset.html")), name="password_reset"),
    url(r"^passwordreset/done/$", login_forbidden(auth_views.PasswordResetDoneView.as_view(template_name="home/pwdresetdone.html")), name="password_reset_done"),
    url(r"^reset/2e7790b51ec46b2b8278f0c3c5a131e5c8d5d6556ef0309d22830f1487543ba2d297472f9541830a9f7928c805e365bb003b77d29da1595b75a2da5086e8de70/(?P<uidb64>[0-9a-zA-Z]+)/(?P<token>.+)/$", auth_views.PasswordResetConfirmView.as_view(template_name="home/resetconfirm.html"), name="password_reset_confirm"),
    url(r"^reset/done/$", auth_views.PasswordResetCompleteView.as_view(template_name="home/resetcomplete.html"), name="password_reset_complete"),
    url(r'^admin-login/home/user/login-as/(?P<uid>[0-9a-zA-Z]+)/$', login_required(views.loginas), name='admin.loginas'),
]