from rest_framework import serializers
from rabble.models import *

class SubrabbleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subrabble
        fields = ['community', 'subrabble_name', 'description', 'is_public', 'num_posts', 'num_comments', 'allow_anon']

class PostSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='user', queryset=User.objects.all())
    subrabble = serializers.SlugRelatedField(slug_field='subrabble_name', queryset=Subrabble.objects.all())
    class Meta:
        model = Post
        fields = ['user', 'subrabble', 'title', 'body', 'num_likes', 'num_comments']