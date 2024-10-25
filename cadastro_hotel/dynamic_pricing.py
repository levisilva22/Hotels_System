from abc import ABC, abstractmethod
from datetime import datetime, date
from decimal import Decimal

# Interface 
class DynamicPricing(ABC):

    # Método que todas as estratégias devem implementar
    @abstractmethod
    def dynamic_pricing(self, base_price, check_in):
        pass

# Todas as estratégias devem herdar a interface
class HighSeason(DynamicPricing):
    
    # Método da interface
    def dynamic_pricing(self, base_price, check_in):
        specific_date = date(datetime.now().year, 8, 1)
        
        if isinstance(check_in, datetime):
            check_in = check_in.date()
                
        if specific_date >= check_in:
            return base_price * 1.2
        
        return base_price
 
class Discount(DynamicPricing):

    def dynamic_pricing(self, base_price, check_in):
        current_date = datetime.now().date()

        if isinstance(check_in, datetime):
            check_in = check_in.date()

        if check_in > current_date:
            return base_price * Decimal(0.9)
        
        return base_price

class Calculate:
    def __init__(self):
        self.strategies = []

    # Strategy: DynamicPrincing, strategy deve ter o mesmo tipo de DynamicPricing
    def add_strategy(self, strategy: DynamicPricing):
        self.strategies.append(strategy)

    def apply_calculation(self, base_price, check_in):

        final_price = base_price

        for strategy in self.strategies:
            final_price = strategy.dynamic_pricing(final_price, check_in)
        
        return final_price
    

if __name__ == '__main__':

    calcular = Calculate()
    calcular.add_strategy(HighSeason())
    calcular.add_strategy(Discount())

    data_especifica = date(2024, 9, 14)

    preco_final = calcular.apply_calculation(250, data_especifica)

    print(preco_final)