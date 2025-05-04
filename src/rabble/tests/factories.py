from factory import Sequence, Faker, SubFactory
from factory.django import DjangoModelFactory
from rabble.models import User, Community, Subrabble, Post, Comment
import string
import factory

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    username = Faker('lexify', text='????????', letters=string.ascii_lowercase)
    email = Faker('lexify', text='???????@example.com', letters=string.ascii_lowercase)
    profile_pic = None
    bio = None
    interests = None

class CommunityFactory(DjangoModelFactory):
    class Meta:
        model = Community
    user = SubFactory(UserFactory)
    community_name = Faker('sentence', nb_words=2)

class SubRabbleFactory(DjangoModelFactory):
    class Meta:
        model = Subrabble
    identifier = Faker('lexify', text='????????', letters=string.ascii_lowercase)
    community = SubFactory(CommunityFactory)
    subrabble_name = Faker('sentence', nb_words=2)
    description = Faker('paragraph', nb_sentences=2)
    is_public = True
    num_posts = 0
    num_comments = 0
    allow_anon = False

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
    user = SubFactory(UserFactory)
    subrabble = SubFactory(SubRabbleFactory)
    title = Faker('sentence', nb_words=4)
    body = Faker('paragraph', nb_sentences=3)
    num_likes = 0
    num_comments = 0

class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment
    user = SubFactory(UserFactory)
    post = SubFactory(PostFactory)
    body = Faker('sentence', nb_words=10)
    num_likes = 0
    num_replies = 0