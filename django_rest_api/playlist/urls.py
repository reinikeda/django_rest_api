from django.urls import path
from . import views


urlpatterns = [
    path('', views.BandList.as_view()),
]
