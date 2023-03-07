from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Band(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=200)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='albums')

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=200)
    duration = models.IntegerField()
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')

    def __str__(self):
        return self.name


class AlbumReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='reviews')
    content = models.CharField(max_length=4000)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.id}, {self.content[:100]}'


class AlbumReviewComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    album_review = models.ForeignKey(AlbumReview, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=4000)

    def __str__(self):
        return f'{self.id}, {self.content[:100]}'


class AlbumReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    album_review = models.ForeignKey(AlbumReview, on_delete=models.CASCADE, related_name='likes')