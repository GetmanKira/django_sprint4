"""
Содержит конфигурацию приложения 'pages'. 
Здесь определяется класс PagesConfig, который наследует от AppConfig 
и настраивает параметры приложения, такие как имя и тип автоматического поля.
"""


from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
