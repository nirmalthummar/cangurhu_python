from django.db.models import Q
from django.db.models import QuerySet

from core.constant import ACTIVE


class UserQueryset(QuerySet):
    def active_users(self):
        return self.filter(Q(is_active=True) & Q(status=ACTIVE))
