# cryptogugu/src/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # Включаем стандартные URL для изменения языка
]

urlpatterns += i18n_patterns(
    path("", include("app.urls")),  # Включаем приложение 'app'
    # Добавьте другие включения и пути по необходимости
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
