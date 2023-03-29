from cgi import print_arguments
from http.client import HTTPResponse
from re import T
from traceback import print_tb
from urllib import request
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic import TemplateView
from apps.config.models import *
from apps.config.api.serializers import *
from django.core.paginator import Paginator
from apps.cook.models import MenuCategory
from apps.cook.api.serializers import MenuCategorySerializer

from django.shortcuts import render, redirect

class AllAppListView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/all-apps-central-parameters.html"

    def get_context_data(self, **kwargs):
        context = super(AllAppListView, self).get_context_data(**kwargs)
        context['all_app_active'] = True
        return context

class NotificationListView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/notification-central.html"

    def get_context_data(self, **kwargs):
        context = super(NotificationListView, self).get_context_data(**kwargs)
        context['notification_active'] = True
        return context


class OperationalKPIListView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/operational-KPI.html"

    def get_context_data(self, **kwargs):
        context = super(OperationalKPIListView, self).get_context_data(**kwargs)
        context['operational_active'] = True
        return context

# GET and POST data into table
class AppConfigListView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/app-configurations-parameters.html"


    def get_context_data(self, **kwargs):
        
        # cook
        context = super(AppConfigListView, self).get_context_data(**kwargs)
        menu_category_data = MenuCategory.objects.all()
        kicf_data = KitchenImageCaptureFrequency.objects.all()
        market_fee_data = MarketingFeeRate.objects.all()
        delivery_fee_data = DeliveryFeesPaidByCook.objects.all()
        food_category_data = CountryWiseFoodCategory.objects.all()
        kitchen_operations_data = FrequentKitchenOperations.objects.all()
        kitchen_equipments_data = KitchenEquipments.objects.all()
        regulations_data = FSCRegulationRulebook.objects.all()
        manual_answers_data = FSCManualAnswers.objects.all()

        # courier
        facial_rec_data = FacialRecognitionImageCapture.objects.all()
        def_search_radius_data = CourierDefaultSearchRadius.objects.all()
        payment_processing_data = PaymentProcessing.objects.all()
        min_delivery_rate_data = MinimumDeliveryPayRate.objects.all()
        buffer_duration_data = BufferDuration.objects.all()
        mileage_loctores_data = CostPerMileLoctoRes.objects.all()
        mileage_restocus_data = CostPerMileResToCus.objects.all()
        courier_positioning_data = DefaultCourierPositioning.objects.all()
        constant_pay_data = ConstantPay.objects.all()
        constant_range_data = ConstantRangeDistance.objects.all()
        aggregated_order_data = AggregatedOrder.objects.all()
        min_search_range_data = DefaultMinimumSearchRange.objects.all()
        hot_zone_data = HotZoneIncentivePercentage.objects.all()

        # customer
        item_filter_data = ItemFilterByPriceRange.objects.all()
        delivery_fee_transit_data = DeliveryFeePaidByCustomer.objects.all()
        tips_data = TipsPercentage.objects.all()
        sales_tax_data = SalesTax.objects.all()
        config_top_dish_data = ConfigParametersTopDish.objects.all()
        config_top_cook_data = ConfigParametersTopCook.objects.all()
        config_feat_cook_data = ConfigParametersFeaturedCook.objects.all()
        config_nearby_cook_data = ConfigParametersNearbyCook.objects.all()
        customer_misc_data = CustomerMiscParams.objects.all()

        # global
        app_avail_data = CangurhuAppAvailability.objects.all()
        payment_constant_data = PaymentRateAndConstant.objects.all()
        payout_constant_data = PayoutRateAndConstant.objects.all()
        message_texts_data = MessageTexts.objects.all()
        cook_grade_explain_data = CookGradeExplaination.objects.all()
        sos_contact_data = SoSDangerContact.objects.all()


        context={
            "app_config_active": True,
            'menu_category_data': menu_category_data,
            "kicf_data": kicf_data, 
            "market_fee_data" : market_fee_data,
            "delivery_fee_data": delivery_fee_data,
            "food_category_data" : food_category_data,
            "kitchen_operations_data" : kitchen_operations_data,
            "kitchen_equipments_data" : kitchen_equipments_data,
            "regulations_data" : regulations_data,
            "manual_answers_data" : manual_answers_data,
            
            "facial_rec_data" : facial_rec_data,
            "def_search_radius_data" : def_search_radius_data,
            "payment_processing_data" : payment_processing_data,
            "min_delivery_rate_data" : min_delivery_rate_data,
            "buffer_duration_data" : buffer_duration_data,
            "mileage_loctores_data" : mileage_loctores_data,
            "mileage_restocus_data" : mileage_restocus_data,
            "courier_positioning_data" : courier_positioning_data,
            "constant_pay_data" : constant_pay_data,
            "constant_range_data" : constant_range_data,
            "aggregated_order_data" : aggregated_order_data,
            "min_search_range_data" : min_search_range_data,
            "hot_zone_data" : hot_zone_data,

            "item_filter_data" : item_filter_data,
            "delivery_fee_transit_data" : delivery_fee_transit_data,
            "tips_data" : tips_data,
            "sales_tax_data" : sales_tax_data,
            "config_top_dish_data" : config_top_dish_data,
            "config_top_cook_data" : config_top_cook_data,
            "config_feat_cook_data" : config_feat_cook_data,
            "config_nearby_cook_data" : config_nearby_cook_data,
            "customer_misc_data" : customer_misc_data,

            "app_avail_data" : app_avail_data,
            "payment_constant_data" : payment_constant_data,
            "payout_constant_data" : payout_constant_data,
            "message_texts_data" : message_texts_data,
            "cook_grade_explain_data" : cook_grade_explain_data,
            "sos_contact_data" : sos_contact_data,
        }
        return context

    def post(self, request):
        serializer=None
        # cook parameter forms
        if "menu_category_form" in request.POST:
            serializer = MenuCategorySerializer(data=request.POST)
        elif "kicf_form" in request.POST:
            serializer = KitchenImageCaptureFrequencySerializer(data=request.POST)
        elif "market_fee_form" in request.POST:
            serializer = MarketingFeeRateSerializer(data=request.POST)
        elif "cook_delivery_fee_form" in request.POST:
            serializer = DeliveryFeesPaidByCookSerializer(data=request.POST)
        elif "food_category_form" in request.POST:
            serializer = CountryWiseFoodCategorySerializer(data=request.POST)
        elif "kitchen_operations_form" in request.POST:
            serializer = FrequentKitchenOperationsSerializer(data=request.POST)
        elif "kitchen_equipments_form" in request.POST:
            serializer = KitchenEquipmentsSerializer(data=request.POST)
        elif "regulations_form" in request.POST:
            serializer = FSCRegulationRulebookSerializer(data=request.POST)
        elif "manual_answers_form" in request.POST:
            serializer = FSCManualAnswersSerializer(data=request.POST)

        # courier parameter forms
        elif "courier_time_zone_misc_form" in request.POST:
            serializer = CourierTimeZoneMiscSerializer(data=request.POST)
        elif "courier_trip_delay_form" in request.POST:
            serializer = CourierTripDelaySerializer(data=request.POST)
        elif "courier_gps_form" in request.POST:
            serializer = CourierGpsImmobileSerializer(data=request.POST)
        elif "courier_reliability_form" in request.POST:
            serializer = CourierReliabilityScoreSerializer(data=request.POST)
        elif "def_search_radius_form" in request.POST:
            serializer = CourierDefaultSearchRadiusSerializer(data=request.POST)
        elif "payment_processing_form" in request.POST:
            serializer = PaymentProcessingSerializer(data=request.POST)
        elif "min_delivery_rate_form" in request.POST:
            serializer = MinimumDeliveryPayRateSerializer(data=request.POST)
        elif "buffer_duration_form" in request.POST:
            serializer = BufferDurationSerializer(data=request.POST)
        elif "mileage_loctores_form" in request.POST:
            serializer = CostPerMileLoctoResSerializer(data=request.POST)
        elif "mileage_restocus_form" in request.POST:
            serializer = CostPerMileResToCusSerializer(data=request.POST)
        elif "courier_positioning_form" in request.POST:
            serializer = DefaultCourierPositioningSerializer(data=request.POST)
        elif "constant_pay_form" in request.POST:
            serializer = ConstantPaySerializer(data=request.POST)
        elif "constant_range_form" in request.POST:
            serializer = ConstantRangeDistanceSerializer(data=request.POST)
        elif "aggregated_order_form" in request.POST:
            serializer = AggregatedOrderSerializer(data=request.POST)
        elif "min_search_range_form" in request.POST:
            serializer = DefaultMinimumSearchRangeSerializer(data=request.POST)
        elif "hot_zone_form" in request.POST:
            serializer = HotZoneIncentivePercentageSerializer(data=request.POST)

        # customer parameter forms    
        elif "item_filter_form" in request.POST:
            serializer = ItemFilterByPriceRangeSerializer(data=request.POST)
        elif "delivery_fee_transit_form" in request.POST:
            serializer = DeliveryFeePaidByCustomerSerializer(data=request.POST)
        elif "tips_form" in request.POST:
            serializer = TipsPercentageSerializer(data=request.POST)
        elif "sales_tax_form" in request.POST:
            serializer = SalesTaxSerializer(data=request.POST)
        elif "config_top_dish_form" in request.POST:
            serializer = ConfigParametersTopDishSerializer(data=request.POST)
        elif "config_top_cook_form" in request.POST:
            serializer = ConfigParametersTopCookSerializer(data=request.POST)
        elif "config_feat_cook_form" in request.POST:
            serializer = ConfigParametersFeaturedCookSerializer(data=request.POST)
        elif "config_nearby_cook_form" in request.POST:
            serializer = ConfigParametersNearbyCookSerializer(data=request.POST)
        elif "customer_misc_form" in request.POST:
            serializer = CustomerMiscParamsSerializer(data=request.POST)

        # global parameters form
        elif "app_avail_form" in request.POST:
            serializer = CangurhuAppAvailabilitySerializer(data=request.POST)
        elif "payment_constant_form" in request.POST:
            serializer = PaymentRateAndConstantSerializer(data=request.POST)
        elif "payout_constant_form" in request.POST:
            serializer = PayoutRateAndConstantSerializer(data=request.POST)
        elif "message_texts_form" in request.POST:
            serializer = MessageTextsSerializer(data=request.POST)
        elif "cook_grade_explain_form" in request.POST:
            serializer = CookGradeExplainationSerializer(data=request.POST)
        elif "sos_contact_form" in request.POST:
            serializer = SoSDangerContactSerializer(data=request.POST)
        
        if serializer.is_valid():
                serializer.save()
            
        return redirect('dashboard:app-configurations-parameters')
        

# Edit (PUT) Table data
class AppConfigListViewUpdate(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/app-configurations-parameters.html"

    def post(self, request, id):
        if "menu_category_edit_form" in request.POST:
            MenuCategory.objects.filter(pk=id).update(category_icon=request.POST.get('category_icon'),category_name=request.POST['category_name'],status=request.POST['status'])            
        elif "kicf_edit_form" in request.POST:
            KitchenImageCaptureFrequency.objects.filter(pk=id).update(country=request.POST['country'],state=request.POST['state'],frequency=request.POST['frequency'])            
        elif "market_fee_edit_form" in request.POST:
            MarketingFeeRate.objects.filter(pk=id).update(country=request.POST['country'], percentage=request.POST['percentage'])
        elif "cook_delivery_fee_edit_form" in request.POST:
            DeliveryFeesPaidByCook.objects.filter(pk=id).update(country=request.POST['country'], state=request.POST['state'], cost_per_mile=request.POST['cost_per_mile'])
        elif "food_category_edit_form" in request.POST:
            CountryWiseFoodCategory.objects.filter(pk=id).update(country=request.POST['country'], category=request.POST['category'])
        elif "kitchen_operations_edit_form" in request.POST:
            FrequentKitchenOperations.objects.filter(pk=id).update(activity=request.POST['activity'], to_perform=request.POST['to_perform'])
        elif "kitchen_equipments_edit_form" in request.POST:
            KitchenEquipments.objects.filter(pk=id).update(items=request.POST['items'], object_analysis_attr=request.POST['object_analysis_attr'], object_media_type=request.POST['object_media_type'], fsc_section=request.POST['fsc_section'])
        elif "regulations_edit_form" in request.POST:
            if request.POST.get('status'):
                status=True
            else:
                status=False
            FSCRegulationRulebook.objects.filter(pk=id).update(country=request.POST['country'], state=request.POST['state'], regulation_rule=request.POST['regulation_rule'],status=status)
        elif "manual_answers_edit_form" in request.POST:
            FSCManualAnswers.objects.filter(pk=id).update(country=request.POST['country'], state=request.POST['state'], question=request.POST['question'], answer=request.POST['answer'])

        elif "facial_rec_edit_form" in request.POST:
            FacialRecognitionImageCapture.objects.filter(pk=id).update(country=request.POST['country'], frequency=request.POST['frequency'])
        elif "def_search_radius_edit_form" in request.POST:
            CourierDefaultSearchRadius.objects.filter(pk=id).update(country=request.POST['country'], vehicle_type=request.POST['vehicle_type'], radius=request.POST['radius'])
        elif "payment_processing_edit_form" in request.POST:
            PaymentProcessing.objects.filter(pk=id).update(real_charge=request.POST['real_charge'], extra_charge=request.POST['extra_charge'], country=request.POST['country'], state=request.POST['state'])
        elif "min_delivery_rate_edit_form" in request.POST:
            MinimumDeliveryPayRate.objects.filter(pk=id).update(country=request.POST['country'], state=request.POST['state'], vehicle_type=request.POST['vehicle_type'], pay_rate=request.POST['pay_rate'])
        elif "buffer_duration_edit_form" in request.POST:
            BufferDuration.objects.filter(pk=id).update(country=request.POST['country'], duration=request.POST['duration'])
        elif "mileage_loctores_edit_form" in request.POST:
            CostPerMileLoctoRes.objects.filter(pk=id).update(country=request.POST['country'], cost=request.POST['cost'])
        elif "mileage_restocus_edit_form" in request.POST:
            CostPerMileResToCus.objects.filter(pk=id).update(country=request.POST['country'], cost=request.POST['cost'])
        elif "courier_positioning_edit_form" in request.POST:
            DefaultCourierPositioning.objects.filter(pk=id).update(country=request.POST['country'], time=request.POST['time'])
        elif "constant_pay_edit_form" in request.POST:
            ConstantPay.objects.filter(pk=id).update(country=request.POST['country'], state=request.POST['state'], low_value=request.POST['low_value'], medium_value=request.POST['medium_value'], high_value=request.POST['high_value'])
        elif "constant_range_edit_form" in request.POST:
            ConstantRangeDistance.objects.filter(pk=id).update(country=request.POST['country'], state=request.POST['state'], minimum_range_distance=request.POST['minimum_range_distance'], maximum_range_distance=request.POST['maximum_range_distance'])
        elif "aggregated_order_edit_form" in request.POST:
            AggregatedOrder.objects.filter(pk=id).update(country=request.POST['country'], vehicle_type=request.POST['vehicle_type'], pickup_radius=request.POST['pickup_radius'], delivery_time_threshold=request.POST['delivery_time_threshold'], delivery_radius=request.POST['delivery_radius'])
        elif "min_search_range_edit_form" in request.POST:
            DefaultMinimumSearchRange.objects.filter(pk=id).update(country=request.POST['country'], vehicle_type=request.POST['vehicle_type'], minimum_range=request.POST['minimum_range'], maximum_range=request.POST['maximum_range'])
        elif "hot_zone_edit_form" in request.POST:
            HotZoneIncentivePercentage.objects.filter(pk=id).update(country=request.POST['country'], state=request.POST['state'], town=request.POST['town'], zip_code=request.POST['zip_code'], start_time=request.POST['start_time'], end_time=request.POST['end_time'], order_rate_hr=request.POST['order_rate_hr'], incentive=request.POST['incentive'])
        
        elif "item_filter_edit_form" in request.POST:
            ItemFilterByPriceRange.objects.filter(pk=id).update(country=request.POST['country'], minimum_price=request.POST['minimum_price'], maximum_price=request.POST['maximum_price'], currency=request.POST['currency'])
        elif "delivery_fee_transit_edit_form" in request.POST:
            DeliveryFeePaidByCustomer.objects.filter(pk=id).update(country=request.POST['country'], state=request.POST['state'], cost_per_mile=request.POST['cost_per_mile'])
        elif "tips_edit_form" in request.POST:
            TipsPercentage.objects.filter(pk=id).update(country=request.POST['country'], state=request.POST['state'], minimum_rate=request.POST['minimum_rate'], medium_rate=request.POST['medium_rate'], highest_rate=request.POST['highest_rate'])
        elif "sales_tax_edit_form" in request.POST:
            SalesTax.objects.filter(pk=id).update(country=request.POST['country'], state=request.POST['state'], pst=request.POST['pst'], gst=request.POST['gst'], hst=request.POST['hst'], total_tax=request.POST['total_tax'])
        
        
        elif "config_top_dish_edit_form" in request.POST:
            if request.POST.get("td_grade_a"):
                td_grade_a = True
            else:
                td_grade_a = False
                    
            if request.POST.get("td_grade_b"):
                td_grade_b = True
            else:
                td_grade_b = False
                    
            if request.POST.get("td_grade_c"):
                td_grade_c = True
            else:
                td_grade_c = False
                    
            if request.POST.get("td_grade_d"):
                td_grade_d = True
            else:
                td_grade_d = False
                    
            if request.POST.get("td_star_1"):
                td_star_1 = True
            else:
                td_star_1 = False
                    
            if request.POST.get("td_star_2"):
                td_star_2 = True
            else:
                td_star_2 = False
                    
            if request.POST.get("td_star_3"):
                td_star_3 = True
            else:
                td_star_3 = False
                    
            if request.POST.get("td_star_4"):
                td_star_4 = True
            else:
                td_star_4 = False
                    
            if request.POST.get("td_star_5"):
                td_star_5 = True
            else:
                td_star_5 = False
                    
            if request.POST.get("td_star_all"):
                td_star_all = True
            else:
                td_star_all = False
                    
            ConfigParametersTopDish.objects.filter(pk=id).update(
                country=request.POST['country'],
                likes=request.POST['likes'],
                radius=request.POST['radius'],
                td_grade_a=td_grade_a,
                td_grade_b=td_grade_b,
                td_grade_c=td_grade_c,
                td_grade_d=td_grade_d,
                td_star_1=td_star_1,
                td_star_2=td_star_2,
                td_star_3=td_star_3,
                td_star_4=td_star_4,
                td_star_5=td_star_5,
                td_star_all=td_star_all)


        elif "config_top_cook_edit_form" in request.POST:
            if request.POST.get("tc_grade_a"):
                tc_grade_a = True
            else:
                tc_grade_a = False
                    
            if request.POST.get("tc_grade_b"):
                tc_grade_b = True
            else:
                tc_grade_b = False
                    
            if request.POST.get("tc_grade_c"):
                tc_grade_c = True
            else:
                tc_grade_c = False
                    
            if request.POST.get("tc_grade_d"):
                tc_grade_d = True
            else:
                tc_grade_d = False
                    
            if request.POST.get("tc_star_1"):
                tc_star_1 = True
            else:
                tc_star_1 = False
                    
            if request.POST.get("tc_star_2"):
                tc_star_2 = True
            else:
                tc_star_2 = False
                    
            if request.POST.get("tc_star_3"):
                tc_star_3 = True
            else:
                tc_star_3 = False
                    
            if request.POST.get("tc_star_4"):
                tc_star_4 = True
            else:
                tc_star_4 = False
                    
            if request.POST.get("tc_star_5"):
                tc_star_5 = True
            else:
                tc_star_5 = False
                    
            if request.POST.get("tc_star_all"):
                tc_star_all = True
            else:
                tc_star_all = False

            ConfigParametersTopCook.objects.filter(pk=id).update(
                country=request.POST['country'],
                likes=request.POST['likes'],
                radius=request.POST['radius'],
                tc_grade_a=tc_grade_a,
                tc_grade_b=tc_grade_b,
                tc_grade_c=tc_grade_c,
                tc_grade_d=tc_grade_d,
                tc_star_1=tc_star_1,
                tc_star_2=tc_star_2,
                tc_star_3=tc_star_3,
                tc_star_4=tc_star_4,
                tc_star_5=tc_star_5,
                tc_star_all=tc_star_all)

        elif "config_feat_cook_edit_form" in request.POST:
            if request.POST.get("fc_grade_a"):
                fc_grade_a = True
            else:
                fc_grade_a = False
                    
            if request.POST.get("fc_grade_b"):
                fc_grade_b = True
            else:
                fc_grade_b = False
                    
            if request.POST.get("fc_grade_c"):
                fc_grade_c = True
            else:
                fc_grade_c = False
                    
            if request.POST.get("fc_grade_d"):
                fc_grade_d = True
            else:
                fc_grade_d = False
                    
            if request.POST.get("fc_star_1"):
                fc_star_1 = True
            else:
                fc_star_1 = False
                    
            if request.POST.get("fc_star_2"):
                fc_star_2 = True
            else:
                fc_star_2 = False
                    
            if request.POST.get("fc_star_3"):
                fc_star_3 = True
            else:
                fc_star_3 = False
                    
            if request.POST.get("fc_star_4"):
                fc_star_4 = True
            else:
                fc_star_4 = False
                    
            if request.POST.get("fc_star_5"):
                fc_star_5 = True
            else:
                fc_star_5 = False
                    
            if request.POST.get("fc_star_all"):
                fc_star_all = True
            else:
                fc_star_all = False
            ConfigParametersFeaturedCook.objects.filter(pk=id).update(
                country=request.POST['country'],
                likes=request.POST['likes'],
                radius=request.POST['radius'],
                fc_grade_a=fc_grade_a,
                fc_grade_b=fc_grade_b,
                fc_grade_c=fc_grade_c,
                fc_grade_d=fc_grade_d,
                fc_star_1=fc_star_1,
                fc_star_2=fc_star_2,
                fc_star_3=fc_star_3,
                fc_star_4=fc_star_4,
                fc_star_5=fc_star_5,
                fc_star_all=fc_star_all)

        elif "config_nearby_cook_edit_form" in request.POST:
            if request.POST.get("nc_grade_a"):
                nc_grade_a = True
            else:
                nc_grade_a = False
                    
            if request.POST.get("nc_grade_b"):
                nc_grade_b = True
            else:
                nc_grade_b = False
                    
            if request.POST.get("nc_grade_c"):
                nc_grade_c = True
            else:
                nc_grade_c = False
                    
            if request.POST.get("nc_grade_d"):
                nc_grade_d = True
            else:
                nc_grade_d = False
                    
            if request.POST.get("nc_star_1"):
                nc_star_1 = True
            else:
                nc_star_1 = False
                    
            if request.POST.get("nc_star_2"):
                nc_star_2 = True
            else:
                nc_star_2 = False
                    
            if request.POST.get("nc_star_3"):
                nc_star_3 = True
            else:
                nc_star_3 = False
                    
            if request.POST.get("nc_star_4"):
                nc_star_4 = True
            else:
                nc_star_4 = False
                    
            if request.POST.get("nc_star_5"):
                nc_star_5 = True
            else:
                nc_star_5 = False
                    
            if request.POST.get("nc_star_all"):
                nc_star_all = True
            else:
                nc_star_all = False
            ConfigParametersNearbyCook.objects.filter(pk=id).update(
                country=request.POST['country'],
                likes=request.POST['likes'],
                radius=request.POST['radius'],
                nc_grade_a=nc_grade_a,
                nc_grade_b=nc_grade_b,
                nc_grade_c=nc_grade_c,
                nc_grade_d=nc_grade_d,
                nc_star_1=nc_star_1,
                nc_star_2=nc_star_2,
                nc_star_3=nc_star_3,
                nc_star_4=nc_star_4,
                nc_star_5=nc_star_5,
                nc_star_all=nc_star_all)

        elif "customer_misc_edit_form" in request.POST:
            CustomerMiscParams.objects.filter(pk=id).update(customer_diner_service_charge=request.POST["customer_diner_service_charge"], spend_point_factor=request.POST["spend_point_factor"], like_point_factor=request.POST["like_point_factor"], social_media_point_factor=request.POST["social_media_point_factor"], monetization_factor=request.POST["monetization_factor"], reward_points_threshold=request.POST["reward_points_threshold"], time_for_feedback_cook=request.POST["time_for_feedback_cook"], time_for_feedback_courier=request.POST["time_for_feedback_courier"])
            
        elif "app_avail_edit_form" in request.POST:
            CangurhuAppAvailability.objects.filter(pk=id).update(country=request.POST['country'], status=request.POST['status'])
        elif "payment_constant_edit_form" in request.POST:
            PaymentRateAndConstant.objects.filter(pk=id).update(banking_payment_fee=request.POST['banking_payment_fee'], banking_payment_constant=request.POST['banking_payment_constant'], country=request.POST['country'])
        elif "payout_constant_edit_form" in request.POST:
            PayoutRateAndConstant.objects.filter(pk=id).update(banking_payout_fee=request.POST['banking_payout_fee'], banking_payout_constant=request.POST['banking_payout_constant'], country=request.POST['country'])
        elif "message_texts_edit_form" in request.POST:
            MessageTexts.objects.filter(pk=id).update(messageID=request.POST['messageID'], header=request.POST['header'], message_text=request.POST['message_text'], priority=request.POST['priority'], receiving_audience=request.POST['receiving_audience'], where_used=request.POST['where_used'])
        elif "cook_grade_explain_edit_form" in request.POST:
            CookGradeExplaination.objects.filter(pk=id).update(grade=request.POST['grade'], description=request.POST['description'])
        elif "sos_contact_edit_form" in request.POST:
            SoSDangerContact.objects.filter(pk=id).update(country=request.POST['country'], contact=request.POST['contact'])
            
        return redirect('dashboard:app-configurations-parameters')


def delete_item(request, name, id):
    data_id=None

    if "deleteMenuCategory" in request.POST:
        data_id = MenuCategory.objects.get(pk=id)
    elif "deleteFSCImageFrequency" in request.POST:
        data_id = KitchenImageCaptureFrequency.objects.get(pk=id)
    elif name=="deleteMarketingFeeRate":
        data_id = MarketingFeeRate.objects.get(pk=id)
    elif name=="deleteDeliveryFeePAIDByCook":
        data_id = DeliveryFeesPaidByCook.objects.get(pk=id)
    elif name=="deleteFoodCategory":
        data_id = CountryWiseFoodCategory.objects.get(pk=id)
    elif name=="deleteFrequentKitchenOperations":
        data_id = FrequentKitchenOperations.objects.get(pk=id)
    elif name=="deleteKitchenEquipments":
        data_id = KitchenEquipments.objects.get(pk=id)
    elif name=="deleteFSCRegulationRulebook":
        data_id = FSCRegulationRulebook.objects.get(pk=id)
    elif name=="deleteFSCManualAnswers":
        data_id = FSCManualAnswers.objects.get(pk=id)

    elif name=="deleteFacialRecognitionImageCapture":
        data_id = FacialRecognitionImageCapture.objects.get(pk=id)
    elif name=="deleteCourierDefaultSearchRadius":
        data_id = CourierDefaultSearchRadius.objects.get(pk=id)
    elif name=="deletePaymentProcessing":
        data_id = PaymentProcessing.objects.get(pk=id)
    elif name=="deleteMinimumDeliveryPayRate":
        data_id = MinimumDeliveryPayRate.objects.get(pk=id)
    elif name=="deleteBufferDuration":
        data_id = BufferDuration.objects.get(pk=id)
    elif name=="deleteCostPerMileLoctoRes":
        data_id = CostPerMileLoctoRes.objects.get(pk=id)
    elif name=="deleteCostPerMileResToCus":
        data_id = CostPerMileResToCus.objects.get(pk=id)
    elif name=="deleteDefaultCourierPositioning":
        data_id = DefaultCourierPositioning.objects.get(pk=id)
    elif name=="deleteConstantPay":
        data_id = ConstantPay.objects.get(pk=id)
    elif name=="deleteConstantRangeDistance":
        data_id = ConstantRangeDistance.objects.get(pk=id)
    elif name=="deleteAggregatedOrder":
        data_id = AggregatedOrder.objects.get(pk=id)
    elif name=="deleteDefaultMinimumSearchRange":
        data_id = DefaultMinimumSearchRange.objects.get(pk=id)
    elif name=="deleteHotZoneIncentivePercentage":
        data_id = HotZoneIncentivePercentage.objects.get(pk=id)

    elif name=="deleteItemFilterByPriceRange":
        data_id = ItemFilterByPriceRange.objects.get(pk=id)
    elif name=="deleteDeliveryFeePaidByCustomer":
        data_id = DeliveryFeePaidByCustomer.objects.get(pk=id)
    elif name=="deleteTipsPercentage":
        data_id = TipsPercentage.objects.get(pk=id)
    elif name=="deleteSalesTax":
        data_id = SalesTax.objects.get(pk=id)
    elif name=="deleteConfigParametersTopDish":
        data_id = ConfigParametersTopDish.objects.get(pk=id)
    elif name=="deleteConfigParametersTopCook":
        data_id = ConfigParametersTopCook.objects.get(pk=id)
    elif name=="deleteConfigParametersFeaturedCook":
        data_id = ConfigParametersFeaturedCook.objects.get(pk=id)
    elif name=="deleteConfigParametersNearbyCook":
        data_id = ConfigParametersNearbyCook.objects.get(pk=id)

    elif name=="deleteCangurhuAppAvailability":
        data_id = CangurhuAppAvailability.objects.get(pk=id)
    elif name=="deletePaymentRateAndConstant":
        data_id = PaymentRateAndConstant.objects.get(pk=id)
    elif name=="deletePayoutRateAndConstant":
        data_id = PayoutRateAndConstant.objects.get(pk=id)
    elif name=="deleteMessageTexts":
        data_id = MessageTexts.objects.get(pk=id)
    elif name=="deleteCookGradeExplaination":
        data_id = CookGradeExplaination.objects.get(pk=id)
    elif name=="deleteSoSDangerContact":
        data_id = SoSDangerContact.objects.get(pk=id)

    data_id.delete()
    return redirect('dashboard:app-configurations-parameters')

        
