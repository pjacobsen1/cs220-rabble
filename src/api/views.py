from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rabble.models import *
from .serializers import *

@api_view(['GET'])
def subrabble_list(request):
    if request.method == 'GET':
        subrabbles = Subrabble.objects.all()
        serializer = SubrabbleSerializer(subrabbles, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_subrabble(request, subrabble_name):
    subrabble = Subrabble.objects.get(subrabble_name=subrabble_name)
    serializer = SubrabbleSerializer(subrabble)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
def subrabble_posts(request, subrabble_name):
    subrabble = Subrabble.objects.get(subrabble_name=subrabble_name)
    if request.method == 'GET':
        posts = Post.objects.filter(subrabble=subrabble)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data.copy()
        data['subrabble'] = subrabble.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def get_post(request, subrabble_name, pk):
    post = Post.objects.get(pk=pk, subrabble_name=subrabble_name)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# api/views.py
@api_view(['POST'])
def change_like(request, subrabble_name, pk):
    subrabble_name = subrabble_name.lstrip('!')
    post = Post.objects.get(pk=pk)
    username = request.data.get('user')
    user = User.objects.get(username=username)
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    
    return Response({
        'liked': liked,
        'like_count': post.likes.count()
    })