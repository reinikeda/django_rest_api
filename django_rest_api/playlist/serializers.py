from rest_framework import serializers
from . import models


class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Band
        fields = ('id', 'name')

class AlbumSerializer(serializers.ModelSerializer):
    band_name = serializers.ReadOnlyField(source='band.name')

    class Meta:
        model = models.Album
        fields = ('id', 'name', 'band', 'band_name')


class SongSerializer(serializers.ModelSerializer):
    album_name = serializers.ReadOnlyField(source='album.name')

    class Meta:
        model = models.Song
        fields = ('id', 'name', 'duration', 'album', 'album_name')


class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    user = serializers.ReadOnlyField(source='user.username')
    album_name = serializers.ReadOnlyField(source='album.name')
    like_count = serializers.SerializerMethodField()

    def get_like_count(self, obj):
        return models.AlbumReviewLike.objects.filter(album_review=obj).count()

    class Meta:
        model = models.AlbumReview
        fields = ('id', 'user_id', 'user', 'album', 'album_name', 'content', 'score', 'like_count')


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    user = serializers.ReadOnlyField(source='user.username')
    review_content = serializers.ReadOnlyField(source='album_review.content')
        
    class Meta:
        model = models.AlbumReviewComment
        fields = ('id', 'user_id', 'user', 'album_review', 'review_content', 'content')


class ReviewLikeSerializer(serializers.ModelSerializer):  
    class Meta:
        model = models.AlbumReviewLike
        fields = ('id', )    
