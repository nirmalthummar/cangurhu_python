from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.notification.api.serializers import NotificationSerializer
from apps.notification.models import Notification
from common.exception import ErrorResponseException


class NotificationDataView(APIView):
    permission_classes = (IsAuthenticated,)
    swagger_tags = ['Notification list']

    def get(self, request,id=None):
        if id is None:
            notification = Notification.objects.filter(user_id=request.user,is_deleted=False)
            serializer = NotificationSerializer(notification, many=True)

        else:
            try:
                notification_detail = Notification.objects.get(id=id,user_id=request.user,is_deleted=False)
                serializer = NotificationSerializer(notification_detail)
            except Notification.DoesNotExist:
                raise ErrorResponseException(f"Notification does not exist!")
        return Response(serializer.data)



    def delete(self, request, id):
        """
            To Delete the particular notification
        """
        user_id = request.user.user_id
        try:
            notification = Notification.objects.get(id=id, user_id=user_id,is_deleted=False)

        except Notification.DoesNotExist:
            raise ErrorResponseException(f"Notification not available!")

        notification.is_deleted=True
        notification.save()


        return Response(
            status=status.HTTP_200_OK
        )
