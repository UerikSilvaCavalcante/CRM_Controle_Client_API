"""
Serializer para o modelo Clientes
"""

from rest_framework import serializers
from clientes.models import Clientes
from nota.models import Nota
from nota.serializers import NotaSerializer


class ClienteSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Clientes

    Campos serializados
    - created_at: datetime - Data de criação do cliente
    - name: str - Nome do cliente
    - email: str - Email do cliente
    - phone: str - Telefone do cliente

    """

    class Meta:
        """
        Meta class para configurar o serializer
        """

        model = Clientes
        fields = "__all__"

        read_only_fields = ["created_at"]

    created_at = serializers.SerializerMethodField()
    vendedor = serializers.ReadOnlyField(source="responsavel.username")
    notas = serializers.SerializerMethodField(read_only=True)

    def create(self, validated_data):
        """
        Garante que o nomer seja salvo com a primeira letra maiuscula

        Parametros
        - validated_data: dict - Dados validados do serializer

        Retorno
        - cliente: Clientes - Instancia do modelo Clientes
        """
        name = validated_data["name"]
        name = name.strip().title()
        validated_data["name"] = name
        cliente = Clientes.objects.create(**validated_data)
        return cliente

    def validate_name(self, value):
        """
        Valida o nome do cliente

        Parametros
        - value: str - Nome do cliente

        Retorno
        - value: str - Nome do cliente
        """
        value = value.strip()
        if value == "":
            raise serializers.ValidationError("O nome não pode ser vazio")
        return value

    def get_created_at(self, obj):
        """
        Formata a data de criação do cliente

        Parametros
        - obj: Clientes - Instancia do modelo Clientes

        Retorno
        - obj.created_at.strftime("%d/%m/%Y"): str - Data formatada

        Ex.:
        - 01/01/2023T00:00:00 = 01/01/2023
        """
        return obj.created_at.strftime("%d/%m/%Y")

    def get_notas(self, obj):
        """
        Retorna as notas do cliente

        Parametros
        - obj: Clientes - Instancia do modelo Clientes

        Retorno
        - notas: list - Lista de notas
        """
        notas = Nota.objects.filter(cliente__id=obj.pk).all()
        if notas:
            notas_serializers = NotaSerializer(notas, many=True).data

            return [
                {
                    "id": nota["id"],
                    "title": nota["title"],
                    "description": nota["description"],
                }
                for nota in notas_serializers
            ]
        return []
