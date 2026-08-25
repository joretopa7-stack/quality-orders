import pytest

from app.pricing import (
    calculate_subtotal,
    calculate_discount,
    calculate_shipping_cost,
    calculate_order_total,
)


# ---------------------------------------------------------------------------
# calculate_subtotal (RN-05)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "unit_price, quantity, expected",
    [
        (10000, 1, 10000),
        (5000, 4, 20000),
        (25000, 3, 75000),
    ],
)
def test_calculate_subtotal(unit_price, quantity, expected):
    """Positiva: subtotal = precio_unitario * cantidad, varias combinaciones."""
    assert calculate_subtotal(unit_price, quantity) == expected


# ---------------------------------------------------------------------------
# calculate_discount (RN-06)
# ---------------------------------------------------------------------------

def test_calculate_discount_below_100000_is_zero():
    """Positiva: por debajo del primer umbral no hay descuento."""
    assert calculate_discount(99999) == 0


def test_calculate_discount_at_exact_100000_boundary():
    """Frontera: exactamente 100000 ya aplica el 10%."""
    assert calculate_discount(100000) == pytest.approx(100000 * 0.10)


def test_calculate_discount_just_below_500000_keeps_10_percent():
    """Frontera: justo debajo de 500000 sigue en el tramo del 10%."""
    assert calculate_discount(499999) == pytest.approx(499999 * 0.10)


def test_calculate_discount_at_exact_500000_boundary():
    """Frontera: exactamente 500000 ya aplica el 15%."""
    assert calculate_discount(500000) == pytest.approx(500000 * 0.15)


def test_calculate_discount_above_500000():
    """Positiva: por encima de 500000 aplica el 15%."""
    assert calculate_discount(600000) == pytest.approx(600000 * 0.15)


# ---------------------------------------------------------------------------
# calculate_shipping_cost (RN-08, RN-09)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "zone, expected_cost",
    [
        ("local", 8000),
        ("regional", 15000),
        ("nacional", 25000),
    ],
)
def test_calculate_shipping_cost_by_zone(zone, expected_cost):
    """Positiva: tarifa fija por zona cuando no aplica envio gratis."""
    assert calculate_shipping_cost(zone, total_after_discount=50000) == expected_cost


def test_calculate_shipping_cost_just_below_free_threshold():
    """Frontera: 699999 (justo debajo del umbral) aun cobra envio."""
    assert calculate_shipping_cost("nacional", 699999) == 25000


def test_calculate_shipping_cost_at_free_threshold():
    """Frontera: exactamente 700000 el envio debe ser gratis."""
    assert calculate_shipping_cost("nacional", 700000) == 0


# ---------------------------------------------------------------------------
# calculate_order_total (RN-10) - pedidos completos
# ---------------------------------------------------------------------------

def test_calculate_order_total_local_no_discount():
    """Pedido completo sin descuento, con envio local."""
    # subtotal 50000 -> sin descuento -> envio local 8000
    total = calculate_order_total(unit_price=10000, quantity=5, zone="local")
    assert total == 58000


def test_calculate_order_total_with_10_percent_discount():
    """Pedido completo con descuento del 10% y envio regional."""
    # subtotal 150000 -> descuento 15000 -> 135000 -> envio regional 15000
    total = calculate_order_total(unit_price=25000, quantity=6, zone="regional")
    assert total == 150000


def test_calculate_order_total_with_free_shipping():
    """Pedido completo que supera el umbral de envio gratis."""
    # subtotal 1000000 -> descuento 15% = 150000 -> 850000 (>=700000) -> envio 0
    total = calculate_order_total(unit_price=50000, quantity=20, zone="nacional")
    assert total == 850000
