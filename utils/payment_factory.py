from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool:
        pass

class CreditCardPayment(Payment):
    def process(self, amount: float) -> bool:
        print(f"Procesando pago de {amount} con tarjeta de crédito")
        return True  # Simulado

class PayPalPayment(Payment):
    def process(self, amount: float) -> bool:
        print(f"Procesando pago de {amount} con PayPal")
        return True  # Simulado

class BankTransferPayment(Payment):
    def process(self, amount: float) -> bool:
        print(f"Procesando pago de {amount} con transferencia bancaria")
        return True  # Simulado

class PaymentFactory:
    @staticmethod
    def create_payment(method: str) -> Payment:
        if method == "tarjeta de crédito":
            return CreditCardPayment()
        elif method == "PayPal":
            return PayPalPayment()
        elif method == "transferencia bancaria":
            return BankTransferPayment()
        else:
            raise ValueError(f"Método de pago no soportado: {method}")