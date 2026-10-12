from datetime import datetime
from caminho import CAMINHO_LOG

def registrar_log(mensagem):
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{data_hora}] {mensagem}\n"

    # Usa o caminho centralizado do executável
    with open(CAMINHO_LOG, "a", encoding="utf-8") as f:
        f.write(linha)