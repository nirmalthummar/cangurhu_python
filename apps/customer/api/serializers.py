from rest_framework import serializers

from apps.address.api.serializers import AddressSerializer
from apps.cook.models import CookOrderDetails
from apps.courier.models import CourierOrder
from apps.customer.models import Customer, CustomerOrder
from apps.order.api.serializers import CookOrderMenuItemSerializer

from apps.order.models import Order, OrderMenuItem


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    mobile_number = serializers.CharField(source='user.mobile_number', read_only=True)

    class Meta:
        model = Customer
        fields = "__all__"


class CustomerOrderListSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    customer_default_address = AddressSerializer(source='customer_address', read_only=True)
    cook_default_address = AddressSerializer(source='cook_address', read_only=True)
    courier_id = serializers.SerializerMethodField()
    order_detail = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'customer', 'customer_name', 'customer_default_address', 'order_id','cook_default_address', 'courier_id', 'order_detail', 'status',
            'created_at',
            'updated_at'
            , 'tip_amount', 'tip_type', 'sub_total', 'shipping', 'total'
            , 'discount', 'grand_total', 'cook_instruction', 'courier_instruction'

        )

    def get_customer_name(self, obj):
        return obj.customer.user.username

    def get_courier_id(self, obj):
        data = CourierOrder.objects.filter(order=obj).first()
        if data:
            return data.courier.courier_id

    @staticmethod
    def get_order_detail(obj):
        order_menu_items = obj.customer_order_value.filter()
        order_menu_item = CookOrderMenuItemSerializer(order_menu_items, many=True).data
        return order_menu_item

