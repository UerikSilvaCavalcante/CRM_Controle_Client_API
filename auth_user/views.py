from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from auth_user.serializers import UserAuthSerializer


class CustomAuthToken(APIView):
    """
    Rota de Autenticação por AuthToken

    Methods:
    POST

    Prameters:
    - username: str
    - password: str

    Returns:
    - token: str
    
    Serializer:
    UserAuthSerializer
    """

    def post(self, request, *args, **kwargs):
        serializer = UserAuthSerializer(
            data=request.data,
        )

        if serializer.is_valid():

            username = serializer.validated_data["username"]  # type: ignore
            password = serializer.validated_data["password"]  # type: ignore
            user = authenticate(request, username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                
                return Response({"token": token.key, "created": token.created})
            else:
                return Response({"error": "Invalid credentials"}, status=401)
        else:
            return Response({"error": "Invalid credentials"}, status=401)
