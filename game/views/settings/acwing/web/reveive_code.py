import json
from django.shortcuts import redirect
from django.core.cache import cache
import requests
from django.contrib.auth.models import User
from game.models.player.player import Player
from django.contrib.auth import login
from random import randint


def receive_code(request):
    data = request.GET
    code = data.get("code")
    state = data.get("state")

    if not cache.has_key(state):
        return redirect("index")

    cache.delete(state)

    apply_access_token_url = "https://www.acwing.com/third_party/api/oauth2/access_token/"
    params = {
        'appid': "2243",
        'secret': "7bb756052c2543a496a2da95438ae86e",
        'code': code,
    }
    access_token_resp = requests.get(apply_access_token_url, params=params).json()
    access_token = access_token_resp['access_token']
    openid = access_token_resp['openid']

    players = Player.objects.filter(openid=openid)
    if players.exists():
        login(request, players[0].user)
        return redirect("index")

    get_userinfo_url = "https://www.acwing.com/third_party/api/meta/identity/getinfo/"
    params = {
        'access_token': access_token,
        'openid': openid,
    }
    userinfo_resp = requests.get(get_userinfo_url, params=params).json()
    if 'error_code' in userinfo_resp:
        return redirect("index")
    username = userinfo_resp['username']
    photo = userinfo_resp['photo']
    
    while User.objects.filter(username=username).exists():
        username += str(randint(0, 9))
    user = User.objects.create(username=username)
    player = Player.objects.create(user=user, photo=photo, openid=openid)
    login(request, user)

    return redirect("index")