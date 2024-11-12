from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.welcome, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout_view'),
     path('add/', views.add_blog_post, name='add_blog_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete_blog_post/<int:post_id>/', views.delete_blog_post, name='delete_blog_post'),
    path('edit_post/<int:post_id>/', views.edit_blog_post, name='edit_blog_post'),


    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)