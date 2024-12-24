from body import Cliente
import flet as ft
import logging

def abrir_tela_clientes(page, gerenciador, voltar_callback):
    logger = logging.getLogger("SistemaReserva.Clientes")

    def adicionar_cliente(e):
        try:
            if not nome_input.value or not telefone_input.value or not email_input.value:
                feedback.value = "⚠️ Todos os campos são obrigatórios! 🚧"
                page.update()
                return

            # Validação separada para e-mail
            if "@" not in email_input.value or "." not in email_input.value.split("@")[1]:
                feedback.value = "❌ E-mail inválido! O formato correto é exemplo@dominio.com"
                page.update()
                return
        
            # Validação separada para telefone
            if not telefone_input.value.isdigit() or not (9 <= len(telefone_input.value) <= 15):
                feedback.value = "❌ Telefone inválido! Deve conter apenas números e entre 9 a 15 dígitos."
                page.update()
                return

            cliente = Cliente(
                nome_input.value.strip(),
                email_input.value.strip(),
                telefone_input.value.strip()
            )
            gerenciador.adicionar_cliente(cliente)

            feedback.value = f"✅ Cliente '{cliente.nome}' foi adicionado com sucesso! ID: {cliente.id_unico} ✅"
            nome_input.value = telefone_input.value = email_input.value = ""
        except ValueError as ve:
            feedback.value = f"❌ Erro: {ve}"
            logger.error(f"Erro ao adicionar cliente: {ve}")
        except Exception as ex:
            feedback.value = f"❌ Erro inesperado: {ex}"
            logger.exception("Erro inesperado ao adicionar cliente")
        finally:
            page.update()

    titulo = ft.Text("Gerenciar Clientes", size=25, weight="bold", color="white")
    nome_input = ft.TextField(label="Nome Completo", width=300)
    telefone_input = ft.TextField(label="Telefone", width=300)
    email_input = ft.TextField(label="E-mail", width=300)
    feedback = ft.Text("", color="white")
    btn_adicionar = ft.ElevatedButton("Adicionar Cliente", on_click=adicionar_cliente)
    btn_voltar = ft.ElevatedButton("Voltar", on_click=voltar_callback)

    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column(
                [titulo, nome_input, telefone_input, email_input, btn_adicionar, feedback, btn_voltar],
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