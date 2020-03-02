from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class Album(models.Model):
    spotify_id = models.CharField(primary_key=True, max_length=200)
    artist = models.TextField()
    title = models.CharField(max_length=200)
    art_url = models.TextField()
    link = models.TextField()

    def __str__(self):
        return self.title

    def artist_slug(self):
        slug = "-".join(self.artist.lower().split(' '))
        return slug

class Review(models.Model):
    class Meta:
        unique_together = (('reviewer','album'),)

    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.reviewer.__str__() + " rated " + self.album.title + " by " + self.album.artist + " " + self.rating.__str__()

# -- START RECEIVERS TO LINK PROFILE MODEL TO USER MODEL --#
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
# -- END  RECEIVERS TO LINK PROFILE MODEL TO USER MODEL --#
