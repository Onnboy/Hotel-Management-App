import uuid
import logging
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Pessoa:
    def __init__(self, __nome, __telefone, __email):
        self.nome = __nome
        self.telefone = __telefone
        self.email = __email
        self.id_unico = str(uuid.uuid4())

class Cliente(Pessoa):
    def __init__(self, nome, email, telefone):
        logging.info(f"Construindo cliente com Nome: {nome}, E-mail: {email}, Telefone: {telefone}")

        email = email.strip()
        telefone = telefone.strip()

        # Validação de e-mail
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            raise ValueError(f"E-mail inválido: '{email}'. O formato deve ser exemplo@dominio.com")

        # Validação de telefone
        if not re.match(r"^\d{9,15}$", telefone):
            raise ValueError(f"Telefone inválido: '{telefone}'. Deve conter apenas números com 9 a 15 dígitos.")

        super().__init__(nome, telefone, email)

    def __str__(self):
        return f"Cliente {self.nome} Id do cliente: ({self.id_unico}) Email do cliente: {self.email} Contato do cliente: {self.telefone}"

class Quarto:
    def __init__(self, numero, tipo, preco, disponivel=True):
        self.numero = numero
        self.tipo = tipo
        self.preco = preco
        self.disponivel = disponivel

    def __str__(self):
        status = "Disponível" if self.disponivel else "Ocupado"
        return f"Quarto {self.numero} - Tipo: {self.tipo} - Preço: R${self.preco:.2f} - {status}"

class Reserva:
    def __init__(self, cliente, quarto, check_in, check_out):
        try:
            self.check_in = datetime.strptime(check_in.strip(), "%Y-%m-%d")
            self.check_out = datetime.strptime(check_out.strip(), "%Y-%m-%d")
        except ValueError as ve:
            raise ValueError(f"Erro no formato das datas: {ve}")

        if self.check_in >= self.check_out:
            raise ValueError("Data de check-in deve ser anterior ao check-out!")

        self.cliente = cliente
        self.quarto = quarto
        self.status = "Ativa"

    def cancelar(self):
        self.status = "Cancelada"
        self.quarto.disponivel = True

    def __str__(self):
        return (f"Reserva de {self.cliente.nome} - Quarto {self.quarto.numero}"
                f"({self.check_in.strftime('%Y-%m-%d')} até {self.check_out.strftime('%Y-%m-%d')}) - Status: {self.status}")

logger = logging.getLogger("SistemaReserva")

class GerenciadorDeReservas:
    def __init__(self):
        self.clientes = []
        self.quartos = []
        self.reservas = []

        for i in range(1, 11):
            self.quartos.append(Quarto(100 + i, "Single", 350.0))
        for i in range(1, 11):
            self.quartos.append(Quarto(200 + i, "Double", 550.0))
        for i in range(1, 11):
            self.quartos.append(Quarto(300 + i, "Suite", 800.0))

        logger.info("Sistema de Gerenciamento de Reservas iniciado.")

    def adicionar_cliente(self, cliente):
        cliente.nome = cliente.nome.strip()
        cliente.email = cliente.email.strip()
        cliente.telefone = cliente.telefone.strip()
        self.clientes.append(cliente)
        logger.info(f"Cliente adicionado: {cliente}")

    def verificar_disponibilidade(self, numero_quarto):
        quarto = next((q for q in self.quartos if q.numero == numero_quarto), None)
        if quarto:
            logger.info(f"Quarto {numero_quarto} está {'disponivel' if quarto.disponivel else 'ocupado'}.")
            return quarto.disponivel
        logger.warning(f"Quarto {numero_quarto} não encontrado")
        return False

    def buscar_cliente_por_id(self, id_unico):
        for cliente in self.clientes:
            if cliente.id_unico == id_unico:
                logger.info(f"Cliente encontrado: {cliente}")
                return cliente
        logger.warning(f"Cliente com ID {id_unico} não encontrado.")
        return None

    def listar_clientes(self):
        logger.info(f"Listando {len(self.clientes)} cliente(s)")
        return self.clientes

    def criar_reserva(self, id_cliente, numero_quarto, check_in, check_out):
        try:
            cliente = self.buscar_cliente_por_id(id_cliente)
            quarto = next((q for q in self.quartos if q.numero == numero_quarto), None)
            if not cliente:
                logger.error(f"Cliente com ID {id_cliente} não encontrado.")
                return None

            if not quarto:
                logger.error(f"Quarto {numero_quarto} não encontrado.")
                return None

            if not quarto.disponivel:
                logger.warning(f"Quarto {numero_quarto} já está ocupado.")

            reserva = Reserva(cliente, quarto, check_in, check_out)
            quarto.disponivel = False
            self.reservas.append(reserva)
            logger.info(
                f"Reserva criada: {reserva}.\n"
                f"Cliente: {cliente.nome}, Quarto: {quarto.numero}, Check-in: {check_in}, Check-out: {check_out}."
            )
            return reserva
        except Exception as er:
            logger.error(f"Erro ao criar reserva: {er}")
            return None

    def modificar_reserva(self, id_cliente, numero_quarto, novo_check_in, novo_check_out):
        reserva = next(
            (r for r in self.reservas if r.cliente.id_unico == id_cliente and r.quarto.numero == numero_quarto), 
            None
        )
        if not reserva:
            logger.warning(f"Reserva não encontrada para o cliente {id_cliente} e quarto {numero_quarto}.")
            return None

        try:
            novo_check_in = datetime.strptime(novo_check_in.strip(), "%Y-%m-%d")
            novo_check_out = datetime.strptime(novo_check_out.strip(), "%Y-%m-%d")

            if novo_check_in >= novo_check_out:
                raise ValueError("A nova data de check-in deve ser anterior ao check-out!")

            reserva.check_in = novo_check_in
            reserva.check_out = novo_check_out
            logger.info(f"Reserva atualizada: {reserva}")
            return reserva
        except Exception as e:
            logger.error(f"Erro ao modificar a reserva: {e}")
            return None

    def listar_reservas(self, status=None):
        reservas_filtrada = (
            self.reservas if status is None else [r for r in self.reservas if r.status == status]
        )
        logger.info(f"Listando {len(reservas_filtrada)} reserva(s).")
        return reservas_filtrada

    def cancelar_reserva(self, id_cliente, numero_quarto):
        reserva = next(
            (r for r in self.reservas if r.cliente.id_unico == id_cliente and r.quarto.numero == numero_quarto),
            None
        )
        if reserva:
            reserva.cancelar()
            logger.info(f"Reserva cancelada: {reserva}")
            return reserva
        logger.warning(f"Reserva para Cliente {id_cliente} e Quarto {numero_quarto} não encontrada.")