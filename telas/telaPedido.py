import flet as ft
from datetime import datetime
import random
import string
import re
from funcoes.banco import criar_tabela_pedidos, inserir_pedido, obter_pedidos, atualizar_status_pedido, obter_clientes, obter_pizzas, obter_cliente_por_nome, obter_pedido_por_id
from funcoes.funcoes import *
from fpdf import FPDF
import os

### Função para criar botões personalizados ###
def botao_personalizado(text, on_click, tooltip):
    return ft.ElevatedButton(
        text,
        style=ft.ButtonStyle(
            color=ft.colors.BLACK,
            bgcolor=ft.colors.with_opacity(1, "#f8bf34"),
            shape=ft.RoundedRectangleBorder(radius=5),
        ),
        width=140,
        height=50,
        on_click=on_click,
        tooltip=tooltip,
    )

### Função para gerar um código aleatório para o pedido ###
def gerar_codigo_aleatorio():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

### Função para gerar o PDF com as informações do pedido ###
def gerar_pdf_pedido(codigo, nome_cliente, nome_pizza, quantidade, tamanho, forma_pagamento, entrega, valor_total, status, data_hora):
    pdf = FPDF('P', 'mm', (80, 200))  # Definir formato do papel para 80mm de largura
    pdf.add_page()

    # Cabeçalho da pizzaria
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 5, "Pizzaria do Carlos", ln=True, align="C")
    pdf.set_font("Arial", "", 8)
    pdf.cell(60, 5, "CNPJ: 12.345.678/0001-90", ln=True, align="C")
    pdf.cell(60, 5, "Rua das Pizzas, 123 - Centro", ln=True, align="C")
    pdf.cell(60, 5, "Tel: (35) 1234-5678", ln=True, align="C")
    pdf.ln(5)

    # Informações do cliente e pedido
    pdf.set_font("Arial", "B", 8)
    pdf.cell(60, 5, f"Pedido # {codigo} ({entrega.upper()})", ln=True)
    pdf.cell(60, 5, f"Cliente: {nome_cliente}", ln=True)
    pdf.ln(2)

    # Endereço de entrega
    pdf.set_font("Arial", "", 8)
    pdf.multi_cell(60, 5, entrega)
    pdf.ln(2)

    # Itens do pedido
    pdf.set_font("Arial", "B", 8)
    pdf.cell(60, 5, "Itens do Pedido", ln=True)
    pdf.set_font("Arial", "", 8)

    # Informações do item
    valor_unitario = valor_total / quantidade
    subtotal = valor_unitario * quantidade
    pdf.cell(60, 5, f"{quantidade}x {nome_pizza} ({tamanho})", ln=True)
    pdf.cell(60, 5, f"Valor unitário: R${valor_unitario:.2f}", ln=True)
    pdf.cell(60, 5, f"Subtotal: R${subtotal:.2f}", ln=True)
    pdf.ln(2)

    # Observações
    # Totais
    pdf.set_font("Arial", "B", 8)
    pdf.cell(60, 5, f"Total: R${valor_total:.2f}", ln=True)
    pdf.cell(60, 5, f"Forma de Pagamento: {forma_pagamento}", ln=True)
    pdf.cell(60, 5, f"Status: {status}", ln=True)
    pdf.cell(60, 5, f"Data e Hora: {data_hora}", ln=True)
    pdf.ln(5)

    # Rodapé
    pdf.set_font("Arial", "", 8)
    pdf.cell(60, 5, "-----------------------------", ln=True, align="C")
    pdf.cell(60, 5, "ESTE NÃO É UM CUPOM FISCAL", ln=True, align="C")

    # Salvando o PDF na pasta 'notas'
    if not os.path.exists("notas"):
        os.makedirs("notas")
    pdf.output(f"notas/{codigo}.pdf")
    
    return f"PDF do pedido {codigo} gerado com sucesso."

def TelaPedido(page, conteudo_principal):
    ### criando o container que armazenará a lista de cadastros de pedidos ###
    cadastros_container = ft.Container(padding=20)
    itens_por_pagina = 7
    pagina_atual = 1

    ### Função para lidar com a troca de página na tabela ###
    def handle_page_change(direction):
        nonlocal pagina_atual
        total_paginas = (len(obter_pedidos()) + itens_por_pagina - 1) // itens_por_pagina
        if direction == "next" and pagina_atual < total_paginas:
            pagina_atual += 1
        elif direction == "prev" and pagina_atual > 1:
            pagina_atual -= 1
        mostrar_cadastros()

    ### Função para calcular o valor total com base no tamanho, quantidade, forma de pagamento e entrega ###
    def calcular_valor_total(tamanho, quantidade, entrega, forma_pagamento):
        precos = {
            "Brotinho": 15,
            "Pequena": 30,
            "Média": 40,
            "Grande": 50
        }

        if tamanho not in precos:
            raise ValueError(f"Tamanho inválido: {tamanho}")

        valor_base = precos[tamanho] * quantidade
        taxa_entrega = 7 if entrega == "Entrega domiciliar" else 0
        taxa_pagamento = 1.50 if forma_pagamento == "Cartão" else 0

        return valor_base + taxa_entrega + taxa_pagamento

    ### Função para salvar um novo pedido ###
    def salvar_cadastro(e, modal):
        data_hora_atual = datetime.now().strftime('%d/%m/%Y - %H:%M')
        codigo = gerar_codigo_aleatorio()

        nome_cliente = nome_cliente_field.value.strip() if nome_cliente_field.value else ''
        nome_pizza = nome_pizza_field.value.strip() if nome_pizza_field.value else ''
        quantidade = int(quantidade_field.value.strip()) if quantidade_field.value else 0
        tamanho = tamanho_field.value if tamanho_field.value else ''
        forma_pagamento = forma_pagamento_field.value if forma_pagamento_field.value else ''
        entrega = entrega_field.value if entrega_field.value else ''

        # Verificando se os campos estão preenchidos corretamente e exibindo uma mensagem específica para cada campo vazio
        if not nome_cliente:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo Nome do Cliente está vazio."), bgcolor=ft.colors.RED))
            return
        if not nome_pizza:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo Nome da Pizza está vazio."), bgcolor=ft.colors.RED))
            return
        if not quantidade or quantidade <= 0:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo Quantidade deve ser maior que zero."), bgcolor=ft.colors.RED))
            return
        if not tamanho or tamanho not in ["Brotinho", "Pequena", "Média", "Grande"]:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Selecione um Tamanho válido (Brotinho, Pequena, Média, Grande)."), bgcolor=ft.colors.RED))
            return
        if not forma_pagamento:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo Forma de Pagamento está vazio."), bgcolor=ft.colors.RED))
            return
        if not entrega:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo Entrega está vazio."), bgcolor=ft.colors.RED))
            return

        try:
            valor_total = calcular_valor_total(tamanho, quantidade, entrega, forma_pagamento)
        except ValueError as e:
            page.show_snack_bar(ft.SnackBar(content=ft.Text(str(e)), bgcolor=ft.colors.RED))
            return

        # Se todos os campos estiverem preenchidos corretamente, salvar o pedido
        try:
            inserir_pedido(codigo, nome_cliente, nome_pizza, quantidade, tamanho, forma_pagamento, entrega, valor_total, "Preparando", data_hora_atual)
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Pedido salvo com sucesso!"), bgcolor=ft.colors.GREEN))
        except TypeError as e:
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Erro ao salvar pedido: {e}"), bgcolor=ft.colors.RED))

            
        # Gerar o PDF do pedido
        gerar_pdf_pedido(codigo, nome_cliente, nome_pizza, quantidade, tamanho, forma_pagamento, entrega, valor_total, "Preparando", data_hora_atual)

        page.show_snack_bar(ft.SnackBar(content=ft.Text("Pedido salvo e PDF gerado com sucesso!"), bgcolor=ft.colors.GREEN))
        resetar_campos()
        mostrar_cadastros()


    ### Função para atualizar o valor total no campo correspondente ###
    def atualizar_valor_total(e):
        tamanho = tamanho_field.value
        quantidade = int(quantidade_field.value) if quantidade_field.value.isdigit() else 0
        entrega = entrega_field.value
        forma_pagamento = forma_pagamento_field.value
        if tamanho and quantidade and entrega and forma_pagamento:
            valor_total_field.value = f"R${calcular_valor_total(tamanho, quantidade, entrega, forma_pagamento):.2f}"
        else:
            valor_total_field.value = "R$0.00"
        page.update()

    ### Função para resetar os campos do formulário ###
    def resetar_campos():
        nome_cliente_field.value = ""
        nome_pizza_field.value = ""
        quantidade_field.value = "1"
        tamanho_field.value = None
        forma_pagamento_field.value = None
        entrega_field.value = None
        valor_total_field.value = "R$0.00"
        nome_cliente_field.focus()
        page.update()


    ### função para fechar o modal ###
    def fechar_modal(modal):
        modal.open = False
        page.dialog = None
        page.update()

    def mostrar_formulario_cadastro(e):
        # Função para atualizar as cores e bordas dos TextFields
        def atualizar_borda_modal_textfields():
            if page.theme_mode == ft.ThemeMode.LIGHT:
                nome_cliente_field.border_color = ft.colors.BLACK  # Borda preta no tema claro
                nome_cliente_field.color = ft.colors.BLACK  # Texto preto no tema claro
                nome_pizza_field.border_color = ft.colors.BLACK
                nome_pizza_field.color = ft.colors.BLACK
                quantidade_field.border_color = ft.colors.BLACK
                quantidade_field.color = ft.colors.BLACK
                tamanho_field.border_color = ft.colors.BLACK
                tamanho_field.color = ft.colors.BLACK
                forma_pagamento_field.border_color = ft.colors.BLACK
                forma_pagamento_field.color = ft.colors.BLACK
                entrega_field.border_color = ft.colors.BLACK
                entrega_field.color = ft.colors.BLACK
                valor_total_field.border_color = ft.colors.BLACK
                valor_total_field.color = ft.colors.BLACK
            else:
                nome_cliente_field.border_color = ft.colors.WHITE  # Borda branca no tema escuro
                nome_cliente_field.color = ft.colors.WHITE  # Texto branco no tema escuro
                nome_pizza_field.border_color = ft.colors.WHITE
                nome_pizza_field.color = ft.colors.WHITE
                quantidade_field.border_color = ft.colors.WHITE
                quantidade_field.color = ft.colors.WHITE
                tamanho_field.border_color = ft.colors.WHITE
                tamanho_field.color = ft.colors.WHITE
                forma_pagamento_field.border_color = ft.colors.WHITE
                forma_pagamento_field.color = ft.colors.WHITE
                entrega_field.border_color = ft.colors.WHITE
                entrega_field.color = ft.colors.WHITE
                valor_total_field.border_color = ft.colors.WHITE
                valor_total_field.color = ft.colors.WHITE

        # Criar modal para cadastro de novo pedido
        modal_cadastro = ft.AlertDialog(
            modal=True,
            title=ft.Text("Cadastro de Novo Pedido"),
            content=ft.Container(
                width=650,
                height=200,
                padding=0,
                content=ft.Column([
                    ft.ResponsiveRow(
                        controls=[
                            ft.Column(col={"sm": 4}, controls=[nome_cliente_field]),
                            ft.Column(col={"sm": 4}, controls=[nome_pizza_field]),
                            ft.Column(col={"sm": 4}, controls=[quantidade_field]),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Column(col={"sm": 6}, controls=[tamanho_field]),
                            ft.Column(col={"sm": 6}, controls=[forma_pagamento_field]),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.ResponsiveRow(
                        controls=[
                            ft.Column(col={"sm": 6}, controls=[entrega_field]),
                            ft.Column(col={"sm": 6}, controls=[valor_total_field]),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]),
            ),
            actions=[
                botao_personalizado(
                    "Salvar",
                    on_click=lambda e: salvar_cadastro(e, modal_cadastro),
                    tooltip="Salvar novo pedido"
                ),
                botao_personalizado(
                    "Fechar",
                    on_click=lambda e: fechar_modal(modal_cadastro),
                    tooltip="Fechar o modal"
                ),
            ],
        )

        # Atualiza as cores dos TextFields no modal
        atualizar_borda_modal_textfields()

        # Abrir o modal
        page.dialog = modal_cadastro
        modal_cadastro.open = True
        page.update()


    ### função para exportar os dados de pedidos para um arquivo Excel ###
    def exportar_dados():
        mensagem = exportar_para_excel('pedidos', 'Pedidos')
        page.show_snack_bar(ft.SnackBar(content=ft.Text(mensagem), bgcolor=ft.colors.GREEN))
    
    def confirmar_notificacao(e, id, funcao_envio, atualizar_status_funcao, status_atual, *args):
        # Cria o modal de confirmação
        modal_confirmacao = ft.AlertDialog(
            modal=True,
            title=ft.Text("Notificar cliente?"),
            content=ft.Text("Você deseja notificar o cliente via WhatsApp?"),
            actions=[
                ft.CupertinoButton(
                    content=ft.Text("Sim", color="white"),
                    bgcolor=ft.colors.GREEN,
                    border_radius=ft.border_radius.all(5),
                    on_click=lambda e: [
                        fechar_modal(modal_confirmacao),
                        funcao_envio(*args), 
                        atualizar_status_funcao(e, id, status_atual)
                    ]
                ),
                ft.CupertinoButton(
                    content=ft.Text("Não", color="white"),
                    bgcolor=ft.colors.RED,
                    border_radius=ft.border_radius.all(5),
                    on_click=lambda e: [
                        fechar_modal(modal_confirmacao),
                        atualizar_status_funcao(e, id, status_atual)
                    ]
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = modal_confirmacao
        modal_confirmacao.open = True
        page.update()

    def cancelar_pedido(e, id):
        pedido = obter_pedido_por_id(id)
        cliente_info = obter_cliente_por_nome(pedido['nome_cliente'])
        
        # Verifica se o cliente foi encontrado
        if cliente_info is None:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Cliente não encontrado!"), bgcolor=ft.colors.RED))
            return
        
        confirmar_notificacao(
            e, 
            id, 
            enviar_mensagem_pedido, 
            atualizar_status, 
            "Cancelado",
            pedido['nome_cliente'], 
            pedido['codigo'], 
            pedido['quantidade'], 
            pedido['nome_pizza'], 
            pedido['valor_total'], 
            re.sub(r'\D', '', cliente_info['telefone']),  # Cliente encontrado, acessando o telefone com segurança
            "cancelar"
        )
        mostrar_cadastros()

    def atualizar_status(e, id, status_atual):
        atualizar_status_pedido(id, status_atual)
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Status atualizado com sucesso!"), bgcolor=ft.colors.GREEN))
        mostrar_cadastros()

    # Exemplo de uso em outra parte onde a função de envio é chamada diretamente
    def grafico_pedido_callback(e, id):
        pedido = obter_pedido_por_id(id)
        cliente_info = obter_cliente_por_nome(pedido['nome_cliente'])
        
        if cliente_info is None:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Cliente não encontrado!"), bgcolor=ft.colors.RED))
            return

        status_atual = pedido['status']
        botao_texto = ""
        botao_disabled = False
        
        if status_atual == "Preparando":
            botao_texto = "Enviar"
        elif status_atual == "Entregando":
            botao_texto = "Concluir"
        elif status_atual == "Concluído":
            botao_texto = "Concluído"
            botao_disabled = True

        # Modal para confirmação antes de atualizar o status do pedido
        pedido_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Informações do Pedido"),
            content=ft.Container(
                width=280,
                height=300,
                content=ft.Column([
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 12}, controls=[ft.Text(f"Código: {pedido['codigo']}")]),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 12}, controls=[ft.Text(f"Cliente: {pedido['nome_cliente']}")]),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 12}, controls=[ft.Text(f"Pizza: {pedido['nome_pizza']}")]),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 12}, controls=[ft.Text(f"Quantidade: {pedido['quantidade']}")]),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 12}, controls=[ft.Text(f"Tamanho: {pedido['tamanho']}")]),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 12}, controls=[ft.Text(f"Forma de Pagamento: {pedido['forma_pagamento']}")]),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 12}, controls=[ft.Text(f"Entrega: {pedido['entrega']}")]),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 12}, controls=[ft.Text(f"Valor Total: R${pedido['valor_total']:.2f}")]),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 12}, controls=[ft.Text(f"Status: {pedido['status']}")]),
                    ]),
                ]),
            ),
            actions=[
                ft.CupertinoButton(
                    content=ft.Text(botao_texto, color="black"),
                    bgcolor=ft.colors.with_opacity(1, "#f8bf34"),
                    border_radius=ft.border_radius.all(5),
                    opacity_on_click=0.5,
                    on_click=lambda e: confirmar_notificacao(
                        e, 
                        id, 
                        enviar_mensagem_pedido, 
                        atualizar_status, 
                        "Entregando" if status_atual == "Preparando" else "Concluído",
                        pedido['nome_cliente'], 
                        pedido['codigo'], 
                        pedido['quantidade'], 
                        pedido['nome_pizza'], 
                        pedido['valor_total'], 
                        re.sub(r'\D', '', cliente_info['telefone']),
                        "enviar" if status_atual == "Preparando" else "concluir"
                    ),
                    disabled=botao_disabled,
                    tooltip="Clique para atualizar o status do pedido"
                ),
                ft.CupertinoButton(
                    content=ft.Text("Fechar", color="black"),
                    bgcolor=ft.colors.with_opacity(1, "#f8bf34"),
                    border_radius=ft.border_radius.all(5),
                    opacity_on_click=0.5,
                    on_click=lambda e: fechar_modal(pedido_modal),
                    tooltip="Clique para fechar a janela"
                ),
            ],
        )
        page.dialog = pedido_modal
        pedido_modal.open = True
        page.update()



    def enviar_mensagem_pedido(nome_cliente, codigo_pedido, quantidade, nome_pizza, valor_total, numero_cliente, status="salvar"):
        if status == "salvar":
            mensagem = mensagem_salvar_pedido(nome_cliente, codigo_pedido, quantidade, nome_pizza, valor_total)
        elif status == "enviar":
            mensagem = mensagem_enviar_pedido(nome_cliente)
        elif status == "concluir":
            mensagem = mensagem_concluir_pedido(nome_cliente)
        elif status == "cancelar":
            mensagem = mensagem_cancelar_pedido(nome_cliente, codigo_pedido)

        enviar_mensagem_whatsapp(numero_cliente, mensagem)


    # Mapeamento de meses em português para inglês
    meses_portugues = {
        'Janeiro': 'January',
        'Fevereiro': 'February',
        'Março': 'March',
        'Abril': 'April',
        'Maio': 'May',
        'Junho': 'June',
        'Julho': 'July',
        'Agosto': 'August',
        'Setembro': 'September',
        'Outubro': 'October',
        'Novembro': 'November',
        'Dezembro': 'December'
    }

    def mostrar_cadastros():
        pedidos = obter_pedidos()  # Agora, já obtém os pedidos em ordem decrescente de data
        
        # Função auxiliar para converter o campo data_hora para datetime
        def converter_para_datetime(pedido):
            return datetime.strptime(pedido[-1], '%d/%m/%Y - %H:%M')

        # Ordenar os pedidos por data/hora decrescente
        pedidos = sorted(pedidos, key=converter_para_datetime, reverse=True)

        ### Aplicando filtros ###
        if filtro_mes.value:
            mes_filtro = meses_portugues.get(filtro_mes.value, '')  # Converte o mês selecionado para inglês
            pedidos = [p for p in pedidos if datetime.strptime(p[-1], '%d/%m/%Y - %H:%M').strftime('%B') == mes_filtro]

        if filtro_ano.value:
            pedidos = [p for p in pedidos if datetime.strptime(p[-1], '%d/%m/%Y - %H:%M').strftime('%Y') == filtro_ano.value]

        if filtro_entrega.value:
            pedidos = [p for p in pedidos if p[7] == filtro_entrega.value]

        # Paginação
        total_paginas = (len(pedidos) + itens_por_pagina - 1) // itens_por_pagina
        inicio = (pagina_atual - 1) * itens_por_pagina
        fim = inicio + itens_por_pagina
        pedidos_pagina = pedidos[inicio:fim]
        
            ### Criando as linhas da tabela com os dados dos pedidos ###
        tabela_dados = []

        # Função para definir a cor do texto com base no status

        def cor_status(status):
            if status == "Concluído":
                return "green"
            elif status == "Preparando":
                return "orange" 
            elif status == "Entregando":
                return "amber"
            elif status == "Cancelado":
                return "red"
            else:
                return "gray"  

        for pedido in pedidos_pagina:
            id, codigo, nome_cliente, nome_pizza, quantidade, tamanho, forma_pagamento, entrega, valor_total, status, data_hora = pedido

            cor_texto_status = cor_status(status)

            tabela_dados.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(content=ft.Text(codigo, text_align=ft.TextAlign.START), width=100)),
                        ft.DataCell(ft.Container(content=ft.Text(nome_cliente, text_align=ft.TextAlign.START), width=150)),
                        ft.DataCell(ft.Container(content=ft.Text(status, text_align=ft.TextAlign.START, color=cor_texto_status), width=100)),
                        ft.DataCell(ft.Container(content=ft.Text(data_hora, text_align=ft.TextAlign.START), width=150)),
                        ft.DataCell(ft.Container(content=ft.IconButton(
                            icon=ft.icons.INFO,
                            icon_size=20,
                            tooltip="Ver mais detalhes do pedido",
                            on_click=lambda e, id=id: grafico_pedido_callback(e, id)
                        ), width=50)),
                        ft.DataCell(ft.Container(content=ft.IconButton(
                            icon=ft.icons.CANCEL,
                            icon_size=20,
                            tooltip="Cancelar pedido",
                            on_click=lambda e, id=id: cancelar_pedido(e, id)
                        ), width=50)),
                        ft.DataCell(ft.Container(content=ft.IconButton(
                            icon=ft.icons.MESSAGE,
                            icon_size=20,
                            tooltip="Enviar mensagem pelo WhatsApp",
                            on_click=lambda e, id=id, nome_cliente=nome_cliente: enviar_mensagem_whatsapp(re.sub(r'\D', '', obter_cliente_por_nome(nome_cliente)['telefone']), f"Olá, o status do seu pedido é: {status}"),
                        ), width=50)),
                    ]
                )
            )

        ### Criando a tabela de pedidos ###
        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Código", text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Cliente", text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Status", text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Data e Hora", text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("", text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Funções", text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("", text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)),
            ],
            rows=tabela_dados,
            heading_row_color=ft.colors.with_opacity(1, "#f8bf34"),
            heading_text_style=ft.TextStyle(color=ft.colors.BLACK),
            border=ft.BorderSide(color=ft.colors.BLACK, width=1),
            width="100%",
        )
        
        paginacao_controls = ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_BACK_IOS, on_click=lambda e: handle_page_change("prev"), tooltip="Página anterior"),
                ft.Text(f"{pagina_atual} de {total_paginas}"),
                ft.IconButton(icon=ft.icons.ARROW_FORWARD_IOS, on_click=lambda e: handle_page_change("next"), tooltip="Próxima página"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        ### Exibindo a tabela e os controles de paginação na página ###
        cadastros_container.content = ft.Column(
            [tabela, paginacao_controls],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.update()


    ### Função para limpar os filtros dos dropdowns ###
    def limpar_filtros(e):
        filtro_mes.value = None
        filtro_ano.value = None
        filtro_entrega.value = None
        mostrar_cadastros()
        page.update()


    ### Criando os campos de entrada de dados para o formulário ###
    nome_cliente_field = ft.Dropdown(
        label="Cliente",
        options=[ft.dropdown.Option(cliente[1]) for cliente in obter_clientes()],
        border_radius=0,
    )
    nome_pizza_field = ft.Dropdown(
        label="Pizza",
        options=[ft.dropdown.Option(pizza[1]) for pizza in obter_pizzas()],
        border_radius=0,
    )
    quantidade_field = ft.TextField(
        label="Quantidade",
        value="1",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_blur=atualizar_valor_total,
    )
    tamanho_field = ft.Dropdown(
        label="Tamanho",
        options=[
            ft.dropdown.Option("Brotinho"),
            ft.dropdown.Option("Pequena"),
            ft.dropdown.Option("Média"),
            ft.dropdown.Option("Grande"),
        ],
        border_radius=0,
        on_change=atualizar_valor_total
    )
    forma_pagamento_field = ft.Dropdown(
        label="Forma de Pagamento",
        options=[
            ft.dropdown.Option("Dinheiro"),
            ft.dropdown.Option("Cartão"),
            ft.dropdown.Option("Online"),
            ft.dropdown.Option("PIX"),
        ],
        on_change=atualizar_valor_total,
    )
    entrega_field = ft.Dropdown(
        label="Entrega",
        options=[
            ft.dropdown.Option("Entrega domiciliar"),
            ft.dropdown.Option("Retirada balcão"),
        ],
        on_change=atualizar_valor_total,
    )
    valor_total_field = ft.TextField(
        label="Total",
        value="R$0.00",
        icon=ft.icons.ATTACH_MONEY,
        read_only=True,
    )

    ### Filtros de mês, ano e entrega ###
    filtro_mes = ft.Dropdown(
        label="Mês",
        options=[
            ft.dropdown.Option("Janeiro"),
            ft.dropdown.Option("Fevereiro"),
            ft.dropdown.Option("Março"),
            ft.dropdown.Option("Abril"),
            ft.dropdown.Option("Maio"),
            ft.dropdown.Option("Junho"),
            ft.dropdown.Option("Julho"),
            ft.dropdown.Option("Agosto"),
            ft.dropdown.Option("Setembro"),
            ft.dropdown.Option("Outubro"),
            ft.dropdown.Option("Novembro"),
            ft.dropdown.Option("Dezembro"),
        ],
        on_change=lambda e: mostrar_cadastros(),
        width=120,
    )
    filtro_ano = ft.Dropdown(
        label="Ano",
        options=[
            ft.dropdown.Option("2024"),
            ft.dropdown.Option("2025"),
            ft.dropdown.Option("2026"),
        ],
        on_change=lambda e: mostrar_cadastros(),
        width=120,
    )
    filtro_entrega = ft.Dropdown(
        label="Entrega",
        options=[
            ft.dropdown.Option("Retirada balcão"),
            ft.dropdown.Option("Entrega domiciliar"),
        ],
        on_change=lambda e: mostrar_cadastros(),
        width=200,
    )

    ### Exibindo o conteúdo principal da tela de pedidos ###
    criar_tabela_pedidos()
    mostrar_cadastros()

    conteudo_principal.content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        filtro_mes,
                        filtro_ano,
                        filtro_entrega,
                        botao_personalizado(
                            "Limpar Filtros",
                            on_click=limpar_filtros,
                            tooltip="Limpar os filtros"
                        ),
                        botao_personalizado(
                            "Cadastrar",
                            on_click=mostrar_formulario_cadastro,
                            tooltip="Cadastrar novo pedido"
                        ),
                        botao_personalizado(
                            "Exportar",
                            on_click=lambda e: exportar_dados(),
                            tooltip="Exportar dados dos pedidos"
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    width="90%",
                ),
                cadastros_container,
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        padding=20,
    )
    page.update()
