from django.db import models
from django.contrib.auth.models import AbstractUser
 
class User(AbstractUser):
  profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
  bio = models.TextField(blank=True, null=True)
  interests = models.TextField(blank=True, null=True)

  class Meta:
    unique_together = ['username', 'email']

class Following(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
  following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

class Community(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  community_name = models.TextField()

class CommunityMember(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  community = models.ForeignKey(Community, on_delete=models.CASCADE)
  is_admin = models.BooleanField(default=False)

class Subrabble(models.Model):
  community = models.ForeignKey(Community, on_delete=models.CASCADE)
  subrabble_name = models.TextField(unique=True)
  description = models.TextField()
  is_public = models.BooleanField()
  num_posts = models.PositiveIntegerField(default=0)
  num_comments = models.PositiveIntegerField(default=0)
  allow_anon = models.BooleanField()
 
class SubrabbleMember(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  subrabble = models.ForeignKey(Subrabble, on_delete=models.CASCADE)

class Post(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  subrabble = models.ForeignKey(Subrabble, on_delete=models.CASCADE)
  title = models.TextField()
  body = models.TextField()
  num_likes = models.PositiveIntegerField(default=0)
  num_comments = models.PositiveIntegerField(default=0)
 
class Comment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  post = models.ForeignKey(Post, on_delete=models.CASCADE)
  body = models.TextField()
  num_likes = models.PositiveIntegerField(default=0)
  num_replies = models.PositiveIntegerField(default=0)
 
class Reply(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
  body = models.TextField()
  num_likes = models.PositiveIntegerField(default=0)

class Conversation(models.Model):
  title = models.TextField()

class ConversationMember(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
  
class ConversationMessage(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
  body = models.TextField()

class CommunityInvite(models.Model):
  community = models.ForeignKey(Community, on_delete=models.CASCADE)
  email = models.EmailField(unique=True)
 
