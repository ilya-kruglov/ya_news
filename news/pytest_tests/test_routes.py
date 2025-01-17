from http import HTTPStatus
import pytest

from pytest_django.asserts import assertRedirects

from django.urls import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('news_id')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    )
)
def test_pages_availability_for_anonymous_user(client, name, args):
    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
@pytest.mark.parametrize(
    'user, status',
    (
        (pytest.lazy_fixture('author'), HTTPStatus.OK),
        (pytest.lazy_fixture('reader'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit')
)
def test_availability_for_comment_edit_and_delete(client, comment, name, user, status):
    client.force_login(user)
    url = reverse(name, args=(comment.pk,))
    response = client.get(url)
    assert response.status_code == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name',
    ('news:delete', 'news:edit')
)
def test_redirect_for_anonymous_client(name, comment, client):
    login_url = reverse('users:login')
    url = reverse(name, args=(comment.pk,))
    redirect_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, redirect_url)
