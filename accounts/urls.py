from django.conf.urls import url
from .views import *

#app_name = 'accounts'

urlpatterns = [
    url(r'^accounts/signup/$', signup_view, name="signup"),
    url(r'^accounts/login/$', login_view, name="login"),
    url(r'^accounts/logout/$', logout_view, name="logout"),
]