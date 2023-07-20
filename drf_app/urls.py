from django.urls import path
from rest_framework.routers import DefaultRouter

from drf_app.apps import DrfAppConfig
from drf_app.views import CourseViewSet, LessonListView, LessonCreateView, LessonUpdateView, LessonDeleteView, \
    LessonDetailView, PaymentListView, PaymentCreateView, PaymentDetailView, PaymentUpdateView, PaymentDeleteView

app_name = DrfAppConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lessons/', LessonListView.as_view(), name='lesson-list'),
                  path('lessons/create/', LessonCreateView.as_view(), name='lesson-create'),
                  path('lessons/<int:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
                  path('lessons/update/<int:pk>/', LessonUpdateView.as_view(), name='lesson-update'),
                  path('lessons/delete/<int:pk>/', LessonDeleteView.as_view(), name='lesson-delete'),
                  path('payment/', PaymentListView.as_view(), name='payment-list'),
                  path('payment/create/', PaymentCreateView.as_view(), name='payment-create'),
                  path('payment/detail/<int:pk>/', PaymentDetailView.as_view(), name='payment-detail'),
                  path('payment/update/<int:pk>/', PaymentUpdateView.as_view(), name='payment-update'),
                  path('payment/delete/<int:pk>/', PaymentDeleteView.as_view(), name='payment-delete'),
              ] + router.urls
