from django.urls.conf import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='article_menu'),
    path('allList/', views.article_list, name='article_list'),
    path('allList/<int:aid>/', views.article_info, name='article_info'),
    path('articleCreate/', views.article_create, name='article_create'),
    path('articleDelete/<int:aid>/', views.article_delete, name='article_delete'),
    path('articleUpdate/<int:aid>/', views.article_update, name='article_update'),
    path('about/', views.about, name='about'),
    path('typing_game/', views.typing_game, name='typing_game'),
]

