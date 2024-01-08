from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}"


class Book(models.Model):
    title = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"


class Song(models.Model):
    title = models.CharField(unique=True, max_length=100)


class Artist(models.Model):
    name = models.CharField(unique=True, max_length=100)
    songs = models.ManyToManyField(to=Song, related_name='artists')
