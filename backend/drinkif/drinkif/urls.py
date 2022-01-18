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
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), 
    path('login', views.login_json, name='login'),
    path('logout', views.logout_json, name='logout'),
    path('register', views.register_json, name='register'),
    path('get_phrases', views.get_phrases, name='get_phrases'),
    path('add_phrases', views.add_phrases, name='add_phrases'),
    path('delete_phrase', views.delete_phrase, name='delete_phrase'),
    path('csrf', views.get_csrf, name='api-csrf'),
    path('get_user_info', views.get_user_info, name='get_user_info'),
    path('edit_phrase', views.edit_phrase, name='edit_phrase'),
    path('get_by_id', views.get_phrase_by_id, name='get_by_id'),
    path('get_friends', views.get_friends, name='get_friends'),
    path('new_friendship_request', views.new_friendship_request, name='new_friendship_request'),
    path('get_friendship_requests', views.get_friendship_requests, name='get_friendship_requests'),
    path('handle_friendship_requests', views.handle_friendship_requests, name='handle_friendship_requests'),
    path('remove_friend', views.remove_friend, name='remove_friend'),
    path('new_seed', views.newseed, name='new_seed'),
    path('gtts', views.gtts, name='gtts'),
]
if settings.ADMIN_ENABLED:
    urlpatterns += [  
        path('admin/', admin.site.urls),
    ]

urlpatterns += staticfiles_urlpatterns()