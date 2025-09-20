from abc import ABC, abstractmethod

class IEnviable(ABC):
    @abstractmethod
    def enviar(self, destinatario, servidor):
        pass

class IRecibible(ABC):
    @abstractmethod
    def recibir(self, mensaje):
        pass

class IListable(ABC):
    @abstractmethod
    def listar(self):
        pass