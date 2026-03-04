import pytest
from faker import Faker
from ddf import G, N
from inventory.models import Product, InventoryMovement

fake = Faker()

@pytest.fixture
def create_100_products(db):
    """Puebla la DB de prueba con 100 productos usando Faker y G."""
    products = []
    for _ in range(100):
        # G crea y guarda en la DB automáticamente
        product = G(Product, 
                    name=fake.unique.ecommerce_name(),
                    category=fake.word(),
                    stock_actual=fake.random_int(min=0, max=500),
                    price=fake.pydecimal(left_digits=3, right_digits=2, positive=True))
        products.append(product)
    return products

