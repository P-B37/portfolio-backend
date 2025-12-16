from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for the API.

    This pagination class extends the `PageNumberPagination` class from
    the Django REST Framework to provide a custom response format. The
    response includes a 'meta' object with pagination details and a
    'results' array with the data.

    Attributes:
        page_size (int): The number of items to include on each page.
        page_size_query_param (str): The name of the query parameter that
            allows clients to override the page size.
        max_page_size (int): The maximum allowed page size.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Returns a paginated response with a custom format.

        This method overrides the default `get_paginated_response` method
        to provide a custom response structure that includes a 'meta'
        object with pagination details and a 'results' array with the
        paginated data.

        Args:
            data (list): The paginated data to be included in the response.

        Returns:
            Response: A Django REST Framework `Response` object with the
                custom paginated response.
        """
        return Response(
            {
                "meta": {
                    "count": self.page.paginator.count,
                    "page": self.page.paginator.num_pages,
                    "current_page": self.page.number,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "results": data,
            }
        )
