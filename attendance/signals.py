from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import StudentProfile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not instance.is_staff:
        StudentProfile.objects.create(user=instance, student_id=f"S{instance.id:04d}")