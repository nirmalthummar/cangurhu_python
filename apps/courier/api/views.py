from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from common.exception import ErrorResponseException
from core.permissions import IsCourier
from apps.courier.api.serializers import (
    CourierSerializer,
    CourierDocumentSerializer,
    CourierVehicleSerializer,
    NewOrderListSerializer,
    CourierOrderSerializer,
    CourierOrderPickupSerializer,
    CourierOrderCalculationSerializer
)

from apps.courier.models import CourierOrder
from apps.cook.models import CookOrderDetails
from apps.order.models import OrderMenuItem, Order
from apps.courier.api.service import CourierOrderCalculation


class CourierAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsCourier)
    serializer_class = CourierSerializer
    swagger_tags = ['Courier']
    parser_classes = [MultiPartParser]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user.courier)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update Courier
        """

        courier = request.user.courier
        serializer = self.get_serializer(data=request.data, instance=courier, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourierDocumentAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsCourier)
    serializer_class = CourierDocumentSerializer
    swagger_tags = ['Courier']
    parser_classes = [MultiPartParser]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user.courier)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update Courier Document
        """

        courier = request.user.courier
        serializer = self.get_serializer(data=request.data, instance=courier, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourierVehicleAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, IsCourier)
    serializer_class = CourierVehicleSerializer
    swagger_tags = ['Courier']
    parser_classes = [MultiPartParser]

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user.courier)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Update Courier Vehicle  """

        courier = request.user.courier
        serializer = self.get_serializer(data=request.data, instance=courier, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourierNewOrderListView(APIView):
    permission_classes = (IsAuthenticated, IsCourier)
    swagger_tags = ['OrderList']
    """
         New Orders list/Detail by order_id 
      """

    def get(self, request, order_id=None):
        if order_id is None:

            order_details = Order.objects.filter(created_at__date=datetime.today().date(),
                                                 status="ACK").order_by("-created_at")
            serializer = NewOrderListSerializer(order_details, many=True,
                                                context={'courier_user_id': request.user.user_id})
        else:

            order_details = Order.objects.filter(order_id=order_id).first()
            serializer = NewOrderListSerializer(order_details, context={'courier_user_id': request.user.user_id})
            print(serializer)

        return Response(serializer.data)


class CourierOrderView(APIView):
    permission_classes = (IsAuthenticated, IsCourier)
    swagger_tags = ['Courier Order Status']

    """
         Order Accepted or Canceled by Courier
      """

    def put(self, request, order_id=None):
        if order_id:
            order_details = Order.objects.filter(order_id=order_id, status="ACK").first()
            courier_order_detail = CourierOrder.objects.create(courier_id=request.user.courier.id,
                                                               order_id=order_details.id,
                                                               eta=30)  # eta static
            courier_order_detail.courier_status = request.data.get("status")
            courier_order_detail.save()
            if order_details.status == "CCR":
                courier_order_detail.reason = request.data.get("reason")
                courier_order_detail.save()
            serializer = NewOrderListSerializer(order_details, context={'courier_user_id': request.user.user_id})
            return Response(serializer.data)
        return Response({"detail": "order id requires"}, status=status.HTTP_400_BAD_REQUEST)


class CourierSetOrderPickedUpView(APIView):
    permission_classes = (IsAuthenticated, IsCourier)
    swagger_tags = ['Courier Order Picked up Status']

    """
        Set Order status Order Picked up by Courier
      """

    def put(self, request, order_id=None):
        if order_id:
            order_details = Order.objects.filter(order_id=order_id, status="RE").first()
            courier_order_detail = CourierOrder.objects.filter(courier_id=request.user.courier.id,
                                                               order_id=order_details.id).first()
            if courier_order_detail:
                courier_order_detail.courier_status = request.data.get("status")
                courier_order_detail.save()
            order_details.status = courier_order_detail.courier_status
            order_details.save()
            serializer = NewOrderListSerializer(order_details, context={'courier_user_id': request.user.user_id})
            return Response(serializer.data)
        else:
            return Response({"detail": "order id requires"}, status=status.HTTP_400_BAD_REQUEST)


# ORDER STATUS=ON THE WAY
# SET AUTOMATIC
class CourierSetOrderDeliveredView(APIView):
    permission_classes = (IsAuthenticated, IsCourier)
    swagger_tags = ['Courier Order Delivered Status']

    """
        Set Order status Order Delivered by Courier
      """

    def put(self, request, order_id=None):
        if order_id:
            order_details = Order.objects.filter(order_id=order_id, status="PIU").first()
            if order_details:
                courier_order_detail = CourierOrder.objects.filter(courier_id=request.user.courier.id,
                                                                   order_id=order_details.id).first()
                if courier_order_detail:
                    courier_order_detail.courier_status = request.data.get("status")
                    courier_order_detail.save()
                    order_details.status = courier_order_detail.courier_status
                    order_details.save()
                else:
                    raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            else:
                raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            cook_order_detail = CookOrderDetails.objects.filter(order_id=order_details.id).first()
            if cook_order_detail:
                cook_order_detail.cook_status = order_details.status
                cook_order_detail.save()
            serializer = NewOrderListSerializer(order_details, context={'courier_user_id': request.user.user_id})
            return Response(serializer.data)
        else:
            return Response({"detail": "order id requires"}, status=status.HTTP_400_BAD_REQUEST)


class CourierReadyToPickupList(APIView):
    permission_classes = (IsAuthenticated, IsCourier)
    swagger_tags = ['Courier Ready To Pickup List']

    """
          Ready to Pickup List/Detail by order_id
      """

    def get(self, request, order_id=None):
        if order_id is None:
            courier_orders = CourierOrder.objects.filter(courier_id=request.user.courier.id,
                                                         order__status__in=['RE', 'CP'])
            if courier_orders:
                order_ids = [courier_order.order.id for courier_order in courier_orders]
                orders = Order.objects.filter(id__in=order_ids)
                serializer = CourierOrderPickupSerializer(orders, many=True)
            else:
                raise ErrorResponseException(f"No Orders for pickup")

        else:
            courier_orders = CourierOrder.objects.filter(courier_id=request.user.courier.id, order__order_id=order_id,
                                                         ).first()
            if courier_orders:
                order_ids = courier_orders.order.id
                orders = Order.objects.filter(id=order_ids).first()
                if orders:
                    serializer = CourierOrderPickupSerializer(orders)
                else:
                    raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            else:
                raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
        return Response(serializer.data)


class CourierPastOrderListView(APIView):
    permission_classes = (IsAuthenticated, IsCourier)
    swagger_tags = ['Courier Past Order List']

    """
       Courier Past Order List
    """

    def get(self, request):
        past_order_details = CourierOrder.objects.filter(courier_id=request.user.courier.id, order__status="DE")
        order_ids = [courier_order.order.id for courier_order in past_order_details]
        orders = Order.objects.filter(id__in=order_ids)
        serializer = CourierOrderSerializer(orders, many=True)
        return Response(serializer.data)


# Courier Calculation
class CourierOrderCalculationView(APIView):
    permission_classes = (IsAuthenticated, IsCourier)
    swagger_tags = ['Courier Calculation']

    """
        Calculating the Courier amount needs to be paid
    """

    def put(self, request, courier_order_id):

        courier_id = request.user.courier.id
        if not courier_id:
            raise ErrorResponseException("Courier is not Exist!")

        payload = request.data
        if len(payload.keys()) == 0:
            raise ErrorResponseException("Payload is empty!")

        order_id = payload.get('order_id')
        if not order_id:
            raise ErrorResponseException("Order is not Exist!")

        try:
            order = Order.objects.get(id=order_id)

        except Order.DoesNotExist:
            raise ErrorResponseException(f"Order is not exist with the order id '{order_id}'!")

        courier_order = CourierOrder.objects.filter(courier_order_id=courier_order_id, courier_status="ACR").first()
        if not courier_order:
            raise ErrorResponseException("Courier order is not exist!")

        order_calculation = CourierOrderCalculation(request, order=order, courier_order=courier_order)
        total_distance, earnings = order_calculation.courier_order_calculation()

        data = {
            "total_distance": total_distance,
            "earnings": earnings
        }

        serializer = CourierOrderCalculationSerializer(instance=courier_order, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise ErrorResponseException(str(serializer.errors))
