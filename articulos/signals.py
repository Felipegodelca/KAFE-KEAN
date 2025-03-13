from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Perfil
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def gestionar_perfil(sender, instance, created, **kwargs):
    """
    Crea o guarda automáticamente un perfil para cada usuario nuevo o existente.
    """
    try:
        if created:
            # Crear perfil automáticamente al crear un nuevo usuario
            Perfil.objects.create(user=instance)
            logger.info(f"Perfil creado para el usuario: {instance.username}")
        else:
            # Guardar perfil asociado al usuario existente
            if hasattr(instance, 'perfil'):
                instance.perfil.save()
                logger.info(f"Perfil actualizado para el usuario: {instance.username}")
    except Exception as e:
        logger.error(f"Error gestionando el perfil para el usuario {instance.username}: {e}")