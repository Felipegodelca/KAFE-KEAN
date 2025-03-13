from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import views as auth_views
from . import views

# ==========================
# 🌐 Espacio de Nombres
# ==========================
app_name = 'articulos'

# ==========================
# 🛠️ Rutas de la Aplicación
# ==========================
urlpatterns = [
    # 📄 Página principal: Lista de artículos
    path('', views.lista_articulos, name='lista_articulos'),
    path('<int:pk>/', views.detalle_articulo, name='detalle_articulo'),

    # 📝 Crear un nuevo artículo
    path(_('crear/'), views.crear_articulo, name='crear_articulo'),

    # 🛠️ Editar un artículo
    path('<int:pk>/editar/', views.editar_articulo, name='editar_articulo'),

    # 🗑️ Eliminar un artículo
    path('<int:pk>/eliminar/', views.eliminar_articulo, name='eliminar_articulo'),

    # 🌍 Cambio de idioma
    path(_('cambiar_idioma/<str:idioma>/'), views.cambiar_idioma, name='cambiar_idioma'),

    # 🌟 Preguntas frecuentes y contacto
    path(_('preguntas-frecuentes/'), views.preguntas_frecuentes, name='preguntas_frecuentes'),
    path(_('contactanos/'), views.contactanos, name='contactanos'),

    # 🚀 Algoritmo de KAFE KEAN
    path(_('ejecutar_algoritmo/'), views.ejecutar_algoritmo, name='ejecutar_algoritmo'),
]

# 🔑 Autenticación y Registro
auth_patterns = [
    path(_('registro/'), views.registro, name='registro'),
    path(_('login/'), views.CustomLoginView.as_view(), name='login'),
    path(_('logout/'), views.CustomLogoutView.as_view(), name='logout'),

    # 🔐 Recuperación de contraseña
    path(_('password_reset/'), auth_views.PasswordResetView.as_view(
        template_name='articulos/password_reset.html'), name='password_reset'),
    
    path(_('password_reset/done/'), auth_views.PasswordResetDoneView.as_view(
        template_name='articulos/password_reset_done.html'), name='password_reset_done'),
    
    path(_('reset/<uidb64>/<token>/'), auth_views.PasswordResetConfirmView.as_view(
        template_name='articulos/password_reset_confirm.html'), name='password_reset_confirm'),
    
    path(_('reset/done/'), auth_views.PasswordResetCompleteView.as_view(
        template_name='articulos/password_reset_complete.html'), name='password_reset_complete'),
]

urlpatterns += auth_patterns

# 🛡️ Depuración (solo en modo DEBUG)
from django.conf import settings
if settings.DEBUG:
    urlpatterns += [
        path('debug/headers/', views.debug_headers, name='debug_headers'),
    ]