from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.customer.models import Customer
from core.permissions import IsCustomer, IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from apps.cart.models import Cart, CartMenuItem, CartMenuSubItem
from rest_framework.response import Response

from apps.cart.api.serializers import CartItemSerializer, CartSerializer

from rest_framework.views import APIView
from common.exception import ErrorResponseException
from rest_framework.exceptions import APIException
from apps.cook.models import MenuItem, MenuSubItem
import decimal

class CartItemRemoveAV(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)

    def delete(self, request, pk):
        menu_item = CartMenuItem.objects.get(pk=pk)
        menu_item.delete()
        return Response({"id": pk},status=status.HTTP_204_NO_CONTENT)


class CartItemAV(APIView):
    permission_classes = (IsAuthenticated, IsCustomer)

    def post(self, request):
        payload = request.data
        customer_id = request.user.customer

        cart, __ = Cart.objects.get_or_create(customer=customer_id)

        menu_item_id = payload.get('menu_item')
        if not menu_item_id:
            raise ErrorResponseException("Menu item is not in the payload!")

        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)
        except MenuItem.DoesNotExist:
            raise ErrorResponseException("Menu item is not exist!")

        quantity = payload.get('quantity')
        if not quantity:
            raise ErrorResponseException("Quantity is not exist!")

        cook_id = menu_item.cook.cook_id
        cart_items = CartMenuItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            cart_cook_id = cart_item.menu_item.cook.cook_id
            if cart_cook_id != cook_id:
                cart_item.delete()

        try:
            cart_menu_item = CartMenuItem.objects.get(menu_item=menu_item, cart=cart)
        except CartMenuItem.DoesNotExist:
            cart_menu_item = CartMenuItem.objects.create(menu_item=menu_item, cart=cart, quantity=quantity)

        cart_sub_menu_item_ids = payload.get('cart_sub_menu')
        if cart_sub_menu_item_ids:
            for sub_menu_item in cart_sub_menu_item_ids:
                try:
                    sub_menu = MenuSubItem.objects.get(id=sub_menu_item)
                except MenuSubItem.DoesNotExist:
                    raise ErrorResponseException(f"Sub menu item {sub_menu_item} not exist!")

                sub_menu_items = MenuSubItem.objects.filter(menu_item=menu_item)
                if sub_menu_items:
                    item_ids = []
                    for item in sub_menu_items:
                        item_ids.append(item.id)
                    if sub_menu.id not in item_ids:
                        raise ErrorResponseException("sub menu item not in menu item")

                try:
                    cart_menu_sub_menu_ = CartMenuSubItem.objects.get(cart_menu_item=cart_menu_item, sub_menu_item=sub_menu)
                except CartMenuSubItem.DoesNotExist:
                    cart_menu_sub_menu_ = CartMenuSubItem.objects.create(cart_menu_item=cart_menu_item, sub_menu_item=sub_menu)

        queryset = CartMenuItem.objects.filter(cart=cart)
        total_price = 0
        for cart_menu_object in queryset:
            cart_quantity = cart_menu_object.quantity[0]
            cart_menu_size = cart_quantity.get('size')
            cart_menu_count = cart_quantity.get('count')

            menu_item_sizes = cart_menu_object.menu_item.size
            for menu_item_size in menu_item_sizes:
                item_size = menu_item_size.get('size')
                if item_size == cart_menu_size:
                    menu_item_price = menu_item_size.get('price')
                    total_menu_item_price = menu_item_price * cart_menu_count
                    total_price = total_price + total_menu_item_price

            cart_sub_menu_item_object = CartMenuSubItem.objects.filter(cart_menu_item=cart_menu_object.id)
            for cart_sub_menu_item in cart_sub_menu_item_object:
                cart_sub_menu_item_price = cart_sub_menu_item.sub_menu_item.price

        final_price = decimal.Decimal(total_price).quantize(decimal.Decimal('0.00'))
        print("total_price", final_price)

        cart.count = len(queryset)
        cart.total = final_price
        cart.save()
        serializer = CartItemSerializer(queryset, many=True)

        return Response(serializer.data)

    def get(self, request):
        menu_item = CartMenuItem.objects.all()
        serializer = CartItemSerializer(menu_item, many=True)
        return Response(serializer.data)


class CartItemAPIView(generics.ListCreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated, IsCustomer)
    swagger_tags = ['Cart']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_future_order']

    def get_queryset(self):
        return CartMenuItem.objects.select_related('cart', 'cart__customer').filter(cart__customer=self.request.user.customer)


class CartItemRemoveAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, IsCustomer)
    swagger_tags = ['Cart']

    def get_queryset(self):
        return CartMenuItem.objects.select_related('cart__customer').filter(cart__customer=self.request.user.customer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        _id = instance.id
        self.perform_destroy(instance)
        return Response({"id": _id}, status=status.HTTP_204_NO_CONTENT)


class CartItemUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated, IsCustomer)
    swagger_tags = ['Cart']

    def get_queryset(self):
        return CartMenuItem.objects.select_related('cart__customer').filter(cart__customer=self.request.user.customer)


class CartAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated, IsCustomer,)
    swagger_tags = ['Cart']

    def get_cart(self):

        try:
            cart, __ = Cart.objects.get_or_create(customer=self.request.user.customer)
            return cart
        except Exception as e:
            print(str(e))

    def get_queryset(self):
        cart = self.get_cart()
        return cart

    def get_object(self):
        cart = self.get_cart()
        return cart


class MoveToCartView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer,)

    def get(self, request, cart_menu_item_id):
        """
            Move to Cart or Save For Later menu item
        """
        query_params = request.GET

        customer = self.request.user.customer

        save_for_later = query_params.get('save_for_later')
        if save_for_later in ["True", "true", True]:
            save_for_later = True
        elif save_for_later in ["False", "false", False]:
            save_for_later = False
        else:
            raise ErrorResponseException("Save for later params is missing or not correct", status_code=status.HTTP_400_BAD_REQUEST)

        cart_item = None
        try:
            cart_item = CartMenuItem.objects.get(id=cart_menu_item_id)

        except CartMenuItem.DoesNotExist:
            raise ErrorResponseException("The menu item in not available in cart", status_code=status.HTTP_400_BAD_REQUEST)

        cart_item.save_for_later = save_for_later
        cart_item.save()

        queryset = CartMenuItem.objects.select_related('cart', 'cart__customer').filter(cart__customer=customer)

        serializer = CartItemSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# This is not in use
class CartItemView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer,)

    def post(self, request):
        """
            Add items in the Cart
        """
        item_data = request.data

        if len(item_data) == 0:
            raise ErrorResponseException("Payload is missing", status_code=status.HTTP_400_BAD_REQUEST)

        cook_id = item_data.get('cook_id')
        if not cook_id:
            raise ErrorResponseException("Cook id is empty", status_code=status.HTTP_400_BAD_REQUEST)

        menu_items = CartMenuItem.objects.select_related('cart', 'cart__customer').filter(cart__customer=self.request.user.customer)
        print("items are...", menu_items)

        if menu_items:
            print("if items")
        else:

            print("no items")

        return Response(
            "Menu items has been successfully added in the cart",
            status=status.HTTP_201_CREATED
        )
