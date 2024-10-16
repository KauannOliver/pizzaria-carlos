import flet as ft
from funcoes.banco import criar_tabela_clientes, inserir_cliente, obter_clientes, deletar_cliente, obter_cliente_por_id, atualizar_cliente
from funcoes.funcoes import criar_textfield, exportar_para_excel, preencher_endereco
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

def TelaCliente(page, conteudo_principal):
    ### criando container que armazenará a lista de cadastros ###
    cadastros_container = ft.Container(padding=20)
    itens_por_pagina = 7
    pagina_atual = 1
    pesquisa_cliente = ""  # Variável de pesquisa

    ### função para lidar com a mudança de página ###
    def handle_page_change(direction):
        nonlocal pagina_atual
        total_paginas = (len(obter_clientes()) + itens_por_pagina - 1) // itens_por_pagina
        if direction == "next" and pagina_atual < total_paginas:
            pagina_atual += 1
        elif direction == "prev" and pagina_atual > 1:
            pagina_atual -= 1
        mostrar_cadastros()
        
    def filtrar_clientes():
        clientes = obter_clientes()
        if pesquisa_cliente:
            return [cliente for cliente in clientes if pesquisa_cliente.lower() in cliente[1].lower()]
        return clientes


    ### função para salvar os dados do cadastro ###
    def salvar_cadastro(e, modal):
        nome = nome_field.value.strip()
        telefone = telefone_field.value.strip()
        cpf = cpf_field.value.strip()
        cep = cep_field.value.strip()
        endereco = endereco_field.value.strip()
        numero = numero_field.value.strip()

        # Verifica se cada campo está vazio e mostra uma mensagem específica
        if not nome:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo Nome está vazio."), bgcolor=ft.colors.RED))
            return
        if not telefone:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo Telefone está vazio."), bgcolor=ft.colors.RED))
            return
        if not cpf:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo CPF está vazio."), bgcolor=ft.colors.RED))
            return
        if not cep:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo CEP está vazio."), bgcolor=ft.colors.RED))
            return
        if not endereco:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo Endereço está vazio."), bgcolor=ft.colors.RED))
            return
        if not numero:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo Número está vazio."), bgcolor=ft.colors.RED))
            return

        # Se todos os campos estiverem preenchidos, salvar o cliente
        inserir_cliente(nome, telefone, cpf, cep, endereco, numero)
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Cliente salvo com sucesso!"), bgcolor=ft.colors.GREEN))

        # Reseta os campos e atualiza a tela
        resetar_campos()
        mostrar_cadastros()


    ### função de callback para editar um cadastro ###
    def editar_cadastro_callback(e, id):
        # Função para atualizar as cores e bordas dos TextFields no modal
        def atualizar_borda_modal_textfields():
            if page.theme_mode == ft.ThemeMode.LIGHT:
                editar_nome_field.border_color = ft.colors.BLACK
                editar_nome_field.color = ft.colors.BLACK
                editar_telefone_field.border_color = ft.colors.BLACK
                editar_telefone_field.color = ft.colors.BLACK
                editar_cpf_field.border_color = ft.colors.BLACK
                editar_cpf_field.color = ft.colors.BLACK
                editar_cep_field.border_color = ft.colors.BLACK
                editar_cep_field.color = ft.colors.BLACK
                editar_endereco_field.border_color = ft.colors.BLACK
                editar_endereco_field.color = ft.colors.BLACK
                editar_numero_field.border_color = ft.colors.BLACK
                editar_numero_field.color = ft.colors.BLACK
            else:
                editar_nome_field.border_color = ft.colors.WHITE
                editar_nome_field.color = ft.colors.WHITE
                editar_telefone_field.border_color = ft.colors.WHITE
                editar_telefone_field.color = ft.colors.WHITE
                editar_cpf_field.border_color = ft.colors.WHITE
                editar_cpf_field.color = ft.colors.WHITE
                editar_cep_field.border_color = ft.colors.WHITE
                editar_cep_field.color = ft.colors.WHITE
                editar_endereco_field.border_color = ft.colors.WHITE
                editar_endereco_field.color = ft.colors.WHITE
                editar_numero_field.border_color = ft.colors.WHITE
                editar_numero_field.color = ft.colors.WHITE

        # Obtém os dados do cliente para edição
        cliente = obter_cliente_por_id(id)
        if cliente:
            editar_nome_field.value = cliente['nome']
            editar_telefone_field.value = cliente['telefone']
            editar_cpf_field.value = cliente['cpf']
            editar_cep_field.value = cliente['cep']
            editar_endereco_field.value = cliente['endereco']
            editar_numero_field.value = cliente['numero']

            # Criação do modal para editar cliente
            editar_cliente_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Editar Cliente"),
                content=ft.Container(
                    width=450,
                    height=300,
                    padding=0,
                    content=ft.Column([
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 12}, controls=[editar_nome_field]),
                        ]),
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 6}, controls=[editar_telefone_field]),
                            ft.Column(col={"sm": 6}, controls=[editar_cpf_field]),
                        ]),
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 9}, controls=[editar_cep_field]),
                            ft.Column(col={"sm": 3}, controls=[
                                botao_personalizado(
                                    "Buscar",
                                    on_click=lambda e: preencher_endereco(page, editar_cep_field, editar_endereco_field, editar_bairro_field, editar_cidade_field, editar_uf_field),
                                    tooltip="Clique para buscar o endereço"
                                ),
                            ]),
                        ]),
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 9}, controls=[editar_endereco_field]),
                            ft.Column(col={"sm": 3}, controls=[editar_numero_field]),
                        ]),
                    ]),
                ),
                actions=[
                    botao_personalizado(
                        "Editar",
                        on_click=lambda e: editar_cliente(e, id, editar_cliente_modal),
                        tooltip="Clique para salvar as alterações"
                    ),
                    botao_personalizado(
                        "Fechar",
                        on_click=lambda e: fechar_modal(editar_cliente_modal),
                        tooltip="Clique para fechar a janela de edição"
                    ),
                ],
            )

            # Atualizar as bordas e cores dos TextFields antes de abrir o modal
            atualizar_borda_modal_textfields()

            # Abrir o modal
            page.dialog = editar_cliente_modal
            editar_cliente_modal.open = True
            page.update()


    ### função para editar o cliente no banco de dados ###
    def editar_cliente(e, id, modal):
        nome = editar_nome_field.value.strip()
        telefone = editar_telefone_field.value.strip()
        cpf = editar_cpf_field.value.strip()
        cep = editar_cep_field.value.strip()
        endereco = editar_endereco_field.value.strip()
        numero = editar_numero_field.value.strip()

        if not nome or not telefone or not cpf or not cep or not endereco or not numero:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Por favor, preencha todos os campos."), bgcolor=ft.colors.RED))
            return

        atualizar_cliente(id, nome, telefone, cpf, cep, endereco, numero)
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Cliente atualizado com sucesso!"), bgcolor=ft.colors.GREEN))
        fechar_modal(modal)
        mostrar_cadastros()

    ### função para deletar o cliente ###
    def deletar_cliente_callback(e, id):
        deletar_cliente(id)
        mostrar_cadastros()
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Cliente deletado com sucesso!"), bgcolor=ft.colors.GREEN))

    ### função que exibe os detalhes do cliente no modal ###
    def grafico_cliente_callback(e, id):


        cliente = obter_cliente_por_id(id)
        if cliente:
            cliente_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Informações do Cliente"),
                content=ft.Container(
                    width=350,
                    height=200,  # Altura ajustada para 200px
                    content=ft.Column([
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 12}, controls=[
                                ft.Row(controls=[
                                    ft.Text("ID: ", weight=ft.FontWeight.BOLD),  # Título em negrito
                                    ft.Text(f"{cliente['id']}"),  # Valor sem negrito
                                ])
                            ]),
                        ]),
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 12}, controls=[
                                ft.Row(controls=[
                                    ft.Text("Nome: ", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"{cliente['nome']}"),
                                ])
                            ]),
                        ]),
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 12}, controls=[
                                ft.Row(controls=[
                                    ft.Text("Telefone: ", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"{cliente['telefone']}"),
                                ])
                            ]),
                        ]),
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 12}, controls=[
                                ft.Row(controls=[
                                    ft.Text("CPF: ", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"{cliente['cpf']}"),
                                ])
                            ]),
                        ]),
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 12}, controls=[
                                ft.Row(controls=[
                                    ft.Text("CEP: ", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"{cliente['cep']}"),
                                ])
                            ]),
                        ]),
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 12}, controls=[
                                ft.Row(controls=[
                                    ft.Text("Endereço: ", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"{cliente['endereco']}"),
                                ])
                            ]),
                        ]),
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 12}, controls=[
                                ft.Row(controls=[
                                    ft.Text("Número: ", weight=ft.FontWeight.BOLD),
                                    ft.Text(f"{cliente['numero']}"),
                                ])
                            ]),
                        ]),
                    ]),
                ),
                actions=[
                    botao_personalizado(
                        "Fechar",
                        on_click=lambda e: fechar_modal(cliente_modal),
                        tooltip="Clique para fechar"
                    ),
                ],
            )
            
            # Neste modal, não há necessidade de atualizar cores de TextFields,
            # mas se fosse necessário, o padrão poderia ser seguido aqui.

            page.dialog = cliente_modal
            cliente_modal.open = True
            page.update()



    ### função para fechar modais ###
    def fechar_modal(modal):
        modal.open = False
        page.dialog = None
        page.update()

    ### função para resetar os campos após salvar ###
    def resetar_campos():
        nome_field.value = ""
        telefone_field.value = ""
        cpf_field.value = ""
        cep_field.value = ""
        endereco_field.value = ""
        bairro_field.value = ""
        cidade_field.value = ""
        uf_field.value = ""
        numero_field.value = ""
        nome_field.focus()
        page.update()

    ### função para exibir os cadastros na tabela ###
    def mostrar_cadastros():
        clientes = filtrar_clientes()  # Usa a função de filtro
        total_paginas = (len(clientes) + itens_por_pagina - 1) // itens_por_pagina
        inicio = (pagina_atual - 1) * itens_por_pagina
        fim = inicio + itens_por_pagina
        clientes_pagina = clientes[inicio:fim]

        ### criando as linhas da tabela com os dados dos clientes ###
        tabela_dados = []
        for cliente in clientes_pagina:
            id, nome, telefone, cpf, cep, endereco, numero = cliente
            tabela_dados.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(content=ft.Text(nome, text_align=ft.TextAlign.START,), width=150)),
                        ft.DataCell(ft.Container(content=ft.Text(telefone, text_align=ft.TextAlign.START,), width=150)),
                        ft.DataCell(ft.Container(content=ft.Text(endereco, text_align=ft.TextAlign.START,), width=250)),
                        ft.DataCell(ft.Container(content=ft.IconButton(
                            icon=ft.icons.EDIT,
                            icon_size=20,
                            tooltip="Editar",
                            on_click=lambda e, id=id: editar_cadastro_callback(e, id)
                        ), width=50)),
                        ft.DataCell(ft.Container(content=ft.IconButton(
                            icon=ft.icons.DELETE,
                            icon_size=20,
                            tooltip="Deletar",
                            on_click=lambda e, id=id: deletar_cliente_callback(e, id)
                        ), width=50)),
                        ft.DataCell(ft.Container(content=ft.IconButton(
                            icon=ft.icons.INFO,
                            icon_size=20,
                            tooltip="Ver Mais",
                            on_click=lambda e, id=id: grafico_cliente_callback(e, id)
                        ), width=50)),
                    ]
                )
            )

        ### criando a tabela de clientes com o cabeçalho em negrito ###
        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome", text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Telefone", text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Endereço", text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD)),
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

        ### criando a paginação ###
        paginacao_controls = ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_BACK_IOS, on_click=lambda e: handle_page_change("prev"), tooltip="Página anterior"),
                ft.Text(f"{pagina_atual} de {total_paginas}"),
                ft.IconButton(icon=ft.icons.ARROW_FORWARD_IOS, on_click=lambda e: handle_page_change("next"), tooltip="Próxima página"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        ### exibindo os cadastros na página ###
        cadastros_container.content = ft.Column(
            [tabela, paginacao_controls],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.update()
        
    def pesquisar_cliente(e):
        nonlocal pesquisa_cliente
        pesquisa_cliente = e.control.value  # Atualiza o valor da pesquisa
        mostrar_cadastros()  # Recarrega a tabela filtrada


    ### função para exibir o formulário de cadastro no modal ###
    def mostrar_formulario_cadastro(e):
        # Função para atualizar as cores e bordas dos TextFields
        def atualizar_borda_modal_textfields():
            if page.theme_mode == ft.ThemeMode.LIGHT:
                nome_field.border_color = ft.colors.BLACK  # Borda preta no tema claro
                nome_field.color = ft.colors.BLACK  # Texto preto no tema claro
                telefone_field.border_color = ft.colors.BLACK
                telefone_field.color = ft.colors.BLACK
                cpf_field.border_color = ft.colors.BLACK
                cpf_field.color = ft.colors.BLACK
                cep_field.border_color = ft.colors.BLACK
                cep_field.color = ft.colors.BLACK
                endereco_field.border_color = ft.colors.BLACK
                endereco_field.color = ft.colors.BLACK
                bairro_field.border_color = ft.colors.BLACK
                bairro_field.color = ft.colors.BLACK
                cidade_field.border_color = ft.colors.BLACK
                cidade_field.color = ft.colors.BLACK
                uf_field.border_color = ft.colors.BLACK
                uf_field.color = ft.colors.BLACK
                numero_field.border_color = ft.colors.BLACK
                numero_field.color = ft.colors.BLACK
            else:
                nome_field.border_color = ft.colors.WHITE  # Borda branca no tema escuro
                nome_field.color = ft.colors.WHITE  # Texto branco no tema escuro
                telefone_field.border_color = ft.colors.WHITE
                telefone_field.color = ft.colors.WHITE
                cpf_field.border_color = ft.colors.WHITE
                cpf_field.color = ft.colors.WHITE
                cep_field.border_color = ft.colors.WHITE
                cep_field.color = ft.colors.WHITE
                endereco_field.border_color = ft.colors.WHITE
                endereco_field.color = ft.colors.WHITE
                bairro_field.border_color = ft.colors.WHITE
                bairro_field.color = ft.colors.WHITE
                cidade_field.border_color = ft.colors.WHITE
                cidade_field.color = ft.colors.WHITE
                uf_field.border_color = ft.colors.WHITE
                uf_field.color = ft.colors.WHITE
                numero_field.border_color = ft.colors.WHITE
                numero_field.color = ft.colors.WHITE

        # Criar modal para cadastro de novo cliente
        modal_cadastro = ft.AlertDialog(
            modal=True,
            title=ft.Text("Cadastro de Novo Cliente"),
            content=ft.Container(
                width=620,
                height=300,
                padding=0,
                content=ft.Column([
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 7}, controls=[nome_field]),
                        ft.Column(col={"sm": 5}, controls=[telefone_field]),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 5}, controls=[cpf_field]),
                        ft.Column(col={"sm": 4}, controls=[cep_field]),
                        ft.Column(col={"sm": 3}, controls=[botao_personalizado(
                            "Buscar",
                            on_click=lambda e: preencher_endereco(page, cep_field, endereco_field, bairro_field, cidade_field, uf_field),
                            tooltip="Buscar endereço pelo CEP"
                        )]),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 6}, controls=[endereco_field]),
                        ft.Column(col={"sm": 6}, controls=[bairro_field]),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 5}, controls=[cidade_field]),
                        ft.Column(col={"sm": 4}, controls=[uf_field]),
                        ft.Column(col={"sm": 3}, controls=[numero_field]),
                    ]),
                ]),
            ),
            actions=[
                botao_personalizado(
                    "Salvar",
                    on_click=lambda e: salvar_cadastro(e, modal_cadastro),
                    tooltip="Salvar cliente"
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


    ### função para exportar os dados dos clientes para Excel ###
    def exportar_dados():
        mensagem = exportar_para_excel('clientes', 'Clientes')
        page.show_snack_bar(ft.SnackBar(content=ft.Text(mensagem), bgcolor=ft.colors.GREEN))

    ### criação dos campos de entrada de dados ###
    nome_field = criar_textfield("Nome", "Carlos Rubens Silva", ft.icons.PERSON, somente_texto=True)
    telefone_field = criar_textfield("Telefone", "(11) 9 1111-1111", ft.icons.PHONE, telefone=True, somente_numeros=True)
    cpf_field = criar_textfield("CPF", "123.456.879-12", ft.icons.BADGE, cpf=True, somente_numeros=True)
    cep_field = criar_textfield("CEP", "78945-612", ft.icons.LOCATION_ON, cep=True, somente_numeros=True)
    endereco_field = criar_textfield("Endereço", "Rua Xavier dos Ipês", ft.icons.HOME, somente_texto=True)
    bairro_field = criar_textfield("Bairro", "Jardim Alterosa", ft.icons.LOCATION_CITY, somente_texto=True)
    cidade_field = criar_textfield("Cidade", "Lavras", ft.icons.LOCATION_CITY, somente_texto=True)
    uf_field = criar_textfield("UF", "Minas Gerais", ft.icons.MAP, somente_texto=True)
    numero_field = criar_textfield("Número", "123", ft.icons.FORMAT_LIST_NUMBERED, somente_numeros=True)

    ### criação dos campos de edição ###
    editar_nome_field = criar_textfield("Nome", "", ft.icons.PERSON, somente_texto=True)
    editar_telefone_field = criar_textfield("Telefone", "", ft.icons.PHONE, telefone=True, somente_numeros=True)
    editar_cpf_field = criar_textfield("CPF", "", ft.icons.BADGE, cpf=True, somente_numeros=True)
    editar_cep_field = criar_textfield("CEP", "", ft.icons.LOCATION_ON, cep=True, somente_numeros=True)
    editar_endereco_field = criar_textfield("Endereço", "", ft.icons.HOME, somente_texto=True)
    editar_bairro_field = criar_textfield("Bairro", "", ft.icons.LOCATION_CITY, somente_texto=True)
    editar_cidade_field = criar_textfield("Cidade", "", ft.icons.LOCATION_CITY, somente_texto=True)
    editar_uf_field = criar_textfield("UF", "", ft.icons.MAP, somente_texto=True)
    editar_numero_field = criar_textfield("N°", "", ft.icons.FORMAT_LIST_NUMBERED, somente_numeros=True)

    ### inicializando o banco de dados de clientes e exibindo os cadastros ###
    criar_tabela_clientes()
    mostrar_cadastros()

    ### exibindo o conteúdo principal da tela de clientes ###
    conteudo_principal.content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="Pesquisar Cliente",
                            hint_text="Digite o nome do cliente",
                            on_change=pesquisar_cliente,  # Chama a função ao digitar
                            width=300,
                        ),
                        botao_personalizado(
                            "Cadastrar",
                            on_click=mostrar_formulario_cadastro,
                            tooltip="Cadastrar novo cliente"
                        ),
                        botao_personalizado(
                            "Exportar",
                            on_click=lambda e: exportar_dados(),
                            tooltip="Exportar dados dos clientes"
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