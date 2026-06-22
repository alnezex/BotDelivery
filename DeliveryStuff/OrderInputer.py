from Order import Order 
from repository import PostgresRepository

class OrderInputer:
    def __init__(self, products_repository: PostgresRepository):
        self.products_list = products_repository.get_products() 

    def is_product_avil(self, product: Order) -> bool:
        for pr in product:
            if product.name == pr[0]:
                return True
        return False
    
    