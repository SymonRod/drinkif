"""drinkif URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from drinkif import views
from drinkif import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('api/login', views.login_json, name='login'),
    path('api/logout', views.logout_json, name='logout'),
    path('api/register', views.register_json, name='register'),
    path('api/get_phrases', views.get_phrases, name='get_phrases'),
    path('api/add_phrases', views.add_phrases, name='add_phrases'),
    path('api/delete_phrase', views.delete_phrase, name='delete_phrase'),
    path('api/csrf', views.get_csrf, name='api-csrf'),
    path('api/get_user_info', views.get_user_info, name='get_user_info'),
    path('api/edit_phrase', views.edit_phrase, name='edit_phrase'),
    path('api/get_by_id', views.get_phrase_by_id, name='get_by_id'),
    path('api/get_friends', views.get_friends, name='get_friends'),
    path('api/new_friendship_request', views.new_friendship_request, name='new_friendship_request'),
    path('api/get_friendship_requests', views.get_friendship_requests, name='get_friendship_requests'),
    path('api/handle_friendship_requests', views.handle_friendship_requests, name='handle_friendship_requests'),
    path('api/remove_friend', views.remove_friend, name='remove_friend'),
    path('api/new_seed', views.newseed, name='new_seed'),
    path('api/gtts', views.gtts, name='gtts'),
]

if not settings.PROD:
    urlpatterns+=[
        path('', views.index, name='index'), 
    ]

if settings.ADMIN_ENABLED:
    urlpatterns += [  
        path('api/admin/', admin.site.urls),
    ]

urlpatterns += staticfiles_urlpatterns()