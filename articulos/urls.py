from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

app_name = "articulos"

urlpatterns = [
    path("", views.lista_articulos, name="lista_articulos"),
    path(_("crear/"), views.crear_articulo, name="crear_articulo"),
    path(_("<int:pk>/editar/"), views.editar_articulo, name="editar_articulo"),
    path(_("<int:pk>/eliminar/"), views.eliminar_articulo, name="eliminar_articulo"),
    path(_("tipos-cambio/"), views.detalle_tipos_cambio, name="detalle_tipos_cambio"),
    path(_("algoritmo-kafe-kean/"), views.vista_kafe_kean, name="vista_kafe_kean"),
    path(_("cambiar_idioma/<str:idioma>/"), views.cambiar_idioma, name="cambiar_idioma"),
    path(_("preguntas-frecuentes/"), views.preguntas_frecuentes, name="preguntas_frecuentes"),
    path(_("contactanos/"), views.contactanos, name="contactanos"),
    path(_("registro/"), views.registro, name="registro"),
    path(_("login/"), views.CustomLoginView.as_view(), name="login"),
    path(_("logout/"), views.CustomLogoutView.as_view(), name="logout"),
    path(
        _("password_reset/"),
        auth_views.PasswordResetView.as_view(template_name="articulos/password_reset.html"),
        name="password_reset",
    ),
    path(
        _("password_reset/done/"),
        auth_views.PasswordResetDoneView.as_view(template_name="articulos/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        _("reset/<uidb64>/<token>/"),
        auth_views.PasswordResetConfirmView.as_view(template_name="articulos/password_reset_confirm.html"),
        name="password_reset_confirm",
    ),
    path(
        _("reset/done/"),
        auth_views.PasswordResetCompleteView.as_view(template_name="articulos/password_reset_complete.html"),
        name="password_reset_complete",
    ),
    path(_("<slug:slug>/"), views.detalle_articulo, name="detalle_articulo"),
]

if settings.DEBUG:
    urlpatterns += [
        path("debug/headers/", views.debug_headers, name="debug_headers"),
    ]
