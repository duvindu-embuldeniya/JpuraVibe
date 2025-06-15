from django.db.models.signals import post_save
from . models import Profile
from django.contrib.auth.models import User


def create_profile(sender,instance,created,*args,**kwargs):
    if created:
        created_user = instance
        Profile.objects.create(
            user = created_user
        )


post_save.connect(create_profile, sender=User)