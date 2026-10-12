import os
import sys

def obter_caminho_base():
    """Retorna o diretório correto onde o .exe ou o script Python está localizado"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Diretório base universal
BASE_DIR = obter_caminho_base()

# Caminhos absolutos centralizados para todo o sistema
CAMINHO_DB = os.path.join(BASE_DIR, "banco.db")
CAMINHO_RELATORIOS = os.path.join(BASE_DIR, "relatorios")
CAMINHO_LOG = os.path.join(BASE_DIR, "historico.log")