from contextlib import contextmanager

import pytest
from flask import template_rendered

from app import POSTS, app


@contextmanager
def captured_templates(flask_app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, flask_app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, flask_app)


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_index_page_uses_index_template(client):
    with captured_templates(app) as templates:
        response = client.get("/")

    assert response.status_code == 200
    assert templates[0][0].name == "index.html"


def test_post_page_uses_post_template(client):
    with captured_templates(app) as templates:
        response = client.get("/posts/1/")

    assert response.status_code == 200
    assert templates[0][0].name == "post.html"


def test_index_template_gets_posts_list(client):
    with captured_templates(app) as templates:
        client.get("/")

    context = templates[0][1]
    assert "posts" in context
    assert context["posts"] == POSTS


def test_post_template_gets_post_object(client):
    with captured_templates(app) as templates:
        client.get("/posts/1/")

    context = templates[0][1]
    assert "post" in context
    assert context["post"]["id"] == 1


def test_post_context_contains_all_required_fields(client):
    with captured_templates(app) as templates:
        client.get("/posts/1/")

    post = templates[0][1]["post"]
    expected_fields = {
        "id",
        "title",
        "author",
        "published_at",
        "image",
        "image_alt",
        "text",
        "comments",
    }
    assert expected_fields.issubset(post.keys())


def test_post_response_has_success_status(client):
    response = client.get("/posts/1/")

    assert response.status_code == 200


def test_post_title_is_rendered(client):
    response = client.get("/posts/1/")

    assert "Первый пост в учебном блоге" in response.get_data(as_text=True)


def test_post_author_is_rendered(client):
    response = client.get("/posts/1/")

    assert "Святослав Кононов" in response.get_data(as_text=True)


def test_post_text_is_rendered(client):
    response = client.get("/posts/1/")

    page = response.get_data(as_text=True)
    assert "Это пример страницы поста для лабораторной работы" in page


def test_post_image_is_rendered(client):
    response = client.get("/posts/1/")

    page = response.get_data(as_text=True)
    assert "img/post-1.svg" in page
    assert "Иллюстрация к первому посту" in page


def test_publication_date_has_correct_format(client):
    response = client.get("/posts/1/")

    page = response.get_data(as_text=True)
    assert "12.03.2026" in page
    assert "2026-03-12T10:30:00" in page


def test_comment_form_title_is_rendered(client):
    response = client.get("/posts/1/")

    assert "Оставьте комментарий" in response.get_data(as_text=True)


def test_comment_form_has_textarea(client):
    response = client.get("/posts/1/")

    page = response.get_data(as_text=True)
    assert '<textarea id="comment-text" name="text"' in page


def test_comment_form_has_submit_button(client):
    response = client.get("/posts/1/")

    page = response.get_data(as_text=True)
    assert 'type="submit"' in page
    assert "Отправить" in page


def test_comments_are_rendered(client):
    response = client.get("/posts/1/")

    page = response.get_data(as_text=True)
    assert "Анна" in page
    assert "Очень полезный пост, всё понятно описано." in page
    assert "Иван" in page
    assert "Интересно посмотреть продолжение темы." in page


def test_comment_replies_are_rendered(client):
    response = client.get("/posts/1/")

    page = response.get_data(as_text=True)
    assert "Спасибо! Рад, что материал оказался полезным." in page
    assert "Согласна, формат страницы удобный." in page


def test_footer_is_rendered_on_index_page(client):
    response = client.get("/")

    page = response.get_data(as_text=True)
    assert "Кононов Святослав" in page
    assert "241-371" in page


def test_footer_is_rendered_on_post_page(client):
    response = client.get("/posts/1/")

    page = response.get_data(as_text=True)
    assert "Кононов Святослав, группа 241-371" in page


def test_second_post_can_be_rendered(client):
    response = client.get("/posts/2/")

    page = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Заметка о Flask-шаблонах" in page
    assert "22.03.2026" in page


def test_nonexistent_post_returns_404(client):
    response = client.get("/posts/999/")

    assert response.status_code == 404
