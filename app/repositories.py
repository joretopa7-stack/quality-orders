"""Repositorio en memoria de pedidos.

Simula el almacenamiento sin depender de una base de datos real,
para que el servicio de pedidos pueda probarse de forma unitaria.
"""


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[str, dict] = {}

    def exists_by_code(self, order_code: str) -> bool:
        return order_code in self._orders

    def save(self, order: dict) -> dict:
        self._orders[order["order_code"]] = order
        return order

    def list_all(self) -> list[dict]:
        return list(self._orders.values())
