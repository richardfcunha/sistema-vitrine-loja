from datetime import datetime

def registrar_log(mensagem):
    """Regista uma ação com data e hora num ficheiro historico.log"""
    data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{data_hora}] {mensagem}\n"
    
    # Abre o ficheiro em modo de adição ('a' - append) para não apagar os registos anteriores
    with open("historico.log", "a", encoding="utf-8") as f:
        f.write(linha)