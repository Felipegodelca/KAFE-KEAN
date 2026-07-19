from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from articulos import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.inicio, name="inicio"),
    path("articulos/", include("articulos.urls", namespace="articulos")),
]

handler404 = "articulos.views.custom_404_view"
handler500 = "articulos.views.custom_500_view"

if settings.DEBUG:
    urlpatterns += [
        path("debug/headers/", views.debug_headers, name="debug_headers"),
    ]
