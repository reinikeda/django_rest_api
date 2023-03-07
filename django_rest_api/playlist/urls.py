from django.urls import path
from . import views


urlpatterns = [
    path('', views.BandList.as_view()),
    path('<int:pk>/', views.BandDetail.as_view()),
    path('albums/', views.AlbumList.as_view()),
    path('album/<int:pk>/', views.AlbumDetail.as_view()),
    path('songs/', views.SongList.as_view()),
    path('song/<int:pk>/', views.SongDetail.as_view()),
    path('reviews/', views.ReviewList.as_view()),
    path('review/<int:pk>', views.ReviewDetails.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('comment/<int:pk>/', views.CommentDetails.as_view()),
    path('<int:album_review_id>/like/', views.ReviewLikeList.as_view()),
]
