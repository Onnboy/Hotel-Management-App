import uuid
import logging
from datetime import datetime
import re

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class Cliente:
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
        
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.id_unico = str(uuid.uuid4())
        
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
        self.clientes.append(cliente)
        logger.info(f"Cliente adicionado: {cliente}")
        
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

    def criar_reserva(self, cliente, quarto, check_in, check_out):
        try:
            if quarto.disponivel:
                reserva = Reserva(cliente, quarto, check_in, check_out)
                quarto.disponivel = False
                self.reservas.append(reserva)
                logger.info(
                    f"Reserva criada: {reserva}.\n"
                    f"Cliente: {cliente.nome}, Quarto: {quarto.numero}, Check-in: {check_in}, Check-out: {check_out}."
                )
                return reserva
            else:
                logger.warning(f"Tentativa de reservar o quarto {quarto.numero}, mas ele não está disponível!")
                return None
        except Exception as e:
            logger.error(f"Erro ao criar reserva: {e}")
            return None