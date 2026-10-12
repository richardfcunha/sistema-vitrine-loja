from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os
from datetime import datetime

def gerar_pdf_alteracoes(itens_alterados):
    """
    Gera um relatório em PDF com data/hora, com nome único para não sobrescrever os anteriores.
    """
    if not itens_alterados:
        print("❌ Nenhum item para gerar no PDF.")
        return False

    os.makedirs("relatorios", exist_ok=True)

    # Captura a data e hora atual
    agora = datetime.now()
    data_hora_texto = agora.strftime("%d/%m/%Y às %H:%M")      # Formato para mostrar dentro do PDF
    data_hora_arquivo = agora.strftime("%Y-%m-%d_%H-%M-%S")    # Formato seguro para usar no nome do arquivo

    # Cria um nome de arquivo único baseado no momento da geração
    nome_arquivo = f"relatorio_vitrine_{data_hora_arquivo}.pdf"
    caminho_completo = os.path.join("relatorios", nome_arquivo)

    # Configuração da página
    doc = SimpleDocTemplate(caminho_completo, pagesize=letter, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36)
    elementos = []

    styles = getSampleStyleSheet()
    
    titulo_style = ParagraphStyle(
        'TituloRelatorio',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f2937'),
        alignment=1, # Centralizado
        spaceAfter=10
    )
    
    sub_style = ParagraphStyle(
        'SubTitulo',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#4b5563'),
        alignment=1,
        spaceAfter=20
    )

    # Cabeçalho do Relatório com Data e Hora dinâmicas
    elementos.append(Paragraph("RELATÓRIO DE ALTERAÇÃO DE PREÇOS - VITRINE", titulo_style))
    elementos.append(Paragraph(f"Gerado em: <b>{data_hora_texto}</b><br/>Atenção: Atualizar as etiquetas dos produtos abaixo na frente da loja.", sub_style))
    elementos.append(Spacer(1, 10))

    # Montando a Tabela de Dados
    dados_tabela = [["Código", "Nome do Produto", "Novo Preço (Venda)"]]

    for item in itens_alterados:
        dados_tabela.append([
            str(item["codigo"]),
            str(item["descricao"]).upper(),
            f"R$ {item['venda']}"
        ])

    tabela = Table(dados_tabela, colWidths=[90, 310, 140])
    
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
    ]))

    elementos.append(tabela)

    doc.build(elementos)
    print(f"\n✅ PDF gerado com sucesso!")
    print(f"📂 Salvo em: {caminho_completo}")
    return True