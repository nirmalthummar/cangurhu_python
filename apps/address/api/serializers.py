from rest_framework import serializers
from rest_framework.fields import ReadOnlyField

from apps.address.models import Address, AddressCategory, AddCard, Cook
from apps.order.models import Order, OrderMenuItem
from apps.cook.models import CookOrderDetails
from apps.courier.models import CourierOrder
from apps.accounts.api.serializers import UserSerializer
from apps.snippets.api.serializers import CountrySerializer


class CourierOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourierOrder
        fields = "__all__"


class CookOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = CookOrderDetails
        fields = "__all__"


class OrderMenuItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderMenuItem
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


class CookSerializer(serializers.ModelSerializer):
    cook_country = serializers.SerializerMethodField()
    class Meta:
        model = Cook
        fields = "__all__"

    def get_cook_country(self, obj):
        return CountrySerializer(obj.country, many=False).data


class AddCardSerializer(serializers.ModelSerializer):
    card_user = serializers.SerializerMethodField()

    class Meta:
        model = AddCard
        fields = "__all__"

    def get_card_user(self, obj):
        return UserSerializer(obj.user).data


class AddressAVserializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    country_id = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = "__all__"
        # depth = 1

    def get_user_id(self, obj):
        print("user id", obj.user_id)
        return UserSerializer(obj.user_id, many=False).data

    def get_country_id(self, obj):
        return CountrySerializer(obj.country_id, many=False).data

    # def to_representation(self, instance):
    #     rep = super(AddressAVserializer, self).to_representation(instance)
    #     rep['country_id'] = instance.country_id.country_name
    #     return rep


class AddressSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = (
        'address_id', 'country_id', 'user_id', 'house_no', 'state', 'latitude', 'longitude', 'zipcode', 'town',
        'landmark', 'address', 'address_type', 'address_category', 'is_default')
        read_only_fields = ('address_id', 'user_id')
        extra_kwargs = {
            'address': {"required": True}
        }

    def get_user_id(self, obj):
        print("user id", obj.user_id)
        return UserSerializer(obj.user_id, many=False).data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        addresses = Address.objects.filter(user_id=user)

        if not addresses:
            validated_data['is_default'] = True

        validated_data['user_id'] = user
        new_address = Address.objects.create(**validated_data)

        is_default = validated_data.get('is_default')
        if is_default in ['True', 'true', True]:
            for address in addresses:
                address.is_default = False
                address.save()

        return new_address


class AddressDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class AddressCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressCategory
        fields = "__all__"
