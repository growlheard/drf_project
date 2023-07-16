from django.urls import path
from rest_framework.routers import DefaultRouter

from drf_app.apps import DrfAppConfig
from drf_app.views import CourseViewSet, LessonListView, LessonCreateView, LessonUpdateView, LessonDeleteView, \
    LessonDetailView

app_name = DrfAppConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lessons/', LessonListView.as_view(), name='lesson-list'),
                  path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
                  path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
                  path('lessons/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson-update'),
                  path('lessons/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson-delete'),
              ] + router.urls
