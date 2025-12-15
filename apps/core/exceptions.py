from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """Custom exception handler for Django REST Framework.

    This function is used to customize the response format of exceptions
    raised in the application. It returns a JSON response with a
    consistent error structure.

    Args:
        exc (Exception): The exception that was raised.
        context (dict): A dictionary containing the context of the exception.

    Returns:
        Response: A Django REST Framework Response object with a custom
                  error format, or None if the exception is not handled.
    """
    response = exception_handler(exc, context)

    if response is not None:
        custom_data =  {
            "success": False,
            "status_code": response.status_code,
            "message": "An Error Occured",
            "errors": response.data
        }

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            custom_data["message"] = "Bad Request"
        elif response.status_code == status.HTTP_401_UNAUTHORIZED:
            custom_data["message"] = "Authentification credentials were not provided or are invalid."
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            custom_data["message"] = "You do not have permission to perform this action."
        elif response.status_code == status.HTTP_404_NOT_FOUND:
            custom_data["message"] = "The requested resource was not found."
        elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            custom_data["message"] = "Internal Server Error. Please try again later."
        elif response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED:
            custom_data["message"] = "The method is not allowed for the requested URL." 
        elif response.status_code == status.HTTP_408_REQUEST_TIMEOUT:
            custom_data["message"] = "The server timed out waiting for the request."    

        response.data = custom_data

    return response