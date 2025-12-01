from django.core.cache import cache
from django.conf import settings
import secrets
import hashlib


class RedisService:
    """
    Serviço para gerenciamento de cache com Redis
    """

    @staticmethod
    def gerar_token(length=32):
        """
        Gera um token aleatório de 32 caracteres
        """
        return secrets.token_urlsafe(length)

    @staticmethod
    def salvar_token(key, value, timeout=3600):
        """
        Salva um token no cache Redis

        Args:
            - key (str): Chave do token
            - value (str): Valor do token
            - timeout (int): Tempo de expiração do token
        """

        cache.set(key, value, timeout)
        return True

    @staticmethod
    def obter_token(key):
        """
        Obtem um token do cache Redis

        Args:
            - key (str): Chave do token

        Returns:
            - str: Valor do token
        """
        return cache.get(key)

    @staticmethod
    def verificar_token(key, token):
        """Verifica se o token é válido"""
        stored_token = cache.get(key)
        if stored_token and stored_token == token:
            return True
        return False
