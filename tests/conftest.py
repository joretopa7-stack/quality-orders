import pytest

from app.repositories import InMemoryOrderRepository
from app.order_service import OrderService


@pytest.fixture
def order_repository():
    """Repositorio en memoria nuevo y vacio para cada prueba.

    Al ser una fixture (no un objeto compartido a nivel de modulo),
    Pytest crea una instancia fresca por cada test, lo que garantiza
    independencia entre pruebas.
    """
    return InMemoryOrderRepository()


@pytest.fixture
def order_service(order_repository):
    """Servicio de pedidos conectado a un repositorio limpio."""
    return OrderService(order_repository)


@pytest.fixture
def valid_order_data():
    """Payload valido de referencia, reutilizable y facil de modificar."""
    return {
        "order_code": "ORD-001",
        "customer_name": "Ana Torres",
        "product_code": "abc123",
        "unit_price": 10000,
        "quantity": 5,
        "shipping_zone": "local",
    }
