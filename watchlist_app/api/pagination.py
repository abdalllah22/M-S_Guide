from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 1
    # page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 2

class WatchListLOPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class WatchListCPagination(CursorPagination):
    page_size = 6