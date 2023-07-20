from rest_framework import serializers

from drf_app.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', read_only=True, many=True)

    def get_num_lessons(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = '__all__'
