import flet as ft
from funcoes.banco import criar_tabela_pizzas, inserir_pizza, obter_pizzas, deletar_pizza, obter_pizza_por_id, atualizar_pizza
from funcoes.funcoes import criar_textfield, exportar_para_excel

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

def TelaPizza(page, conteudo_principal):
    ### criando o container para armazenar a lista de cadastros de pizzas ###
    cadastros_container = ft.Container(padding=20)
    itens_por_pagina = 7
    pagina_atual = 1
    pesquisa_pizza = ""  # Variável de pesquisa

    ### função para lidar com a troca de página na tabela ###
    def handle_page_change(direction):
        nonlocal pagina_atual
        total_paginas = (len(obter_pizzas()) + itens_por_pagina - 1) // itens_por_pagina
        if direction == "next" and pagina_atual < total_paginas:
            pagina_atual += 1
        elif direction == "prev" and pagina_atual > 1:
            pagina_atual -= 1
        mostrar_cadastros()

    ### função para salvar uma nova pizza ###
    def salvar_cadastro(e, modal):
        nome = nome_field.value.strip() if nome_field.value else ''
        ingredientes = ingredientes_field.value.strip() if ingredientes_field.value else ''

        # Verificando qual campo está vazio e mostrando uma mensagem específica
        if not nome:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo Nome está vazio."), bgcolor=ft.colors.RED))
            return
        if not ingredientes:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("O campo Ingredientes está vazio."), bgcolor=ft.colors.RED))
            return

        # Se ambos os campos estiverem preenchidos, salva a pizza
        inserir_pizza(nome, ingredientes)
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Pizza salva com sucesso!"), bgcolor=ft.colors.GREEN))
        
        # Resetar os campos após salvar
        resetar_campos()

        # Atualizar a listagem de cadastros
        mostrar_cadastros()
        
    def filtrar_pizzas():
        pizzas = obter_pizzas()
        if pesquisa_pizza:
            return [pizza for pizza in pizzas if pesquisa_pizza.lower() in pizza[1].lower()]
        return pizzas

    ### função de callback para editar uma pizza ###
    def editar_pizza_callback(e, id):
        pizza = obter_pizza_por_id(id)
        if pizza:
            # Atribuir valores aos campos
            editar_nome_field.value = pizza['nome']
            editar_ingredientes_field.value = pizza['ingredientes']

            ### Função para atualizar cores dos TextFields dentro do modal ###
            def atualizar_borda_modal_textfields():
                if page.theme_mode == ft.ThemeMode.LIGHT:
                    editar_nome_field.border_color = ft.colors.BLACK  # Borda preta no tema claro
                    editar_nome_field.color = ft.colors.BLACK  # Texto preto no tema claro
                    editar_ingredientes_field.border_color = ft.colors.BLACK
                    editar_ingredientes_field.color = ft.colors.BLACK
                else:
                    editar_nome_field.border_color = ft.colors.WHITE  # Borda branca no tema escuro
                    editar_nome_field.color = ft.colors.WHITE  # Texto branco no tema escuro
                    editar_ingredientes_field.border_color = ft.colors.WHITE
                    editar_ingredientes_field.color = ft.colors.WHITE

            # Criar o modal para edição de pizza
            editar_pizza_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Editar Pizza"),
                content=ft.Container(
                    width=450,
                    height=250,
                    padding=0,
                    content=ft.Column([
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 12}, controls=[editar_nome_field]),
                        ]),
                        ft.ResponsiveRow([
                            ft.Column(col={"sm": 12}, controls=[editar_ingredientes_field]),
                        ]),
                    ]),
                ),
                actions=[
                    botao_personalizado(
                        "Salvar",
                        on_click=lambda e: editar_pizza(e, id, editar_pizza_modal),
                        tooltip="Clique para salvar as alterações"
                    ),
                    botao_personalizado(
                        "Fechar",
                        on_click=lambda e: fechar_modal(editar_pizza_modal),
                        tooltip="Clique para fechar o modal de edição"
                    ),
                ],
            )

            # Atualiza as cores dos TextFields no modal ao abrir
            atualizar_borda_modal_textfields()

            # Abrir o modal
            page.dialog = editar_pizza_modal
            editar_pizza_modal.open = True
            page.update()


    ### função para salvar as alterações da pizza editada ###
    def editar_pizza(e, id, modal):
        nome = editar_nome_field.value.strip()
        ingredientes = editar_ingredientes_field.value.strip()

        if not nome or not ingredientes:
            page.show_snack_bar(ft.SnackBar(content=ft.Text("Por favor, preencha todos os campos."), bgcolor=ft.colors.RED))
            return

        atualizar_pizza(id, nome, ingredientes)
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Pizza atualizada com sucesso!"), bgcolor=ft.colors.GREEN))
        fechar_modal(modal)
        mostrar_cadastros()

    ### função para deletar uma pizza e atualizar a tabela ###
    def deletar_pizza_e_mostrar(id):
        deletar_pizza(id)
        page.show_snack_bar(ft.SnackBar(content=ft.Text("Pizza deletada com sucesso!"), bgcolor=ft.colors.GREEN))
        mostrar_cadastros()

    ### função para exibir a tabela de cadastros de pizzas ###
    def mostrar_cadastros():
        pizzas = filtrar_pizzas()  # Usa a função de filtro
        total_paginas = (len(pizzas) + itens_por_pagina - 1) // itens_por_pagina
        inicio = (pagina_atual - 1) * itens_por_pagina
        fim = inicio + itens_por_pagina
        pizzas_pagina = pizzas[inicio:fim]

        ### criando as linhas da tabela com os dados das pizzas ###
        tabela_dados = []
        for pizza in pizzas_pagina:
            id, nome, ingredientes = pizza
            tabela_dados.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Container(content=ft.Text(nome, text_align=ft.TextAlign.START,), width=150)),
                        ft.DataCell(ft.Container(content=ft.Text(ingredientes, text_align=ft.TextAlign.START,), width=300)),
                        ft.DataCell(ft.Container(content=ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    icon_size=20,
                                    tooltip="Editar pizza",
                                    on_click=lambda e, id=id: editar_pizza_callback(e, id)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    icon_size=20,
                                    tooltip="Deletar pizza",
                                    on_click=lambda e, id=id: deletar_pizza_e_mostrar(id)
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        ), width=100)),
                    ]
                )
            )

        ### criando a tabela de pizzas com cabeçalho em negrito ###
        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Nome", text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Ingredientes", text_align=ft.TextAlign.START, weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Funções", text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.BOLD)),
            ],
            rows=tabela_dados,
            heading_row_color=ft.colors.with_opacity(1, "#f8bf34"),
            heading_text_style=ft.TextStyle(color=ft.colors.BLACK),
            border=ft.BorderSide(color=ft.colors.BLACK, width=1),
            width="100%",
        )

        ### criando controles de paginação ###
        paginacao_controls = ft.Row(
            controls=[
                ft.IconButton(icon=ft.icons.ARROW_BACK_IOS, on_click=lambda e: handle_page_change("prev"), tooltip="Página anterior"),
                ft.Text(f"{pagina_atual} de {total_paginas}"),
                ft.IconButton(icon=ft.icons.ARROW_FORWARD_IOS, on_click=lambda e: handle_page_change("next"), tooltip="Próxima página"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        ### exibindo a tabela e os controles de paginação na página ###
        cadastros_container.content = ft.Column(
            [tabela, paginacao_controls],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        page.update()
        
    def pesquisar_pizza(e):
        nonlocal pesquisa_pizza
        pesquisa_pizza = e.control.value  # Atualiza o valor da pesquisa
        mostrar_cadastros()  # Recarrega a tabela filtrada

    ### função para exibir o formulário de cadastro de pizzas como um modal ###
    def mostrar_formulario_cadastro(e):
        # Função para atualizar as cores e bordas dos TextFields
        def atualizar_borda_modal_textfields():
            if page.theme_mode == ft.ThemeMode.LIGHT:
                nome_field.border_color = ft.colors.BLACK  # Borda preta no tema claro
                nome_field.color = ft.colors.BLACK  # Texto preto no tema claro
                ingredientes_field.border_color = ft.colors.BLACK
                ingredientes_field.color = ft.colors.BLACK
            else:
                nome_field.border_color = ft.colors.WHITE  # Borda branca no tema escuro
                nome_field.color = ft.colors.WHITE  # Texto branco no tema escuro
                ingredientes_field.border_color = ft.colors.WHITE
                ingredientes_field.color = ft.colors.WHITE

        # Criar modal para cadastro de nova pizza
        modal_cadastro = ft.AlertDialog(
            modal=True,
            title=ft.Text("Cadastro de Nova Pizza"),
            content=ft.Container(
                width=450,
                height=250,
                padding=0,
                content=ft.Column([
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 12}, controls=[nome_field]),
                    ]),
                    ft.ResponsiveRow([
                        ft.Column(col={"sm": 12}, controls=[ingredientes_field]),
                    ]),
                ]),
            ),
            actions=[
                botao_personalizado(
                    "Salvar",
                    on_click=lambda e: salvar_cadastro(e, modal_cadastro),
                    tooltip="Clique para salvar a nova pizza"
                ),
                botao_personalizado(
                    "Fechar",
                    on_click=lambda e: fechar_modal(modal_cadastro),
                    tooltip="Clique para fechar o modal de cadastro"
                ),
            ],
        )

        # Atualiza as cores dos TextFields no modal
        atualizar_borda_modal_textfields()

        # Abrir o modal
        page.dialog = modal_cadastro
        modal_cadastro.open = True
        page.update()


    ### função para resetar os campos do formulário ###
    def resetar_campos():
        nome_field.value = ""
        ingredientes_field.value = ""
        nome_field.focus()
        page.update()

    ### função para exportar os dados de pizzas para um arquivo Excel ###
    def exportar_dados():
        mensagem = exportar_para_excel('pizzas', 'Pizzas')
        page.show_snack_bar(ft.SnackBar(content=ft.Text(mensagem), bgcolor=ft.colors.GREEN))

    ### função para fechar o modal de edição ###
    def fechar_modal(modal):
        modal.open = False
        page.update()

    ### criação dos campos de texto para o formulário ###
    nome_field = criar_textfield("Nome", "Margherita", ft.icons.LOCAL_PIZZA, somente_texto=True)
    ingredientes_field = criar_textfield("Ingredientes", "Mussarela, tomate, manjericão", ft.icons.RESTAURANT_MENU, somente_texto=True)

    ### criação dos campos de edição ###
    editar_nome_field = criar_textfield("Nome", "", ft.icons.LOCAL_PIZZA, somente_texto=True)
    editar_ingredientes_field = criar_textfield("Ingredientes", "", ft.icons.RESTAURANT_MENU, somente_texto=True)

    ### inicializando a tabela de pizzas e exibindo os cadastros ###
    criar_tabela_pizzas()
    mostrar_cadastros()

    ### exibindo o conteúdo principal da tela de pizzas ###
    conteudo_principal.content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="Pesquisar Pizza",
                            hint_text="Digite o nome da pizza",
                            on_change=pesquisar_pizza,  # Chama a função ao digitar
                            width=300,
                        ),
                        botao_personalizado(
                            "Cadastrar",
                            on_click=mostrar_formulario_cadastro,
                            tooltip="Cadastrar nova pizza"
                        ),
                        botao_personalizado(
                            "Exportar",
                            on_click=lambda e: exportar_dados(),
                            tooltip="Exportar dados das pizzas"
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
