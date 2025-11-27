from rest_framework import serializers


class UserAuthSerializer(serializers.Serializer):
    """
    Serializer para a autenticação do usuario

    Campos:
    - username: str - Nome do usuario
    - password: str - Senha do usuario
    """

    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
