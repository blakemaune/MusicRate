from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

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
        unique_together = (('author', 'album'),)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=10, validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now, blank=True, null=True)

    def __str__(self):
        return self.author.__str__() + " rated " + self.album.title + " by " + self.album.artist + " " + self.rating.__str__()
