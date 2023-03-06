from rest_framework import serializers
from . import models


class BandSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = models.Band
        fields = ('id', 'band', 'user', 'user_id')