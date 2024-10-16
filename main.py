import flet as ft
from telas.telaCliente import TelaCliente
from telas.telaPizza import TelaPizza
from telas.telaPedido import TelaPedido

def main(page: ft.Page):
    ### Definindo as propriedades da página principal ###
    page.title = "Pizzaria do Carlos"
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 0
    page.spacing = 0
    page.window.width = 1400
    page.window.height = 730
    page.window.center()

    ### Função para alternar tema claro e escuro ###
    def switch_theme(is_light_theme):
        if is_light_theme:
            page.theme_mode = ft.ThemeMode.LIGHT
        else:
            page.theme_mode = ft.ThemeMode.DARK
        atualizar_cores()
        page.update()

    ### Função para atualizar cores com base no tema atual ###
    def atualizar_cores():
        if page.theme_mode == ft.ThemeMode.LIGHT:
            conteudo_principal.bgcolor = ft.colors.WHITE
            menu_lateral.bgcolor = ft.colors.with_opacity(1, "#262626")
            texto_cor = ft.colors.BLACK
            botao_bgcolor = ft.colors.with_opacity(1, "#f8bf34")
            textfield_border_color = ft.colors.BLACK  # Borda preta no tema claro
        else:
            conteudo_principal.bgcolor = ft.colors.BLACK
            menu_lateral.bgcolor = ft.colors.with_opacity(1, "#333333")
            texto_cor = ft.colors.WHITE
            botao_bgcolor = ft.colors.with_opacity(1, "#f8bf34")
            textfield_border_color = ft.colors.WHITE  # Borda branca no tema escuro

        # Atualiza a cor dos botões e texto
        for control in menu_lateral.content.controls:
            if isinstance(control, ft.ElevatedButton):
                control.style.color = ft.colors.BLACK  # Define o texto dos botões como preto
                control.style.bgcolor = botao_bgcolor

        # Atualiza a cor do texto no conteúdo principal
        atualizar_textos(conteudo_principal, texto_cor)

        # Atualiza a cor da borda dos TextFields e Dropdowns
        atualizar_borda_textfields(conteudo_principal, textfield_border_color)

        # Atualiza toda a página após mudar as cores
        page.update()

    ### Função para atualizar a cor dos textos ###
    def atualizar_textos(container, texto_cor):
        if hasattr(container, 'controls'):
            for control in container.controls:
                if isinstance(control, ft.Text):
                    control.color = texto_cor
                elif isinstance(control, (ft.Container, ft.Column, ft.Row)):
                    atualizar_textos(control, texto_cor)
        elif hasattr(container, 'content'):
            if isinstance(container.content, ft.Text):
                container.content.color = texto_cor
            elif isinstance(container.content, (ft.Container, ft.Column, ft.Row)):
                atualizar_textos(container.content, texto_cor)

    ### Função para atualizar a borda dos TextFields e Dropdowns ###
    def atualizar_borda_textfields(container, border_color):
        if hasattr(container, 'controls'):
            for control in container.controls:
                if isinstance(control, ft.TextField):
                    control.border_color = border_color
                elif isinstance(control, ft.Dropdown):
                    control.border_color = border_color  # Aplica borda ao Dropdown
                elif isinstance(control, (ft.Container, ft.Column, ft.Row)):
                    atualizar_borda_textfields(control, border_color)
        elif hasattr(container, 'content'):
            if isinstance(container.content, ft.TextField):
                container.content.border_color = border_color
            elif isinstance(container.content, ft.Dropdown):
                container.content.border_color = border_color  # Aplica borda ao Dropdown
            elif isinstance(container.content, (ft.Container, ft.Column, ft.Row)):
                atualizar_borda_textfields(container.content, border_color)

    ### Função para carregar a tela de clientes e atualizar as cores ###
    def carregar_tela_cliente():
        TelaCliente(page, conteudo_principal)
        atualizar_cores()  # Atualiza as cores sempre que mudar de aba

    ### Função para carregar a tela de pizzas e atualizar as cores ###
    def carregar_tela_pizza():
        TelaPizza(page, conteudo_principal)
        atualizar_cores()  # Atualiza as cores sempre que mudar de aba

    ### Função para carregar a tela de pedidos e atualizar as cores ###
    def carregar_tela_pedido():
        TelaPedido(page, conteudo_principal)
        atualizar_cores()  # Atualiza as cores sempre que mudar de aba

    ### Cria o container que será atualizado com as telas de clientes, pizzas e pedidos ###
    conteudo_principal = ft.Container(
        content=None,
        expand=True,
        padding=0,
        bgcolor=ft.colors.WHITE,
        border_radius=ft.border_radius.all(0),
    )

    ### Função para criar botões laterais do menu com estilo e funcionalidades ###
    def botao_menu_lateral(text, on_click):
        return ft.ElevatedButton(
            text,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,  # Cor do texto do botão
                bgcolor=ft.colors.with_opacity(1, "#f8bf34"),  # Cor de fundo do botão
                shape=ft.RoundedRectangleBorder(radius=5),
            ),
            width=230,
            height=60,
            on_click=on_click,
            tooltip=f"Botão para abrir a tela de {text.lower()}",
        )

    ### Criando o menu lateral com botões para acessar as telas ###
    menu_lateral = ft.Container(
        content=ft.Column(
            controls=[
                botao_menu_lateral("Clientes", lambda _: carregar_tela_cliente()),
                botao_menu_lateral("Pizzas", lambda _: carregar_tela_pizza()),
                botao_menu_lateral("Pedidos", lambda _: carregar_tela_pedido()),
                botao_menu_lateral("Sair", lambda _: page.window.close()),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        ),
        width=240,
        padding=10,
        bgcolor=ft.colors.with_opacity(1, "#262626"),
        tooltip="Menu lateral com opções de clientes, pizzas, pedidos e sair",
    )

    ### Criando o cabeçalho com a imagem e o título da pizzaria ###
    cabeçalho_cor = "#262626"  # Cor fixa do cabeçalho
    cabecalho = ft.Container(
        content=ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Image(
                            src="carlinhos.jpg",
                            width=100,
                            height=100,
                            tooltip="Logo da Pizzaria do Carlos",
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("Pizzaria do Carlos", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),  # Sempre branco
                                ft.Text("Gerência e Resultados", size=16, color=ft.colors.WHITE),  # Sempre branco
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=5,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.SUNNY,
                            icon_color="yellow",
                            icon_size=30,
                            tooltip="Tema Claro",
                            on_click=lambda _: switch_theme(True),
                        ),
                        ft.IconButton(
                            icon=ft.icons.BRIGHTNESS_2,
                            icon_color="white",
                            icon_size=30,
                            tooltip="Tema Escuro",
                            on_click=lambda _: switch_theme(False),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                    expand=True,
                )
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15,
        ),
        padding=10,
        bgcolor=cabeçalho_cor,  # Usa a cor fixa para o cabeçalho
        tooltip="Cabeçalho com logo e nome da pizzaria",
    )

    ### Adicionando os elementos criados à página ###
    page.add(
        ft.Column(
            controls=[cabecalho, ft.Row(controls=[menu_lateral, conteudo_principal], expand=True, spacing=0)],
            expand=True,
            spacing=0,
        )
    )

    ### Chamando a tela de clientes quando a aplicação iniciar ###
    carregar_tela_cliente()

    ### Inicializando o tema claro ###
    atualizar_cores()

ft.app(target=main, view=ft.WEB_BROWSER)
