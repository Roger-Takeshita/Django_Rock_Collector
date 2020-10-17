from django.shortcuts import render
from django.http import HttpResponse

class Rock:
    def __init__(self, name, type, description, age):
        self.name = name
        self.type = type
        self.description = description
        self.age = age

rocks = [
    Rock('Rock 1', 'Rock 1 Name', 'Rock 1 Description', 3),
    Rock('Rock 2', 'Rock 2 Name', 'Rock 1 Description', 0),
    Rock('Rock 3', 'Rock 3 Name', 'Rock 1 Description', 4)
]

def home(request):
    return HttpResponse('<h1>Hello World</h1>')

def about(request):
    return render(request, 'about.html')

def rocks_index(request):
    return render(request, 'rocks/index.html', { 'rocks': rocks })