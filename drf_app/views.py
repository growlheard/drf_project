import time

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import viewsets, generics, status
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from drf_app.models import Course, Lesson, Payment, Subscription
from drf_app.paginations import CoursePagination, LessonPagination
from drf_app.permissions import IsModerator, IsOwner
from drf_app.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from drf_app.services import confirm_payment, create_payment, retrieve_payment
from users.serializers import PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    Представление для работы с курсами.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all().order_by('name')
    permission_classes = [IsModerator | IsOwner | IsAdminUser]
    pagination_class = CoursePagination


class LessonListView(generics.ListAPIView):
    """
    Представление для получения списка уроков.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all().order_by('name')
    permission_classes = [IsModerator | IsOwner]
    pagination_class = LessonPagination


class LessonCreateView(generics.CreateAPIView):
    """
    Представление для создания урока.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsAdminUser]


class LessonDeleteView(generics.DestroyAPIView):
    """
    Представление для удаления урока.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner | IsAdminUser]


class LessonDetailView(generics.RetrieveAPIView):
    """
    Представление для получения деталей урока.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateView(generics.UpdateAPIView):
    """
    Представление для обновления урока.
    """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class PaymentListView(generics.ListAPIView):
    """
    Представление для получения списка платежей.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course_pay', 'lesson_pay', 'payment_method']
    ordering_fields = ['date']
    permission_classes = [IsModerator | IsOwner]


class PaymentDeleteView(generics.DestroyAPIView):
    """
    Представление для удаления платежа.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsOwner]


class PaymentDetailView(generics.RetrieveAPIView):
    """
    Представление для получения деталей платежа.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsModerator | IsOwner]


class PaymentUpdateView(generics.UpdateAPIView):
    """
    Представление для обновления платежа.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsModerator | IsOwner]


class SubscriptionCreateView(generics.CreateAPIView):
    """
    Представление для создания подписки.
    """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsOwner]


class SubscriptionUpdateView(generics.UpdateAPIView):
    """
    Представление для обновления подписки.
    """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsOwner]


class SubscriptionDeleteView(generics.DestroyAPIView):
    """
    Представление для удаления подписки.
    """
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
    permission_classes = [IsOwner]


class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        course_pay = request.data.get('course_pay')
        user_id = request.data.get('user')
        payment_token = request.data.get('payment_method')
        amount = request.data.get('amount')

        try:
            payment = create_payment(course_pay, user_id, payment_token, amount)
            return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RetrievePaymentView(APIView):
    def get(self, request, payment_intent_id):
        try:
            time.sleep(1)

            status = retrieve_payment(payment_intent_id)
            return Response({'status': status})
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class ConfirmPaymentView(APIView):
    def patch(self, request, payment_intent_id):
        payment_method_id = request.data.get('payment_method_id')
        if payment_method_id is None:
            return Response({'error': 'Не указан payment_method_id.'}, status=status.HTTP_400_BAD_REQUEST)
        payment = get_object_or_404(Payment, payment_intent_id=payment_intent_id)
        payment.payment_method_id = payment_method_id
        payment.status = Payment.PAID
        payment.save()
        try:
            subscription = Subscription.objects.filter(user=payment.user, course=payment.course_pay).first()
            if subscription:
                subscription.status = True
                subscription.save()
            else:
                Subscription.objects.create(user=payment.user, course=payment.course_pay, status=True)
        except Exception as e:
            raise Exception(f'Ошибка изменения статуса подписки: {str(e)}')
        return Response({'message': 'Платеж успешно подтвержден.'})
