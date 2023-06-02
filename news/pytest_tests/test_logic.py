from http import HTTPStatus
import pytest

from pytest_django.asserts import assertRedirects, assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.django_db
def test_anonymous_user_cant_create_comment(client, form_data, news_detail_url):
    client.post(news_detail_url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(auth_client, user, form_data, news, news_detail_url, url_to_comments):
    response = auth_client.post(news_detail_url, data=form_data)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.text == form_data['text']
    assert comment.news == news
    assert comment.author == user


def test_user_cant_use_bad_words(auth_client, news_detail_url):
    bad_words_data = {'text': f'Какой-то текст, {BAD_WORDS[0]}, еще текст'}
    response = auth_client.post(news_detail_url, data=bad_words_data)
    assertFormError(
        response,
        form='form',
        field='text',
        errors=WARNING
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, comment, url_to_comments, comment_delete_url):
    response = author_client.delete(comment_delete_url)
    assertRedirects(response, url_to_comments)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_edit_comment(author_client, new_form_data, comment, url_to_comments, comment_edit_url):
    response = author_client.post(comment_edit_url, data=new_form_data)
    assertRedirects(response, url_to_comments)
    comment.refresh_from_db()
    assert comment.text == new_form_data['text']


def test_user_cant_delete_comment_of_another_user(reader_client, comment, comment_delete_url):
    response = reader_client.delete(comment_delete_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comments_count = Comment.objects.count()
    assert comments_count == 1


def test_user_cant_edit_comment_of_another_user(reader_client, new_form_data, comment, comment_edit_url):
    response = reader_client.post(comment_edit_url, data=new_form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_text = comment.text
    comment.refresh_from_db()
    assert comment.text == comment_text
