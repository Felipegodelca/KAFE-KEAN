from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from articulos import views

# ==========================
# 🌐 URLs PRINCIPALES
# ==========================
urlpatterns = [
    # 🛠️ Administración
    path('admin/', admin.site.urls),

    # 🏠 Página de inicio
    path('', views.inicio, name='inicio'),

    # 📚 Artículos (Rutas específicas de la app)
    path('articulos/', include('articulos.urls', namespace='articulos')),

    # 🌍 Cambio de idioma
    path('cambiar_idioma/<str:idioma>/', views.cambiar_idioma, name='cambiar_idioma'),

    # 🔑 Autenticación con Django-Allauth
    path('accounts/', include('allauth.urls')),
]

# ==========================
# 🛠️ MANEJO DE ARCHIVOS ESTÁTICOS Y MEDIOS
# ==========================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ==========================
# 🛠️ MANEJO DE ERRORES
# ==========================
handler404 = 'articulos.views.custom_404_view'
handler500 = 'articulos.views.custom_500_view'