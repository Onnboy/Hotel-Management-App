from body import Reserva
import logging
import flet as ft

def abrir_tela_reservas(page, gerenciador, voltar_callback):
    logger = logging.getLogger("SistemaReserva.Reservas")

    def reservar_quarto(e):
        try:
            if not cliente_input.value or not quarto_input.value or not check_in_input.value or not check_out_input.value:
                feedback.value = "⚠️ Todos os campos são obrigatórios! ⚠️"
                page.update()
                return

            cliente = gerenciador.buscar_cliente_por_id(cliente_input.value.strip())
            if not cliente:
                feedback.value = "⚠️ Cliente não encontrado! Verifique o ID. ⚠️"
                logger.warning("Tentativa de reserva com cliente inexistente.")
                page.update()
                return

            quarto = next((q for q in gerenciador.listar_quartos() if q.numero == int(quarto_input.value.strip()) and q.disponivel), None)
            if not quarto:
                feedback.value = "⚠️ Quarto não disponível ou inexistente! ⚠️"
                logger.warning("Tentativa de reserva com quarto indisponível ou inexistente.")
                page.update()
                return

            reserva = gerenciador.criar_reserva(cliente, quarto, check_in_input.value.strip(), check_out_input.value.strip())
            if reserva:
                feedback.value = f"✅ Reserva criada com sucesso para o cliente '{cliente.nome}' no quarto {quarto.numero}! ✅"
                logger.info("Reserva criada com sucesso.")
            else:
                feedback.value = "⚠️ Falha ao criar reserva. Verifique os dados! ⚠️"
                logger.error("Falha ao criar reserva, dados incorretos.")
        except ValueError as ve:
            feedback.value = f"❌ Erro: {ve} ❌"
            logger.error(f"Erro ao criar reserva: {ve}")
        except Exception as ex:
            feedback.value = f"❌ Erro inesperado: {ex} ❌"
            logger.exception("Erro inesperado ao criar reserva")
        finally:
            page.update()

    titulo = ft.Text("Gerenciar Reservas", size=25, weight="bold", color="white")
    cliente_input = ft.TextField(label="ID do Cliente", width=300)
    quarto_input = ft.TextField(label="Número do Quarto", width=300)
    check_in_input = ft.TextField(label="Data de Check-in (YYYY-MM-DD)", width=300)
    check_out_input = ft.TextField(label="Data de Check-out (YYYY-MM-DD)", width=300)
    feedback = ft.Text("", color="white")

    btn_reserva = ft.ElevatedButton("Criar Reserva", on_click=reservar_quarto)
    btn_voltar = ft.ElevatedButton("Voltar", on_click=voltar_callback)

    page.controls.clear()
    page.add(
        ft.Container(
            content=ft.Column(
                [titulo, cliente_input, quarto_input, check_in_input, check_out_input, btn_reserva, feedback, btn_voltar],
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