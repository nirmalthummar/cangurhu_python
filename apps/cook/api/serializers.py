from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.address.api.serializers import AddressSerializer
from apps.cook.models import (
    Cook,
    KitchenPremises,
    MenuCategory,
    MenuItem,
    MenuSubItem,
    FSCCatalogue,
    FSCCatalogueImage, CookOrderDetails
)

from apps.order.models import OrderMenuSubItem, Order, OrderMenuItem
from apps.order.api.service import get_user_default_address

User = get_user_model()


class KitchenPremisesSerializer(serializers.ModelSerializer):
    cook_id = serializers.CharField(source='cook.cook_id', max_length=14, allow_null=True, read_only=True)
    kitchen_premises = serializers.FileField(required=False)

    class Meta:
        model = KitchenPremises
        fields = ('document_id', 'kitchen_premises', 'cook', 'cook_id')


class CookSerializer(serializers.ModelSerializer):
    image = serializers.FileField(required=False)
    dob = serializers.DateField(required=True)
    country_id = serializers.IntegerField(required=True)
    cook_name = serializers.CharField(source='user.username', allow_null=True, read_only=True)
    email = serializers.CharField(source='user.email', allow_null=True, read_only=True)
    address = serializers.SerializerMethodField()

    class Meta:
        model = Cook
        fields = (
            'id', 'cook_id', 'user_id', 'image', 'dob', 'country_id', 'work_permit', 'govt_cert', 'cook_name',
            'email', 'address', 'insurance_cert', 'medical_clearance', 'food_cert', 'kitchen_premises', 'status', 'total_review',
            'avg_star_rating'
        )
        depth = 1
        read_only_fields = ('cook_id', 'user_id', 'status')

    def get_address(self, obj):
        address = get_user_default_address(user_id=obj.user_id)
        return address.address_id


class CookFSCDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cook
        fields = ('medical_clearance', 'food_cert', 'kitchen_premises')
        depth = 1


class MenuCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuCategory
        fields = ('id', 'category_name', 'category_icon')

    def validate(self, attrs):
        print(attrs.get("category_icon"))
        return super().validate(attrs)


class SubMenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuSubItem
        fields = (
            'id', 'title', 'price', 'prepare_time', 'total_calories', 'nutrition_info',
            'cultural_facts', 'commercial_info', 'menu_item'
        )
        extra_kwargs = {
            "title": {"required": False},
        }


class SubMenuItemSerializerAV(serializers.ModelSerializer):

    class Meta:
        model = MenuSubItem
        fields = "__all__"


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension,)

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


class MenuItemSerializerAV(serializers.ModelSerializer):
    # menu_sub_items = SubMenuItemSerializerAV(read_only=True)
    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    menu_sub_items = SubMenuItemSerializer(many=True)
    # Data URI Type
    item_img = Base64ImageField(
        max_length=None, use_url=True, required=False
    )
    cook_id = serializers.CharField(source='cook.cook_id', allow_null=True, read_only=True)
    cook_name = serializers.CharField(source='cook.user.username', allow_null=True, read_only=True)
    category_name = serializers.CharField(source='category.category_name', allow_null=True, read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(source='category', queryset=MenuCategory.objects.all())
    size = serializers.ListSerializer(child=serializers.DictField(), default=list)

    class Meta:
        model = MenuItem
        fields = (
            'id', 'item_number', 'title', 'item_img', 'category_id', 'category_name', 'cook_id', 'cook_name',
            'size',
            'warning', 'prepare_time', 'item_type', 'nutrition_info', 'cultural_facts', 'commercial_info',
            'status', 'created_at', 'updated_at', 'menu_sub_items'
        )
        read_only_fields = ('item_number', 'cook', 'created_at', 'updated_at',)
        extra_kwargs = {
            "title": {"required": False},
            "size": {"required": True},
            "warning": {"required": True},
            "item_type": {"required": True},
            "nutrition_info": {"required": True},
            "cultural_facts": {"required": True},
            "commercial_info": {"required": True}
        }

    def create(self, validated_data):
        request = self.context['request']
        menu_sub_items = validated_data.pop('menu_sub_items', [])
        menu_item = MenuItem.objects.create(**validated_data, cook=request.user.cook)
        if menu_sub_items:
            msi = []
            for item in menu_sub_items:
                msi.append(MenuSubItem(menu_item=menu_item, **item))
            MenuSubItem.objects.bulk_create(msi)
        return menu_item

    def sub_item_instance(self, item_id):
        try:
            return MenuSubItem.objects.get(id=item_id)
        except Exception as e:
            return None

    def update(self, instance, validated_data):
        menu_sub_items_data = validated_data.pop('menu_sub_items', [])

        super(MenuItemSerializer, self).update(instance=instance, validated_data=validated_data)

        if menu_sub_items_data:
            create_sub_item_list = []
            for sub_item in menu_sub_items_data:
                if "id" in sub_item.keys():
                    sub_item_id = sub_item.get('id')
                    menu_sub_item = self.sub_item_instance(sub_item_id)
                    if menu_sub_item:
                        for (key, value) in sub_item.items():
                            setattr(menu_sub_item, key, value)
                        menu_sub_item.save()
                else:
                    create_sub_item_list.append(MenuSubItem(menu_item=instance, **sub_item))
            if create_sub_item_list:
                MenuSubItem.objects.bulk_create(create_sub_item_list)
        print(instance)
        return instance


class TopDishesSerializer(MenuItemSerializer):
    total_like = serializers.SerializerMethodField()
    total_dislike = serializers.SerializerMethodField()

    class Meta(MenuItemSerializer.Meta):
        fields = MenuItemSerializer.Meta.fields + ('total_like', 'total_dislike')

    def get_total_like(self, obj):
        return 0

    def get_total_dislike(self, obj):
        return 0


class TopCookSerializer(CookSerializer):
    total_star = serializers.SerializerMethodField()
    total_review = serializers.SerializerMethodField()
    menu_items = serializers.SerializerMethodField()

    class Meta(CookSerializer.Meta):
        model = Cook
        fields = CookSerializer.Meta.fields + ('total_star', 'total_review', 'menu_items')

    def get_total_star(self, obj):
        return obj.avg_star_rating

    def get_total_review(self, obj):
        return obj.total_review

    def get_menu_items(self, obj):
        return MenuItemSerializer(obj.cook_menu_item.all(), many=True).data


class FSCCatalogueImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = FSCCatalogueImage
        fields = ('id', 'image', 'fsc_catalogue', 'cook', 'status', 'feedback')


class FSCCatalogueSerializer(serializers.ModelSerializer):
    description = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = FSCCatalogue
        fields = ('id', 'name', 'quantity', 'fsc_type', 'description', 'images', 'status')
        read_only_fields = ('created_at', 'updated_at', 'status',)

    def get_description(self, obj):
        return 'Description'

    def get_images(self, obj):
        return FSCCatalogueImageSerializer(obj.fsc_catalogue_images.all(), many=True).data


class CookOrderSerializer(serializers.ModelSerializer):

    order_id = serializers.CharField()
    status = serializers.CharField()
    cook_instruction = serializers.CharField()
    customer_name = serializers.CharField(source='customer.user.username')
    customer_default_address = AddressSerializer(source='customer_address', read_only=True)
    cook_default_address = AddressSerializer(source='cook_address', read_only=True)
    order_detail = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "order_id", "status", "cook_instruction", "customer_name", "customer_default_address","cook_default_address", "order_detail",
            'is_future_order', 'order_date', 'is_cook_agree'
        )

    @staticmethod
    def get_order_detail(obj):
        from apps.order.api.serializers import CookOrderMenuItemSerializer
        order_menu_item = CookOrderMenuItemSerializer(OrderMenuItem.objects.filter(order=obj), many=True).data
        return order_menu_item

    @staticmethod
    def get_address(obj):
        return AddressSerializer(obj.address).data


class CookFutureOrderSerializer(serializers.ModelSerializer):
    # order = serializers.CharField()
    # order_id = serializers.CharField()
    # status = serializers.CharField()
    # cook_instruction = serializers.CharField()
    customer_name = serializers.CharField(source='customer.user.username')
    address = serializers.SerializerMethodField()
    order_detail = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "id", "order_id", "status", "cook_instruction", "customer_name", "address", "order_detail",
            'is_future_order', 'order_date', 'is_cook_agree'
        )

    @staticmethod
    def get_order_detail(obj):
        from apps.order.api.serializers import CookOrderMenuItemSerializer
        order_menu_item = CookOrderMenuItemSerializer(OrderMenuItem.objects.filter(order=obj), many=True).data
        return order_menu_item

    @staticmethod
    def get_address(obj):
        return AddressSerializer(obj.address).data


class CookOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookOrderDetails
        fields = ('cook_order_id', 'order_id', 'cook_id', 'eta', 'reason')


class ModifyOrderSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField()
    status = serializers.CharField()
    cook_instruction = serializers.CharField()
    customer_name = serializers.CharField(source='customer.user.username')
    address = serializers.SerializerMethodField()
    order_detail = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = (
            "order_id", "status", "cook_instruction", "customer_name", "address", "order_detail"
        )
