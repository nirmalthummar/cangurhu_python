from rest_framework import serializers

from apps.address.api.serializers import AddressSerializer
from apps.address.models import Address
from apps.courier.models import (Courier, CourierOrder)
from apps.order.models import (Order, )

from apps.accounts.api.serializers import UserSerializer, BankAccountSerializer

from apps.accounts.models import BankAccount


class CourierSerializer(serializers.ModelSerializer):
    image = serializers.FileField(required=False)
    dob = serializers.DateField(required=True)
    country_id = serializers.IntegerField(required=True)
    user = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()

    class Meta:
        model = Courier
        fields = (
            'courier_id', 'user_id', 'image', 'dob', 'country_id', 'work_permit', 'govt_cert',
            'driving_licence', 'contract_signature', 'e_signed_contract', 'vehicle_type',
            'vehicle_registration', 'vehicle_insurance', 'status', 'user', 'address'
        )

        read_only_fields = ('courier_id', 'user_id', 'status')

    @staticmethod
    def get_user(obj):
        return BankAccountSerializer(BankAccount.objects.filter(user_id=obj.user), many=True).data

    @staticmethod
    def get_address(obj):
        return AddressSerializer(Address.objects.filter(user_id=obj.user), many=True).data


class CourierDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = (
            'courier_id', 'user_id', 'work_permit', 'govt_cert',
            'driving_licence', 'contract_signature', 'e_signed_contract'
        )

        read_only_fields = ('courier_id', 'user_id')


class CourierVehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = (
            'courier_id', 'user_id', 'vehicle_type',
            'vehicle_registration', 'vehicle_insurance'
        )

        read_only_fields = ('courier_id', 'user_id')


class NewOrderListSerializer(serializers.ModelSerializer):
    customer_name = serializers.SerializerMethodField()
    courier_address = serializers.SerializerMethodField()
    cook_address = serializers.SerializerMethodField()
    customer_address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'courier_address', 'cook_address', 'order_id', 'customer', 'customer_name', 'customer_address',
            'courier_instruction',
            'status',
            'grand_total', 'created_at',

        )

    def get_customer_name(self, obj):
        return obj.customer.user.username

    def get_customer_address(self, obj):
        location = Address.objects.filter(user_id=obj.customer.user.user_id).first()
        return AddressSerializer(location).data

    def get_courier_address(self, obj):
        user_id = self.context.get("courier_user_id")
        location = Address.objects.filter(user_id=user_id).first()
        return AddressSerializer(location).data

    def get_cook_address(self, obj):
        cook_location = Address.objects.filter(user_id=obj.cook_order.filter().first().cook.user.user_id).first()
        return AddressSerializer(cook_location).data


class CourierOrderSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.user.username')
    status = serializers.CharField()

    class Meta:
        model = Order
        fields = ('order_id', 'customer_name', 'status')


class CourierOrderPickupSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.user.username')
    cook_address = serializers.SerializerMethodField()
    customer_address = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            'id', 'order_id', 'cook_address', 'customer_name', 'customer_address',
            'courier_instruction', 'status', 'tip_amount', 'tip_type', 'sub_total', 'shipping', 'total', 'discount',
            'grand_total', 'created_at'
        )

    def get_customer_address(self, obj):
        location = Address.objects.filter(user_id=obj.customer.user.user_id).first()
        return AddressSerializer(location).data

    def get_cook_address(self, obj):
        cook_location = Address.objects.filter(user_id=obj.cook_order.filter().first().cook.user.user_id).first()
        return AddressSerializer(cook_location).data


class CourierOrderCalculationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourierOrder
        fields = "__all__"
