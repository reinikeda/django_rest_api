from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Band(models.Model):
    band = models.CharField(max_length=200)


class Album(models.Model):
    name = models.CharField(max_length=200)
    band_id = models.ForeignKey(Band, on_delete=models.CASCADE, related_name='albums')


class Song(models.Model):
    name = models.CharField(max_length=200)
    duration = models.IntegerField()
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')


class AlbumReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='reviews')
    content = models.CharField(max_length=4000)
    score = models.IntegerField()


class AlbumReviewComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    album_review_id = models.ForeignKey(AlbumReview, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=4000)


class AlbumReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    album_review_id = models.ForeignKey(AlbumReview, on_delete=models.CASCADE, related_name='likes')