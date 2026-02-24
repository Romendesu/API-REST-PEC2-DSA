from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, subtotal: float) -> float:
        pass

class NormalDiscount(DiscountStrategy):
    def apply_discount(self, subtotal: float) -> float:
        return subtotal  # 0% discount

class PremiumDiscount(DiscountStrategy):
    def apply_discount(self, subtotal: float) -> float:
        return subtotal * 0.9  # 10% discount

class VIPDiscount(DiscountStrategy):
    def apply_discount(self, subtotal: float) -> float:
        return subtotal * 0.8  # 20% discount

class DiscountFactory:
    @staticmethod
    def get_strategy(tipo_cliente: str) -> DiscountStrategy:
        if tipo_cliente == "premium":
            return PremiumDiscount()
        elif tipo_cliente == "VIP":
            return VIPDiscount()
        else:
            return NormalDiscount()