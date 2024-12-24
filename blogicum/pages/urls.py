"""
Содержит маршруты для приложения 'pages'. 
Определила URL-шаблоны, которые соответствуют представлениям 
страниц 'О нас' и 'Правила'. Задала пространство имен для маршрутов приложения.
"""


from django.urls import path

from . import views

app_name = 'pages' # Пространство имен для URL

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
    # URL для страницы 'О нас'
    path('rules/', views.RulesView.as_view(), name='rules'),
    # URL для страницы с правилами
]
