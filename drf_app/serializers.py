from rest_framework import serializers

from drf_app.models import Course, Lesson, Subscription
from drf_app.validators import VideoValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        validators = [VideoValidator(field='video')]
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    num_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(source='lesson_set', read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, instance):
        user = self.context['request'].user

        if user.is_authenticated:
            if Subscription.objects.filter(user=user, course=instance).exists():
                return True
        return False

    def get_num_lessons(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
