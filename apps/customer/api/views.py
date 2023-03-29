from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from core.permissions import IsCustomer
from .serializers import CustomerSerializer, CustomerOrderListSerializer

from rest_framework.views import APIView
from common.exception import ErrorResponseException
from apps.customer.models import Customer, CustomerOrder
from django.contrib.auth import get_user_model

from ...order.models import Order

User = get_user_model()


# class CustomerAPIView(generics.RetrieveUpdateAPIView):
#     permission_classes = (IsAuthenticated, IsCustomer)
#     serializer_class = CustomerSerializer
#     swagger_tags = ['Customer']
#     parser_classes = [MultiPartParser]
#
#     def retrieve(self, request, *args, **kwargs):
#         serializer = self.get_serializer(request.user.customer)
#         return Response(serializer.data)
#
#     def update(self, request, *args, **kwargs):
#         """
#         Update Cook Profile
#         """
#
#         customer = request.user.customer
#         serializer = self.get_serializer(data=request.data, instance=customer, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)


class CustomerDetailView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)

    def get(self, request):
        """
           Get the customer profile
        """
        customer_id = request.user.customer
        customer = Customer.objects.get(customer_id=customer_id)

        serializer = CustomerSerializer(customer)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request):
        """
           Update the customer profile
        """
        user_id = request.user.user_id
        customer = Customer.objects.get(user=user_id)

        payload = request.data

        username = payload.get('username')
        if not username:
            raise ErrorResponseException("username is required!")

        email = payload.get('email')
        if not email:
            raise ErrorResponseException("'email' is required!")

        country = payload.get('country')
        if not country:
            raise ErrorResponseException("'country' is required!")

        mobile_number = payload.get('mobile_number')
        if not mobile_number:
            raise ErrorResponseException("'mobile_number' is required!")

        serializer = CustomerSerializer(data=payload, instance=customer, partial=True)
        if serializer.is_valid():
            try:
                customer.user.username = username
                customer.user.email = email
                customer.user.mobile_number = mobile_number
                customer.user.save()
            except Exception as e:
                raise ErrorResponseException(e)
            serializer.save()
        else:
            raise ErrorResponseException(str(serializer.errors))

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class CustomerOrderCancelStatusView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)
    swagger_tags = ['Courier Order Status']

    def put(self, request, order_id=None):
        if order_id:
            try:
                order_details = Order.objects.get(order_id=order_id, status="OP")

                customer_order_detail = CustomerOrder.objects.create(customer_id=request.user.customer.id,
                                                                     order_id=order_details.id
                                                                     )
                customer_order_detail.customer_status = request.data.get("status")
                customer_order_detail.save()
            except Order.DoesNotExist:
                raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            order_details.status = customer_order_detail.customer_status
            order_details.save()
            if order_details.status == "CCU":
                customer_order_detail.reason = request.data.get("reason")
                customer_order_detail.save()
            serializer = CustomerOrderListSerializer(order_details, context={'user_id': request.user.user_id})
            return Response(serializer.data)
        return Response({"detail": "order id requires"}, status=status.HTTP_400_BAD_REQUEST)


class CustomerOngoingOrderListView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)
    swagger_tags = ['Customer Ongoing OrderList']

    def get(self, request, order_id=None):
        if order_id is None:
            order_details = Order.objects.filter(customer_id=request.user.customer.id).exclude(
                status__in=['OP', 'CCK', 'CCR', 'DE', 'PE','CCU'])
            serializer = CustomerOrderListSerializer(order_details, many=True,
                                                     context={'user_id': request.user.user_id})
        else:
            try:
                order_details = Order.objects.get(order_id=order_id)
                serializer = CustomerOrderListSerializer(order_details, context={'user_id': request.user.user_id})
            except Order.DoesNotExist:
                raise ErrorResponseException(f"Order does not exist in Ongoing Orders with Order ID '{order_id}'!")
        return Response(serializer.data)


class CustomerCompletedOrderListView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)
    swagger_tags = ['Customer Completed OrderList']

    def get(self, request, order_id=None):
        if order_id is None:
            order_details = Order.objects.filter(customer_id=request.user.customer.id, status="DE").order_by(
                "-created_at")
            serializer = CustomerOrderListSerializer(order_details, many=True,
                                                     context={'user_id': request.user.user_id})
        else:
            try:
                order_details = Order.objects.get(order_id=order_id)
                serializer = CustomerOrderListSerializer(order_details, context={'user_id': request.user.user_id})
            except Order.DoesNotExist:
                raise ErrorResponseException(f"Order does not exist in Ongoing Orders with Order ID '{order_id}'!")
        return Response(serializer.data)


class CustomerCanceledOrderListView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)
    swagger_tags = ['Customer Canceled OrderList']

    def get(self, request, order_id=None):
        if order_id is None:
            order_details = Order.objects.filter(customer_id=request.user.customer.id, status="CCU").order_by(
                "-created_at")
            serializer = CustomerOrderListSerializer(order_details, many=True,
                                                     context={'user_id': request.user.user_id})
        else:
            try:
                order_details = Order.objects.get(order_id=order_id)
                serializer = CustomerOrderListSerializer(order_details, context={'user_id': request.user.user_id})
            except Order.DoesNotExist:
                raise ErrorResponseException(f"Order does not exist in Ongoing Orders with Order ID '{order_id}'!")
        return Response(serializer.data)
