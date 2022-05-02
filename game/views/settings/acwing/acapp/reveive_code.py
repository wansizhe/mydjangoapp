from django.http import JsonResponse
from django.core.cache import cache
import requests
from django.contrib.auth.models import User
from game.models.player.player import Player
from random import randint


def receive_code(request):
    data = request.GET

    if 'errcode' in data:
        return JsonResponse({
            'result': "apply_failed",
            'errcode': data['errcode'],
            'errmsg': data['errmsg'],
        })

    code = data.get("code")
    state = data.get("state")

    if not cache.has_key(state):
        return JsonResponse({
            'result': "state_not_exists",
        })

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
        player = players[0];
        return JsonResponse({
            'result': "success",
            'username': player.user.username,
            'photo': player.photo,
        })

    get_userinfo_url = "https://www.acwing.com/third_party/api/meta/identity/getinfo/"
    params = {
        'access_token': access_token,
        'openid': openid,
    }
    userinfo_resp = requests.get(get_userinfo_url, params=params).json()
    if 'errcode' in userinfo_resp:
        return JsonResponse({
            'result': "get_userinfo_failed",
            'errcode': userinfo_resp['errcode'],
            'errmsg': userinfo_resp['errmsg'],
        })
    username = userinfo_resp['username']
    photo = userinfo_resp['photo']
    
    while User.objects.filter(username=username).exists():
        username += str(randint(0, 9))
    user = User.objects.create(username=username)
    player = Player.objects.create(user=user, photo=photo, openid=openid)

    return JsonResponse({
        'result': "success",
        'username': player.user.username,
        'photo': player.photo,
    })
