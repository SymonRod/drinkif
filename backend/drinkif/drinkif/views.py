import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import CSRF_SESSION_KEY, get_token
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from drinkif.models import *
import json, os

def validate_password_strength(value):
    """Validates that a password is as least 8 characters long and has at least
    1 digit and 1 letter.
    """
    min_length = 8

    if len(value) < min_length:
        return False

    # check for digit
    if not any(char.isdigit() for char in value):
        return False

    # check for letter
    if not any(char.isalpha() for char in value):
        return False
    return True




def index(request):
    return render(request, 'index.html')

@never_cache
def login_json(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    
    user = User.objects.filter(username=username).first()

    if not user:
        return JsonResponse({'status': 'fail','description':'login.errors.username-does-not-exits'} , status=403)

    user = authenticate(username=username, password=password)

    if user:
        login(request, user)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'fail','description':'login.errors.password-incorrect'} , status=403)

@never_cache

def logout_json(request):
    logout(request)
    return redirect('/')

@never_cache
def register_json(request):
    data = json.loads(request.body)
    username = data['username']
    password = data['password']
    
    # Check if username is already taken
    if User.objects.filter(username=username).exists():
        return JsonResponse({'status': 'fail','description':'sign-up.errors.username-taken'}, status=400)
    
    
    if not validate_password_strength(password):
        return JsonResponse({'status': 'fail','description':'sign-up.errors.password-requirements'}, status=400)
    
    if username is not None and password is not None:
        user = User.objects.create_user(username,'',password)
        user.save()
        login(request, user)
        return JsonResponse({'status': 'success'})

@never_cache
def get_phrases(request):
    if request.user.is_authenticated:
        data = phrases.objects.filter(creator=request.user)
        phrases_list = []
        for phrase in data:
            temp = {'phrase_text': phrase.phrase_text, 'id': phrase.id}
            phrases_list.append(temp)
        return JsonResponse({'phrases': phrases_list})
    else:
        return JsonResponse({'status': 'fail'}, status=403)

@never_cache
def add_phrases(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        phrases_list = data['phrases']
        for phrase in phrases_list:
            new_phrase = phrases(creator=request.user, phrase_text=phrase)
            new_phrase.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'fail'}, status=403)

@never_cache
def delete_phrase(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        id = data['id']
        phrase = phrases.objects.get(id=id)
        if phrase.creator == request.user:
            phrase.delete()
            return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'fail'}, status=403)

@csrf_exempt
def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response


@never_cache
def get_user_info(request):
    if request.user.is_authenticated:
        data = {'username': request.user.username, 'id': request.user.id, 'is_authenticated': True}
        return JsonResponse(data)
    else:
        return JsonResponse({'status': 'fail'}, status=403)


@never_cache
def edit_phrase(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        id = data['id']
        phrase = phrases.objects.get(id=id)
        if phrase.creator == request.user:
            phrase.phrase_text = data['text']
            phrase.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail'}, status=403)
    else:
        return JsonResponse({'status': 'fail'}, status=403)

@never_cache
@csrf_exempt
def get_phrase_by_id(request):
    data = json.loads(request.body)
    id = data['id']
    phrase = phrases.objects.get(id=id)
    return JsonResponse({'sentence':{'id': phrase.id, 'text': phrase.phrase_text}})