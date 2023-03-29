from decimal import Decimal
from django.db.models import Sum
from rest_framework import serializers

from apps.cook.models import MenuItem
from apps.cart.models import (
    Cart,
    CartMenuItem,
    CartMenuSubItem
)


class CartSubMenuItemSerializer(serializers.ModelSerializer):
    sub_menu_item_name = serializers.CharField(source='sub_menu_item.title', read_only=True)
    price = serializers.DecimalField(source='sub_menu_item.price', decimal_places=4, max_digits=19, read_only=True)

    class Meta:
        model = CartMenuSubItem
        fields = ('id', 'cart_menu_item', 'sub_menu_item', 'sub_menu_item_name', 'price', 'quantity')


class CartItemSerializer(serializers.ModelSerializer):
    cart_sub_menu = CartSubMenuItemSerializer(many=True)
    total_like = serializers.SerializerMethodField()
    total_dislike = serializers.SerializerMethodField()
    warning = serializers.CharField(source='menu_item.warning', read_only=True)
    category_name = serializers.CharField(source='menu_item.category.category_name', read_only=True)
    calories = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    total_sub_items = serializers.SerializerMethodField()
    quantity = serializers.ListSerializer(child=serializers.DictField(), default=list)

    class Meta:
        model = CartMenuItem
        fields = ('id', 'menu_item', 'menu_item_name', 'cook_id', 'cook_name', 'warning', 'category_name',
                  'quantity', 'is_future_order', 'save_for_later', 'calories', 'price', 'cart_sub_menu',
                  'total_like', 'total_dislike', 'total_sub_items', 'order_date')

        extra_kwargs = {
            "menu_item": {"required": True},
            # "cart_sub_menu": {"required": True},
            "quantity": {"required": True},
            # "is_future_order": {"required": True}
        }

    def validate_quantity(self, quantity):
        if not quantity:
            raise serializers.ValidationError("This field is required")

        menu_item = self.initial_data.get('menu_item')
        if not menu_item:
            raise serializers.ValidationError("menu_item: This field is required")

        menu_item = MenuItem.objects.filter(pk=menu_item).first()
        sizes = [item.get('size') for item in menu_item.size]

        for q in quantity:
            size = q.get('size', '')
            if size not in sizes:
                raise serializers.ValidationError(f"{size} size is not valid choice.")
        return quantity

    def get_total_like(self, obj):
        return obj.menu_item.total_like

    def get_total_dislike(self, obj):
        return obj.menu_item.total_dislike

    def get_total_sub_items(self, obj):
        return obj.cart_sub_menu.count()

    def get_price(self, obj):
        sub_menu = obj.cart_sub_menu.aggregate(Sum('sub_menu_item__price'))
        sub_item_price = sub_menu['sub_menu_item__price__sum']
        price = Decimal(0.0)
        quantity = obj.quantity
        for q in quantity:
            size = q.get('size')
            count = q.get('count', 1)
            for item in obj.menu_item.size:
                if size == item.get('size'):
                    menu_item_price = item.get('price') * count
                    price += menu_item_price

        if sub_item_price:
            price += Decimal(sub_item_price)

        # obj.cart.total = price
        # obj.cart.save()
        return price

    def get_calories(self, obj):
        sub_menu = obj.cart_sub_menu.aggregate(Sum('sub_menu_item__total_calories'))
        return sub_menu['sub_menu_item__total_calories__sum']

    def create(self, validated_data):

        """
        {
            "menu_item": 21,
            "size": "large",
            "quantity: [
                {
                    "size": "medium",
                    "count": 1
                },
                {
                    "size": "small",
                    "count": 2
                }
            ],
            "sub_menu_items": [
                {
                    "sub_menu_item": 42,
                    "quantity": 3
                }
            ],
            "is_future_order": False
        }
        """

        sub_menu_items = validated_data.pop('cart_sub_menu')
        request = self.context.get('request')
        customer = request.user.customer
        menu_item = validated_data.get('menu_item')
        cook_id = menu_item.cook.cook_id

        cart, __ = Cart.objects.get_or_create(customer=customer)

        cart_items = CartMenuItem.objects.filter(cart=cart)

        if cart_items:
            for cart_item in cart_items:
                cart_menu_cook_id = cart_item.menu_item.cook.cook_id
                if cart_menu_cook_id != cook_id:
                    CartMenuItem.objects.get(id=cart_item.id).delete()

        cart_menu_item = CartMenuItem.objects.create(cart=cart, **validated_data)

        if sub_menu_items:
            sub_items = []
            for sub_item in sub_menu_items:
                sub_items.append(CartMenuSubItem(cart_menu_item=cart_menu_item, **sub_item))
            CartMenuSubItem.objects.bulk_create(sub_items)
        return cart_menu_item

    def update(self, instance, validated_data):
        """
        {
            "menu_item": 23,
            "quantity": [
                {
                    "size": "small",
                    "count": 3
                }
            ],
            "cart_sub_menu": [
                {
                    "sub_menu_item": 42,
                    "quantity": 1
                }
            ]
        }
        """
        sub_menu_items = validated_data.pop('cart_sub_menu')
        instance = super(CartItemSerializer, self).update(instance, validated_data)

        ids = []
        if sub_menu_items:
            for sub_item in sub_menu_items:
                sub_menu = instance.cart_sub_menu.filter(sub_menu_item=sub_item.get('sub_menu_item')).first()
                if sub_menu:
                    sub_menu.quantity = sub_item.get('quantity')
                    sub_menu.save()
                    ids.append(sub_menu.id)

        if ids:
            r_ids = instance.cart_sub_menu.exclude(id__in=ids)
            r_ids.delete()
        return instance


class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('id', 'customer', 'total', 'count', 'cart_items')

    def is_future_query_param(self):
        is_future_order = False
        request = self.context.get('request')
        if request is None:
            return is_future_order

        is_future = request.query_params.get('is_future_order', False)
        if is_future in ['false', 'False', '0', False]:
            is_future_order = False
        if is_future in ['true', 'True', '1', True]:
            is_future_order = True
        return is_future_order

    def get_cart_items(self, obj):
        is_future_order = self.is_future_query_param()
        return CartItemSerializer(obj.cart_menu.select_related('menu_item', 'cart').filter(
            is_future_order=is_future_order), many=True).data

    def get_count(self, obj):
        is_future_order = self.is_future_query_param()
        return obj.cart_menu.filter(is_future_order=is_future_order).count()

    def get_total(self, obj):
        return obj.total
