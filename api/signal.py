from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def confirm_tailor_user(sender, instance, created, **kwargs):
    if created and instance.idRoles_id == 1:  # Vérifiez si le rôle est 1 (tailleur)
        instance.is_active = False  # Désactivez l'utilisateur par défaut
        instance.save()
