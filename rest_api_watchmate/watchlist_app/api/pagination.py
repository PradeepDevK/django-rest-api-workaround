from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
)


class WatchListPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_strings = ('last',)
    
    
class WatchListOffsetPagination(LimitOffsetPagination):
    default_limit = 5
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 10
    