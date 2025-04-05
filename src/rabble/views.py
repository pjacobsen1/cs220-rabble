from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    context = {"welcome": "Hello, world!"}

    return render(request, "rabble/index.html", context)

def profile(request):
  print("Profile view called!")  # Debugging line
  return render(request, 'rabble/profile.html', {
        'username': request.user.username,
        'email': request.user.email,
    })
