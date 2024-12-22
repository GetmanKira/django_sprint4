"""содержит конфигурацию приложения
используется для определения параметров, связанных с приложением
 """
from django.apps import AppConfig

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Блог'
