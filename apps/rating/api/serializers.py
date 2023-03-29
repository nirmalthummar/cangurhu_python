from rest_framework import serializers

from apps.courier.api.serializers import CourierSerializer
from apps.rating.models import CookFeedback, DishGrade
from apps.cook.api.serializers import CookSerializer


class CookFeedbackSerializer(serializers.ModelSerializer):

    # def __init__(self, *args, **kwargs):
    #     super(CookFeedbackSerializer, self).__init__(*args, **kwargs)
    #     request = self.context.get('request')
    #     if request and request.method == 'POST':
    #         self.Meta.depth = 0
    #     else:
    #         self.Meta.depth = 1

    cook = serializers.SerializerMethodField()
    courier = serializers.SerializerMethodField()

    class Meta:
        model = CookFeedback
        fields = "__all__"
        include = ["cook"]

    def get_cook(self, obj):
        return CookSerializer(obj.cook, many=False).data

    def get_courier(self, obj):
        return CourierSerializer(obj.courier_user, many=False).data


class CookFeedbackSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model = CookFeedback
        fields = "__all__"


class DishGradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DishGrade
        fields = "__all__"
