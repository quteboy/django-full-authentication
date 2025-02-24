from django.urls import path,include

from .views import register,user_login

app_name = 'basic_app'

urlpatterns=[
    path('register/',register,name='register'),
    path('user_login/',user_login, name='user_login')
]