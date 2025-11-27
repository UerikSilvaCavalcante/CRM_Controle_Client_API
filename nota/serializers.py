from rest_framework import serializers
from .models import Nota
from clientes.models import Clientes


class NotaSerializer(serializers.ModelSerializer):
    """
    Serializer para Nota model

    Serializa os campos com base na Model de Nota

    """

    # cliente = serializers.SerializerMethodField()
    nome_cliente = serializers.ReadOnlyField(source="cliente.__str__")

    class Meta:
        model = Nota
        fields = "__all__"

        read_only_fields = ["created_at", "updated_at"]

    def get_created_at(self, obj):
        """
        Formata a data de criação da nota

        Parametros
        - obj: Nota - Instancia do modelo Nota

        Retorno
        - obj.created_at.strftime("%d/%m/%Y"): str - Data formatada
        """
        return obj.created_at.strftime("%d/%m/%Y")

    def get_updated_at(self, obj):
        """
        Formata a data de alteração da nota

        Parametros
        - obj: Nota - Instancia do modelo Nota

        Retorno
        - obj.updated_at.strftime("%d/%m/%Y"): str - Data formatada
        """
        return obj.updated_at.strftime("%d/%m/%Y")

    def validate_cliente(self, value):
        """
        Valida o cliente da nota

        Parametros
        - value: Clientes - Instancia do modelo Clientes

        Retorno
        - value: Clientes - Instancia do modelo Clientes
        """
        cliente = value
        # print(cliente.id)
        exists_cliente = Clientes.objects.filter(pk=cliente.pk).exists()
        if not cliente:
            raise serializers.ValidationError("O cliente da nota é obrigatório")
        if not exists_cliente:
            raise serializers.ValidationError("O cliente não existe no banco de dados")
        return value

    # def get_cliente(self, obj):
    #     """
    #     Retorna o nome do cliente da nota

    #     Parametros
    #     - obj: Nota - Instancia do modelo Nota

    #     Retorno
    #     - obj.cliente.name: str - Nome do cliente
    #     """
    #     return obj.cliente.__str__()
