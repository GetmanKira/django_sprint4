"""
Содержит  URL конфигурацию проекта. Тут связываются URL-адреса с 
представлениями, а также определяется как обрабатывать  маршруты в приложении. 
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),# Главная страница блога
    path('auth/', include('django.contrib.auth.urls')),# Страницы приложения pages
    path('auth/registration/', include('users.urls')),# Регистрация
]
#Обработчики ошибок 403, 404, 500
handler403 = 'pages.views.csrf_failure'

handler404 = 'pages.views.page_not_found'

handler500 = 'pages.views.internal_error'

if settings.DEBUG:
    import debug_toolbar
    # Добавляется список адресов из приложения debug_toolbar к urlpatterns,
    # если проект находится в режиме отладки.
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
# Обработка статических файлов в режиме отладки
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
