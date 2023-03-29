import calendar
import datetime
import math
import random
from django_otp.util import random_hex


def base36encode(number, alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
    if not isinstance(number, (int)):
        raise TypeError('number must be an integer')

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36


def base36decode(number):
    return int(number, 36)


# Get Current UNIX Timestamp
def get_current_timestamp():
    ts = datetime.datetime.utcnow()  # GET Current UTC Datetime
    ts = calendar.timegm(ts.timetuple())  # Convert into UNIX Timestamp
    return ts


def default_key():
    return random_hex(20)


def upload_path_handler(instance, filename):
    return "{model}/{id}/{file}".format(model=instance._meta.model_name, id=instance.pk, file=filename)


def next_string(s):
    a1 = range(65, 91)  # capital letters
    a2 = range(97, 123)  # letters
    a3 = range(48, 58)  # numbers
    char = ord(s[-1])

    for a in [a1, a2, a3]:
        if char in a:
            if char + 1 in a:
                return s[:-1] + chr(char + 1)
            else:
                ns = next_string(s[:-1]) if s[:-1] else chr(a[0])
                return ns + chr(a[0])


def generate_sequence(country, holder, seq=None):
    if not seq:
        seq = 'AA00000000'
    next_seq = next_string(seq)
    return f"{country}{holder}{next_seq}"


def generate_item_sequence(cook_id, seq='X0000'):
    next_seq = next_string(seq)
    return f"{cook_id}{next_seq}"


def generate_order_sequence(date, country, seq='AAA000A'):
    next_seq = next_string(seq)
    return f"{date}{country}-{next_seq}"
