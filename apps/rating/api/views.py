from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsCustomer, IsOwnerOrReadOnly
from common.exception import ErrorResponseException
from apps.rating.models import CookFeedback, DishGrade
from apps.rating.api.serializers import CookFeedbackSerializer, CookFeedbackSaveSerializer, DishGradeSerializer
from apps.cook.models import Cook, MenuItem
from apps.customer.models import Customer
from apps.courier.models import Courier


class CookFeedbackView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer,)

    def get(self, request):
        """
            Get all the feedback for particular cook
        """
        query_params = request.GET

        queryset = CookFeedback.objects.filter(active=True)

        if 'cook_id' in query_params:
            cook_id = query_params.get('cook_id')
            try:
                cook = Cook.objects.get(cook_id=cook_id)
                queryset = queryset.filter(cook=cook)

            except Cook.DoesNotExist:
                raise ErrorResponseException(f"Cook is not exist with '{cook_id}' cook ID!")

        if 'courier_id' in query_params:
            courier_id = query_params.get('courier_id')
            try:
                courier = Courier.objects.get(courier_id=courier_id)
                queryset = queryset.filter(courier_user=courier)

            except Courier.DoesNotExist:
                raise ErrorResponseException(f"Courier is not exist with courier ID '{courier_id}'!")

        serializer = CookFeedbackSerializer(queryset, many=True)

        return Response(
            {
                'feedback': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """
            Give rating and feedback to cook
        """
        customer_id = request.user.customer
        customer = Customer.objects.get(customer_id=customer_id)
        payload = request.data
        cook_id = payload.get('cook_id')
        courier_id = payload.get('courier_id')

        courier = None
        cook = None
        if cook_id:
            try:
                cook = Cook.objects.get(cook_id=cook_id)

            except Cook.DoesNotExist:
                raise ErrorResponseException(f"Cook is not exist with cook ID '{cook_id}'!")

        elif courier_id:
            try:
                courier = Courier.objects.get(courier_id=courier_id)

            except Courier.DoesNotExist:
                raise ErrorResponseException(f"Courier is not exist with courier ID '{courier_id}'!")
        else:
            raise ErrorResponseException(f"Cook or Courier ID is required!")

        star_rating = payload.get('star_rating')
        if not star_rating:
            raise ErrorResponseException("star rating is empty!")
        star_rating = str(star_rating)
        if not 1 <= int(star_rating) <= 5:
            raise ErrorResponseException("Rating should be between 1 to 5!")
        star_rating = int(star_rating)

        payload['customer'] = customer.id

        if cook_id:
            payload['cook'] = cook.id
            payload['courier_user'] = None
        else:
            payload['courier_user'] = courier.id
            payload['cook'] = None

        cook_feedback = None
        try:
            cook_feedback = CookFeedback.objects.get(customer=customer, cook=cook, courier_user=courier)


        except CookFeedback.DoesNotExist:
            serializer = CookFeedbackSaveSerializer(
                data=payload
            )
            if serializer.is_valid():
                serializer.save()
                star_rating = CookFeedback.objects.filter(cook=cook)
                star_rating_sum = 0
                for rating in star_rating:
                    star_rating_sum += rating.star_rating
                if cook_id:
                    cook.total_review += 1
                    cook.save()
                    total_reviews = cook.total_review
                    avg_rating = star_rating_sum / total_reviews
                    cook.avg_star_rating = avg_rating

                    cook.save()

            else:
                raise ErrorResponseException(str(serializer.errors))

        if cook_feedback:
            raise ErrorResponseException(f"Feedback is already given by Customer '{customer.user.username}'!")

        return Response(
            {
                'feedback': serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class CookFeedbackDetailView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer,)

    def put(self, request, feedback_id):
        """
            To update the particular feedback of customer
        """
        customer_id = request.user.customer
        customer = Customer.objects.get(customer_id=customer_id)
        payload = request.data

        try:
            cook_feedback = CookFeedback.objects.get(id=feedback_id, customer=customer)

        except CookFeedback.DoesNotExist:
            raise ErrorResponseException(f"Feedback is not given by the Customer {customer_id}!")

        # cook_id = payload.get('cook_id')
        # courier_id = payload.get('courier_id')
        #
        # if cook_id:
        #     try:
        #         cook = Cook.objects.get(cook_id=cook_id)
        #
        #     except Cook.DoesNotExist:
        #         raise ErrorResponseException(f"Cook is not exist with cook ID '{cook_id}'!")
        #
        # elif courier_id:
        #     try:
        #         courier = Courier.objects.get(courier_id=courier_id)
        #
        #     except Courier.DoesNotExist:
        #         raise ErrorResponseException(f"Courier is not exist with courier ID '{courier_id}'!")
        #
        # else:
        #     raise ErrorResponseException(f"Cook or Courier ID is required!")

        star_rating = str(payload.get('star_rating'))
        if not star_rating:
            raise ErrorResponseException("star rating is empty!")
        if not 1 <= int(star_rating) <= 5:
            raise ErrorResponseException("Rating should be between 1 to 5!")
        star_rating = int(star_rating)

        feedback = payload.get('feedback')
        if not feedback:
            raise ErrorResponseException("Feedback is empty!")

        serializer = CookFeedbackSaveSerializer(
            instance=cook_feedback,
            data={
                'star_rating': star_rating,
                'feedback': feedback
            },
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
        else:
            raise ErrorResponseException(str(serializer.errors))

        return Response(
            {
                'feedback': serializer.data
            },
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, feedback_id):
        """
            To update the particular feedback of customer
        """
        customer_id = request.user.customer
        customer = Customer.objects.get(customer_id=customer_id)

        try:
            cook_feedback = CookFeedback.objects.get(id=feedback_id, customer=customer)

        except CookFeedback.DoesNotExist:
            raise ErrorResponseException(f"Feedback is not given by the Customer {customer_id}!")

        cook_feedback.delete()

        return Response(
            status=status.HTTP_200_OK
        )


class DishGradeView(APIView):
    permission_classes = (IsAuthenticated, IsCustomer,)

    def get(self, request, menu_item_id):
        """
            Get all the feedback for particular Menu Item
        """
        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)

        except MenuItem.DoesNotExist:
            raise ErrorResponseException(f"Menu Item is not exist with '{menu_item_id}' ID!")

        queryset = DishGrade.objects.filter(menu_item=menu_item)

        serializer = DishGradeSerializer(queryset, many=True)

        return Response(
            {
                'feedback': serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request, menu_item_id):
        """
            Give rating and feedback to Cook Menu Item
        """
        customer_id = request.user.customer
        customer = Customer.objects.get(customer_id=customer_id)

        payload = request.data

        try:
            menu_item = MenuItem.objects.get(id=menu_item_id)

        except MenuItem.DoesNotExist:
            raise ErrorResponseException(f"Menu Item is not exist with '{menu_item_id}' ID!")

        like = payload.get('like')
        if like and like not in ["0", "1", 0, 1]:
            raise ErrorResponseException("like value should be either 0 or 1!")

        dislike = payload.get('dislike')
        if dislike and dislike not in ["0", "1", 0, 1]:
            raise ErrorResponseException("dislike value should be either 0 or 1!")
        star_rating=payload.get('star_rating')
        taste = payload.get('taste')
        use_of_ingredients = payload.get('use_of_ingredients')
        presentation = payload.get('presentation')

        dish_grade = None

        try:
            dish_grade = DishGrade.objects.get(customer=customer, menu_item=menu_item)

        except DishGrade.DoesNotExist:
            serializer = DishGradeSerializer(
                data={
                    'customer': customer.id,
                    'menu_item': menu_item.id,
                    'star_rating':star_rating,
                    'like': like,
                    'dislike': dislike,
                    'taste': taste,
                    'use_of_ingredients': use_of_ingredients,
                    'presentation': presentation
                }
            )
            if serializer.is_valid():
                print("heelo")
                serializer.save()
                if like:
                    menu_item.total_like += 1
                if dislike:
                    menu_item.total_dislike += 1
                menu_item.total_review += 1
                menu_item.save()
                star_rating = DishGrade.objects.filter(menu_item=menu_item)
                star_rating_sum = 0
                for rating in star_rating:
                    star_rating_sum += rating.star_rating
                total_reviews = menu_item.total_review
                avg_star_rating = star_rating_sum / total_reviews
                menu_item.avg_star_rating = avg_star_rating
                menu_item.save()


            else:

                raise ErrorResponseException(str(serializer.errors))

        if dish_grade:
            raise ErrorResponseException(
                f"Feedback is already given by Customer '{customer.user.username}' to Menu Item '{menu_item.title}'!")

        return Response(
            {
                'feedback': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
