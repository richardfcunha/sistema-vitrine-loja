import os
import sys

def obter_caminho_base():
    """
    Retorna sempre a pasta real onde o .exe está a correr 
    (ou a pasta do script se estiver a testar em .py).
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = obter_caminho_base()

# Tudo fica fixo na pasta do executável, independentemente do computador
CAMINHO_DB = os.path.join(BASE_DIR, "banco.db")
CAMINHO_RELATORIOS = os.path.join(BASE_DIR, "relatorios")
CAMINHO_LOG = os.path.join(BASE_DIR, "historico.log")