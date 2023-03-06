from rest_framework import serializers
from . import models


class BandSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Band
        fields = ('id', 'band')