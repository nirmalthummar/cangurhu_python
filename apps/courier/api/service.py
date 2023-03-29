from apps.order.api.service import get_user_default_address, get_distance
from apps.config.models import (
    CostPerMileLoctoRes,
    CostPerMileResToCus,
    MinimumDeliveryPayRate,
)

from common.exception import ErrorResponseException
from decimal import Decimal


class CourierOrderCalculation:

    def __init__(self, request, order, courier_order):
        self.request = request
        self.order = order
        self.courier_order = courier_order
        self.country = "canada"

    def get_distance1(self):
        """
           distance1: Distance between Driver position and Cook address
        """

        # courier live should be there, need to get it from the firebase
        courier_address = get_user_default_address(user_id=self.request.user.user_id)  # TODO
        cook_address = self.order.cook_address

        distance1 = get_distance(courier_address, cook_address)

        return distance1

    def get_distance2(self):
        """
           distance2: Distance between Cook address and Customer address
        """

        cook_address = self.order.cook_address
        customer_address = self.order.customer_address

        distance2 = get_distance(cook_address, customer_address)

        return distance2

    def get_total_distance(self, distance1, distance2):
        """
           distance1: Distance between Driver position and Cook address
           distance2: Distance between Cook address and Customer address
        """

        total = distance1 + distance2
        total_distance = float("{:.2f}".format(total))

        return total_distance

    def distance1_cost(self, distance1):
        """
            COST1_PERMILE: Cost per mileage for Distance 1
            This cost would be typically lower than the cost for Distance 2
            Ex: 0.05 $ / MILE
            This is a Configuration Parameter. It varies by city and zone (postal code)
        """

        try:
            FP0003C = CostPerMileLoctoRes.objects.get(country=self.country)

        except CostPerMileLoctoRes.DoesNotExist:
            raise ErrorResponseException(f"Config Parameter 'COST PER MILE FROM COURIER LOCATION TO RESTAURANT' is not available for Country '{self.country}'!")

        cost1_per_mile = FP0003C.cost
        decimal_value = Decimal(distance1) * cost1_per_mile
        distance1_cost = decimal_value.quantize(Decimal('0.00'))

        return distance1_cost

    def distance2_cost(self, distance2):
        """
            COST2_PERMILE: Cost per mileage for Distance 2
            Ex: 0.08 $ / MILE
            This is a Configuration Parameter. It varies by city and zone (postal code)
        """

        try:
            FP0004C = CostPerMileResToCus.objects.get(country=self.country)

        except CostPerMileResToCus.DoesNotExist:
            raise ErrorResponseException(
                f"Config Parameter 'COST PER MILE FROM RESTAURANT TO CUSTOMER' is not available for Country '{self.country}'!")

        cost2_per_mile = FP0004C.cost
        decimal_value = Decimal(distance2) * cost2_per_mile
        distance2_cost = decimal_value.quantize(Decimal('0.00'))

        return distance2_cost

    def check_hot_zone(self):
        is_hot_zone = False  # TODO
        return is_hot_zone

    def get_hot_zone_incentive(self):
        """
            Incentive given to Courier when a Zone is considered HOT with either
                - a high demand
                - peak time
                - other considerations
            ex: 10%
            This incentive is added on top of the courier normal price
            This is a Configuration Parameter
        """
        hot_zone_incentive_pct = Decimal(0.00)

        is_hot_zone = self.check_hot_zone()

        if is_hot_zone:
            hot_zone_incentive_pct = 100.0  # TODO

        return hot_zone_incentive_pct

    def get_courier_minimum_pay(self, total_distance):
        """
            Minimum Delivery Pay, in case the delivery distances are too short.
            If Distance1 + Distance 2 is higher than 3 miles, then Minimum delivery Fees is ZERO.
            This is a Configuration Parameter
        """

        if total_distance > 3:
            minimum_delivery_pay = Decimal(0.00)
        else:
            try:
                FP0006C = MinimumDeliveryPayRate.objects.get(country=self.country)
                minimum_delivery_pay = FP0006C.pay_rate

            except MinimumDeliveryPayRate.DoesNotExist:
                raise ErrorResponseException(
                    f"Config Parameter 'MINIMUM DELIVERY PAY' is not available for Country '{self.country}'!")

        return minimum_delivery_pay

    def courier_order_calculation(self):

        distance1 = self.get_distance1()
        distance2 = self.get_distance2()
        total_distance = self.get_total_distance(distance1, distance2)
        print("Distance1...", distance1)
        print("Distance2...", distance2)
        print("Total Distance...", total_distance)

        distance1_cost = self.distance1_cost(distance1)
        distance2_cost = self.distance2_cost(distance2)
        print("Distance1 Cost...", distance1_cost)
        print("Distance2 Cost...", distance2_cost)

        hot_zone_incentive_pct = self.get_hot_zone_incentive()
        print("Hot Zone...", hot_zone_incentive_pct)

        minimum_delivery_pay = self.get_courier_minimum_pay(total_distance)
        print("Minimum Delivery Pay...", minimum_delivery_pay)

        transit_pay = distance1_cost + distance2_cost + hot_zone_incentive_pct + minimum_delivery_pay
        print("Transit pay...", transit_pay)

        return total_distance, transit_pay
