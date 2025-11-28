from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """
    Example: You can override authenticate() to add extra logging
    or restrictions.
    """

    def authenticate(self, request):
        result = super().authenticate(request)
        return result
