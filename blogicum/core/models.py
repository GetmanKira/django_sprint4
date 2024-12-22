"""
Содержит абстрактные модели для использования в других моделях приложения.
Определены модели IsPublished и CreatedAt, с помощью которых появляется возможность 
управлять статусом публикации и временем ее создания

"""


from django.db import models


class IsPublished(models.Model):
    """Модель статуса публикации."""

    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True


class CreatedAt(models.Model):
    """Модель времени создания."""

    created_at = models.DateTimeField(
        'Добавлено',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
