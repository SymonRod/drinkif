from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import CSRF_SESSION_KEY, get_token
from django.views.decorators.cache import never_cache
from django.http import JsonResponse, request
from drinkif.models import *
from drinkif.settings import BASE_DIR
import json, os, random, string, requests, hashlib, urllib

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
        phrases_list = []
        friend_phrases = phrases.objects.filter(creator__in=list(request.user.data.friends.all()) + [request.user])

        for phrase in friend_phrases:
            temp = {'phrase_text': phrase.phrase_text, 'id': phrase.id, 'creator': phrase.creator.username}
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

        return JsonResponse(request.user.data.user_data())
    else:
        return JsonResponse({'status': 'fail'}, status=403)

@never_cache
def remove_friend(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'fail'}, status=403)

    data = json.loads(request.body)
    username = data['username']

    friend = User.objects.filter(username=username).first()

    if not friend:
        return JsonResponse({'status': 'fail','description':'friends.errors.username-does-not-exits'} , status=400)

    if request.user in friend.data.friends.all():
        friend.data.friends.remove(request.user)

    if friend in request.user.data.friends.all():
        request.user.data.friends.remove(friend)
    
    return JsonResponse({'status': 'success'})


@never_cache
def new_friendship_request(request):

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'fail'}, status=403)

    data = json.loads(request.body)
    username = data['username']

    sender = request.user
    receiver = User.objects.filter(username=username).first()

    if not receiver:
        return JsonResponse({'status': 'fail', 'description': 'friends.errors.username-does-not-exists'}, status=400)

    if receiver == sender:
        return JsonResponse({'status': 'fail'}, status=400)

    if FriendshipRequest.objects.filter(sender=receiver, receiver=sender).exists():
        return JsonResponse({'status': 'fail', 'description': 'friends.errors.check-your-invoice'}, status=400)

    if FriendshipRequest.objects.filter(sender=sender, receiver=receiver).exists():
        return JsonResponse({'status': 'fail', 'description': 'friends.errors.already-requested'}, status=400)

    if sender not in receiver.data.friends.all():
        friendshiprequest = FriendshipRequest(sender=sender, receiver=receiver)
        friendshiprequest.save()
    else:
        return JsonResponse({'status': 'fail', 'description': 'friends.errors.already-friends'}, status=400)
    return JsonResponse({'status': 'success'})
    

@never_cache
def get_friendship_requests(request):
    if request.user.is_authenticated:
        requests = []
        for request in  FriendshipRequest.objects.filter(receiver=request.user):
            requests.append(request.sender.data.user_data())
        return JsonResponse({'requests': requests})

@never_cache
def handle_friendship_requests(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        username = data['username']
        accepted = data['accepted']

        sender = User.objects.filter(username=username).first()
        receiver = request.user

        friendshiprequest =  FriendshipRequest.objects.filter(sender=sender, receiver=receiver).first()

        if friendshiprequest:
            if accepted:

                if sender not in receiver.data.friends.all():
                    receiver.data.friends.add(sender)

                if receiver not in sender.data.friends.all():
                    sender.data.friends.add(receiver)

                friendshiprequest.delete()
                return JsonResponse({'status': 'success'})
            else:
                friendshiprequest.delete()
                return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'fail', 'description': 'friends.errors.no-request-found'}, status=400)


@never_cache
def get_friends(request):
    if request.user.is_authenticated:
        friends = []
        for friend in request.user.data.friends.all():
           
            if not ExtendedUser.objects.filter(user=friend).exists():
                extendedUser = ExtendedUser(user=friend)
                extendedUser.avatar_seed = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
                extendedUser.save()
           
            if friend:
                data = friend.data.user_data()
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

@never_cache
def get_TTS(request):
    sentence = request.GET.get('sentence',False)

    if not sentence:
        return JsonResponse({'status': 'fail'}, status=400)

    sentence = urllib.parse.quote(sentence)
    hash_sentence = hashlib.md5(sentence.encode('utf-8')).hexdigest()+".mp3"

    if not (os.path.isfile(os.path.join(BASE_DIR / "static/mp3" / hash_sentence))):

        req = requests.get(f"https://freetts.com/Home/PlayAudio?Language=it-IT&Voice=it-IT-Standard-A&TextMessage={sentence}&type=0")
        
        if  req.status_code == 200:
            id = json.loads(req.text)["id"]
            print(f"https://freetts.com/audio/{id}")
            mp3_req = requests.get(f"https://freetts.com/audio/{id}")
            with open(BASE_DIR / "static/mp3" / hash_sentence, 'wb') as f:
                f.write(mp3_req.content)

    return redirect(f"/static/mp3/{hash_sentence}")



    # a = input("Inserisci il testo: ")
    # a= urllib.parse.quote(a)
    # req = requests.get(f"https://freetts.com/Home/PlayAudio?Language=it-IT&Voice=it-IT-Standard-A&TextMessage={a}&type=0")
    # if  req.status_code == 200:
    #     id = json.loads(req.text)["id"]
    #     print(id)
    #     mp3_req = requests.get(f"https://freetts.com/audio/{id}")
    #     with open(id, 'wb') as f:
    #         f.write(mp3_req.content)

from gtts import gTTS

@never_cache
def gtts(request):
    sentence = request.GET.get('sentence',False)

    if not sentence:
        return JsonResponse({'status': 'fail'}, status=400)
    
    hash_sentence = hashlib.md5(sentence.encode('utf-8')).hexdigest()+".mp3"

    if not (os.path.isfile(os.path.join(BASE_DIR / "static/mp3" / hash_sentence))):
        tts = gTTS(text=sentence, lang='it')
        tts.save(BASE_DIR / "static/mp3" / hash_sentence)

    return redirect(f"/static/mp3/{hash_sentence}")