import sqlite3
import os

def conectar():
    # Salva o banco de dados na pasta 'Documentos' do usuário para não apagar ao atualizar o .exe
    pasta_documentos = os.path.join(os.path.expanduser("~"), "Documents", "SistemaVitrine")
    os.makedirs(pasta_documentos, exist_ok=True)
    
    caminho_banco = os.path.join(pasta_documentos, "banco.db")
    
    conexao = sqlite3.connect(caminho_banco)
    return conexao

def criar_tabela():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos_exposicao (
            codigo TEXT PRIMARY KEY,
            descricao TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()

def inserir_produto(codigo, descricao):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO produtos_exposicao
            (codigo, descricao)
            VALUES (?, ?)
            """,
            (codigo, descricao)
        )

        conexao.commit()
        print("Produto cadastrado!")

    except sqlite3.IntegrityError:
        print(f"Produto {codigo} já existe.")

    finally:
        conexao.close()

def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM produtos_exposicao")

    produtos = cursor.fetchall()

    conexao.close()

    return produtos

def buscar_produto(codigo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT * FROM produtos_exposicao
        WHERE codigo = ?
        """,
        (codigo,)
    )

    produto = cursor.fetchone()

    conexao.close()

    return produto

def atualizar_descricao(codigo, nova_descricao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE produtos_exposicao
        SET descricao = ?
        WHERE codigo = ?
        """,
        (nova_descricao, codigo)
    )

    conexao.commit()
    conexao.close()

def excluir_produto(codigo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM produtos_exposicao
        WHERE codigo = ?
        """,
        (codigo,)
    )

    conexao.commit()
    conexao.close()

def produto_existe(codigo):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM produtos_exposicao
        WHERE codigo = ?
        """,
        (codigo,)
    )

    resultado = cursor.fetchone()

    conexao.close()

    return resultado is not None

def contar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM produtos_exposicao
        """
    )

    total = cursor.fetchone()[0]

    conexao.close()

    return total