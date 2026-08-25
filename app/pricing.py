"""Calculos de precios del pedido.

Cada regla vive en su propia funcion para poder probarla de manera aislada
y detectar con precision cual calculo falla si algo se rompe.
"""

DISCOUNT_TIER_1_THRESHOLD = 100000
DISCOUNT_TIER_2_THRESHOLD = 500000
DISCOUNT_TIER_1_RATE = 0.10
DISCOUNT_TIER_2_RATE = 0.15

SHIPPING_COSTS = {
    "local": 8000,
    "regional": 15000,
    "nacional": 25000,
}

FREE_SHIPPING_THRESHOLD = 700000


def calculate_subtotal(unit_price: float, quantity: int) -> float:
    """RN-05: subtotal = precio_unitario * cantidad."""
    return unit_price * quantity


def calculate_discount(subtotal: float) -> float:
    """RN-06: descuento escalonado segun el subtotal."""
    if subtotal < DISCOUNT_TIER_1_THRESHOLD:
        return 0.0
    if subtotal < DISCOUNT_TIER_2_THRESHOLD:
        return subtotal * DISCOUNT_TIER_1_RATE
    return subtotal * DISCOUNT_TIER_2_RATE


def calculate_shipping_cost(zone: str, total_after_discount: float) -> float:
    """RN-08 y RN-09: tarifa de envio por zona, gratis desde el umbral."""
    if total_after_discount >= FREE_SHIPPING_THRESHOLD:
        return 0.0
    return SHIPPING_COSTS[zone]


def calculate_order_total(unit_price: float, quantity: int, zone: str) -> float:
    """RN-10: total = subtotal - descuento + costo_envio."""
    subtotal = calculate_subtotal(unit_price, quantity)
    discount = calculate_discount(subtotal)
    total_after_discount = subtotal - discount
    shipping_cost = calculate_shipping_cost(zone, total_after_discount)
    return total_after_discount + shipping_cost
