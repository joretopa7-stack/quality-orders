"""Servicio de dominio que coordina la creacion de pedidos.

No depende de FastAPI, HTTP ni de una base de datos real: recibe un
repositorio (en este proyecto, InMemoryOrderRepository) y opera sobre el.
"""

from app.exceptions import DuplicateOrderError
from app.validators import (
    validate_customer_name,
    validate_product_code,
    validate_unit_price,
    validate_quantity,
    validate_shipping_zone,
)
from app.pricing import (
    calculate_subtotal,
    calculate_discount,
    calculate_shipping_cost,
)


class OrderService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def create(self, data: dict) -> dict:
        # 1. Validar y normalizar datos.
        customer_name = validate_customer_name(data["customer_name"])
        product_code = validate_product_code(data["product_code"])
        unit_price = validate_unit_price(data["unit_price"])
        quantity = validate_quantity(data["quantity"])
        zone = validate_shipping_zone(data["shipping_zone"])
        order_code = data["order_code"]

        # 2. Verificar que order_code no exista.
        if self.repository.exists_by_code(order_code):
            raise DuplicateOrderError(
                f"Ya existe un pedido con el codigo: {order_code}"
            )

        # 3-6. Calcular subtotal, descuento, envio y total.
        subtotal = calculate_subtotal(unit_price, quantity)
        discount = calculate_discount(subtotal)
        total_after_discount = subtotal - discount
        shipping_cost = calculate_shipping_cost(zone, total_after_discount)
        total = total_after_discount + shipping_cost

        # 7. Construir el pedido con estado pending.
        order = {
            "order_code": order_code,
            "customer_name": customer_name,
            "product_code": product_code,
            "unit_price": unit_price,
            "quantity": quantity,
            "shipping_zone": zone,
            "subtotal": subtotal,
            "discount": discount,
            "shipping_cost": shipping_cost,
            "total": total,
            "status": "pending",
        }

        # 8. Guardar y retornar el pedido.
        return self.repository.save(order)
