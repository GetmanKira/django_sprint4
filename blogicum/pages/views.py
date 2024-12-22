"""
Файл содержит представления для страниц веб-приложения. 
Здесь определены классы и функции для обработки запросов к статическим страницам, 
таким как 'О нас' и 'Правила', а также обработчики ошибок для различных статусов HTTP
"""


from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    """Представление для страницы 'О нас'."""
    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Представление для страницы с правилами."""
    template_name = 'pages/rules.html'


def page_not_found(request, *args, **kwargs):
    """Обработчик для страницы 404 (Не найдено)."""
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, *args, **kwargs):
    """Обработчик для ошибки CSRF (403)."""
    return render(request, 'pages/403csrf.html', status=403)


def internal_error(request, *args, **kwargs):
    """Обработчик для внутренней ошибки сервера (500)."""
    return render(request, 'pages/500.html', status=500)
