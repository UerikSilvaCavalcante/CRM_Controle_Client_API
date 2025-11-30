from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from auth_user.serializers import UserAuthSerializer
from django.core.mail import send_mail
from services.redis_service import RedisService
from clientes.models import Clientes
from django.conf import settings
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import permissions


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

    serializer_class = UserAuthSerializer

    @swagger_auto_schema(
        operation_summary="Login de Usuário",
        operation_description="Autentica um usuário com username e password, retornando um token de autenticação",
        request_body=UserAuthSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "token": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Token de autenticação",
                    )
                },
            ),
            401: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Mensagem de erro",
                    )
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Mensagem de erro",
                    )
                },
            ),
        },
        tags=["Autenticação"],
        security=[],
    )
    def post(self, request, *args, **kwargs) -> Response:
        """
        Autenticação por AuthToken

        """
        serializer = UserAuthSerializer(
            data=request.data,
        )

        if serializer.is_valid():

            username = serializer.validated_data["username"]  # type: ignore
            password = serializer.validated_data["password"]  # type: ignore
            user = authenticate(request, username=username, password=password)

            if user is not None:
                token, created = Token.objects.get_or_create(user=user)

                return Response(
                    {"token": token.key, "created": token.created}, status=200
                )
            else:
                return Response({"error": "Invalid credentials"}, status=401)
        else:
            return Response({"error": "Invalid credentials"}, status=401)


class CustomClienteAuthToken(APIView):
    """
    Rota de Autenticação por AuthToken

    Methods:
    POST

    Prameters:
    - email: str

    Returns:
    - is_authenticate: bool


    """

    @swagger_auto_schema(
        operation_summary="Login de Cliente",
        operation_description="Autentica um usuário com email, enviando um token de autenticação pelo email do cliente",
        request_body=UserAuthSerializer,
        responses={
            200: UserAuthSerializer,
            401: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Mensagem de erro",
                    )
                },
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Mensagem de erro",
                    )
                },
            ),
        },
        tags=["Autenticação"],
        security=[],
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        cliente = Clientes.objects.get(email=email)

        token = RedisService.gerar_token()

        RedisService.salvar_token(cliente.email, token)

        send_mail(
            subject="Token de Autenticação",
            message=f"Aqui está seu token de autenticação: {token}, vencendo em 1 hora, se não foi você apenas ignore essa mensagem.",
            recipient_list=[cliente.email],
            fail_silently=False,
            from_email=settings.EMAIL_HOST_USER,
        )
        return Response({"authenticate": True})
