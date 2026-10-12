def extrair_dados_email(texto):
    """
    Recebe o texto bruto do e-mail e retorna uma lista com os códigos e preços.
    """
    linhas = texto.strip().split("\n")
    alteracoes = []

    for linha in linhas:
        if not linha.strip():
            continue
        
        dados = linha.split()
        if len(dados) >= 3:
            codigo = dados[0]
            custo = dados[1]
            venda = dados[2]
            
            alteracoes.append({
                "codigo": codigo,
                "custo": custo,
                "venda": venda
            })
            
    return alteracoes