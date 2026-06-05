# ============================================================
# database.py — Exemplo de uso seguro do sistema de logs
# ------------------------------------------------------------
# Aqui mostramos como:
#   ✔ usar o SecureLogger
#   ✔ aplicar o decorator secure_log_decorator
#   ✔ mascarar senhas manualmente
#   ✔ simular uma conexão segura com banco de dados
# ============================================================

from security_utils import SecureLogger, secure_log_decorator, mask_secret

# Cria um logger seguro para este módulo
secure_logger = SecureLogger(__name__)


# ------------------------------------------------------------
# A função abaixo simula uma conexão com banco de dados.
# Ela é decorada com secure_log_decorator, então:
#   ✔ argumentos sensíveis são mascarados automaticamente
#   ✔ logs são registrados antes e depois da execução
#   ✔ erros são capturados com segurança
# ------------------------------------------------------------
@secure_log_decorator
def connect_database(host, user, password, database):
    """Conecta ao banco de dados de forma segura."""

    # ------------------------------------------------------------
    # Logs seguros — sem expor a senha real
    # ------------------------------------------------------------
    secure_logger.info(f"Conectando ao banco {database} em {host}")
    secure_logger.info(f"Usuário: {user}")
    secure_logger.info(f"Senha configurada: {password is not None}")

    # ------------------------------------------------------------
    # Cria uma connection string mascarada
    # (em sistemas reais, NUNCA logamos a senha)
    # ------------------------------------------------------------
    connection_string = f"postgresql://{user}:{mask_secret(password)}@{host}/{database}"
    secure_logger.debug(f"Connection string (mascarada): {connection_string}")

    # ------------------------------------------------------------
    # Simulação de conexão real
    # ------------------------------------------------------------
    return {
        "status": "connected",
        "connection_string": connection_string
    }
