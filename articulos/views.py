import os
import requests
import logging
import openai  # Asegúrate de instalarlo con `pip install openai`
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import activate, gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import JsonResponse
from django.conf import settings

from .models import Articulo
from .forms import ArticuloForm
from .kafe_kean import ejecutar_q_learning, calcular_esfuerzo  # Algoritmo KAFE KEAN
from articulos.context_processors import obtener_imagen_inspiradora

# Configuración de logging
logger = logging.getLogger(__name__)

# ==========================
# 🌟 Autenticación y Sesiones
# ==========================
class CustomLoginView(LoginView):
    template_name = "articulos/login.html"
    redirect_authenticated_user = True
    next_page = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["imagen_inspiradora"] = obtener_imagen_inspiradora()  # ✅ Ahora sí se pasa la imagen
        return context

class CustomLoginView(LoginView):
    template_name = "articulos/login.html"  # ✅ Ahora apunta correctamente
    redirect_authenticated_user = True
    next_page = '/'

class CustomLogoutView(LogoutView):
    next_page = '/'


# ==========================
# 🌟 Manejo de Errores
# ==========================
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


def custom_500_view(request):
    return render(request, '500.html', status=500)


# ==========================
# 🌟 Funcionalidades Auxiliares
# ==========================
def debug_headers(request):
    headers = {key: value for key, value in request.META.items() if key.startswith('HTTP_')}
    return JsonResponse(headers)


def cambiar_idioma(request, idioma):
    idiomas_permitidos = ["es", "en", "de"]  # Idiomas soportados
    if idioma not in idiomas_permitidos:
        messages.error(request, _("Idioma no soportado."))
        return redirect('inicio')
    
    activate(idioma)
    request.session['django_language'] = idioma
    messages.success(request, _("Idioma cambiado exitosamente."))
    return redirect('inicio')

# ==========================
# 🌟 Función para obtener la imagen inspiradora de Unsplash
# ==========================
def obtener_imagen_inspiradora():
    url = "https://api.unsplash.com/photos/random"
    query = "courage, overcoming fear, resilience"  # Buscar por estas palabras clave
    headers = {
        "Authorization": f"Client-ID {settings.UNSPLASH_ACCESS_KEY}"  # Usar la clave de API desde settings.py
    }
    params = {
        "query": query,
        "orientation": "landscape",
        "count": 1
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        if data:
            return data[0]["urls"]["regular"]  # Retorna la URL de la imagen
        else:
            logger.error("No se encontraron imágenes.")
            return None
    except requests.RequestException as e:
        logger.error(f"Error al obtener la imagen: {e}")
        return None


# ==========================
# 🌟 Tipos de Cambio (Comentar esta sección para desactivarla temporalmente)
# ==========================
# def obtener_tipo_cambio():
#     url = f"http://api.currencylayer.com/live"
#     api_key = settings.CURRENCY_LAYER_API_KEY  # Asegúrate de tener la clave en settings.py
#     monedas = ["MXN", "BRL", "CAD"]
#     tipos_de_cambio = []
#     fecha_actual = None

#     params = {
#         "access_key": api_key,
#         "currencies": ",".join(monedas),
#         "source": "USD",
#         "format": 1,
#     }

#     try:
#         response = requests.get(url, params=params, timeout=5)
#         response.raise_for_status()
#         data = response.json()

#         if data.get("success"):
#             fecha_actual = datetime.fromtimestamp(data.get("timestamp")).strftime('%Y-%m-%d %H:%M:%S')
#             quotes = data.get("quotes", {})
#             for moneda in monedas:
#                 key = f"USD{moneda}"
#                 valor_actual = quotes.get(key, 0)
#                 if valor_actual:
#                     tipos_de_cambio.append({
#                         "currency": moneda,
#                         "buy": round(valor_actual, 4),
#                         "sell": round(valor_actual * 1.02, 4),
#                         "variation": 0,
#                     })
#         else:
#             error_info = data.get("error", {}).get("info", _("Error desconocido."))
#             logger.error("Error en la API de CurrencyLayer: %s", error_info)
#             raise ValueError(_("Error al obtener datos de la API de CurrencyLayer."))

#     except requests.Timeout:
#         logger.error(_("Error de conexión: Tiempo de espera agotado."))
#         tipos_de_cambio = [{'currency': m, 'buy': 0, 'sell': 0, 'variation': 0} for m in monedas]
#     except requests.RequestException as e:
#         logger.error(_("Error de conexión a la API de CurrencyLayer: %s"), e)
#         tipos_de_cambio = [{'currency': m, 'buy': 0, 'sell': 0, 'variation': 0} for m in monedas]

#     return {'tipos_de_cambio': tipos_de_cambio, 'fecha': fecha_actual}



# ==========================
# 🌟 Generador de Consejos con https://openrouter.ai/settings/keys
# ==========================
def generar_consejo(mejor_accion, resultado_final):
    try:
        url = f"{settings.OPENROUTER_BASE_URL}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        prompt = (
            f"Eres un mentor experto en desarrollo personal. Basado en la siguiente información:\n\n"
            f"- Mejor acción recomendada: {mejor_accion}\n"
            f"- Resultado final numérico: {resultado_final}\n\n"
            f"Brinda un consejo práctico en 2-3 frases que ayude al usuario a mejorar su vida y encontrar propósito."
        )

        data = {
            "model": "meta-llama/llama-3.2-3b-instruct:free",  # 📌 Modelo gratuito
            "messages": [
                {"role": "system", "content": "Eres un mentor experto en desarrollo personal."},
                {"role": "user", "content": prompt}
            ]
        }

        logger.info(f"📢 Enviando solicitud a OpenRouter: {data}")  # ✅ Muestra el JSON enviado
        response = requests.post(url, headers=headers, json=data)

        logger.info(f"📢 Respuesta de OpenRouter: {response.status_code} - {response.text}")  # ✅ Imprime la respuesta

        if response.status_code == 200:
            response_data = response.json()
            if "choices" in response_data and len(response_data["choices"]) > 0:
                consejo = response_data["choices"][0]["message"]["content"].strip()
                return consejo
            else:
                logger.error(f"⚠️ OpenRouter no devolvió resultados válidos: {response_data}")
                return _("No se pudo generar un consejo en este momento, intenta más tarde.")
        else:
            logger.error(f"🚨 Error en la solicitud a OpenRouter: {response.status_code} - {response.text}")
            return _("No se pudo generar un consejo en este momento, intenta más tarde.")

    except Exception as e:
        logger.error(f"🔥 Error con OpenRouter: {e}")
        return _("No se pudo generar un consejo en este momento, intenta más tarde.")
    
# ==========================
# 🌟 Ejecución del Algoritmo KAFE KEAN
# ==========================
def ejecutar_algoritmo(request):
    try:
        Q, recompensas_totales, estado_final = ejecutar_q_learning()
        mejor_accion = Q.mean().idxmax()
        resultado_final = calcular_esfuerzo(*estado_final)
        consejo = generar_consejo(mejor_accion, resultado_final)

        return JsonResponse({
            "mejor_accion": mejor_accion,
            "resultado_final": resultado_final,
            "consejo_practico": consejo
        })
    except Exception as e:
        logger.error(f"Error al ejecutar el algoritmo: {e}")
        return JsonResponse({"error": "Error al procesar el algoritmo."}, status=500)


# ==========================
# 🌟 Vista de Inicio
# ==========================
def inicio(request):
    imagen_inspiradora = obtener_imagen_inspiradora()  # Obtener la imagen inspiradora
    # Comenta la línea que llama a obtener_tipo_cambio()
    # datos_tipos_cambio = obtener_tipo_cambio()  # Desactivada temporalmente
    return render(request, 'articulos/inicio.html', {
        'imagen_inspiradora': imagen_inspiradora,  # Pasar la imagen al template
        # **datos_tipos_cambio  # Se comentará temporalmente
    })

# ==========================
# 🌟 CRUD Artículos
# ==========================
def lista_articulos(request):
    articulos = Articulo.objects.all().order_by('-fecha_publicacion')
    imagen_inspiradora = obtener_imagen_inspiradora()  # 🔥 Se obtiene manualmente
    
    return render(request, "articulos/lista_articulos.html", {
        "articulos": articulos,
        "imagen_inspiradora": imagen_inspiradora  # 🔥 Se pasa explícitamente a la plantilla
    })

def crear_articulo(request):
    imagen_inspiradora = obtener_imagen_inspiradora()
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, _("Artículo creado exitosamente."))
            return redirect('lista_articulos')  
    else:
        form = ArticuloForm()
    
    return render(request, 'articulos/crear_articulo.html', {
        'form': form,
        'imagen_inspiradora': imagen_inspiradora
    })
    
def editar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    imagen_inspiradora = obtener_imagen_inspiradora()
    
    if request.method == 'POST':
        form = ArticuloForm(request.POST, request.FILES, instance=articulo)
        if form.is_valid():
            form.save()
            messages.success(request, _("Artículo editado exitosamente."))
            return redirect('lista_articulos')
    else:
        form = ArticuloForm(instance=articulo)
    
    return render(request, 'articulos/editar_articulo.html', {
        'form': form,
        'imagen_inspiradora': imagen_inspiradora
    })

def eliminar_articulo(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    imagen_inspiradora = obtener_imagen_inspiradora()
    
    if request.method == 'POST':
        articulo.delete()
        messages.success(request, _("Artículo eliminado exitosamente."))
        return redirect('lista_articulos')
    
    return render(request, 'articulos/eliminar_articulo.html', {
        'articulo': articulo,
        'imagen_inspiradora': imagen_inspiradora
    })

def detalle_articulo(request, slug):
    articulo = get_object_or_404(Articulo, slug=slug)
    imagen_inspiradora = obtener_imagen_inspiradora()
    
    return render(request, 'articulos/detalle_articulo.html', {
        'articulo': articulo,
        'imagen_inspiradora': imagen_inspiradora
    })

#def login_view(request):
#   imagen_inspiradora = obtener_imagen_inspiradora()
#    return render(request, "articulos/login.html", {"imagen_inspiradora": imagen_inspiradora})


def login_view(request):
    articulo = get_object_or_404(Articulo, slug=slug)
    
    return render(request, 'articulos/login.html', {
        'articulo': articulo,
     })
      
#def login_view(request):
#    return render(request, "articulos/login.html")  # ✅ Ya estaba bien

# ==========================
# 🌟 Registro de Usuarios
# ==========================
def registro(request):
    imagen_inspiradora = obtener_imagen_inspiradora()
    form = UserCreationForm(request.POST or None)
    
    if form.is_valid():
        form.save()
        messages.success(request, _("Cuenta creada exitosamente. ¡Ahora puedes iniciar sesión!"))
        return redirect('articulos:login')
    
    return render(request, 'articulos/registro.html', {
        'form': form,
        'imagen_inspiradora': imagen_inspiradora
    })


# ==========================
# 🌟 Páginas Estáticas
# ==========================
def preguntas_frecuentes(request):
    imagen_inspiradora = obtener_imagen_inspiradora()
    return render(request, 'articulos/preguntas_frecuentes.html', {"imagen_inspiradora": imagen_inspiradora})

def contactanos(request):
    imagen_inspiradora = obtener_imagen_inspiradora()
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')
        messages.success(request, _("Mensaje enviado exitosamente."))
        return redirect('articulos:contactanos')
    
    return render(request, 'articulos/contactanos.html', {
        "imagen_inspiradora": imagen_inspiradora
    })

def password_reset(request):
    imagen_inspiradora = obtener_imagen_inspiradora()
    return render(request, 'password_reset.html', {"imagen_inspiradora": imagen_inspiradora})

def password_reset_done(request):
    imagen_inspiradora = obtener_imagen_inspiradora()
    return render(request, 'password_reset_done.html', {"imagen_inspiradora": imagen_inspiradora})

def password_reset_confirm(request):
    imagen_inspiradora = obtener_imagen_inspiradora()
    return render(request, 'password_reset_confirm.html', {"imagen_inspiradora": imagen_inspiradora})

def password_reset_complete(request):
    imagen_inspiradora = obtener_imagen_inspiradora()
    return render(request, 'password_reset_complete.html', {"imagen_inspiradora": imagen_inspiradora})

def tipos_cambio(request):
    imagen_inspiradora = obtener_imagen_inspiradora()
    return render(request, 'tipos_cambio.html', {"imagen_inspiradora": imagen_inspiradora})
