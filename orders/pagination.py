from rest_framework import pagination
from rest_framework.response import Response


class OrderCustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000000
    page_query_param = 'page'

    def get_paginated_response(self, data):
        current_page = 1
        if self.page.has_previous():
            current_page = self.page.previous_page_number() + 1
        elif self.page.has_next():
            current_page = self.page.next_page_number() - 1

        return Response({
            'orders_on_page': len(data),
            'page': current_page,
            'orders': data
        })