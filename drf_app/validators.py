from rest_framework import serializers


class VideoValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if value.get('video'):
            if 'youtube.com' not in value.get('video'):
                raise serializers.ValidationError('Разрешено размещение ссылок только с ресурса youtube.com')