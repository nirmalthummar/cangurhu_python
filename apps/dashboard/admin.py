from django.contrib import admin
from apps.config.models import *
# Register your models here.

# cook
@admin.register(KitchenImageCaptureFrequency)
class KitchenImageCaptureFrequencyAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "frequency")

@admin.register(MarketingFeeRate)
class MarketingFeeRateAdmin(admin.ModelAdmin):
    list_display = ("country", "percentage")

@admin.register(DeliveryFeesPaidByCook)
class DeliveryFeesPaidByCookAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "cost_per_mile")

@admin.register(CountryWiseFoodCategory)
class CountryWiseFoodCategoryAdmin(admin.ModelAdmin):
    list_display = ("country", "category")

@admin.register(FrequentKitchenOperations)
class FrequentKitchenOperationsAdmin(admin.ModelAdmin):
    list_display = ("activity", "to_perform")

@admin.register(KitchenEquipments)
class KitchenEquipmentsAdmin(admin.ModelAdmin):
    list_display = ("items", "object_analysis_attr", "object_media_type", "fsc_section")

@admin.register(FSCRegulationRulebook)
class FSCRegulationRulebookAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "regulation_rule", "status")

@admin.register(FSCManualAnswers)
class FSCManualAnswersAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "question", "answer")


# courier
@admin.register(CourierTimeZoneMisc)
class CourierTimeZoneMiscAdmin(admin.ModelAdmin):
    list_display = ("time_variance", "diner_surcharge_customer", "threshold_for_order_assigned", "courier_reliability_min_threshold", "courier_immobile", "courier_makes_stop")

@admin.register(CourierTripDelay)
class CourierTripDelayAdmin(admin.ModelAdmin):
    list_display = ("time", "warning_msg")

@admin.register(CourierGpsImmobile)
class CourierGpsImmobileAdmin(admin.ModelAdmin):
    list_display = ("time", "warning_msg")

@admin.register(CourierReliabilityScore)
class CourierReliabilityScoreAdmin(admin.ModelAdmin):
    list_display = ("threshold", "incr_percentage", "decr_percentage")

@admin.register(FacialRecognitionImageCapture)
class FacialRecognitionImageCaptureAdmin(admin.ModelAdmin):
    list_display = ("country", "frequency")

@admin.register(CourierDefaultSearchRadius)
class CourierDefaultSearchRadiusAdmin(admin.ModelAdmin):
    list_display = ("country", "vehicle_type", "radius")

@admin.register(PaymentProcessing)
class PaymentProcessingAdmin(admin.ModelAdmin):
    list_display = ("real_charge", "extra_charge", "country", "state")

@admin.register(MinimumDeliveryPayRate)
class MinimumDeliveryPayRateAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "vehicle_type", "pay_rate")

@admin.register(BufferDuration)
class BufferDurationAdmin(admin.ModelAdmin):
    list_display = ("country", "duration")

@admin.register(CostPerMileLoctoRes)
class CostPerMileLoctoResAdmin(admin.ModelAdmin):
    list_display = ("country", "cost")

@admin.register(CostPerMileResToCus)
class CostPerMileResToCusAdmin(admin.ModelAdmin):
    list_display = ("country", "cost")

@admin.register(DefaultCourierPositioning)
class DefaultCourierPositioningAdmin(admin.ModelAdmin):
    list_display = ("country", "time")

@admin.register(ConstantPay)
class ConstantPayAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "low_value", "medium_value", "high_value")

@admin.register(ConstantRangeDistance)
class ConstantRangeDistanceAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "minimum_range_distance", "maximum_range_distance")

@admin.register(AggregatedOrder)
class AggregatedOrderAdmin(admin.ModelAdmin):
    list_display = ("country", "vehicle_type", "pickup_radius", "delivery_time_threshold", "delivery_radius")

@admin.register(DefaultMinimumSearchRange)
class DefaultMinimumSearchRangeAdmin(admin.ModelAdmin):
    list_display = ("country", "vehicle_type", "minimum_range", "maximum_range")

@admin.register(HotZoneIncentivePercentage)
class HotZoneIncentivePercentageAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "town", "zip_code", "start_time", "end_time", "order_rate_hr", "incentive")


# customer
@admin.register(ItemFilterByPriceRange)
class ItemFilterByPriceRangeAdmin(admin.ModelAdmin):
    list_display = ("country", "minimum_price", "maximum_price", "currency")

@admin.register(DeliveryFeePaidByCustomer)
class DeliveryFeePaidByCustomerAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "cost_per_mile")

@admin.register(TipsPercentage)
class TipsPercentageAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "minimum_rate", "medium_rate", "highest_rate")

@admin.register(SalesTax)
class SalesTaxAdmin(admin.ModelAdmin):
    list_display = ("country", "state", "pst", "gst", "hst", "total_tax")

@admin.register(ConfigParametersTopDish)
class ConfigParametersTopDishAdmin(admin.ModelAdmin):
    list_display = ("country", "likes", "radius", "td_grade_a", "td_grade_b", "td_grade_c", "td_grade_d", "td_star_1", "td_star_2", "td_star_3", "td_star_4", "td_star_5", "td_star_all")

@admin.register(ConfigParametersTopCook)
class ConfigParametersTopCookAdmin(admin.ModelAdmin):
    list_display = ("country", "likes", "radius", "tc_grade_a", "tc_grade_b", "tc_grade_c", "tc_grade_d", "tc_star_1", "tc_star_2", "tc_star_3", "tc_star_4", "tc_star_5", "tc_star_all")

@admin.register(ConfigParametersFeaturedCook)
class ConfigParametersFeaturedCookAdmin(admin.ModelAdmin):
    list_display = ("country", "likes", "radius", "fc_grade_a", "fc_grade_b", "fc_grade_c", "fc_grade_d", "fc_star_1", "fc_star_2", "fc_star_3", "fc_star_4", "fc_star_5", "fc_star_all")

@admin.register(ConfigParametersNearbyCook)
class ConfigParametersNearbyCookAdmin(admin.ModelAdmin):
    list_display = ("country", "likes", "radius", "nc_grade_a", "nc_grade_b", "nc_grade_c", "nc_grade_d", "nc_star_1", "nc_star_2", "nc_star_3", "nc_star_4", "nc_star_5", "nc_star_all")

@admin.register(CustomerMiscParams)
class CustomerMiscParamsAdmin(admin.ModelAdmin):
    list_display = ("customer_diner_service_charge", "spend_point_factor", "like_point_factor", "social_media_point_factor", "monetization_factor", "reward_points_threshold", "time_for_feedback_cook", "time_for_feedback_courier")


# global
@admin.register(CangurhuAppAvailability)
class CangurhuAppAvailabilityAdmin(admin.ModelAdmin):
    list_display = ("country", "status")

@admin.register(PaymentRateAndConstant)
class PaymentRateAndConstantAdmin(admin.ModelAdmin):
    list_display = ("banking_payment_fee", "banking_payment_constant", "country")

@admin.register(PayoutRateAndConstant)
class PayoutRateAndConstantAdmin(admin.ModelAdmin):
    list_display = ("banking_payout_fee", "banking_payout_constant", "country")

@admin.register(MessageTexts)
class MessageTextsAdmin(admin.ModelAdmin):
    list_display = ("messageID", "header", "message_text", "priority", "receiving_audience", "where_used")

@admin.register(CookGradeExplaination)
class CookGradeExplainationAdmin(admin.ModelAdmin):
    list_display = ("grade", "description")

@admin.register(SoSDangerContact)
class SoSDangerContactAdmin(admin.ModelAdmin):
    list_display = ("country", "contact")


