from abc import ABC, abstractmethod

class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount):
        """Procesa un cobro y devuelve True/False"""
        pass
