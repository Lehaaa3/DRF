from rest_framework import serializers

from materials.models import Course, Lesson, Subscription
from materials.validators import LessonUrlValidation


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'description', 'course', 'url')
        validators = [LessonUrlValidation(field='url')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['title', 'image', 'description', 'payment', 'lesson_count', 'lesson', 'is_subscribed']

    def get_lesson_count(self, instance):
        return instance.lesson.count()

    def get_is_subscribed(self, instance):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=instance).exists()
