import decimal

from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.address.models import Address, AddressCategory, AddCard, Cook, MenuCategory
from apps.order.models import Order, OrderMenuItem, OrderMenuSubItem
from apps.cart.models import CartMenuItem, MenuItem, CartMenuSubItem, Cart
from apps.cook.models import CookOrderDetails
from apps.courier.models import CourierOrder
from apps.address.api.serializers import AddressSerializer, AddressDetailSerializer
from common.exception import ErrorResponseException
from apps.address.api.serializers import AddressSerializer, AddressCategorySerializer, AddressAVserializer, \
    AddCardSerializer, CookSerializer, OrderSerializer, CookOrderSerializer, CourierOrderSerializer


class CookAPIView(APIView): # TestingAPI Cook
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user.user_id
        payload = request.data
        payload['user'] = user
        serializer = CookSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def get(self, request):
        user = request.user.user_id
        cook_list = Cook.objects.get(user=user)
        serializer = CookSerializer(cook_list)
        return Response(serializer.data)


class CookDetailAPI(APIView):
    def get(self, request, pk):
        user = request.user.user_id
        try:
            cook_list = Cook.objects.get(user=user, id=pk)
        except Cook.DoesNotExist:
            raise ErrorResponseException("Cook Not Available")
        serializer = CookSerializer(cook_list)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user.user_id
        payload = request.data
        try:
            cook_detail = Cook.objects.get(user=user, id=pk)
        except Cook.DoesNotExist:
            raise ErrorResponseException("cook not found")
        serializer = CookSerializer(cook_detail, data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        user = request.user.user_id
        try:
            cook_detail = Cook.objects.get(user=user, id=pk)
        except Cook.DoesNotExist:
            raise ErrorResponseException("cook datail not available")
        cook_detail.delete()
        return Response(status=status.HTTP_200_OK)

class AddressAV(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user_id = request.user.user_id
        payload = request.data
        payload['user_id'] = user_id
        serializer = AddressAVserializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def get(self, request):
        user_id = request.user.user_id
        address_list = Address.objects.filter(user_id=user_id)
        serializer = AddressAVserializer(address_list, many=True)
        return Response(serializer.data)


class AddressDetailAV(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user_id = request.user.user_id
        try:
            address = Address.objects.get(user_id=user_id, address_id=pk)
        except Address.DoesNotExist:
            raise ErrorResponseException("Address not Available")
        serializer = AddressAVserializer(address)
        return Response(serializer.data)

    def put(self, request, pk):
        user_id = request.user.user_id
        payload = request.data
        #payload['user_id'] = user_id
        try:
            address = Address.objects.get(user_id=user_id, address_id=pk)
        except:
            raise ErrorResponseException("address not available")
        serializer = AddressAVserializer(address, data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    def delete(self, request, pk):
        user_id = request.user.user_id
        address = Address.objects.get(address_id=pk, user_id=user_id)
        address.delete()
        return Response(status=status.HTTP_200_OK)


class AddressAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = AddressSerializer
    queryset = Address.objects.all()
    swagger_tags = ['User']

    def get_queryset(self):
        user_id = self.request.user
        addresses = Address.objects.filter(user_id=user_id)
        return addresses

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user_id=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AddressDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, address_id):
        """
            To get the particular Address of user
        """

        user_id = request.user.user_id

        try:
            address = Address.objects.get(address_id=address_id, user_id=user_id)

        except Address.DoesNotExist:
            raise ErrorResponseException(f"Address is not available!")

        serializer = AddressDetailSerializer(address)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, address_id):
        """
            To update the particular Address of user
        """
        payload = request.data
        user_id = request.user.user_id

        try:
            address = Address.objects.get(address_id=address_id, user_id=user_id)

        except Address.DoesNotExist:
            raise ErrorResponseException(f"Address is not available!")

        serializer = AddressDetailSerializer(
            instance=address,
            data=payload,
            partial=True
        )
        if serializer.is_valid():
            addresses = Address.objects.filter(user_id=user_id)
            is_default = payload.get('is_default')
            if is_default in ['True', 'true', True]:
                for existing_address in addresses:
                    existing_address.is_default = False
                    existing_address.save()
            serializer.save()
        else:
            raise ErrorResponseException(str(serializer.errors))

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, address_id):
        """
            To Delete the particular Address of customer
        """

        user_id = request.user.user_id

        try:
            address = Address.objects.get(address_id=address_id, user_id=user_id)

        except Address.DoesNotExist:
            raise ErrorResponseException(f"Address is not available!")

        address.delete()

        return Response(
            status=status.HTTP_200_OK
        )


class AddressCategoryView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        """
            Get all the Address Category
        """

        queryset = AddressCategory.objects.filter(is_active=True)

        serializer = AddressCategorySerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CourierOrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, order_id):
        courier = request.user.courier
        payload = request.data
        courier_status = payload.get('courier_status')

        if (not courier_status) or (courier_status not in ["ACR", "CCR"]):
            raise ErrorResponseException("courier status not given or invalid")
        order = Order.objects.get(id=order_id)
        courier_order = CourierOrder.objects.create(courier=courier, order=order, courier_status=courier_status)
        courier_order.save()
        order.status = courier_status
        if courier_status == 'CCR':
            courier_order.reason = payload.get('reason')
        order.save()
        serializer = CourierOrderSerializer(courier_order)
        return Response(serializer.data)


class CookOrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, order_id):
        cook = request.user.cook
        payload = request.data
        cook_status = payload.get('cook_status')
        if not cook_status or cook_status not in ['ACK','CCK']:
            raise ErrorResponseException("cook status not given or invalid")
        order = Order.objects.get(id=order_id)
        cook_order = CookOrderDetails.objects.create(cook=cook, order=order, cook_status=cook_status)
        cook_order.save()
        order.status = cook_status
        if cook_status == 'ACK':
            order.is_cook_agree = True
        else:
            order.is_cook_agree = False
            cook_order.reason = 'cook is busy or not available'
            cook_order.save()
        order.save()

        serializer = CookOrderSerializer(cook_order)

        return Response(serializer.data)


class OrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        customer = request.user.customer.id
        user_id = request.user.user_id
        payload = request.data
        payload['customer'] = customer
        customer_address = Address.objects.get(user_id=user_id, is_default=True)

        payload['customer_address'] = customer_address.address_id
        cart = request.user.customer.cart.id
        cart_menu_item = CartMenuItem.objects.filter(cart=cart).first()
        cook = cart_menu_item.menu_item.cook.user.user_id
        cook_address = Address.objects.get(user_id=cook, is_default=True)
        payload['cook_address'] = cook_address.address_id
        serializer = OrderSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class OrderUpdateAPIView(APIView):

    def put(self, request, pk):
        customer = request.user.customer.id
        payload = request.data
        try:
            order_receipt = Order.objects.get(customer=customer, id=pk)
        except Order.DoesnotExist:
            raise ErrorResponseException({"order Detail not available"})
        serializer = OrderSerializer(order_receipt, data=payload)
        if serializer.is_valid():
            serializer.save()
            payment_status = payload['payment_details']['status']
            if payment_status == "PaymentIntentsStatus.Succeeded":
                cart_menu_items = CartMenuItem.objects.filter(cart__customer=customer)
                if cart_menu_items:
                    for cart_menu_item in cart_menu_items:

                        mi_id = cart_menu_item.menu_item
                        cart_quantity = cart_menu_item.quantity[0]

                        cart_menu_size = cart_quantity.get('size')
                        cart_menu_count = cart_quantity.get('count')
                        menu_items = cart_menu_item.menu_item.size
                        for items in menu_items:
                            menu_item_size = items.get('size')
                            if cart_menu_size == menu_item_size:
                                menu_item_price = items.get('price')
                                total_price = menu_item_price * cart_menu_count
                                final_price = decimal.Decimal(total_price).quantize(decimal.Decimal('0.00'))
                                order_menu_item = OrderMenuItem.objects.create(order=order_receipt, menu_item=mi_id, quantity=cart_quantity, price=final_price)
                                order_menu_item.save()

                                cart_sub_menu_items = CartMenuSubItem.objects.filter(cart_menu_item=cart_menu_item)
                                if cart_sub_menu_items:
                                    for cart_sub_menu_item in cart_sub_menu_items:
                                        sub_menu_item = cart_sub_menu_item.sub_menu_item
                                        sub_menu_item_price = sub_menu_item.price
                                        order_sub_menu_item = OrderMenuSubItem.objects.create(menu_sub_item=sub_menu_item, order_menu_item=order_menu_item, price=sub_menu_item_price)
                                        order_sub_menu_item.save()

            cart = Cart.objects.get(customer=customer)
            cart_total = cart.total
            order_receipt.sub_total = cart_total
            order_receipt.save()
            cart_menu_items.delete()
            cart.total = 0
            cart.count = 0
            cart.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class AddCardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user.user_id
        payload = request.data
        payload['user'] = user
        serializer = AddCardSerializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def get(self, request):
        user = request.user.user_id
        card_detail = AddCard.objects.filter(user=user)
        serializer = AddCardSerializer(card_detail, many=True)
        return Response(serializer.data)


class AddCardDetail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = request.user.user_id
        try:
            card_detail = AddCard.objects.get(user=user, id=pk)
        except:
            raise ErrorResponseException("card detail not available")
        serializer = AddCardSerializer(card_detail)
        return Response(serializer.data)

    def put(self, request, pk):
        user = request.user.user_id
        payload = request.data
        payload['user'] = user
        try:
            card_detail = AddCard.objects.get(user=user, id=pk)
        except AddCard.DoesNotExist:
            raise ErrorResponseException("card detail not Exist")
        serializer = AddCardSerializer(card_detail, data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        user = request.user.user_id
        card_detail = AddCard.objects.get(user=user, id=pk)
        card_detail.delete()
        return Response(f"card has been Deleted ")






