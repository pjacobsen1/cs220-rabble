import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rabble.models import Post
from .factories import UserFactory, CommunityFactory, SubRabbleFactory, PostFactory

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_subrabble_get(api_client):
    community = CommunityFactory(community_name="default")
    subrabble = SubRabbleFactory(community=community)

    response = api_client.get(reverse('get-subrabble', args=[subrabble.identifier]))
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
        "title": "test post",
        "body": "body of post"
    }

    response = api_client.post(reverse('get-post', args=[subrabble.identifier]), data)
    assert response.status_code == 201
    post = Post.objects.get(pk=response.data['id'])
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

    response = api_client.patch(reverse('get-post', args=[subrabble.identifier, post.pk]), data)
    assert response.status_code == 200
    post.refresh_from_db()
    assert post.title == data["title"]