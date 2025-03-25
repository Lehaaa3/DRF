from rest_framework import serializers

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('title', 'description', 'course',)


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'image', 'description', 'lesson_count', 'lesson']

    def get_lesson_count(self, instance):
        return instance.lesson.count()
