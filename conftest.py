import pytest

from django.urls import reverse

from news.models import Comment, News

COMMENT_TEXT = 'Текст комментария'
NEW_COMMENT_TEXT = 'Обновлённый комментарий'


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(username='Мимо Крокодил')


@pytest.fixture
def auth_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def form_data():
    return {
        'text': COMMENT_TEXT
    }


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор комментария')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def reader(django_user_model):
    return django_user_model.objects.create(username='Читатель')


@pytest.fixture
def reader_client(reader, client):
    client.force_login(reader)
    return client


@pytest.fixture
def new_form_data():
    return {
        'text': NEW_COMMENT_TEXT
    }


@pytest.fixture
def news():
    return News.objects.create(title='Заголовок', text='Текст')


@pytest.fixture
def news_id(news):
    return news.id,


@pytest.fixture
def comment(news, author):
    return Comment.objects.create(
            news=news,
            author=author,
            text=COMMENT_TEXT
    )


@pytest.fixture
def news_detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def url_to_comments(news_detail_url):
    return f'{news_detail_url}#comments'


@pytest.fixture
def comment_delete_url(news):
    return reverse('news:delete', args=(news.id,))


@pytest.fixture
def comment_edit_url(news):
    return reverse('news:edit', args=(news.id,))
