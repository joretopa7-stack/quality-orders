"""Validadores de campos de entrada del pedido.

Cada funcion es intencionalmente pequena y con una unica responsabilidad,
para que pueda probarse de forma aislada sin depender de otras reglas.
"""

from app.exceptions import (
    InvalidCustomerNameError,
    InvalidProductCodeError,
    InvalidPriceError,
    InvalidQuantityError,
    InvalidShippingZoneError,
)

MIN_CUSTOMER_NAME_LENGTH = 3
MIN_PRODUCT_CODE_LENGTH = 3
MIN_QUANTITY = 1
MAX_QUANTITY = 20
ALLOWED_SHIPPING_ZONES = {"local", "regional", "nacional"}


def validate_customer_name(customer_name: str) -> str:
    """RN-01: normaliza espacios y exige minimo 3 caracteres."""
    if customer_name is None:
        raise InvalidCustomerNameError("El nombre del cliente es requerido.")

    normalized = customer_name.strip()
    if len(normalized) < MIN_CUSTOMER_NAME_LENGTH:
        raise InvalidCustomerNameError(
            f"El nombre del cliente debe tener minimo {MIN_CUSTOMER_NAME_LENGTH} "
            f"caracteres: '{customer_name}'"
        )
    return normalized


def validate_product_code(product_code: str) -> str:
    """RN-02: normaliza a mayusculas y exige minimo 3 caracteres."""
    if product_code is None:
        raise InvalidProductCodeError("El codigo de producto es requerido.")

    normalized = product_code.strip().upper()
    if len(normalized) < MIN_PRODUCT_CODE_LENGTH:
        raise InvalidProductCodeError(
            f"El codigo de producto debe tener minimo {MIN_PRODUCT_CODE_LENGTH} "
            f"caracteres: '{product_code}'"
        )
    return normalized


def validate_unit_price(unit_price: float) -> float:
    """RN-03: el precio unitario debe ser mayor que 0."""
    price = float(unit_price)
    if price <= 0:
        raise InvalidPriceError(
            f"El precio unitario debe ser mayor que 0: {unit_price}"
        )
    return price


def validate_quantity(quantity: int) -> int:
    """RN-04: la cantidad permitida esta entre 1 y 20, inclusive."""
    qty = int(quantity)
    if qty < MIN_QUANTITY or qty > MAX_QUANTITY:
        raise InvalidQuantityError(
            f"La cantidad debe estar entre {MIN_QUANTITY} y {MAX_QUANTITY} "
            f"unidades: {quantity}"
        )
    return qty


def validate_shipping_zone(zone: str) -> str:
    """RN-07: normaliza a minusculas y exige una zona permitida."""
    if zone is None:
        raise InvalidShippingZoneError("La zona de envio es requerida.")

    normalized = zone.strip().lower()
    if normalized not in ALLOWED_SHIPPING_ZONES:
        raise InvalidShippingZoneError(f"Zona de envio no permitida: '{zone}'")
    return normalized
