from django.urls import path
from . import views
urlpatterns = [
    path('', views.login_page, name= "login_page"),
    path('registration', views.registration, name="registration"),
    path('registration_page', views.registration_page, name="registration_page"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
]

