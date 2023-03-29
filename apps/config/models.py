from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.

# cook app config
class KitchenImageCaptureFrequency(models.Model):
    country=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    frequency=models.IntegerField(null=True, blank=True)

    class Meta:
     db_table="table_kitchenimagecapturefrequency"

class MarketingFeeRate(models.Model):
    country = models.CharField(max_length=100)
    percentage = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "table_marketingfeerate"


class DeliveryFeesPaidByCook(models.Model):
    cost_per_mile = models.IntegerField(null=True, blank=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    class Meta:
        db_table = "table_deliveryfeespaidbycook"


class CountryWiseFoodCategory(models.Model):
      country = models.CharField(max_length=100)
      category = models.TextField(null=True, blank=True)

      class Meta:
           db_table = "table_countrywisefoodcategory"


class FrequentKitchenOperations(models.Model):
    activity = models.TextField(null=True, blank=True)
    to_perform = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "table_frequentkitchenoperations"


class KitchenEquipments(models.Model):
    items = models.CharField(max_length=100, null=True, blank=True)
    object_analysis_attr = models.CharField(max_length=50, null=True, blank=True)
    object_media_type = models.CharField(max_length=50, null=True, blank=True)
    fsc_section = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "table_kitchenequipments"


class FSCRegulationRulebook(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    regulation_rule = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=False)

    class Meta:
        db_table = "table_fscregulationsrulebook"


class FSCManualAnswers(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    class Meta:
        db_table = "table_fscmanualanswers"



# courier app config
class CourierTimeZoneMisc(models.Model):
    time_variance = models.IntegerField(null=True, blank=True)
    diner_surcharge_customer = models.IntegerField(null=True, blank=True)
    threshold_for_order_assigned = models.IntegerField(null=True, blank=True)
    courier_reliability_min_threshold = models.IntegerField(null=True, blank=True)
    courier_immobile = models.IntegerField(null=True, blank=True)
    courier_makes_stop = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "table_couriertimezonemisc"

class CourierTripDelay(models.Model):
    time = models.IntegerField(null=True, blank=True)
    warning_msg = models.TextField(null=True, blank=True)
    class Meta:
        db_table = "table_couriertripdelay"

class CourierGpsImmobile(models.Model):
    time = models.IntegerField(null=True, blank=True)
    warning_msg = models.TextField(null=True, blank=True)
    class Meta:
        db_table = "table_couriergpsimmobile"

class CourierReliabilityScore(models.Model):
    threshold = models.IntegerField(null=True, blank=True)
    incr_percentage = models.IntegerField(null=True, blank=True)
    decr_percentage = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "table_courierreliabilityscore"

class FacialRecognitionImageCapture(models.Model):
    country = models.CharField(max_length=100)
    frequency = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "table_facialrecognitionimagecapture"

class CourierDefaultSearchRadius(models.Model):
    country = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    radius = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "table_courierdefaultsearchradius"

class PaymentProcessing(models.Model):
    real_charge = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    extra_charge = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    class Meta:
        db_table = "table_paymentprocessing"

class MinimumDeliveryPayRate(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    pay_rate = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = "table_minimumdeliverypayrate"

class BufferDuration(models.Model):
    country = models.CharField(max_length=100)
    duration = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "table_bufferduration"

class CostPerMileLoctoRes(models.Model):
    country = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = "table_costpermileloctores"

class CostPerMileResToCus(models.Model):
    country = models.CharField(max_length=100)
    cost = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = "table_costpermilerestocus"

class DefaultCourierPositioning(models.Model):
    country = models.CharField(max_length=100)
    time = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "table_defaultcourierpositioning"

class ConstantPay(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    low_value = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    medium_value = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    high_value = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = "table_constantpay"

class ConstantRangeDistance(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    minimum_range_distance = models.IntegerField(null=True, blank=True)
    maximum_range_distance = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "table_constantrangedistance"

class AggregatedOrder(models.Model):
    country = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    pickup_radius = models.IntegerField(null=True, blank=True)
    delivery_time_threshold = models.IntegerField(null=True, blank=True)
    delivery_radius = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "table_aggregatedorder"

class DefaultMinimumSearchRange(models.Model):
    country = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    minimum_range = models.IntegerField(null=True, blank=True)
    maximum_range = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "table_defaultminimumsearchrange"

class HotZoneIncentivePercentage(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    town = models.CharField(max_length=100)
    zip_code = models.IntegerField(validators=[MaxValueValidator(999999)])
    start_time = models.IntegerField(validators=[MaxValueValidator(2359)])
    end_time = models.IntegerField(validators=[MaxValueValidator(2359)])
    order_rate_hr = models.IntegerField()
    incentive = models.DecimalField(max_digits=4, decimal_places=2)
    class Meta:
        db_table = "table_hotzoneincentivepercentage"



# customer app config
class ItemFilterByPriceRange(models.Model):
    country = models.CharField(max_length=100)
    minimum_price = models.IntegerField(null=True, blank=True)
    maximum_price = models.IntegerField(null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)
    class Meta:
        db_table = "table_itemfilterbypricerange"

class DeliveryFeePaidByCustomer(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    cost_per_mile = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = "table_deliveryfeepaidbycustomer"

class TipsPercentage(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    minimum_rate = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    medium_rate = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    highest_rate = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = "table_tipspercentage"

class SalesTax(models.Model):
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pst = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    gst = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    hst = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    total_tax = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    class Meta:
        db_table = "table_salextax"

class ConfigParametersTopDish(models.Model):
    country = models.CharField(max_length=100)
    likes = models.IntegerField(null=True, blank=True)
    radius = models.IntegerField(null=True, blank=True)
    td_grade_a = models.BooleanField(default=False)
    td_grade_b = models.BooleanField(default=False)
    td_grade_c = models.BooleanField(default=False)
    td_grade_d = models.BooleanField(default=False)
    td_star_1 = models.BooleanField(default=False)
    td_star_2 = models.BooleanField(default=False)
    td_star_3 = models.BooleanField(default=False)
    td_star_4 = models.BooleanField(default=False)
    td_star_5 = models.BooleanField(default=False)
    td_star_all = models.BooleanField(default=False)
    class Meta:
        db_table = "table_configparameterstopdish"
        
class ConfigParametersTopCook(models.Model):
    country = models.CharField(max_length=100)
    likes = models.IntegerField(null=True, blank=True)
    radius = models.IntegerField(null=True, blank=True)
    tc_grade_a = models.BooleanField(default=False)
    tc_grade_b = models.BooleanField(default=False)
    tc_grade_c = models.BooleanField(default=False)
    tc_grade_d = models.BooleanField(default=False)
    tc_star_1 = models.BooleanField(default=False)
    tc_star_2 = models.BooleanField(default=False)
    tc_star_3 = models.BooleanField(default=False)
    tc_star_4 = models.BooleanField(default=False)
    tc_star_5 = models.BooleanField(default=False)
    tc_star_all = models.BooleanField(default=False)
    class Meta:
        db_table = "table_configparameterstopcook"

class ConfigParametersFeaturedCook(models.Model):
    country = models.CharField(max_length=100)
    likes = models.IntegerField(null=True, blank=True)
    radius = models.IntegerField(null=True, blank=True)
    fc_grade_a = models.BooleanField(default=False)
    fc_grade_b = models.BooleanField(default=False)
    fc_grade_c = models.BooleanField(default=False)
    fc_grade_d = models.BooleanField(default=False)
    fc_star_1 = models.BooleanField(default=False)
    fc_star_2 = models.BooleanField(default=False)
    fc_star_3 = models.BooleanField(default=False)
    fc_star_4 = models.BooleanField(default=False)
    fc_star_5 = models.BooleanField(default=False)
    fc_star_all = models.BooleanField(default=False)
    class Meta:
        db_table = "table_configparametersfeaturedcook"

class ConfigParametersNearbyCook(models.Model):
    country = models.CharField(max_length=100)
    likes = models.IntegerField(null=True, blank=True)
    radius = models.IntegerField(null=True, blank=True)
    nc_grade_a = models.BooleanField(default=False)
    nc_grade_b = models.BooleanField(default=False)
    nc_grade_c = models.BooleanField(default=False)
    nc_grade_d = models.BooleanField(default=False)
    nc_star_1 = models.BooleanField(default=False)
    nc_star_2 = models.BooleanField(default=False)
    nc_star_3 = models.BooleanField(default=False)
    nc_star_4 = models.BooleanField(default=False)
    nc_star_5 = models.BooleanField(default=False)
    nc_star_all = models.BooleanField(default=False)
    class Meta:
        db_table = "table_configparametersnearbycook"

class CustomerMiscParams(models.Model):
    customer_diner_service_charge = models.IntegerField(null=True, blank=True)
    spend_point_factor = models.IntegerField(null=True, blank=True)
    like_point_factor = models.IntegerField(null=True, blank=True)
    social_media_point_factor = models.IntegerField(null=True, blank=True)
    monetization_factor = models.IntegerField(null=True, blank=True)
    reward_points_threshold = models.IntegerField(null=True, blank=True)
    time_for_feedback_cook = models.IntegerField(null=True, blank=True)
    time_for_feedback_courier = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = "table_customermiscparams"



# global       
class CountryWiseBankList(models.Model):
    country = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        db_table = "table_countrywise_bank_list"

class CangurhuAppAvailability(models.Model):
    country = models.CharField(max_length=100)
    status = models.CharField(max_length=100, null=True, blank=True)
    class Meta:
        db_table = "table_cangurhuappavailability"

class PaymentRateAndConstant(models.Model):
    banking_payment_fee = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    banking_payment_constant = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    country = models.CharField(max_length=100)
    class Meta:
        db_table = "table_bankingpaymentrateandconstant"

class PayoutRateAndConstant(models.Model):
    banking_payout_fee = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    banking_payout_constant = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    country = models.CharField(max_length=100)
    class Meta:
        db_table = "table_bankingpayoutrateandconstant"

class MessageTexts(models.Model):
    messageID = models.CharField(max_length=100, null=True, blank=True)
    header = models.CharField(max_length=100, null=True, blank=True)
    message_text = models.TextField(null=True, blank=True)
    priority = models.CharField(max_length=100, null=True, blank=True)
    receiving_audience = models.CharField(max_length=100, null=True, blank=True)
    where_used = models.CharField(max_length=100, null=True, blank=True)
 
    class Meta:
        db_table = "table_messagetexts"

class CookGradeExplaination(models.Model):
    grade = models.CharField(max_length=1, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        db_table = "table_ccookgradeexplaination"

class SoSDangerContact(models.Model):
    country = models.CharField(max_length=100)
    contact = models.CharField(max_length=10, null=True, blank=True)
    class Meta:
        db_table = "table_sosdangercontact"





    



