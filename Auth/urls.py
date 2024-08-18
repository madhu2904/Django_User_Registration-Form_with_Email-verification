from django.urls import path
from . import views
app_name="Auth"
urlpatterns=[path("",views.index,name="index"),
             path("register/",views.register,name="register"),
             path("success/",views.success,name="success"),
             path("token/",views.token,name="token"),
             path("login/",views.home,name="home"),
             path('verify/<auth_token>' ,views.verify ,name = "verify"),
             path('error' ,views.error_page , name = "error")]