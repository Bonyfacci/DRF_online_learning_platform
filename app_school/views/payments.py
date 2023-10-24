import stripe
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from app_school.models import Payments
from app_school.serializers.payments import PaymentsSerializer, PaymentSuccessSerializer, PaymentRetrieveSerializer
from config.settings import STRIPE_SECRET_KEY


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_set_fields = ('paid_course', 'paid_lesson', 'payment_method')
    ordering_fields = ('date_of_payment',)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentRetrieveSerializer
    queryset = Payments.objects.all()
    permission_classes = [IsAuthenticated]


class PaymentSuccessAPIView(generics.RetrieveAPIView):
    stripe.api_key = STRIPE_SECRET_KEY
    serializer_class = PaymentSuccessSerializer
    queryset = Payments.objects.all()

    def get_object(self):

        session_id = self.request.query_params.get('session_id')
        session = stripe.checkout.Session.retrieve(session_id)

        payment_id = session.metadata['payment_id']
        obj = get_object_or_404(self.get_queryset(), pk=payment_id)

        if not obj.is_paid:
            if session.payment_status == 'paid':
                obj.is_paid = True
                obj.save()
        return obj
