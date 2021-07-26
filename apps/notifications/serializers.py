import json

from rest_framework import serializers

from apps.notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    body = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'notice_type', 'is_on_credit',
            'is_viewed', 'body', 'created_at'
        ]
        extra_kwargs = {
            'notice_type': {'read_only': True},
            'is_on_credit': {'read_only': True},
            'body': {'read_only': True},
            'is_viewed': {'required': True},
        }

    def get_body(self, obj):
        return json.loads(obj.body)
