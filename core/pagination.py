from collections import OrderedDict
from rest_framework import pagination
from rest_framework.response import Response


class CustomPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_count', self.page.paginator.num_pages),
            ('next', self.get_next_link() if self.get_next_link() else ""),
            ('previous', self.get_previous_link() if self.get_previous_link() else ""),
            ('results', data)
        ]))
