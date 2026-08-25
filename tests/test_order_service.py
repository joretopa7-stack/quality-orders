import pytest

from app.exceptions import DuplicateOrderError, InvalidQuantityError


def test_create_valid_order_returns_normalized_data(order_service, valid_order_data):
    """Positiva: el pedido creado devuelve los datos normalizados."""
    # Arrange (fixtures) / Act
    order = order_service.create(valid_order_data)
    # Assert
    assert order["customer_name"] == "Ana Torres"
    assert order["product_code"] == "ABC123"
    assert order["shipping_zone"] == "local"


def test_create_valid_order_calculates_totals_correctly(order_service, valid_order_data):
    """Positiva: subtotal, descuento, envio y total quedan bien calculados."""
    order = order_service.create(valid_order_data)
    # unit_price 10000 * quantity 5 = 50000 subtotal, sin descuento, envio local 8000
    assert order["subtotal"] == 50000
    assert order["discount"] == 0
    assert order["shipping_cost"] == 8000
    assert order["total"] == 58000


def test_create_valid_order_starts_in_pending_status(order_service, valid_order_data):
    """Positiva: RN-12, todo pedido creado inicia en estado pending."""
    order = order_service.create(valid_order_data)
    assert order["status"] == "pending"


def test_create_valid_order_saves_exactly_one_order(order_service, order_repository, valid_order_data):
    """Positiva: el pedido valido queda persistido en el repositorio."""
    order_service.create(valid_order_data)
    assert len(order_repository.list_all()) == 1


def test_create_rejects_duplicate_order_code(order_service, valid_order_data):
    """Negativa: RN-11, no se permiten dos pedidos con el mismo codigo."""
    # Arrange: se crea el primer pedido
    order_service.create(valid_order_data)
    # Act / Assert: el segundo intento con el mismo codigo debe fallar
    with pytest.raises(DuplicateOrderError):
        order_service.create(valid_order_data)


def test_duplicate_order_does_not_save_second_record(order_service, order_repository, valid_order_data):
    """Negativa: un intento de duplicado no debe alterar el repositorio."""
    order_service.create(valid_order_data)
    with pytest.raises(DuplicateOrderError):
        order_service.create(valid_order_data)
    assert len(order_repository.list_all()) == 1


def test_invalid_order_data_is_not_stored(order_service, order_repository, valid_order_data):
    """Negativa: un pedido con datos invalidos no debe almacenarse."""
    # Arrange
    invalid_data = dict(valid_order_data)
    invalid_data["quantity"] = 0  # viola RN-04
    # Act / Assert
    with pytest.raises(InvalidQuantityError):
        order_service.create(invalid_data)
    assert order_repository.list_all() == []


def test_can_create_two_distinct_orders_in_same_repository(order_service, order_repository, valid_order_data):
    """Positiva: dos pedidos con codigos distintos coexisten sin problema."""
    order_service.create(valid_order_data)
    second_order = dict(valid_order_data)
    second_order["order_code"] = "ORD-002"
    order_service.create(second_order)
    assert len(order_repository.list_all()) == 2


def test_new_repository_starts_empty_independent_of_other_tests(order_repository):
    """Prueba de independencia: cada test recibe un repositorio nuevo y vacio,
    sin importar lo que hayan guardado otras pruebas antes."""
    assert order_repository.list_all() == []
