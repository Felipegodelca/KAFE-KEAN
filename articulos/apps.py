from django.apps import AppConfig
import logging  # Para registrar mensajes en caso de errores

class ArticulosConfig(AppConfig):
    """
    Configuración de la aplicación 'articulos'.
    """
    # Campo predeterminado para claves primarias de los modelos
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre de la aplicación
    name = 'articulos'

    def ready(self):
        """
        Este método se ejecuta cuando la aplicación está lista para usarse.
        Se utiliza para registrar las señales definidas en signals.py.
        """
        try:
            import articulos.signals  # Importa las señales de la aplicación
        except ImportError as e:
            # Registra un mensaje de error en el sistema de logs
            logger = logging.getLogger(__name__)
            logger.error("Error al importar 'signals.py' en la aplicación 'articulos': %s", e)
            raise ImportError(
                "No se pudo importar el archivo de señales 'signals.py'. "
                "Por favor, asegúrate de que el archivo exista y sea válido."
            )