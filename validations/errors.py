from rest_framework.response import Response

def api_error(code: str,message: str,details=None, status_code: int =400) -> Response:
    """
    Standard error payload used across the API
    """
    if details is None:
        details = {}
    return Response(
        { "code": code, "message": message, "details": details },
        status=status_code,
    )