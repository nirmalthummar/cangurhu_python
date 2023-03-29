from rest_framework import status
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.cart.models import CartMenuItem, Cart, CartMenuSubItem
from apps.customer.api.serializers import CustomerOrderListSerializer

from apps.order.api.serializers import (OrderSerializer, OrderMenuItemSerializer, CookOrderMenuItemSerializer,
                                        FutureOrderSerializer)

from apps.order.api.serializers import (OrderSerializer, OrderMenuItemSerializer)
from apps.order.models import (Order, OrderMenuItem, OrderMenuSubItem)
from common.exception import ErrorResponseException

from core.permissions import IsCustomer
from apps.cart.api.serializers import CartItemSerializer
from apps.cook.models import MenuItem, MenuSubItem

# Order Calculation
from apps.order.api.service import delete_cache_order, OrderCalculation, get_user_default_address

from apps.address.models import Address


class OrderView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)
    swagger_tags = ['Order']

    # parser_classes = [MultiPartParser]


    def get(self, request, id=None):
        if id is None:
            order_details = Order.objects.filter(customer_id=request.user.customer.id)
            serializer = CustomerOrderListSerializer(order_details, many=True)
        else:
            try:
                order_details = Order.objects.get(customer_id=request.user.customer.id, id=id)
            except:
                return Response({"detail": 'Order not Found'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = CustomerOrderListSerializer(order_details)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = request.data

        delete_cache_order(user)

        serializer = OrderSerializer(data=data)

        if serializer.is_valid():
            customer_address = get_user_default_address(user)
            serializer.save(customer_id=user.customer.id, customer_address_id=customer_address.address_id)

            last_order = Order.objects.filter(customer_id=user.customer.id).last()

            if last_order:
                order = OrderCalculation(user=user, order=last_order)
                order.create_order_items()
                updated_order = order.get_order_calculation()
            else:
                raise ErrorResponseException("Order is not exist!")

            serializer = OrderSerializer(updated_order, many=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        if id is not None:
            order_detail = Order.objects.filter(customer_id=request.user.customer.id, id=id).first()
            if order_detail:
                serializer = OrderSerializer(order_detail, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    if order_detail.order_id:
                        cart_delete_menu_sub_item = CartMenuSubItem.objects.filter(
                            cart_menu_item_id__cart_id__customer_id=request.user.customer.id)
                        if cart_delete_menu_sub_item:
                            cart_delete_menu_sub_item.delete()
                            cart_delete_menu_item = CartMenuItem.objects.filter(
                                cart_id__customer_id=request.user.customer.id)
                            if cart_delete_menu_item:
                                cart_delete_menu_item.delete()
                                cart_empty = Cart.objects.get(customer_id=request.user.customer.id)
                                if cart_empty:
                                    cart_empty.count = 0
                                    cart_empty.total = 0.00
                                    cart_empty.save()

                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "order_id doesnt exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "order id requires"}, status=status.HTTP_400_BAD_REQUEST)


class FutureOrderAPIView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)
    swagger_tags = ['Order']

    # parser_classes = [MultiPartParser]

    def get(self, request, id=None):
        if id is None:
            order_details = Order.objects.filter(customer_id=request.user.customer.id)
            serializer = CustomerOrderListSerializer(order_details, many=True)
        else:
            try:
                order_details = Order.objects.get(customer_id=request.user.customer.id, id=id)
            except:
                return Response({"detail": 'Order not Found'}, status=status.HTTP_400_BAD_REQUEST)

            serializer = CustomerOrderListSerializer(order_details)
        return Response(serializer.data)

    def post(self, request):
        # check_order_menu_sub_item = OrderMenuSubItem.objects.filter(
        #     order_menu_item__order__customer_id=request.user.customer.id, order_menu_item__order__status='PE',
        #     order_menu_item__order__amount_paid='pending', order_menu_item__order__is_future_order=False)

        # if check_order_menu_sub_item:
        #     check_order_menu_sub_item.delete()
        #     check_order_menu_item = OrderMenuItem.objects.filter(
        #         order__customer_id=request.user.customer.id, order__status='PE',
        #         order__amount_paid='pending')
        #     if check_order_menu_item:
        #         check_order_menu_item.delete()
        #         check_order = Order.objects.filter(
        #             customer_id=request.user.customer.id, status='PE', amount_paid='pending',
        #             order_menu_item__order__is_future_order=False)
        #
        #         if check_order:
        #             check_order.delete()
        serializer = FutureOrderSerializer(data=request.data)

        if serializer.is_valid():
            address = Address.objects.filter(user_id=request.user.user_id, is_default=True).first()
            if address:
                serializer.save(customer_id=request.user.customer.id, address_id=address.address_id)
            else:
                return Response({"detail": "No default address of current user"}, status=status.HTTP_400_BAD_REQUEST)
            order_detail = Order.objects.filter(customer_id=request.user.customer.id).last()
            if order_detail:
                cart_menu_items = CartMenuItem.objects.filter(cart_id=request.user.customer.cart.id)

                if cart_menu_items:
                    for cart_menu_item in cart_menu_items:
                        menu_item_id = cart_menu_item.menu_item.id
                        quantity = cart_menu_item.quantity
                        price = Decimal(0.0)

                        future_order = cart_menu_item.is_future_order
                        order_date = cart_menu_item.order_date

                        for q in quantity:
                            size = q.get('size')
                            count = q.get('count', 1)
                            for item in cart_menu_item.menu_item.size:
                                if size == item.get('size'):
                                    menu_item_price = item.get('price') * count
                                    price += menu_item_price
                        order_menu_item_id = OrderMenuItem.objects.create(order_id=order_detail.id,
                                                                          menu_item_id=menu_item_id,
                                                                          price=price,
                                                                          quantity=quantity)
                        # saving future order data in order table
                        order_detail.is_future_order = future_order
                        order_detail.order_date = order_date
                        order_detail.save()

                        cart_sub_item = CartMenuSubItem.objects.filter(cart_menu_item_id=cart_menu_item.id)
                        if cart_sub_item:
                            for sub_item in cart_sub_item:
                                submenu_id = sub_item.sub_menu_item_id
                                submenu_price = sub_item.sub_menu_item.price
                                OrderMenuSubItem.objects.create(menu_sub_item_id=submenu_id,
                                                                order_menu_item_id=order_menu_item_id.id,
                                                                price=submenu_price)
                        else:
                            return Response({"detail": " menu sub item  requires in cart"},
                                            status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"detail": " menu item  requires in cart"}, status=status.HTTP_400_BAD_REQUEST)

            cart_total = Cart.objects.get(customer_id=request.user.customer.id)

            order_detail.sub_total = cart_total.total
            order_detail.save()

            # Send notification to cook
            order_id = Order.objects.filter(customer_id=request.user.customer.id).last()
            # menu_item_id = OrderMenuItem.objects.filter(order_id=order_id).values_list('menu_item_id', flat=True)
            # cook_id = MenuItem.objects.filter(menu_item_id=menu_item_id).values_list('cook_id', flat=True)

            print("order_id", order_id, "menu_item_id", "cook_id")
            # OrderMenuItem.objects.filter(order_id__)
            # if order.is_future_order:
            #     user_id = order.customer.user_id
            #
            #     user_device_tokens = [store_token.device_token for store_token in
            #                           StoreToken.objects.filter(user_id_id=user_id)]
            #     print("token", user_device_tokens)
            # if user_device_tokens:
            #     message = ""
            #     Notification.objects.create(user_id=user_id, message="your order is accepted")
            #     send_notification(user_device_tokens, 'order accepte0d', 'you order is accepted')

            serializer = FutureOrderSerializer(order_detail, many=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        if id is not None:
            order_detail = Order.objects.filter(customer_id=request.user.customer.id, id=id).first()
            if order_detail:
                serializer = OrderSerializer(order_detail, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    if order_detail.order_id:
                        cart_delete_menu_sub_item = CartMenuSubItem.objects.filter(
                            cart_menu_item_id__cart_id__customer_id=request.user.customer.id)
                        if cart_delete_menu_sub_item:
                            cart_delete_menu_sub_item.delete()
                            cart_delete_menu_item = CartMenuItem.objects.filter(
                                cart_id__customer_id=request.user.customer.id)
                            if cart_delete_menu_item:
                                cart_delete_menu_item.delete()
                                cart_empty = Cart.objects.get(customer_id=request.user.customer.id)
                                if cart_empty:
                                    cart_empty.count = 0
                                    cart_empty.total = 0.00
                                    cart_empty.save()

                    return Response(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail": "order_id doesnt exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "order id requires"}, status=status.HTTP_400_BAD_REQUEST)


def FutureOrderPayment(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)
    swagger_tags = ['Order']


class OrderMenuItemView(APIView):
    permission_classes = (IsAuthenticated,)
    swagger_tags = ['Order']

    def get(self, request, id=None):
        if id is None:
            order_details = OrderMenuItem.objects.all()
            serializer = OrderMenuItemSerializer(order_details, many=True)
        else:

            order_details = OrderMenuItem.objects.filter(id=id).first()
            serializer = OrderMenuItemSerializer(order_details)

        return Response(serializer.data)

    def post(self, request):
        serializer = OrderMenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReOrderAPIView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)
    # swagger_tags = ['Order']

    parser_classes = [MultiPartParser]

    def post(self, request):

        order_id = request.data.get('order_id')
        order_id = str(order_id)
        try:
            order_details = Order.objects.get(customer_id=request.user.customer.id, order_id=order_id)
            if order_details:

                # print("order_details", order_details)
                serializer = CustomerOrderListSerializer(order_details)
                data = serializer.data
                # order_details_data = data['order_detail']
                for i in data['order_detail']:
                    menu_item_code = i['order_menu_items']['item_number']
                    quantity = i['order_menu_items']['quantity']
                    sub_menu_title = i['order_menu_sub_items'][0]['title']

                    menu_id = MenuItem.objects.values_list('id', flat=True).filter(item_number=menu_item_code)[0]

                    sub_menu_id = MenuSubItem.objects.filter(menu_item_id=menu_id).values_list('id', flat=True)[0]

                    data = {"menu_item": menu_id,
                            "quantity": quantity,
                            "cart_sub_menu": [{"id": sub_menu_id}],
                            "is_future_order": False,
                            "save_for_later": False,
                            }

                    obj = CartItemSerializer(data=data, context={'request': request})
                    if obj.is_valid():
                        obj.save()
                    else:
                        print(obj.errors)

                    print("-----------------------")

                return Response({"Items Added To cart successfully"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": 'Order not Found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e)


import redis

r = redis.Redis()


class PushDataToRedis(APIView):
    def post(self, request):
        order = Order.objects.filter(status='ACK')
        if order:
            queue = "source"
            accepted_order = order
            r.lpush(queue, accepted_order)
            while r.llen(queue) != 0:
                print(r.rpop(queue))
        else:
            return Response({"No New orders to push in redis"}, status=status.HTTP_201_CREATED)

        return Response({"Data successfully pushed"}, status=status.HTTP_201_CREATED)
