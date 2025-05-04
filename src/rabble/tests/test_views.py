import pytest
from django.urls import reverse
from rabble.models import Post
from .factories import UserFactory, CommunityFactory, SubRabbleFactory, PostFactory, CommentFactory

@pytest.mark.django_db
def test_index_view(client):
    community = CommunityFactory(community_name="default")
    subrabble1 = SubRabbleFactory.create(community=community, subrabble_name="subrabble1")
    subrabble2 = SubRabbleFactory.create(community=community, subrabble_name="subrabble2")
    subrabble3 = SubRabbleFactory.create(community=community, subrabble_name="subrabble3")
    subrabble4 = SubRabbleFactory.create(community=community, subrabble_name="subrabble4")
    subrabble5 = SubRabbleFactory.create(community=community, subrabble_name="subrabble5")
    user = UserFactory()
    client.force_login(user)

    response = client.get(reverse('index'))
    assert 'subrabbles' in response.context
    assert response.status_code == 200

    html = response.content.decode()
    assert subrabble1.subrabble_name in html
    assert subrabble2.subrabble_name in html
    assert subrabble3.subrabble_name in html
    assert subrabble4.subrabble_name in html
    assert subrabble5.subrabble_name in html

@pytest.mark.django_db
def test_subrabble_detail_view(client):
    community = CommunityFactory(community_name="default")
    subrabble = SubRabbleFactory(community=community, subrabble_name="subrabble")
    posts = PostFactory.create_batch(6, subrabble=subrabble)
    user = UserFactory()
    client.force_login(user)

    for post in posts:
        CommentFactory.create_batch(2, post=post)

    response = client.get(reverse('subrabble-detail', args=[subrabble.subrabble_name]))
    assert response.status_code == 200
    
    html = response.content.decode()
    for post in posts:
        assert post.title in html
    assert 'posts' in response.context
    for post in response.context['posts']:
        assert post.comment_set.count() == 2

@pytest.mark.django_db
def test_post_create_view(client):
    user = UserFactory()
    client.force_login(user)
    community = CommunityFactory(community_name = "default")
    subrabble = SubRabbleFactory(community=community, subrabble_name="subrabble")

    data = {
        "user": user.username,
        "subrabble": subrabble.subrabble_name,
        "title": "post titleeeeeee",
        "body": "post bodyyyyy",
        "num_likes": 7,
        "num_comments": 0
    }

    response = client.post(reverse('post-create', args=[subrabble.subrabble_name]), data=data, follow=True)
    assert response.status_code == 200
    
    post = Post.objects.latest('id')
    assert post.subrabble == subrabble
    assert post.title == data['title']
    assert post.body == data['body']
