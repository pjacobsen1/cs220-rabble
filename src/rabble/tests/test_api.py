import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rabble.models import Post
from .factories import UserFactory, CommunityFactory, SubRabbleFactory, PostFactory
from rest_framework import status


@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_subrabble_get(api_client):
    community = CommunityFactory(community_name="default")
    subrabble = SubRabbleFactory(community=community)

    response = api_client.get(reverse('get-subrabble', args=[subrabble.subrabble_name]))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["subrabble_name"] == subrabble.subrabble_name
    assert data["description"] == subrabble.description
    assert data["identifier"] == subrabble.identifier

@pytest.mark.django_db
def test_post_post(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    community = CommunityFactory(community_name="default")
    subrabble = SubRabbleFactory(community=community)

    data = {
        "user": user.username,
        "subrabble": subrabble.subrabble_name,
        "title": "I dont know what class I should take.",
        "body": "I will take Introduction to Software Development.",
        "num_likes": 7,
        "num_comments": 0
    }

    response = api_client.post(reverse('subrabble-posts', kwargs={'subrabble_name': subrabble.subrabble_name}), data)
    assert response.status_code == 201
    post = Post.objects.get(title=data['title'], body=data['body'])
    assert post.title == data["title"]
    assert post.body == data["body"]
    assert post.subrabble == subrabble

@pytest.mark.django_db
def test_post_patch(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    community = CommunityFactory(community_name="default")
    subrabble = SubRabbleFactory(community=community)
    post = PostFactory(user=user, subrabble=subrabble, title="old title")
    data = {"title": "new title"}

    response = api_client.patch(reverse('get-post', args=[subrabble.subrabble_name, post.pk]), data)
    assert response.status_code == 200
    post.refresh_from_db()
    assert post.title == data["title"]
