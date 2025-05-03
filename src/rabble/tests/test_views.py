import pytest
from django.urls import reverse
from rabble.models import Post
from .factories import UserFactory, CommunityFactory, SubRabbleFactory, PostFactory, CommentFactory

@pytest.mark.django_db
def test_index_view(client):
    community = CommunityFactory(community_name="default")
    subrabbles = SubRabbleFactory.create_batch(6, community=community)

    response = client.get(reverse('index'))
    assert 'subrabbles' in response.context
    assert len(response.context['subrabbles']) == len(subrabbles)
    assert response.status_code == 200

    html = response.content.decode()
    for subrabble in subrabbles:
        assert subrabble.subrabble_name in html

@pytest.mark.django_db
def test_subrabble_detail_view(client):
    community = CommunityFactory(community_name="default")
    subrabble = SubRabbleFactory(community=community)
    posts = PostFactory.create_batch(6, subrabble=subrabble)

    for post in posts:
        CommentFactory.create_batch(2, post=post)

    response = client.get(reverse('subrabble_detail', args=[subrabble.identifier]))
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
    subrabble = SubRabbleFactory(community=community)

    post = {
        'title': 'post title',
        'body': 'body of the post',
        'subrabble': subrabble.id,
    }

    response = client.post(reverse('post_create', args=[subrabble.identifier]), data=post, follow=True)

    assert response.status_code == 200
    post_exists = Post.objects.filter(title='post title', subrabble=subrabble).exists()
    assert post_exists
