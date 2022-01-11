import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import CSRF_SESSION_KEY, get_token
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, request
from drinkif.models import *
import json, os, random, string

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
def register_json(request: request):
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
        if not ExtendedUser.objects.filter(user=request.user).exists():
            extendedUser = ExtendedUser(user=request.user)
            extendedUser.avatar_seed = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
            extendedUser.save()

        return JsonResponse(request.user.extendeduser.user_data())
    else:
        return JsonResponse({'status': 'fail'}, status=403)

@never_cache
def new_friendship_request(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        username = data['username']
        friend = User.objects.filter(username=username).first()
        if friend:
            for friendship in Friendship.objects.filter(user=request.user):
                if friendship.friend == friend:
                    return JsonResponse({'status': 'fail', 'description': 'friendship.errors.already-friends'}, status=400)
            if FriendshipRequest.objects.filter(sender=request.user, receiver=friend).first():
                return JsonResponse({'status': 'fail', 'description': 'friendship.errors.already-requested'}, status=400)
            friendshiprequest = FriendshipRequest(sender=request.user, receiver=friend)
            friendshiprequest.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'description': 'friendship.errors.user-does-not-exists'}, status=400)
    else:
        return JsonResponse({'status': 'fail'}, status=403)

@never_cache
def get_friendship_requests(request):
    if request.user.is_authenticated:
        requests = []
        for request in  FriendshipRequest.objects.filter(receiver=request.user):
            requests.append(request.sender.extendeduser.user_data())
        return JsonResponse({'requests': requests})

@never_cache
def handle_friendship_requests(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        username = data['username']
        accepted = data['accepted']

        sender = User.objects.filter(username=username).first()
        receiver = request.user

        if FriendshipRequest.objects.filter(sender=sender, receiver=receiver).first():
            if accepted:
                friendship = Friendship(user=sender, friend=receiver)
                friendship.save()
                friendship = Friendship(user=receiver, friend=sender)
                friendship.save()
                FriendshipRequest.objects.filter(sender=sender, receiver=receiver).delete()
                return JsonResponse({'status': 'success'})
            else:
                FriendshipRequest.objects.filter(sender=sender, receiver=receiver).first().delete()
                return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'description': 'friendship.errors.no-request-found'}, status=400)


@never_cache
def get_friends(request):
    if request.user.is_authenticated:
        friends = []
        for friendship in Friendship.objects.filter(user=request.user):
            if not ExtendedUser.objects.filter(user=friendship.friend).exists():
                extendedUser = ExtendedUser(user=friendship.friend)
                extendedUser.avatar_seed = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
                extendedUser.save()
            if friendship:
                data = friendship.friend.extendeduser.user_data()
                friends.append(data)
        return JsonResponse({'friends': friends})
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