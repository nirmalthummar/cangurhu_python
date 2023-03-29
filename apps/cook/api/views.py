from math import radians, acos, sin, cos

from django.contrib.auth import get_user_model
from django.core.serializers import serialize
from django.db import models
from django.db.models import FloatField, ExpressionWrapper
from django.http import HttpResponse
import json
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from haversine import Unit

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.cook.models import (
    Cook,
    MenuCategory,
    MenuItem,
    FSCCatalogue,
    FSCCatalogueImage, CookOrderDetails, MenuSubItem
)
from common.exception import ErrorResponseException
from core.constant import ACTIVE
from core.permissions import IsCook, IsOwnerOrReadOnly
from core.utils import generate_order_sequence

from apps.cook.api.serializers import (
    CookSerializer,
    CookFSCDataSerializer,
    KitchenPremisesSerializer,
    MenuCategorySerializer,
    MenuItemSerializer,
    TopDishesSerializer,
    TopCookSerializer,
    FSCCatalogueSerializer,
    FSCCatalogueImageSerializer, CookOrderSerializer, CookOrderDetailSerializer, CookFutureOrderSerializer,
    MenuItemSerializerAV, SubMenuItemSerializer, SubMenuItemSerializerAV
)
from apps.cook.api.cook_service import get_user_in_range
from apps.cook.api.fsc import predict_image_object_detection_sample
from apps.accounts.models import StoreToken
from apps.address.models import Address
from apps.notification.models import Notification
from apps.notification.notification import send_notification
from apps.order.models import OrderMenuSubItem, Order

from django.shortcuts import get_object_or_404

User = get_user_model()


class CookAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated,)
    serializer_class = CookSerializer
    swagger_tags = ['Cook']
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_id='Update Courier Profile Details',
        operation_description='Update Courier Profile Details',
        manual_parameters=[
            openapi.Parameter(
                'kitchen_premises',
                openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description='Work Permit Document to be uploaded'
            ),
        ],
        responses={
            status.HTTP_200_OK: CookSerializer()
        }
    )
    def update(self, request, *args, **kwargs):

        serializer = CookSerializer(data=request.data, instance=request.user.cook, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user.cook)
        return Response(serializer.data)


class CookFSCDataAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated, IsCook)
    serializer_class = CookFSCDataSerializer
    swagger_tags = ['Cook']
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_id='Update Courier Profile Details',
        operation_description='Update Courier Profile Details',
        manual_parameters=[
            openapi.Parameter(
                'kitchen_premises',
                openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description='Work Permit Document to be uploaded'
            ),
        ],
        responses={
            status.HTTP_200_OK: CookSerializer()
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Update Cook Profile
        """

        kitchen_premises = None
        if 'kitchen_premises' in request.data:
            kitchen_premises = request.data.pop('kitchen_premises')

        cook = request.user.cook
        if kitchen_premises:
            self.create_kitchen_premises(kitchen_premises, cook)

        serializer = self.get_serializer(data=request.data, instance=cook, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_kitchen_premises(self, premises, cook):
        for file in premises:
            kps = KitchenPremisesSerializer(data={"kitchen_premises": file})
            kps.is_valid(raise_exception=True)
            kps.save(cook=cook)


class MenuCategoryView(APIView):

    def post(self, request):
        serializer = MenuCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def get(self, request):
        menu_category = MenuCategory.objects.all()
        serializer = MenuCategorySerializer(menu_category, many=True)
        return Response(serializer.data)


class MenuCategoryDetail(APIView):
    def get(self, request, pk):
        try:
            menu_category = MenuCategory.objects.get(pk=pk)
        except MenuCategory.DoesNotExist:
            return Response({'Error': 'not fond'}, status=status.HTTP_404_NOT_FOUND)

        serializer = MenuCategorySerializer(menu_category)
        return Response(serializer.data)

    def put(self, request, pk):
        menu_category = MenuCategory.objects.get(pk=pk)
        serializer = MenuCategorySerializer(menu_category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        menu_category = MenuCategory.objects.get(pk=pk)
        menu_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MenuCategoryListAPIView(generics.ListAPIView):
    serializer_class = MenuCategorySerializer
    queryset = MenuCategory.objects.all()
    swagger_tags = ['Menu Item', ]


class MenuItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsCook)
    ordering = ['-created_at']
    swagger_tags = ['Menu Item']

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.is_cook:
            return MenuItem.objects.select_related('category').filter(cook=self.request.user.cook)
        return MenuItem.objects.select_related('category').filter(status=ACTIVE)


class MenuItemListCreateAV(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsCook)

    def post(self, request):
        cook_id = request.user.cook.id
        payload = request.data
        payload['cook'] = cook_id
        menu_sub_items = payload.get('menu_sub_items')

        serializer_class = MenuItemSerializerAV(data=payload)
        if serializer_class.is_valid():
            serializer_class.save()
        else:
            return Response(serializer_class.errors)

        menu_item_data = serializer_class.data
        menu_item_id = menu_item_data.get('id')

        msi = []
        for items in menu_sub_items:
            items['menu_item'] = menu_item_id
            sub_menu_serializer_class = SubMenuItemSerializerAV(data=items)
            if sub_menu_serializer_class.is_valid():
                sub_menu_serializer_class.save()
                msi.append(sub_menu_serializer_class.data)

        menu_item_data['sub_menu_item'] = msi
        return Response(menu_item_data)

    def get(self, request):
        cook_id = request.user.cook.id
        menu_item_list = MenuItem.objects.filter(cook=cook_id)
        serializer_class = MenuItemSerializerAV(menu_item_list, many=True)
        return Response(serializer_class.data)


class MenuItemDetailAV(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly, IsCook)

    def get(self, request, pk):
        cook_id = request.user.cook.id
        try:
            menu_item= MenuItem.objects.get(cook=cook_id, id=pk)
        except MenuItem.DoesNotExist:
            return Response({'Error': 'not fond'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MenuItemSerializerAV(menu_item)
        menu_item_data = serializer.data
        menu_item_id = menu_item_data.get('id')
        queryset = MenuSubItem.objects.filter(menu_item=menu_item_id)
        sub_menu_serializer = SubMenuItemSerializerAV(queryset, many=True)
        menu_item_data['sub_menu_items'] = sub_menu_serializer.data
        return Response(menu_item_data)

    def put(self, request, pk):
        cook_id = request.user.cook.id
        menu_item = MenuItem.objects.get(id=pk)
        serializer = MenuItemSerializerAV(menu_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class MenuItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsCook)
    swagger_tags = ['Menu Item']
    queryset = MenuItem.objects.all()

    # def get_queryset(self):
    #     if self.request.user.is_authenticated and self.request.user.is_cook:
    #         return MenuItem.objects.select_related('category').filter(cook=self.request.user.cook)
    #     return MenuItem.objects.select_related('category').filter(status=ACTIVE)


class CookDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = TopCookSerializer
    queryset = Cook.objects.all()
    lookup_field = 'cook_id'
    swagger_tags = ['Cook']


class TopDishesAPIView(generics.ListAPIView):
    serializer_class = TopDishesSerializer
    queryset = MenuItem.objects.select_related('category').filter(status=ACTIVE)
    swagger_tags = ['Cook']
    filterset_fields = ['title', 'cook__user__username']


class TopCookAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TopCookSerializer
    swagger_tags = ['Cook']
    filterset_fields = ['country_id']

    def get_queryset(self):
        customer_address = Address.objects.get(user_id=self.request.user.user_id, is_default=True)
        cook_list = (get_user_in_range(float(customer_address.latitude), float(customer_address.longitude)))
        top_cooks = Cook.objects.filter(avg_star_rating__gte=3,user_id__in=cook_list).order_by('-id')
        return top_cooks


class FeaturedCookAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TopCookSerializer
    swagger_tags = ['Cook']

    def get_queryset(self):
        return Cook.objects.filter(featured_cook=True)


class NearByCookAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TopCookSerializer
    swagger_tags = ['Cook']

    def get_queryset(self):
        return Cook.objects.filter(near_by_cook=True)


class OfferZoneCookAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = TopCookSerializer
    queryset = Cook.objects.all()
    swagger_tags = ['Cook']

    def get_queryset(self):
        return Cook.objects.all()


class CookSearchAPIView(APIView):
    serializer_class = TopCookSerializer

    swagger_tags = ['Customer', ]

    def get_queryset(self):

        category = self.request.GET.get('category', '')
        queryset = Cook.objects.distinct()
        if category:
            queryset = queryset.filter(cook_menu_item__category__category_name__icontains=category)

        return queryset

    def get(self, request):
        query = request.GET.get('q')
        if query:
            response = {
                "top_cook": TopCookSerializer(Cook.objects.all()[:5], many=True).data,
                "top_dish": TopDishesSerializer(MenuItem.objects.select_related('category').filter(status=ACTIVE)[:5],
                                                many=True).data,
                "featured_cook": TopCookSerializer(Cook.objects.all()[:5], many=True).data
            }
            return Response(response, status=status.HTTP_200_OK)

        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FSCCatalogueAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated, IsCook)
    serializer_class = FSCCatalogueSerializer
    swagger_tags = ['Food Compliance Catalogue']
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        fsc_type = self.request.query_params.get('fsc_type', 'CS')
        return FSCCatalogue.objects.filter(fsc_type=fsc_type.upper())

    def get_fsc_title(self, fsc):
        if fsc == FSCCatalogue.CS:
            return "Cleaning & Sanitizing"

        if fsc == FSCCatalogue.KM:
            return "Kitchen Maintenance"

        if fsc == FSCCatalogue.FH:
            return "Food Handling"

        if fsc == FSCCatalogue.SF:
            return "Sanitary Facility"

        return ""

    def list(self, request, *args, **kwargs):
        response = super().list(request, args, kwargs)
        fsc_type = self.request.query_params.get('fsc_type', 'CS')
        title = self.get_fsc_title(fsc_type.upper())
        response.data['title'] = title
        response.data['description'] = title
        return response

    def post(self, request, *args, **kwargs):
        """
        Create Cook Food Compliance catalogue Data
        """
        print("I am here")
        print(request.data)
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # fsc_type = serializer.data.get("fsc_type")
        queryset = self.get_queryset()
        serializer = FSCCatalogueSerializer(queryset, many=True)
        data = {
            "images": serializer.data,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class FSCCatalogueImageAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsCook)
    serializer_class = FSCCatalogueImageSerializer
    swagger_tags = ['Food Compliance Catalogue']
    parser_classes = [MultiPartParser]

    def get_queryset(self, fsc_catalogue):
        return FSCCatalogueImage.objects.filter(cook=self.request.user.cook, fsc_catalogue=fsc_catalogue)

    def create(self, request, *args, **kwargs):
        """
        Create Cook Food Compliance catalogue Data
        """
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(cook=self.request.user.cook)
        fsc_catalogue = serializer.data.get("fsc_catalogue")
        queryset = self.get_queryset(fsc_catalogue=fsc_catalogue)
        serializer = FSCCatalogueImageSerializer(queryset, many=True)
        data = {
            "images": serializer.data,
            "count": queryset.count()
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        queryset = get_object_or_404(FSCCatalogueImage, pk=kwargs['id'])
        serializer = FSCCatalogueImageSerializer(queryset, data=request.data, partial=True)
        if serializer.is_valid():
            queryset = serializer.save()
            return Response(FSCCatalogueImageSerializer(queryset).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# from PIL import Image
# import base64
# from google.cloud import aiplatform
# from google.cloud.aiplatform.gapic.schema import predict
import os

os.environ[
    "GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\venky\OneDrive\Desktop\Quytech\Cangurhu\Cangurhu\cangurhu_python\fsc.json"


def predict_image_object_detection_sample(
        project: str,
        endpoint_id: str,
        filename: str,
        object_id: str,
        id: str,
        location: str = "us-central1",
        api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    # The AI Platform services require regional API endpoints.
    # client_options = {"api_endpoint": api_endpoint}
    # Initialize client that will be used to create and send requests.
    # This client only needs to be created once, and can be reused for multiple requests.
    # client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # with open(filename, "rb") as f:
    #     file_content = f.read()
    #
    # # The format of each instance should conform to the deployed model's prediction input schema.
    # encoded_content = base64.b64encode(file_content).decode("utf-8")
    # instance = predict.instance.ImageObjectDetectionPredictionInstance(
    #     content=encoded_content,
    # ).to_value()
    # instances = [instance]
    # # See gs://google-cloud-aiplatform/schema/predict/params/image_object_detection_1.0.0.yaml for the format of the parameters.
    # parameters = predict.params.ImageObjectDetectionPredictionParams(
    #     confidence_threshold=0.5, max_predictions=5,
    # ).to_value()
    # endpoint = client.endpoint_path(
    #     project=project, location=location, endpoint=endpoint_id
    # )
    # response = client.predict(
    #     endpoint=endpoint, instances=instances, parameters=parameters
    # )
    # print("response")
    # print(" deployed_model_id:", response.deployed_model_id)
    # See gs://google-cloud-aiplatform/schema/predict/prediction/image_object_detection_1.0.0.yaml for the format of the predictions.
    # predictions = response.predictions
    predictions = {'displayNames': ['dirty_microwave_oven'], 'confidences': [0.832795203],
                   'ids': ['8177088316735225856'], 'bboxes': [[0.203493953, 0.862704039, 0.239147604, 0.638348758]]}

    # for prediction in predictions:
    #     print(" prediction:", dict(prediction))

    object_names = FSCCatalogue.objects.filter(id=object_id)

    for object_name in object_names:
        print(object_name.name)
        if predictions['displayNames'][0] == object_name.name:
            # FSCCatalogueImage.objects.update(status="Pass")

            FSCCatalogueImage.objects.filter(id=id).update(status="Pass")
        else:

            FSCCatalogueImage.objects.filter(id=id).update(status="Fail")

    return True


class FSC(APIView):
    # parser_classes = [MultiPartParser, ]

    def get(self, request):
        try:

            cook_id = Cook.objects.filter(user_id=self.request.user.user_id)
            queryset = FSCCatalogueImage.objects.filter(
                cook_id=list(cook_id.values_list("id", flat=True))[0])  # self.request.user.cook

            for i in queryset:
                predict_image_object_detection_sample(
                    project="1047982198075",
                    endpoint_id="790513675998855168",
                    location="us-central1",
                    filename=i.image,
                    object_id=i.fsc_catalogue_id,
                    id=i.id
                )
                status = list(FSCCatalogueImage.objects.filter(cook_id=i.cook_id).values("image", "status"))

            return Response({"status": "success", "status_object": status})
        except:
            return Response({"status": "no cook id found", "status_object": None})


class CookOrderPlaceView(APIView):
    permission_classes = (IsAuthenticated, IsCook)
    swagger_tags = ['Cook OrderList']

    """
         Cook Orders list/Detail by order_id
      """

    def get(self, request, order_id=None):
        if order_id:
            order_menu_sub_item = OrderMenuSubItem.objects.filter(
                menu_sub_item__menu_item__cook__id=request.user.cook.id,
                order_menu_item__order__order_id=order_id,
                order_menu_item__order__status="OP"
            ).first()
            if order_menu_sub_item:
                order = Order.objects.filter(id=order_menu_sub_item.order_menu_item.order.id).first()
                if order:
                    serializer = CookOrderSerializer(order)
                else:
                    raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            else:
                raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")

        else:
            order_menu_sub_items = OrderMenuSubItem.objects.filter(
                menu_sub_item__menu_item__cook__id=request.user.cook.id,
                order_menu_item__order__status="OP"
            )
            print("order_menu_sub_items", order_menu_sub_items)

            order_ids = [order_menu_sub_item.order_menu_item.order.id for order_menu_sub_item in order_menu_sub_items]
            print("order_ids", order_ids)
            orders = Order.objects.filter(id__in=order_ids)
            print("orders", orders)
            serializer = CookOrderSerializer(orders, many=True)
        return Response(serializer.data)


class CookFutureOrderPlaceView(APIView):
    permission_classes = (IsAuthenticated, IsCook)
    swagger_tags = ['Cook Future Order List']

    """
         Cook Future Orders list/Detail by order_id
      """

    def get(self, request, order=None):

        if order:
            raise ErrorResponseException("This feature is not developed yet, Please contact with backend developer")
            pass
            # order_details = Order.objects.filter(id=order, is_future_order=True)
            # print("order_details", order_details)
            # if order_details:
            #     serializer = CookFutureOrderSerializer(order_details)
            #     print("serializer", serializer.data)
            # else:
            #     raise ErrorResponseException(f"Order Does not exist with ID '{order}'!")

        else:
            order_menu_sub_items = OrderMenuSubItem.objects.filter(
                menu_sub_item__menu_item__cook__id=request.user.cook.id,
                order_menu_item__order__status="PE",
                order_menu_item__order__is_future_order=True
            )
            order_ids = [order_menu_sub_item.order_menu_item.order.id for order_menu_sub_item in order_menu_sub_items]
            orders = Order.objects.filter(id__in=order_ids, is_future_order=True)
            serializer = CookOrderSerializer(orders, many=True)
            return Response(serializer.data)


class CookAgreeFutureOrderAPIView(APIView):
    permission_classes = (IsAuthenticated, IsCook)
    swagger_tags = ['Cook Future Order Agree']

    """
         Cook Agree on Future Orders
      """

    def put(self, request, id=None):
        print(id)
        if id:
            order = Order.objects.filter(id=id, is_future_order=True).first()
            if order:
                order.is_cook_agree = request.data.get("status")
                print("order", order.is_cook_agree)
                order.save()
            else:
                raise ErrorResponseException(f"Order Does not exist with this ID '{id}'!")
            order = Order.objects.get(is_cook_agree=True, id=id)
            user_id = order.customer.user_id
            print("user_id", user_id)

            user_device_tokens = [store_token.device_token for store_token in
                                  StoreToken.objects.filter(user_id_id=user_id)]
            if user_device_tokens:
                if request.data.get("status"):
                    message = "Cook agreed on your future order. Kindly proceed for the payment. "
                    Notification.objects.create(user_id=user_id, message=message)
                    send_notification(user_device_tokens, 'Cook Agreed on your Order', message)
                    data = {"message": " Data saved and success response sent to customer successfully"}
                    return Response(data, status=status.HTTP_201_CREATED)
                else:
                    message = "Cook denied to agree on your future order. So this order could not be fulfilled. "
                    Notification.objects.create(user_id=user_id, message=message)
                    send_notification(user_device_tokens, 'Cook Denied to accept your Order', message)
                    data = {"message": " Data saved and Order Disagree response sent to customer successfully"}
                    return Response(data, status=status.HTTP_201_CREATED)


# http://127.0.0.1:8000/api/v1/cook/fsc/catalogue/upload/


import redis

r = redis.Redis()


class CookOrderView(APIView):
    permission_classes = (IsAuthenticated, IsCook)
    swagger_tags = ['Cook Order Accept/Canceled']

    """
       Order Accepted or Canceled by Cook
    """

    def put(self, request, order_id=None):
        if order_id:
            order_menu_sub_item = OrderMenuSubItem.objects.filter(
                menu_sub_item__menu_item__cook__id=request.user.cook.id,
                order_menu_item__order__order_id=order_id,
                order_menu_item__order__status="OP"  # order placed
            ).first()
            if order_menu_sub_item:
                order = Order.objects.filter(id=order_menu_sub_item.order_menu_item.order.id).first()
                if order:
                    cook_order_detail = CookOrderDetails.objects.create(cook_id=request.user.cook.id, order_id=order.id,
                                                                        eta=30)  # eta static
                    cook_order_detail.cook_status = request.data.get("status")
                    cook_order_detail.save()
                    order.status = cook_order_detail.cook_status
                    order.save()
                    order_detail = Order.objects.filter(order_id=order.order_id, status="ACK")
                    for order_data in order_detail:
                        order_id = order_data.order_id
                        if order_id:
                            queue = "source"
                            serializer = CookOrderSerializer(order_data)
                            from django.core.serializers.json import DjangoJSONEncoder
                            encoder = DjangoJSONEncoder()
                            session_data = encoder.encode(serializer.data)
                            r.lpush(queue, session_data)
                            # while r.llen(queue) != 0:
                            #     print("queue: \n", r.rpop(queue), "")

                else:
                    raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            else:
                raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            if cook_order_detail.cook_status == "CCK":  # canceled by cook
                cook_order_detail.reason = request.data.get("reason")
                cook_order_detail.save()

            if order.status == "ACK":
                user_id = order.customer.user_id

                user_device_tokens = [store_token.device_token for store_token in
                                      StoreToken.objects.filter(user_id_id=user_id)]
                print("token", user_device_tokens)
                if user_device_tokens:
                    message = ""
                    Notification.objects.create(user_id=user_id, message="your order is accepted")
                    send_notification(user_device_tokens, 'order accepted', 'you order is accepted')

            if order.status == "CCK":
                user_id = order.customer.user_id

                user_device_tokens = [store_token.device_token for store_token in
                                      StoreToken.objects.filter(user_id_id=user_id)]
                print("token", user_device_tokens)
                if user_device_tokens:
                    message = "We are sorry the cook declined your food order for this reason: <reason of cook " \
                              "decline>.  Please order again from other featured cooks in town. "
                    Notification.objects.create(user_id=user_id, message=message)
                    send_notification(user_device_tokens, 'Order Declined', message)

            serializer = CookOrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response({"detail": "order id requires"}, status=status.HTTP_400_BAD_REQUEST)


# FLOW
# 1.ACK/CCK
# 2.PREPARING INGREDIENTS
# 3.FINISHED PREPARING INGREDIENTS
# 4.READY TO COOK

# 2,3,4 WILL BE AUTO
# AFTER 4 COOK MANUALLY CHANGE STATUS TO COOKING IN PROGRESS(CP)

class CookOrderStatusToCooking(APIView):
    permission_classes = (IsAuthenticated, IsCook)
    swagger_tags = ['Cook Order Start Cooking ']

    """
        Order Status to Cooking In Progress by Cook
    """

    def put(self, request, order_id=None):
        if order_id:
            order_menu_sub_item = OrderMenuSubItem.objects.filter(
                menu_sub_item__menu_item__cook__id=request.user.cook.id,
                order_menu_item__order__order_id=order_id,
                order_menu_item__order__status="RCK"  # Ready to cook
            ).first()
            if order_menu_sub_item:
                order = Order.objects.filter(id=order_menu_sub_item.order_menu_item.order.id).first()
                if order:
                    cook_order_detail = CookOrderDetails.objects.filter(cook_id=request.user.cook.id,
                                                                        order_id=order.id).first()
                    if cook_order_detail:
                        cook_order_detail.cook_status = request.data.get("status")
                        cook_order_detail.save()
                    else:
                        raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
                else:
                    raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            else:
                raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            order.status = cook_order_detail.cook_status
            order.save()
            serializer = CookOrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response({"detail": "order id requires"}, status=status.HTTP_400_BAD_REQUEST)


class CookingInProgressListView(APIView):
    permission_classes = (IsAuthenticated,)
    swagger_tags = ['Cook Cooking In Progress List']

    """
         Cooking In Progress Orders List
      """

    def get(self, request, order_id=None):
        if order_id:
            order_menu_sub_item = OrderMenuSubItem.objects.filter(
                menu_sub_item__menu_item__cook__id=request.user.cook.id,
                order_menu_item__order__order_id=order_id,
                order_menu_item__order__status="CP"  # cooking in progress
            ).first()
            if order_menu_sub_item:
                order = Order.objects.filter(id=order_menu_sub_item.order_menu_item.order.id).first()
                if order:
                    serializer = CookOrderSerializer(order)
                else:
                    raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            else:
                raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")

        else:
            order_menu_sub_items = OrderMenuSubItem.objects.filter(
                menu_sub_item__menu_item__cook__id=request.user.cook.id,
                order_menu_item__order__status="CP"  # cooking in progress
            )
            order_ids = [order_menu_sub_item.order_menu_item.order.id for order_menu_sub_item in order_menu_sub_items]
            orders = Order.objects.filter(id__in=order_ids)
            serializer = CookOrderSerializer(orders, many=True)

        return Response(serializer.data)


# COOK CHANGE STATUS MANUALLY TO READY TO PICKUP

class OrderReadyToPickup(APIView):
    permission_classes = (IsAuthenticated, IsCook)
    swagger_tags = ['Cook Order Ready To Pickup ']
    """
         Order Status to Ready to Pickup changed by Cook
     """

    def put(self, request, order_id=None):
        if order_id:
            order_menu_sub_item = OrderMenuSubItem.objects.filter(
                menu_sub_item__menu_item__cook__id=request.user.cook.id,
                order_menu_item__order__order_id=order_id,
                order_menu_item__order__status="CP"
            ).first()
            if order_menu_sub_item:
                order = Order.objects.filter(id=order_menu_sub_item.order_menu_item.order.id).first()
                if order:
                    cook_order_detail = CookOrderDetails.objects.filter(cook_id=request.user.cook.id,
                                                                        order_id=order.id).first()
                    if cook_order_detail:
                        cook_order_detail.cook_status = request.data.get("status")
                        cook_order_detail.save()
                else:
                    raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            else:
                raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            order.status = cook_order_detail.cook_status
            order.save()
            serializer = CookOrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response({"detail": "order id requires"}, status=status.HTTP_400_BAD_REQUEST)


class ReadyToPickupListView(APIView):
    permission_classes = (IsAuthenticated,)
    swagger_tags = ['Cook Ready To Pickup List']

    """
        Ready To Pickup Orders List/Detail by order_id
      """

    def get(self, request, order_id=None):
        if order_id:
            order_menu_sub_item = OrderMenuSubItem.objects.filter(
                menu_sub_item__menu_item__cook__id=request.user.cook.id,
                order_menu_item__order__order_id=order_id,
                order_menu_item__order__status="RE"  # READY
            ).first()
            if order_menu_sub_item:
                order = Order.objects.filter(id=order_menu_sub_item.order_menu_item.order.id).first()
                if order:
                    serializer = CookOrderSerializer(order)
                else:
                    raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            else:
                raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
        else:
            order_menu_sub_items = OrderMenuSubItem.objects.filter(
                menu_sub_item__menu_item__cook__id=request.user.cook.id,
                order_menu_item__order__status="RE"  # READY
            )
            order_ids = [order_menu_sub_item.order_menu_item.order.id for order_menu_sub_item in order_menu_sub_items]
            orders = Order.objects.filter(id__in=order_ids)
            serializer = CookOrderSerializer(orders, many=True)

        return Response(serializer.data)


class CookPastOrderListView(APIView):
    permission_classes = (IsAuthenticated, IsCook)
    swagger_tags = ['Cook Past Order List']

    """
         Past Order(Orders that are delivered) list/Detail by order_id
      """

    def get(self, request, order_id=None):
        if order_id:
            order_menu_sub_item = OrderMenuSubItem.objects.filter(
                menu_sub_item__menu_item__cook__id=request.user.cook.id,
                order_menu_item__order__order_id=order_id,
                order_menu_item__order__status="DE"
            ).first()
            if order_menu_sub_item:
                order = Order.objects.filter(id=order_menu_sub_item.order_menu_item.order.id).first()
                if order:
                    serializer = CookOrderSerializer(order)
                else:
                    raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")
            else:
                raise ErrorResponseException(f"Order Does not exist with Order ID '{order_id}'!")

        else:
            order_menu_sub_items = OrderMenuSubItem.objects.filter(
                menu_sub_item__menu_item__cook__id=request.user.cook.id,
                order_menu_item__order__status="DE"
            )
            order_ids = [order_menu_sub_item.order_menu_item.order.id for order_menu_sub_item in order_menu_sub_items]
            orders = Order.objects.filter(id__in=order_ids)
            serializer = CookOrderSerializer(orders, many=True)

        return Response(serializer.data)
