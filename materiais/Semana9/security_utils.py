# ============================================================
# security_utils.py — Utilitários de segurança para mascaramento de logs
# ------------------------------------------------------------
# Este módulo ensina como proteger informações sensíveis
# (senhas, tokens, API keys, secrets) antes que apareçam nos logs.
#
# Ele contém:
#   ✔ SecureLogger — logger que mascara automaticamente dados sensíveis
#   ✔ mask_secret — função que esconde parte de um secret
#   ✔ secure_log_decorator — decorator que mascara argumentos sensíveis
#
# Esta é uma prática REAL usada em empresas.
# ============================================================

import re          # Usado para encontrar padrões sensíveis com expressões regulares
import logging     # Biblioteca padrão de logs do Python
from functools import wraps  # Permite criar decorators mantendo metadados da função


# ============================================================
# CLASSE: SecureLogger
# ------------------------------------------------------------
# Um logger que intercepta mensagens e mascara automaticamente
# qualquer informação sensível antes de registrar no log.
# ============================================================
class SecureLogger:
    """Logger que automaticamente mascara informações sensíveis."""

    def __init__(self, logger_name):
        # Cria um logger normal do Python
        self.logger = logging.getLogger(logger_name)

        # ------------------------------------------------------------
        # Lista de padrões que devem ser mascarados.
        # Cada item é uma tupla: (regex_para_encontrar, texto_para_substituir)
        # ------------------------------------------------------------
        self.sensitive_patterns = [
            (r'password["\s]*[:=]["\s]*([^"\s,}]+)', r'password="***MASKED***"'),
            (r'api[_-]?key["\s]*[:=]["\s]*([^"\s,}]+)', r'api_key="***MASKED***"'),
            (r'token["\s]*[:=]["\s]*([^"\s,}]+)', r'token="***MASKED***"'),
            (r'secret["\s]*[:=]["\s]*([^"\s,}]+)', r'secret="***MASKED***"'),
        ]

    # ------------------------------------------------------------
    # Função interna que recebe uma mensagem e substitui qualquer
    # dado sensível por "***MASKED***".
    # ------------------------------------------------------------
    def _mask_sensitive_data(self, message):
        for pattern, replacement in self.sensitive_patterns:
            message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)
        return message

    # ------------------------------------------------------------
    # Métodos de log (info, error, debug)
    # Todos passam pela função de mascaramento antes de registrar.
    # ------------------------------------------------------------
    def info(self, message):
        masked_message = self._mask_sensitive_data(str(message))
        self.logger.info(masked_message)

    def error(self, message):
        masked_message = self._mask_sensitive_data(str(message))
        self.logger.error(masked_message)

    def debug(self, message):
        masked_message = self._mask_sensitive_data(str(message))
        self.logger.debug(masked_message)


# ============================================================
# Função auxiliar: mask_secret
# ------------------------------------------------------------
# Recebe um secret (senha, token, etc.) e esconde o meio,
# deixando apenas alguns caracteres visíveis.
#
# Exemplo:
#   mask_secret("1234567890") → "1234****7890"
# ============================================================
def mask_secret(secret, visible_chars=4):
    if not secret or len(secret) <= visible_chars * 2:
        return "***MASKED***"

    return (
        secret[:visible_chars]
        + "*" * (len(secret) - visible_chars * 2)
        + secret[-visible_chars:]
    )


# ============================================================
# Decorator: secure_log_decorator
# ------------------------------------------------------------
# Ele intercepta a chamada de uma função e:
#   ✔ mascara argumentos sensíveis
#   ✔ registra logs seguros antes e depois da execução
#   ✔ captura erros sem expor dados sensíveis
#
# É perfeito para funções como:
#   - login
#   - conexão com banco
#   - chamadas de API
# ============================================================
def secure_log_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        secure_logger = SecureLogger(func.__module__)

        # ------------------------------------------------------------
        # Mascara automaticamente argumentos sensíveis
        # ------------------------------------------------------------
        safe_kwargs = {}
        for key, value in kwargs.items():
            if any(sensitive in key.lower() for sensitive in ['password', 'key', 'token', 'secret']):
                safe_kwargs[key] = mask_secret(str(value))
            else:
                safe_kwargs[key] = value

        secure_logger.info(f"Executando {func.__name__} com args: {safe_kwargs}")

        try:
            result = func(*args, **kwargs)
            secure_logger.info(f"{func.__name__} executado com sucesso")
            return result

        except Exception as e:
            secure_logger.error(f"Erro em {func.__name__}: {str(e)}")
            raise

    return wrapper
