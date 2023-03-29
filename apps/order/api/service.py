import haversine as hs
from haversine import Unit

from decimal import Decimal
from rest_framework import status

from apps.cart.models import CartMenuItem, Cart, CartMenuSubItem
from apps.order.models import OrderMenuSubItem, OrderMenuItem, Order
from apps.address.models import Address
from common.exception import ErrorResponseException


def delete_cache_order(user):

    check_order_menu_sub_item = OrderMenuSubItem.objects.filter(
        order_menu_item__order__customer_id=user.customer.id, order_menu_item__order__status='PE',
        order_menu_item__order__amount_paid='pending')

    if check_order_menu_sub_item:
        check_order_menu_sub_item.delete()
        check_order_menu_item = OrderMenuItem.objects.filter(
            order__customer_id=user.customer.id, order__status='PE', order__amount_paid='pending')
        if check_order_menu_item:
            check_order_menu_item.delete()
            check_order = Order.objects.filter(
                customer_id=user.customer.id, status='PE', amount_paid='pending')

            if check_order:
                check_order.delete()


def get_user_default_address(user_id):
    address = Address.objects.filter(user_id=user_id, is_default=True).first()
    if not address:
        raise ErrorResponseException("No default address of current user!")
    return address


def get_distance(address1, address2):

    address1_lat = address1.latitude
    address1_lon = address1.longitude
    address2_lat = address2.latitude
    address2_lon = address2.longitude

    if not address1_lat:
        raise ErrorResponseException(f"User '{address1.user_id}' latitude is missing!")

    if not address1_lon:
        raise ErrorResponseException(f"User '{address1.user_id}' longitude is missing!")

    if not address2_lat:
        raise ErrorResponseException(f"User '{address2.user_id}' latitude is missing!")

    if not address2_lon:
        raise ErrorResponseException(f"User '{address2.user_id}' longitude is missing!")

    address1 = (float(address1_lat), float(address1_lon))
    address2 = (float(address2_lat), float(address2_lon))

    distance = hs.haversine(address1, address2)

    if not distance:
        raise ErrorResponseException(f"Unable to find the distance b/w {address1} and {address2}")

    distance = float("{:.2f}".format(distance))

    return distance


class OrderCalculation:

    def __init__(self, user, order):
        self.user = user
        self.order = order

    def get_cook_address(self):
        cart_menu_item = CartMenuItem.objects.filter(cart_id=self.user.customer.cart.id).first()
        if cart_menu_item:
            cook_user_id = cart_menu_item.menu_item.cook.user
            if cook_user_id:
                address = get_user_default_address(cook_user_id)
            else:
                raise ErrorResponseException("Cook is not exist!")
        else:
            raise ErrorResponseException("Cart is empty!")
        return address

    def get_customer_address(self):
        address = get_user_default_address(self.user.user_id)
        return address

    def calculate_shipping_charges(self, distance):
        shipping = 0.00
        courier_minimum_pay_rate = 0.60  # This needs to get from the App configuration parameters
        shipping = float("{:.2f}".format(distance * courier_minimum_pay_rate))
        return shipping

    def get_sub_total(self):
        try:
            cart = Cart.objects.get(customer_id=self.user.customer.id)
        except Cart.DoesNotExist:
            raise ErrorResponseException("Cart is not exist for this user!", status_code=status.HTTP_404_NOT_FOUND)
        cart_total = float(cart.total)
        return cart_total

    def create_order_items(self):
        cart_menu_items = CartMenuItem.objects.filter(cart_id=self.user.customer.cart.id)
        if cart_menu_items:
            for cart_menu_item in cart_menu_items:
                menu_item_id = cart_menu_item.menu_item.id
                quantity = cart_menu_item.quantity
                price = Decimal(0.0)
                for q in quantity:
                    size = q.get('size')
                    count = q.get('count', 1)
                    for item in cart_menu_item.menu_item.size:
                        if size == item.get('size'):
                            menu_item_price = item.get('price') * count
                            price += menu_item_price
                order_menu_item_id = OrderMenuItem.objects.create(order_id=self.order.id,
                                                                  menu_item_id=menu_item_id,
                                                                  price=price,
                                                                  quantity=quantity)
                cart_sub_item = CartMenuSubItem.objects.filter(cart_menu_item_id=cart_menu_item.id)
                if cart_sub_item:
                    for sub_item in cart_sub_item:
                        submenu_id = sub_item.sub_menu_item_id
                        submenu_price = sub_item.sub_menu_item.price
                        OrderMenuSubItem.objects.create(menu_sub_item_id=submenu_id,
                                                        order_menu_item_id=order_menu_item_id.id,
                                                        price=submenu_price
                                                        )
                else:
                    raise ErrorResponseException("Menu sub item requires in cart")
        else:
            raise ErrorResponseException("Menu item requires in cart")

    def get_order_calculation(self):
        customer_address = self.get_customer_address()
        cook_address = self.get_cook_address()

        distance = get_distance(customer_address, cook_address)

        sub_total = self.get_sub_total()
        shipping = self.calculate_shipping_charges(distance)
        grand_total = sub_total + shipping

        self.order.shipping = shipping
        self.order.sub_total = sub_total
        self.order.grand_total = grand_total
        self.order.cook_address = cook_address
        self.order.distance = distance
        self.order.save()
        return self.order


