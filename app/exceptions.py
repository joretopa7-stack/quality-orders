"""Excepciones de dominio del sistema de pedidos Quality Orders.

Todas las excepciones especificas heredan de OrderError, la excepcion
base del dominio, para permitir capturas genericas cuando sea necesario
y capturas especificas cuando se requiera distinguir el motivo del fallo.
"""


class OrderError(Exception):
    """Excepcion base para todos los errores del dominio de pedidos."""


class InvalidCustomerNameError(OrderError):
    """Se lanza cuando el nombre del cliente no cumple RN-01."""


class InvalidProductCodeError(OrderError):
    """Se lanza cuando el codigo de producto no cumple RN-02."""


class InvalidPriceError(OrderError):
    """Se lanza cuando el precio unitario no cumple RN-03."""


class InvalidQuantityError(OrderError):
    """Se lanza cuando la cantidad solicitada no cumple RN-04."""


class InvalidShippingZoneError(OrderError):
    """Se lanza cuando la zona de envio no cumple RN-07."""


class DuplicateOrderError(OrderError):
    """Se lanza cuando se intenta registrar un codigo de pedido ya existente (RN-11)."""
