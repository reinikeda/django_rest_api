from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from . import models, serializers


class UserOwnedObjectRUDMixin():
    def delete(self, request, *args, **kwargs):
        obj = self.queryset.filter(pk=kwargs['pk'], user=self.request.user)
        if obj.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('Object not found or does not belong to you.'))

    def put(self, request, *args, **kwargs):
        obj = self.queryset.filter(pk=kwargs['pk'], user=self.request.user)
        if obj.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_('Object not found or does not belong to you.'))


class AdminOwnedObjectRUDMixin():
    def delete(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('Object not found or does not belong to you.'))

    def put(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_('Object not found or does not belong to you.'))


class BandList(generics.ListCreateAPIView):
    serializer_class = serializers.BandSerializer
    queryset = models.Band.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class BandDetail(AdminOwnedObjectRUDMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.BandSerializer
    queryset = models.Band.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class AlbumList(generics.ListCreateAPIView):
    serializer_class = serializers.AlbumSerializer
    queryset = models.Album.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class AlbumDetail(AdminOwnedObjectRUDMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AlbumSerializer
    queryset = models.Album.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class SongList(generics.ListCreateAPIView):
    serializer_class = serializers.SongSerializer
    queryset = models.Song.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class SongDetail(AdminOwnedObjectRUDMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.SongSerializer
    queryset = models.Song.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
        

class ReviewList(generics.ListCreateAPIView):
    serializer_class = serializers.ReviewSerializer
    queryset = models.AlbumReview.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    

class ReviewDetails(UserOwnedObjectRUDMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.ReviewSerializer
    queryset = models.AlbumReview.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class CommentList(generics.ListCreateAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = models.AlbumReviewComment.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def perform_create(self, serializer):
    #     serializer.validated_data['user'] = self.request.user
    #     serializer.validated_data['album_review'] = models.AlbumReview.objects.get(id=self.kwargs['album_review_id'])
    #     serializer.save()

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = qs.filter(album_review__id = self.kwargs['album_review_id'])
    #     return qs


class CommentDetails(UserOwnedObjectRUDMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CommentSerializer
    queryset = models.AlbumReviewComment.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


# class ReviewLikeList(generics.ListCreateAPIView):
#     serializer_class = serializers.ReviewLikeSerializer
#     queryset = models.AlbumReviewLike.objects.all()
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user, )


# class ReviewLikeDetails(generics.RetrieveUpdateDestroyAPIView, UserOwnedObjectRUDMixin):
#     serializer_class = serializers.ReviewLikeSerializer
#     queryset = models.AlbumReviewLike.objects.all()
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, )