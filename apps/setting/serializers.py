from rest_framework import serializers

from .models import AppVersion


class AppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppVersion
        fields = (
            'android_version',
            'android_force_update',
            'ios_build_number',
            'ios_version',
            'ios_force_update',
        )


class HelpPageSerializer(serializers.Serializer):
    """Serializer for help page"""
    title = serializers.CharField(required=True)
    text = serializers.CharField(required=True)
