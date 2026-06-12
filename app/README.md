# Лабораторная работа 1 — готовое Flask-приложение

Что сделано:

1. Добавлен шаблон `templates/post.html` для отображения страницы поста.
2. В базовый шаблон `templates/base.html` добавлен footer с ФИО и номером группы.
3. Реализована передача данных поста из `app.py` в шаблоны.
4. Добавлены комментарии и вложенные ответы на комментарии.
5. Добавлены тесты в `tests/test_posts.py` — 20 тестов.

## Запуск приложения

```bash
cd app
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

После запуска откройте в браузере:

```text
http://127.0.0.1:5000/
http://127.0.0.1:5000/posts/1/
```

## Запуск тестов

```bash
cd app
python -m pytest tests/
```
