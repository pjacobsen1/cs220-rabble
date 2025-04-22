from django.shortcuts import render
from django.http import HttpResponse
from .models import Subrabble, Post, Comment
from .forms import PostForm
from django.shortcuts import redirect, reverse
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        subrabbles = Subrabble.objects.all()
        return render(request, "rabble/index.html", {"subrabbles": subrabbles})
    else:
        return render(request, "rabble/not_logged_in.html")
    
@login_required
def profile(request):
    print("Profile view called!")  # Debugging line
    return render(request, 'rabble/profile.html', {
        'username': request.user.username,
        'email': request.user.email,
    })

@login_required
def subrabble_detail(request, subrabble_name):
    subrabble = Subrabble.objects.get(subrabble_name=subrabble_name)
    posts = Post.objects.filter(subrabble=subrabble)
    return render(request, "rabble/subrabble_detail.html", {
        "subrabble": subrabble,
        "posts": posts,
    })

@login_required
def post_detail(request, subrabble_name, pk):
    subrabble = Subrabble.objects.get(subrabble_name=subrabble_name)
    post = Post.objects.get(pk=pk, subrabble=subrabble)
    comments = Comment.objects.filter(post=post)
    
    return render(request, "rabble/post_detail.html", {
        "subrabble": subrabble,
        "post": post,
        "comments": comments,
    })

@login_required
def post_create(request, subrabble_name):
    subrabble = Subrabble.objects.get(subrabble_name=subrabble_name)

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.subrabble = subrabble
            post.user = request.user
            post.save()
            return redirect('post-detail', subrabble_name=subrabble_name, pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'rabble/post_form.html', {
        'form': form,
        'subrabble': subrabble,
        'is_editing': False,
    })

@login_required
def post_edit(request, subrabble_name, pk):
    subrabble = Subrabble.objects.get(subrabble_name=subrabble_name)
    post = Post.objects.get(pk=pk, subrabble=subrabble)
    
    if post.user == request.user:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post-detail', subrabble_name=subrabble_name, pk=post.pk)
        else:
            form = PostForm(instance=post)

        return render(request, 'rabble/post_form.html', {
            'form': form,
            'subrabble': subrabble,
            'is_editing': True,
        })
