import logging

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import activate, gettext_lazy as _

from .algoritmos.kafe_kean import calcular_esfuerzo, ejecutar_q_learning
from .forms import ArticuloForm
from .models import Articulo

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    template_name = "articulos/login.html"
    redirect_authenticated_user = True
    next_page = "/"


class CustomLogoutView(LogoutView):
    next_page = "/"

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect(self.next_page)


def custom_404_view(request, exception):
    return render(request, "articulos/404.html", status=404)


def custom_500_view(request):
    return render(request, "articulos/500.html", status=500)


def debug_headers(request):
    headers = {key: value for key, value in request.META.items() if key.startswith("HTTP_")}
    return JsonResponse(headers)


def cambiar_idioma(request, idioma):
    idiomas_permitidos = ["es", "en", "de"]
    if idioma not in idiomas_permitidos:
        messages.error(request, _("Idioma no soportado."))
        return redirect("inicio")

    activate(idioma)
    request.session["django_language"] = idioma
    messages.success(request, _("Idioma cambiado exitosamente."))
    return redirect("inicio")


def obtener_imagen_inspiradora():
    if not getattr(settings, "UNSPLASH_ACCESS_KEY", None):
        return "img/fondo.svg"

    url = "https://api.unsplash.com/photos/random"
    headers = {"Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"}
    params = {"query": "resilience", "orientation": "landscape", "count": 1}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data:
            return data[0].get("urls", {}).get("regular") or "img/fondo.svg"
    except requests.RequestException as exc:
        logger.warning("Error al obtener imagen de Unsplash: %s", exc)
    return "img/fondo.svg"


def _homepage_algorithm_context(request):
    proposito = _safe_number(request.session.get("proposito", 5), 5)
    progreso = _safe_number(request.session.get("progreso", 5), 5)
    mejor_accion = None
    esfuerzo_final = None

    try:
        q_table, _recompensas, estado_final = ejecutar_q_learning()
        mejor_accion = q_table.mean().idxmax() if not q_table.empty else None
        esfuerzo_final = calcular_esfuerzo(*estado_final) if estado_final else calcular_esfuerzo(proposito, progreso)
    except Exception as exc:
        logger.warning("Error en algoritmo de inicio: %s", exc)
        esfuerzo_final = calcular_esfuerzo(proposito, progreso)

    progreso_clamped = max(0, min(10, progreso))
    progreso_altura = round(progreso_clamped * 18, 2)
    progreso_y = round(190 - progreso_altura, 2)

    return {
        "proposito": proposito,
        "progreso": progreso,
        "mejor_accion": mejor_accion,
        "esfuerzo_final": esfuerzo_final,
        "progreso_y": progreso_y,
        "progreso_altura": progreso_altura,
    }


def _safe_number(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _tipos_de_cambio_demo():
    return [
        {"currency": "USD", "buy": 17.92, "sell": 18.38, "variation": 0.24},
        {"currency": "EUR", "buy": 20.83, "sell": 21.42, "variation": -0.18},
        {"currency": "CAD", "buy": 13.12, "sell": 13.56, "variation": 0},
    ]


def inicio(request):
    contexto = {
        "imagen_inspiradora": obtener_imagen_inspiradora(),
        "articulos": Articulo.objects.all().order_by("-fecha_publicacion")[:5],
        "tipos_de_cambio": _tipos_de_cambio_demo(),
    }
    contexto.update(_homepage_algorithm_context(request))
    return render(request, "articulos/inicio.html", contexto)


def lista_articulos(request):
    articulos = Articulo.objects.all().order_by("-fecha_publicacion")
    return render(request, "articulos/lista_articulos.html", {"articulos": articulos})


def detalle_articulo(request, slug):
    articulo = get_object_or_404(Articulo, slug=slug)
    return render(request, "articulos/detalle_articulo.html", {"articulo": articulo})


def crear_articulo(request):
    if request.method == "POST":
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Artículo creado exitosamente."))
            return redirect("articulos:lista_articulos")
        messages.error(request, _("Hubo un error al crear el artículo."))
    else:
        form = ArticuloForm()
    return render(request, "articulos/crear_articulo.html", {"form": form})


def editar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    if request.method == "POST":
        form = ArticuloForm(request.POST, request.FILES, instance=articulo)
        if form.is_valid():
            form.save()
            messages.success(request, _("Artículo actualizado exitosamente."))
            return redirect("articulos:detalle_articulo", slug=articulo.slug)
    else:
        form = ArticuloForm(instance=articulo)
    return render(request, "articulos/editar_articulo.html", {"form": form, "articulo": articulo})


def eliminar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    if request.method == "POST":
        articulo.delete()
        messages.success(request, _("Artículo eliminado exitosamente."))
        return redirect("articulos:lista_articulos")
    return render(request, "articulos/eliminar_articulo.html", {"articulo": articulo})


def detalle_tipos_cambio(request):
    return render(request, "articulos/detalle_tipos_cambio.html", {"tipos_de_cambio": _tipos_de_cambio_demo()})


def preguntas_frecuentes(request):
    return render(request, "articulos/preguntas_frecuentes.html")


def contactanos(request):
    if request.method == "POST":
        messages.success(request, _("Gracias por contactarnos. Responderemos pronto."))
        return redirect("articulos:contactanos")
    return render(request, "articulos/contactanos.html")


def registro(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, _("Cuenta creada exitosamente. Ahora puedes iniciar sesión."))
        return redirect("articulos:login")
    return render(request, "articulos/registro.html", {"form": form})


def vista_kafe_kean(request):
    try:
        q_table, recompensas_totales, estado_final = ejecutar_q_learning()
        mejor_accion = q_table.mean().idxmax() if not q_table.empty else None
        esfuerzo_final = calcular_esfuerzo(*estado_final) if estado_final else None
    except Exception as exc:
        logger.warning("Error en algoritmo KAFE KEAN: %s", exc)
        mejor_accion = None
        esfuerzo_final = None
        recompensas_totales = []

    return render(
        request,
        "articulos/vista_kafe_kean.html",
        {
            "mejor_accion": mejor_accion,
            "esfuerzo_final": esfuerzo_final,
            "recompensas": recompensas_totales[-80:],
        },
    )
