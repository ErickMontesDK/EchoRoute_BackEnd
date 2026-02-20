from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    """
    Custom exception handler to format error responses globally.
    """
    response = exception_handler(exc, context)

    if response is not None:
        status_code = response.status_code
        
        status_names = {
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            405: "Method Not Allowed",
            500: "Internal Server Error",
        }
        
        status_name = status_names.get(status_code, "Error")
        
        original_data = response.data
        message = original_data
        
        if isinstance(original_data, dict) and 'detail' in original_data:
            message = original_data['detail']
        
        response.data = {
            "error": f"{status_code} - {status_name}",
            "message": message
        }

    return response
