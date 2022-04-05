from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    line1 = '<h1 style="text-align: center">Home Page</h1>'
    line2 = '<a href="/play/">play game</a>'
    return HttpResponse(line1 + line2)

def play(request):
    line1 = '<h1 style="text-align: center">Play Game</h1>'
    line2 = '<a href="/">home</a>'
    return HttpResponse(line1 + line2)
