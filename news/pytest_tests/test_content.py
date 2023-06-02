from datetime import timedelta

from django.conf import settings
from django.utils import timezone

import pytest

from news.models import Comment


@pytest.mark.django_db
def test_news_count(client, home_url, all_news):
    response = client.get(home_url)
    object_list = response.context['object_list']
    news_count = len(object_list)
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
def test_news_order(client, home_url, all_news):
    response = client.get(home_url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comments_order(client, news_detail_url, news, author):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Tекст {index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    response = client.get(news_detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.django_db
def test_anonymous_client_has_no_form(client, news_detail_url):
    response = client.get(news_detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(auth_client, news_detail_url):
    response = auth_client.get(news_detail_url)
    assert 'form' in response.context
