from django.urls import path, include
from .views import *


urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('signup/', user_signup, name='signup'),
    path('edit/', profile_edit, name='edit'),
    path('user_mail_send/', user_mail_send, name='sendemail'),
]