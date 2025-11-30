from rest_framework import authentication
from rest_framework import exceptions
from services.redis_service import RedisService


class ClienteAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        email = request.query_params.get("email")
        token = request.headers.get("Authorization")
        if not token:
            return None

        try:
            is_authenticated = RedisService.verificar_token(email, token)
            if not is_authenticated:
                return None
            return (email, None)
        except Exception as e:
            raise exceptions.AuthenticationFailed("Invalid token")
