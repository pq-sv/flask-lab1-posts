from datetime import datetime
from flask import Flask, abort, render_template

app = Flask(__name__)

POSTS = [
    {
        "id": 1,
        "title": "Первый пост в учебном блоге",
        "author": "Святослав Кононов",
        "published_at": datetime(2026, 3, 12, 10, 30),
        "image": "img/post-1.svg",
        "image_alt": "Иллюстрация к первому посту",
        "text": (
            "Это пример страницы поста для лабораторной работы. "
            "Все основные данные — заголовок, автор, дата публикации, "
            "изображение, текст и комментарии — передаются в шаблон из приложения."
        ),
        "comments": [
            {
                "id": 1,
                "author": "Анна",
                "text": "Очень полезный пост, всё понятно описано.",
                "replies": [
                    {
                        "id": 2,
                        "author": "Святослав Кононов",
                        "text": "Спасибо! Рад, что материал оказался полезным.",
                        "replies": [],
                    }
                ],
            },
            {
                "id": 3,
                "author": "Иван",
                "text": "Интересно посмотреть продолжение темы.",
                "replies": [
                    {
                        "id": 4,
                        "author": "Мария",
                        "text": "Согласна, формат страницы удобный.",
                        "replies": [],
                    }
                ],
            },
        ],
    },
    {
        "id": 2,
        "title": "Заметка о Flask-шаблонах",
        "author": "Святослав Кононов",
        "published_at": datetime(2026, 3, 22, 18, 15),
        "image": "img/post-2.svg",
        "image_alt": "Иллюстрация о шаблонах Flask",
        "text": (
            "Шаблоны позволяют отделить HTML-разметку от логики приложения. "
            "Такой подход делает проект понятнее, а тесты помогают проверить, "
            "что на страницу попадают нужные данные."
        ),
        "comments": [
            {
                "id": 5,
                "author": "Павел",
                "text": "Теперь стало понятнее, зачем нужен base.html.",
                "replies": [],
            }
        ],
    },
]


@app.template_filter("post_date")
def post_date(value: datetime) -> str:
    """Return publication date in the format required by the tests: DD.MM.YYYY."""
    return value.strftime("%d.%m.%Y")


def get_post_or_404(post_id: int) -> dict:
    for post in POSTS:
        if post["id"] == post_id:
            return post
    abort(404)


@app.get("/")
def index():
    return render_template("index.html", posts=POSTS)


@app.get("/posts/<int:post_id>/")
def post_detail(post_id: int):
    post = get_post_or_404(post_id)
    return render_template("post.html", post=post)


if __name__ == "__main__":
    app.run(debug=True)
