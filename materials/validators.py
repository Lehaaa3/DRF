import re

from rest_framework import serializers


class LessonUrlValidation:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = r'youtube\.com/?'
        url_value = dict(value).get(self.field)
        if url_value:
            if not re.search(reg, url_value, re.IGNORECASE):
                raise serializers.ValidationError('Url должен быть ссылкой только на youtube.com')
