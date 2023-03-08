from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import models, serializers


User = get_user_model()


class UserCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.AllowAny, )

    def delete(self, request, *args, **kwargs):
        user = User.objects.filter(pk=self.request.user.pk)
        if user.exists():
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('User does not exist')
    

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

# only superuser should add new data
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


class ReviewLikeList(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.ReviewLikeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return models.AlbumReviewLike.objects.filter(
            user=self.request.user,
            album_review=models.AlbumReview.objects.get(id=self.kwargs['album_review_id'])
        )

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError(_('You already like this'))
        else:
            serializer.save(
                user=self.request.user,
                album_review=models.AlbumReview.objects.get(id=self.kwargs['album_review_id'])
            )

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(_('You cannot unlike what you don\'t like'))