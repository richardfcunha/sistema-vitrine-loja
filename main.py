from database import criar_tabela, inserir_produto, listar_produtos, buscar_produto, excluir_produto, atualizar_descricao
from processar_email import extrair_dados_email
from gerar_pdf import gerar_pdf_alteracoes
from logger import registrar_log

def exibir_menu():
    print("\n" + "=" * 45)
    print(" 🏷️  SISTEMA DE PRECIFICAÇÃO DA VITRINE")
    print("=" * 45)
    print("[1] Cadastrar produto na vitrine")
    print("[2] Listar produtos da vitrine")
    print("[3] Atualizar descrição de um produto")
    print("[4] Processar e-mails de alteração de preço")
    print("[5] Remover produto da vitrine")
    print("[6] Sair")
    print("-" * 45)

def main():
    # Garante que a tabela existe ao iniciar o programa
    criar_tabela()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- CADASTRAR NOVO PRODUTO NA VITRINE ---")
            codigo = input("Digite o código do produto: ").strip()
            descricao = input("Digite o nome/descrição do produto: ").strip()
            
            if codigo and descricao:
                inserir_produto(codigo, descricao)
                registrar_log(f"Produto cadastrado: Código {codigo} - {descricao}") # <--- AQUI
                print("✅ Produto cadastrado com sucesso!") # (Opcional, mas bom para feedback visual)
            else:
                print("❌ Erro: Código e descrição não podem estar vazios.")

        elif opcao == "2":
            print("\n--- PRODUTOS ATUALMENTE NA VITRINE ---")
            produtos = listar_produtos()
            if not produtos:
                print("Nenhum produto cadastrado na vitrine ainda.")
            else:
                for codigo, descricao in produtos:
                    print(f"Código: {codigo} | Produto: {descricao}")

        elif opcao == "3":
            print("\n--- ATUALIZAR DESCRIÇÃO DO PRODUTO ---")
            codigo = input("Digite o código do produto que deseja atualizar: ").strip()
            
            if codigo:
                produto = buscar_produto(codigo)
                if produto:
                    _, descricao_atual = produto
                    print(f"Produto encontrado: {descricao_atual}")
                    nova_descricao = input("Digite a nova descrição do produto: ").strip()
                    
                    if nova_descricao:
                        atualizar_descricao(codigo, nova_descricao)
                        registrar_log(f"Descrição atualizada - Código {codigo}: '{descricao_atual}' para '{nova_descricao}'") # <--- AQUI
                        print("✅ Descrição atualizada com sucesso!")
                    else:
                        print("❌ A nova descrição não pode estar vazia.")
                else:
                    print(f"❌ O produto com o código '{codigo}' não foi encontrado na vitrine.")
            else:
                print("❌ Código inválido.")

        elif opcao == "4":
            print("\n--- PROCESSANDO ALTERAÇÕES DE PREÇO ---")
            print("Cole o texto do e-mail abaixo.")
            print("Dica: Quando terminar de colar, digite a palavra 'FIM' em uma nova linha e aperte Enter:\n")

            linhas_digitadas = []
            while True:
                try:
                    linha = input()
                    if linha.strip().upper() == "FIM":
                        break
                    linhas_digitadas.append(linha)
                except EOFError:
                    break

            texto_email = "\n".join(linhas_digitadas)

            if not texto_email.strip():
                print("\n❌ Nenhum texto foi inserido.")
                continue

            dados_email = extrair_dados_email(texto_email)
            itens_vitrine_alterados = []

            for item in dados_email:
                codigo = item["codigo"]
                produto = buscar_produto(codigo)

                if produto:
                    _, descricao = produto
                    itens_vitrine_alterados.append({
                        "descricao": descricao,
                        "codigo": codigo,
                        "custo": item["custo"],
                        "venda": item["venda"]
                    })

            print("\n" + "=" * 50)
            print("🏷️  RELATÓRIO DE ALTERAÇÃO DE PREÇOS - VITRINE")
            print("=" * 50)
            print(f"Total de itens na vitrine que mudaram: {len(itens_vitrine_alterados)}\n")

            if not itens_vitrine_alterados:
                print("Nenhum item da vitrine sofreu alteração com os dados informados.")
            else:
                for item in itens_vitrine_alterados:
                    print(f"📦 Produto   : {item['descricao'].upper()}")
                    print(f"   Código    : {item['codigo']}")
                    print(f"   Novo Preço: R$ {item['venda']} (Custo: R$ {item['custo']})")
                    print("-" * 50)

                # PERGUNTA SE DESEJA GERAR O PDF PARA IMPRESSÃO
                gerar = input("\nDeseja gerar um arquivo PDF com essa lista para impressão? (s/n): ").strip().lower()
                if gerar == 's':
                    gerar_pdf_alteracoes(itens_vitrine_alterados)

        elif opcao == "5":
            print("\n--- REMOVER PRODUTO DA VITRINE ---")
            codigo = input("Digite o código do produto que deseja remover: ").strip()
            
            if codigo:
                produto = buscar_produto(codigo)
                if produto:
                    _, descricao = produto
                    confirmacao = input(f"Confirma a remoção de '{descricao}' (Código: {codigo}) da vitrine? (s/n): ").strip().lower()
                    if confirmacao == 's':
                        excluir_produto(codigo)
                        registrar_log(f"Produto removido da vitrine - Código {codigo} ({descricao})") # <--- AQUI
                        print("✅ Produto removido com sucesso!")
                    else:
                        print("❌ Operação cancelada.")
                else:
                    print(f"❌ O produto com o código '{codigo}' não foi encontrado na vitrine.")
            else:
                print("❌ Código inválido.")

        elif opcao == "6":
            print("\nSaindo do sistema. Até logo!")
            break
        else:
            print("\n❌ Opção inválida! Escolha um número de 1 a 6.")

if __name__ == "__main__":
    main()