from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.address.api.serializers import AddressSerializer
from apps.address.models import Address
from apps.cook.api.serializers import MenuCategorySerializer

from apps.order.models import (
    Order, OrderMenuItem, OrderMenuSubItem
)
from core.utils import generate_order_sequence

User = get_user_model()


class OrderSerializer(serializers.ModelSerializer):
    customer_default_address = AddressSerializer(source='customer_address', read_only=True)
    cook_default_address = AddressSerializer(source='cook_address', read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'order_id', 'status', 'customer', 'customer_default_address', 'cook_default_address', 'cook_instruction',
            'courier_instruction', 'sub_total', 'tip_amount', 'tip_type',
            'total', 'shipping', 'discount', 'grand_total', 'created_at', 'amount_paid', 'payment_details', 'distance')

    def update(self, instance, validated_data):
        instance = self.instance
        tip_type = validated_data.get('tip_type', None)
        payment_details = validated_data.get('payment_details', None)
        order_id = validated_data.get('order_id', None)
        print("payment_details", payment_details)
        if tip_type:
            instance.tip_type = validated_data.get('tip_type')
            if instance.tip_type == 'percentage':
                data = validated_data.get('tip_amount')
                tip_amount = (data / 100) * instance.sub_total
                instance.tip_amount = tip_amount
            if instance.tip_type == 'amount':
                instance.tip_amount = validated_data.get('tip_amount')
            # validated_data.pop("order_id")
            instance.total = instance.sub_total + instance.tip_amount

        if payment_details:
            instance.payment_details = payment_details
            payment_status = payment_details['status']
            if payment_status == "PaymentIntentsStatus.Succeeded":
                instance.amount_paid = "succeeded"
                instance.status = "OP"
                if order_id is None:
                    from datetime import datetime
                    date = datetime.today().strftime('%Y%m%d')
                    country_iso = instance.customer.country.iso2
                    last_order = Order.objects.filter(order_id__isnull=False).last()
                    if last_order:
                        last_order_id = last_order.order_id[11:]
                        instance.order_id = generate_order_sequence(date, country_iso, last_order_id)
                    else:
                        instance.order_id = generate_order_sequence(date, country_iso)

            else:
                instance.amount_paid = "failed"

        return super().update(instance, validated_data)


class FutureOrderSerializer(serializers.ModelSerializer):
    customer_address = AddressSerializer(source='address', read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'order_id', 'status', 'customer', 'address', 'customer_address', 'cook_instruction',
            'courier_instruction',
            'sub_total', 'tip_amount', 'tip_type',
            'total', 'shipping', 'discount', 'grand_total', 'created_at', 'amount_paid', 'payment_details',
            'is_future_order', 'order_date',)

    def update(self, instance, validated_data):
        instance = self.instance
        tip_type = validated_data.get('tip_type', None)
        payment_details = validated_data.get('payment_details', None)
        order_id = validated_data.get('order_id', None)
        print("order_id", order_id)
        if tip_type:
            instance.tip_type = validated_data.get('tip_type')
            if instance.tip_type == 'percentage':
                data = validated_data.get('tip_amount')
                tip_amount = (data / 100) * instance.sub_total
                instance.tip_amount = tip_amount
            if instance.tip_type == 'amount':
                instance.tip_amount = validated_data.get('tip_amount')
            # validated_data.pop("order_id")
            instance.total = instance.sub_total + instance.tip_amount
            instance.amount_paid = "pending"
        print(" in serializer", super().update(instance, validated_data))
        return super().update(instance, validated_data)
        # if payment_details:
        #     instance.payment_details = payment_details
        #     payment_status = payment_details['status']
        #     if payment_status == "PaymentIntentsStatus.Succeeded":
        #         instance.amount_paid = "succeeded"
        #         instance.status = "OP"
        #         if order_id is None:
        #             from datetime import datetime
        #             date = datetime.today().strftime('%Y%m%d')
        #             country_iso = instance.customer.country.iso2
        #             last_order = Order.objects.all().exclude(id=instance.id).last()
        #             if last_order:
        #                 last_order_id = last_order.order_id[11:]
        #                 instance.order_id = generate_order_sequence(date, country_iso, last_order_id)
        #             else:
        #                 instance.order_id = generate_order_sequence(date, country_iso)
        #     else:
        #         instance.amount_paid = "failed"

        # return super().update(instance, validated_data)


class OrderMenuItemSerializer(serializers.ModelSerializer):
    item_number = serializers.CharField(source='menu_item.item_number')
    title = serializers.CharField(source='menu_item.title')
    item_img = serializers.CharField(source='menu_item.item_img')
    size = serializers.CharField(source='menu_item.size')
    warning = serializers.CharField(source='menu_item.warning')
    prepare_time = serializers.CharField(source='menu_item.prepare_time')
    item_type = serializers.CharField(source='menu_item.item_type')
    nutrition_info = serializers.CharField(source='menu_item.nutrition_info')
    cultural_facts = serializers.CharField(source='menu_item.cultural_facts')
    commercial_info = serializers.CharField(source='menu_item.commercial_info')
    total_like = serializers.CharField(source='menu_item.total_like')
    total_dislike = serializers.CharField(source='menu_item.total_dislike')
    total_review = serializers.CharField(source='menu_item.total_review')
    avg_star_rating = serializers.CharField(source='menu_item.avg_star_rating')
    category = serializers.CharField(source='menu_item.category')

    class Meta:
        model = OrderMenuItem
        fields = ('id',
                  'order', 'category', 'item_number', 'title', 'item_img', 'size', 'warning', 'prepare_time',
                  'item_type',
                  'nutrition_info',
                  'cultural_facts', 'commercial_info', 'total_like', 'total_dislike', 'total_review', 'avg_star_rating',
                  'quantity', 'price',
                  )


class OrderMenuSubItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='menu_sub_item.title')
    price = serializers.CharField(source='menu_sub_item.price')
    prepare_time = serializers.CharField(source='menu_sub_item.prepare_time')
    total_calories = serializers.CharField(source='menu_sub_item.total_calories')
    nutrition_info = serializers.CharField(source='menu_sub_item.nutrition_info')
    cultural_facts = serializers.CharField(source='menu_sub_item.cultural_facts')
    commercial_info = serializers.CharField(source='menu_sub_item.commercial_info')

    class Meta:
        model = OrderMenuSubItem
        fields = (
            'id',
            'title', 'price', 'prepare_time', 'total_calories', 'nutrition_info', 'cultural_facts', 'commercial_info',
        )


class CookOrderMenuItemSerializer(serializers.ModelSerializer):
    order_menu_sub_items = serializers.SerializerMethodField()
    order_menu_items = serializers.SerializerMethodField()
    cook_id = serializers.CharField(source='menu_item.cook.cook_id')
    cook_name = serializers.CharField(source='menu_item.cook.user.username')
    cook_address = serializers.SerializerMethodField()

    class Meta:
        model = OrderMenuItem
        fields = (
            'order', 'cook_id', 'cook_name', 'cook_address', 'order_menu_items', 'order_menu_sub_items'
        )

    def get_cook_address(self, obj):
        cook_location = Address.objects.filter(user_id=obj.menu_item.cook.user.user_id).first()
        return AddressSerializer(cook_location).data

    @staticmethod
    def get_order_menu_items(obj):
        return OrderMenuItemSerializer(obj).data

    @staticmethod
    def get_order_menu_sub_items(obj):
        order_menu_sub_items = obj.order_menu_sub_item.filter()
        return OrderMenuSubItemSerializer(order_menu_sub_items, many=True).data

