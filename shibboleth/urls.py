from django.urls import path
from shibboleth import views

app_name = 'shibboleth'
urlpatterns = [
    path('login', views.shibboleth_login, name='login'),
    path('test', views.shibboleth_test, name='test'),
]
