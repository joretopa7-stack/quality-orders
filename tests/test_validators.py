import pytest

from app.validators import (
    validate_customer_name,
    validate_product_code,
    validate_unit_price,
    validate_quantity,
    validate_shipping_zone,
)
from app.exceptions import (
    InvalidCustomerNameError,
    InvalidProductCodeError,
    InvalidPriceError,
    InvalidQuantityError,
    InvalidShippingZoneError,
)


# ---------------------------------------------------------------------------
# validate_customer_name (RN-01)
# ---------------------------------------------------------------------------

def test_validate_customer_name_normalizes_whitespace():
    """Positiva: quita espacios al inicio y al final."""
    # Arrange
    raw_name = "   Ana Torres   "
    # Act
    result = validate_customer_name(raw_name)
    # Assert
    assert result == "Ana Torres"


def test_validate_customer_name_accepts_exact_minimum_length():
    """Frontera: exactamente 3 caracteres debe ser aceptado."""
    result = validate_customer_name("Ana")
    assert result == "Ana"


def test_validate_customer_name_raises_when_too_short():
    """Negativa: menos de 3 caracteres debe lanzar excepcion."""
    with pytest.raises(InvalidCustomerNameError):
        validate_customer_name("Al")


# ---------------------------------------------------------------------------
# validate_product_code (RN-02)
# ---------------------------------------------------------------------------

def test_validate_product_code_normalizes_to_uppercase():
    """Positiva: se normaliza a mayusculas y se recortan espacios."""
    result = validate_product_code("  abc123  ")
    assert result == "ABC123"


def test_validate_product_code_accepts_exact_minimum_length():
    """Frontera: exactamente 3 caracteres debe ser aceptado."""
    result = validate_product_code("abc")
    assert result == "ABC"


def test_validate_product_code_raises_when_too_short():
    """Negativa: menos de 3 caracteres debe lanzar excepcion."""
    with pytest.raises(InvalidProductCodeError):
        validate_product_code("ab")


# ---------------------------------------------------------------------------
# validate_unit_price (RN-03)
# ---------------------------------------------------------------------------

def test_validate_unit_price_accepts_positive_value():
    """Positiva: un precio mayor que 0 se acepta y retorna como float."""
    result = validate_unit_price(1500)
    assert result == 1500.0


def test_validate_unit_price_raises_when_zero():
    """Frontera/negativa: 0 no es un precio valido."""
    with pytest.raises(InvalidPriceError):
        validate_unit_price(0)


def test_validate_unit_price_raises_when_negative():
    """Negativa: un precio negativo no es valido."""
    with pytest.raises(InvalidPriceError):
        validate_unit_price(-100)


# ---------------------------------------------------------------------------
# validate_quantity (RN-04)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("quantity", [1, 20])
def test_validate_quantity_accepts_boundary_values(quantity):
    """Frontera/positiva: 1 y 20 son los limites validos inclusive."""
    result = validate_quantity(quantity)
    assert result == quantity


@pytest.mark.parametrize("quantity", [0, 21])
def test_validate_quantity_raises_outside_boundaries(quantity):
    """Frontera/negativa: 0 y 21 estan fuera del rango permitido."""
    with pytest.raises(InvalidQuantityError):
        validate_quantity(quantity)


# ---------------------------------------------------------------------------
# validate_shipping_zone (RN-07)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "raw_zone, expected",
    [
        ("local", "local"),
        ("REGIONAL", "regional"),
        ("  Nacional  ", "nacional"),
        ("Local", "local"),
    ],
)
def test_validate_shipping_zone_normalizes(raw_zone, expected):
    """Positiva: las zonas validas se normalizan a minusculas."""
    result = validate_shipping_zone(raw_zone)
    assert result == expected


def test_validate_shipping_zone_raises_when_unknown():
    """Negativa: una zona fuera de la lista permitida lanza excepcion."""
    with pytest.raises(InvalidShippingZoneError):
        validate_shipping_zone("internacional")
