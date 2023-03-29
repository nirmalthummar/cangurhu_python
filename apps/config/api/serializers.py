from rest_framework import serializers
from apps.config.models import *

# cook
class KitchenImageCaptureFrequencySerializer(serializers.ModelSerializer):
    class Meta:
        model=KitchenImageCaptureFrequency
        fields="__all__"

class MarketingFeeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketingFeeRate
        fields = "__all__"

class DeliveryFeesPaidByCookSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryFeesPaidByCook
        fields = "__all__"

class CountryWiseFoodCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryWiseFoodCategory
        fields = "__all__"

class FrequentKitchenOperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrequentKitchenOperations
        fields = "__all__"

class KitchenEquipmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitchenEquipments
        fields = "__all__"

class FSCRegulationRulebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = FSCRegulationRulebook
        fields = "__all__"

class FSCManualAnswersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FSCManualAnswers
        fields = "__all__"
        

# courier       
class CourierTimeZoneMiscSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierTimeZoneMisc
        fields = "__all__"

class CourierTripDelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierTripDelay
        fields = "__all__"

class CourierGpsImmobileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierGpsImmobile
        fields = "__all__"

class CourierReliabilityScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierReliabilityScore
        fields = "__all__"

class FacialRecognitionImageCaptureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacialRecognitionImageCapture
        fields = "__all__"

class CourierDefaultSearchRadiusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierDefaultSearchRadius
        fields = "__all__"

class PaymentProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentProcessing
        fields = "__all__"

class MinimumDeliveryPayRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinimumDeliveryPayRate
        fields = "__all__"

class BufferDurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BufferDuration
        fields = "__all__"

class CostPerMileLoctoResSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostPerMileLoctoRes
        fields = "__all__"

class CostPerMileResToCusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostPerMileResToCus
        fields = "__all__"

class DefaultCourierPositioningSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultCourierPositioning
        fields = "__all__"

class ConstantPaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstantPay
        fields = "__all__"

class ConstantRangeDistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConstantRangeDistance
        fields = "__all__"

class AggregatedOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = AggregatedOrder
        fields = "__all__"

class DefaultMinimumSearchRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultMinimumSearchRange
        fields = "__all__"

class HotZoneIncentivePercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotZoneIncentivePercentage
        fields = "__all__"


# customer
class ItemFilterByPriceRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemFilterByPriceRange
        fields = "__all__"

class DeliveryFeePaidByCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryFeePaidByCustomer
        fields = "__all__"

class TipsPercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipsPercentage
        fields = "__all__"

class SalesTaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesTax
        fields = "__all__"

class ConfigParametersTopDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigParametersTopDish
        fields = "__all__"

class ConfigParametersTopCookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigParametersTopCook
        fields = "__all__"

class ConfigParametersFeaturedCookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigParametersFeaturedCook
        fields = "__all__"

class ConfigParametersNearbyCookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigParametersNearbyCook
        fields = "__all__"

class CustomerMiscParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerMiscParams
        fields = "__all__"


# global        
class CountryWiseBankListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryWiseBankList
        fields = "__all__"

class CangurhuAppAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CangurhuAppAvailability
        fields = "__all__"

class PaymentRateAndConstantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentRateAndConstant
        fields = "__all__"

class PayoutRateAndConstantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutRateAndConstant
        fields = "__all__"

class MessageTextsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTexts
        fields = "__all__"

class CookGradeExplainationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookGradeExplaination
        fields = "__all__"

class SoSDangerContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoSDangerContact
        fields = "__all__"

