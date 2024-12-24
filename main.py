from body import GerenciadorDeReservas, Cliente, Quarto, Reserva
import flet as ft
import logging

def main(page: ft.Page):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("sistema_reservas.log"),
            logging.StreamHandler()
        ]
    )

    gerenciador = GerenciadorDeReservas()

    def exibir_opcoes_quartos(tipo: str, cliente: Cliente):
        opcoes = {
            "Single": [f"10{i}" for i in range(1, 11)],
            "Double": [f"20{i}" for i in range(1, 11)],
            "Family": [f"30{i}" for i in range(1, 11)],
        }

        opcoes_quartos = opcoes.get(tipo, [])

        # Criar dropdown dinâmico para os números de quartos
        dropdown_quartos = ft.Dropdown(
            label="Selecione o número do quarto",
            options=[ft.dropdown.Option(q) for q in opcoes_quartos],
        )

        def confirmar_selecao(e):
            if dropdown_quartos.value:
                quarto_selecionado = dropdown_quartos.value
                # Atribuir o quarto ao cliente
                cliente.quarto = quarto_selecionado
                # Marcar o quarto como não disponível
                quarto = next((q for q in gerenciador.quartos if q.numero == quarto_selecionado), None)
                if quarto:
                    quarto.disponivel = False
                exibir_feedback(f"Quarto {quarto_selecionado} atribuído ao cliente {cliente.nome}!")

                # Adicionar reserva e retornar à tela de Gerenciar Reservas
                reserva = Reserva(cliente, quarto, "2024-12-01", "2024-12-05")
                gerenciador.reservas.append(reserva)
                abrir_tela_reservas()

        # Exibir diálogo com as opções disponíveis
        dialogo = ft.AlertDialog(
            title=ft.Text(f"Quartos disponíveis ({tipo})"),
            content=ft.Column([dropdown_quartos], tight=True),
            actions=[
                ft.ElevatedButton("Confirmar", on_click=confirmar_selecao),
            ],
        )
        page.overlay.append(dialogo)
        dialogo.open = True
        page.update()

    def tela_inicial():
        titulo = ft.Text("Pousada Refúgio dos Sonhos", size=40, weight="bold", color="white")
        subtitulo = ft.Text("Gerenciamento de Reservas", size=20, color="white")

        btn_clientes = ft.ElevatedButton(
            "Gerenciar Clientes", on_click=lambda _: abrir_tela_clientes(), bgcolor="#3A86FF", color="white"
        )
        btn_reservas = ft.ElevatedButton(
            "Gerenciar Reservas", on_click=lambda _: abrir_tela_reservas(), bgcolor="#FF006E", color="white"
        )
        btn_quartos = ft.ElevatedButton(
            "Gerenciar Quartos", on_click=lambda _: abrir_tela_quartos(), bgcolor="#8338EC", color="white"
        )

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    [titulo, subtitulo, btn_clientes, btn_reservas, btn_quartos],
                    horizontal_alignment="center",
                    spacing=20,
                ),
                padding=50,
                alignment=ft.alignment.center,
                bgcolor="#2E2E2E",
                border_radius=10,
                expand=True
            )
        )
        page.update()

    def exibir_feedback(message, success=True):
        color = "#06D6A0" if success else "#EF476F"
        feedback_bar = ft.Text(message, color="white", size=18, weight="bold")

        snack_bar = ft.SnackBar(content=feedback_bar, bgcolor=color, duration=3000)
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()

    def abrir_tela_clientes():
        def listar_clientes():
            lista = ft.ListView(expand=True)
            if not gerenciador.clientes:
                lista.controls.append(ft.Text("Nenhum cliente cadastrado.", color="white"))
            else:
                for cliente in gerenciador.listar_clientes():
                    lista.controls.append(
                        ft.Text(f"{cliente.nome} - {cliente.email} - {cliente.telefone} - ID: {cliente.id_unico}", color="white")
                    )
            return lista

        def adicionar_cliente(e):
            if nome_input.value and email_input.value and telefone_input.value:
                try:
                    cliente = Cliente(
                        nome_input.value.strip(),
                        email_input.value.strip(),
                        telefone_input.value.strip()
                    )
                    gerenciador.adicionar_cliente(cliente)
                    exibir_feedback(f"Cliente '{cliente.nome}' adicionado com sucesso!", success=True)
                    nome_input.value = email_input.value = telefone_input.value = ""

                    # Atualizar opções de tipos de quartos
                    botoes_tipos.visible = True

                    # Chamar a tela para selecionar o quarto
                    def escolher_quarto(tipo_quarto):
                        exibir_opcoes_quartos(tipo_quarto, cliente)

                    # Botões para tipos de quartos
                    botoes_tipos.controls.clear()
                    botoes_tipos.controls.extend([
                        ft.ElevatedButton(
                            "Single",
                            on_click=lambda e: escolher_quarto("Single"),
                            bgcolor="#3A86FF",
                            color="white",
                        ),
                        ft.ElevatedButton(
                            "Double",
                            on_click=lambda e: escolher_quarto("Double"),
                            bgcolor="#FF006E",
                            color="white",
                        ),
                        ft.ElevatedButton(
                            "Family",
                            on_click=lambda e: escolher_quarto("Family"),
                            bgcolor="#8338EC",
                            color="white",
                        ),
                    ])
                    page.update()

                except ValueError as ve:
                    exibir_feedback(f"Erro: {ve}", success=False)
            else:
                exibir_feedback("Todos os campos são obrigatórios!", success=False)
            page.update()

        titulo = ft.Text("Gerenciar Clientes", size=25, weight="bold", color="white")
        nome_input = ft.TextField(label="Nome Completo", width=300)
        email_input = ft.TextField(label="E-mail", width=300)
        telefone_input = ft.TextField(label="Telefone", width=300)

        # Botões para tipos de quartos
        botoes_tipos = ft.Row([])
        botoes_tipos.visible = False

        btn_adicionar = ft.ElevatedButton("Adicionar Cliente", on_click=adicionar_cliente, bgcolor="#06D6A0", color="white")
        btn_voltar = ft.ElevatedButton("Voltar", on_click=lambda _: tela_inicial(), bgcolor="#118AB2", color="white")

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    [titulo, nome_input, email_input, telefone_input, btn_adicionar, botoes_tipos, listar_clientes(), btn_voltar],
                    horizontal_alignment="center",
                    spacing=10,
                ),
                padding=50,
                alignment=ft.alignment.center,
                bgcolor="#2E2E2E",
                border_radius=10,
                expand=True
            )
        )
        page.update()

    def abrir_tela_reservas():
        def listar_reservas():
            lista = ft.ListView(expand=True)
            if not gerenciador.reservas:
                lista.controls.append(ft.Text("Nenhuma reserva encontrada.", color="white"))
            else:
                for reserva in gerenciador.reservas:
                    item = ft.Row([
                        ft.Text(f"{reserva.cliente.nome} - Quarto {reserva.quarto.numero if reserva.quarto else reserva.cliente.quarto} - {reserva.status}", color="white"),
                        ft.ElevatedButton("Cancelar", on_click=lambda e, r=reserva: cancelar_reserva(r), bgcolor="#EF476F", color="white")
                    ])
                    lista.controls.append(item)
            return lista

        def cancelar_reserva(reserva):
            gerenciador.reservas.remove(reserva)
            if reserva.quarto:
                reserva.quarto.disponivel = True
            exibir_feedback(f"Reserva de {reserva.cliente.nome} cancelada com sucesso.", success=True)
            abrir_tela_reservas()

        titulo = ft.Text("Gerenciar Reservas", size=25, weight="bold", color="white")
        btn_voltar = ft.ElevatedButton("Voltar", on_click=lambda _: tela_inicial(), bgcolor="#118AB2", color="white")

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    [titulo, listar_reservas(), btn_voltar],
                    horizontal_alignment="center",
                    spacing=10,
                ),
                padding=50,
                alignment=ft.alignment.center,
                bgcolor="#2E2E2E",
                border_radius=10,
                expand=True
            )
        )
        page.update()

    def abrir_tela_quartos():
        def listar_quartos():
            lista = ft.ListView(expand=True)
            if not gerenciador.quartos:
                lista.controls.append(ft.Text("Nenhum quarto encontrado.", color="white"))
            else:
                for quarto in gerenciador.quartos:
                    lista.controls.append(
                        ft.Text(f"Quarto {quarto.numero} - {quarto.tipo} - {'Disponível' if quarto.disponivel else 'Ocupado'}", color="white")
                    )
            return lista

        titulo = ft.Text("Gerenciar Quartos", size=25, weight="bold", color="white")
        btn_voltar = ft.ElevatedButton("Voltar", on_click=lambda _: tela_inicial(), bgcolor="#118AB2", color="white")

        page.controls.clear()
        page.add(
            ft.Container(
                content=ft.Column(
                    [titulo, listar_quartos(), btn_voltar],
                    horizontal_alignment="center",
                    spacing=10,
                ),
                padding=50,
                alignment=ft.alignment.center,
            )
        )
        
        page.update()

    tela_inicial()

ft.app(target=main)
