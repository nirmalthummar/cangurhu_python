from haversine import Unit

from apps.address.models import Address
from common.exception import ErrorResponseException


def get_user_in_range(lat, lang):
    import haversine as hs
    address1_lat = float(lat)
    address1_lon = float(lang)
    if not address1_lat and address1_lon:
        raise ErrorResponseException("There is issue with the Address Latitude and Longitude")
    address1 = (address1_lat, address1_lon)
    users = Address.objects.filter(user_id__role__contains=['cook'])
    user_id_list = []
    radius=10
    for user in users:
        address2_lat = float(user.latitude)
        address2_lon = float(user.longitude)
        address2 = (address2_lat, address2_lon)
        distance = hs.haversine(address1, address2, unit=Unit.KILOMETERS)
        if float(distance) <= float(radius):
            user_id_list.append(user.user_id)

    return user_id_list