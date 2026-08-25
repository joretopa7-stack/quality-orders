# Quality Orders

Componente interno para el registro de pedidos, construido para el
Proyecto Evaluable del Modulo II del Curso de Pruebas de Software
(Automatizacion de pruebas unitarias con Pytest).

## Objetivo de las pruebas

Verificar mediante pruebas unitarias automatizadas que la logica de
negocio de Quality Orders (validaciones, calculos de precios y el
servicio de pedidos) cumple las reglas definidas, sin depender de
FastAPI, HTTP, una base de datos real ni servicios externos. El foco es
exclusivamente la prueba unitaria de funciones, validadores, el
repositorio en memoria y el servicio de dominio.

## Reglas de negocio implementadas

| ID | Regla | Implementada en |
|----|-------|------------------|
| RN-01 | Nombre de cliente normalizado, minimo 3 caracteres | `validators.validate_customer_name` |
| RN-02 | Codigo de producto en mayusculas, minimo 3 caracteres | `validators.validate_product_code` |
| RN-03 | Precio unitario mayor que 0 | `validators.validate_unit_price` |
| RN-04 | Cantidad entre 1 y 20 inclusive | `validators.validate_quantity` |
| RN-05 | subtotal = precio_unitario * cantidad | `pricing.calculate_subtotal` |
| RN-06 | Descuento por tramos (0%, 10%, 15%) | `pricing.calculate_discount` |
| RN-07 | Zonas permitidas normalizadas a minusculas | `validators.validate_shipping_zone` |
| RN-08 | Tarifa de envio por zona | `pricing.calculate_shipping_cost` |
| RN-09 | Envio gratis desde 700000 | `pricing.calculate_shipping_cost` |
| RN-10 | total = subtotal - descuento + costo_envio | `pricing.calculate_order_total` / `order_service.OrderService.create` |
| RN-11 | No se permiten codigos de pedido duplicados | `order_service.OrderService.create` + `repositories.InMemoryOrderRepository` |
| RN-12 | Todo pedido inicia en estado `pending` | `order_service.OrderService.create` |

## Requisitos

- Python 3.10 o superior.
- No requiere base de datos, servidor HTTP ni servicios externos.

## Instalacion

```bash
python -m venv .venv
source .venv/bin/activate        # En Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

## Ejecucion de la suite

```bash
python -m pytest              # ejecuta toda la suite
python -m pytest -v           # modo detallado
python -m pytest tests/test_validators.py -v
python -m pytest tests/test_pricing.py -v
python -m pytest tests/test_order_service.py -v
python -m pytest -k discount -v
python -m pytest --lf         # solo los ultimos fallidos
```

## Estructura de carpetas

```
quality-orders/
|-- app/
|   |-- __init__.py
|   |-- exceptions.py     # excepciones de dominio
|   |-- validators.py     # RN-01, RN-02, RN-03, RN-04, RN-07
|   |-- pricing.py        # RN-05, RN-06, RN-08, RN-09, RN-10
|   |-- repositories.py   # repositorio en memoria
|   `-- order_service.py  # coordina validaciones, calculos y guardado
|-- tests/
|   |-- conftest.py
|   |-- test_validators.py
|   |-- test_pricing.py
|   `-- test_order_service.py
|-- .gitignore
|-- pyproject.toml
|-- requirements-dev.txt
`-- README.md
```

## Cantidad total de casos ejecutados

**43 pruebas**, todas en estado `PASSED` (ver `python -m pytest -v`).

## Resumen de pruebas positivas, negativas y de frontera

| Tipo | Cantidad aproximada | Ejemplos |
|------|----------------------|----------|
| Positivas | 20 | normalizacion de nombre/codigo/zona, calculo de subtotal, pedido completo sin descuento |
| Negativas | 12 | nombre/codigo/precio/zona invalidos, cantidad fuera de rango, pedido duplicado, datos invalidos no almacenados |
| Frontera | 11 | nombre de 3 caracteres, cantidad 1 y 20, descuento en 100000/500000, envio gratis en 699999/700000 |

## Fixtures y parametrizacion utilizadas

- `order_repository`: entrega un `InMemoryOrderRepository` nuevo y vacio en
  cada prueba, lo que garantiza independencia entre tests.
- `order_service`: entrega un `OrderService` ya conectado a un
  `order_repository` limpio.
- `valid_order_data`: payload de referencia valido, reutilizable y facil
  de modificar para generar variantes invalidas.
- `pytest.mark.parametrize` se usa para cubrir varias combinaciones de
  cantidad (1, 20, 0, 21), zonas de envio (local, regional, nacional y
  variantes con mayusculas/espacios) y combinaciones de subtotal, sin
  duplicar la estructura Arrange-Act-Assert.

## Matriz de casos de prueba (minimo 25, se documentan 30)

| ID | Regla | Tipo | Dato / escenario | Resultado esperado |
|----|-------|------|--------------------|----------------------|
| CP-01 | RN-01 | Positiva | Nombre con espacios extra | Nombre recortado y normalizado |
| CP-02 | RN-01 | Frontera | Nombre de exactamente 3 caracteres | Aceptado |
| CP-03 | RN-01 | Negativa | Nombre menor a 3 caracteres | Excepcion `InvalidCustomerNameError` |
| CP-04 | RN-02 | Positiva | Codigo en minusculas con espacios | Normalizado a mayusculas |
| CP-05 | RN-02 | Frontera | Codigo de exactamente 3 caracteres | Aceptado |
| CP-06 | RN-02 | Negativa | Codigo menor a 3 caracteres | Excepcion `InvalidProductCodeError` |
| CP-07 | RN-03 | Positiva | Precio = 1500 | Aceptado como float |
| CP-08 | RN-03 | Frontera/Negativa | Precio = 0 | Excepcion `InvalidPriceError` |
| CP-09 | RN-03 | Negativa | Precio = -100 | Excepcion `InvalidPriceError` |
| CP-10 | RN-04 | Frontera | Cantidad = 1 | Aceptada |
| CP-11 | RN-04 | Frontera | Cantidad = 20 | Aceptada |
| CP-12 | RN-04 | Frontera/Negativa | Cantidad = 0 | Excepcion `InvalidQuantityError` |
| CP-13 | RN-04 | Frontera/Negativa | Cantidad = 21 | Excepcion `InvalidQuantityError` |
| CP-14 | RN-07 | Positiva | Zona "local", "REGIONAL", " Nacional ", "Local" | Normalizadas a minusculas |
| CP-15 | RN-07 | Negativa | Zona "internacional" | Excepcion `InvalidShippingZoneError` |
| CP-16 | RN-05 | Positiva | (10000,1), (5000,4), (25000,3) | Subtotales 10000, 20000, 75000 |
| CP-17 | RN-06 | Positiva | Subtotal = 99999 | Descuento 0 |
| CP-18 | RN-06 | Frontera | Subtotal = 100000 | Descuento 10% |
| CP-19 | RN-06 | Frontera | Subtotal = 499999 | Descuento 10% |
| CP-20 | RN-06 | Frontera | Subtotal = 500000 | Descuento 15% |
| CP-21 | RN-06 | Positiva | Subtotal = 600000 | Descuento 15% |
| CP-22 | RN-08 | Positiva | Zonas local/regional/nacional | Tarifas 8000/15000/25000 |
| CP-23 | RN-09 | Frontera | Total tras descuento = 699999 | Cobra envio |
| CP-24 | RN-09 | Frontera | Total tras descuento = 700000 | Envio gratis |
| CP-25 | RN-10 | Positiva | Pedido local sin descuento | Total 58000 |
| CP-26 | RN-10 | Positiva | Pedido regional con 10% descuento | Total 150000 |
| CP-27 | RN-10 | Positiva | Pedido nacional con envio gratis | Total 850000 |
| CP-28 | RN-11 | Negativa | Segundo pedido con mismo `order_code` | Excepcion `DuplicateOrderError`, no se guarda |
| CP-29 | RN-12 | Positiva | Pedido creado correctamente | `status == "pending"` |
| CP-30 | General | Negativa | Pedido con cantidad invalida | No se almacena en el repositorio |

## Registro del defecto controlado detectado por la suite

Como parte de la Fase 15, se introdujo temporalmente un defecto en
`pricing.calculate_shipping_cost`, cambiando la condicion de envio gratis
de `>=` a `>` sobre `FREE_SHIPPING_THRESHOLD` (RN-09).

- **Antes del defecto:** 43 pruebas, 43 `PASSED`.
- **Con el defecto introducido:** 42 `PASSED`, **1 `FAILED`**:
  `tests/test_pricing.py::test_calculate_shipping_cost_at_free_threshold`,
  que esperaba envio gratis (`0`) en el limite exacto de 700000 y recibio
  `25000`.
- **Despues de revertir el defecto:** nuevamente 43 `PASSED`.

Esto confirma que la prueba de frontera diseñada para RN-09 cumple su
proposito: detecta con precision un cambio incorrecto en el operador de
comparacion del umbral.

## Preguntas de reflexion final

**1. ¿Que diferencia hubo entre una prueba positiva, una negativa y una de frontera?**
Las positivas confirman que datos validos producen el resultado
esperado (por ejemplo, una cantidad de 10 se acepta). Las negativas
confirman que datos invalidos son rechazados con la excepcion correcta
(cantidad = 25). Las de frontera prueban los valores exactos donde
cambia el comportamiento (cantidad = 1, 20, 0, 21; subtotal = 100000 y
500000; total tras descuento = 700000), que es donde suelen esconderse
los errores de operadores como `<` vs `<=`.

**2. ¿Cual fue la regla de negocio mas propensa a errores y por que?**
RN-09 (envio gratis) resulto la mas propensa a errores porque combina
dos calculos previos (subtotal y descuento) antes de evaluar un umbral,
y su condicion depende de un operador de comparacion (`>=`) facil de
confundir con `>`. El ejercicio de deteccion de defectos lo demostro
directamente.

**3. ¿Que ventaja aporto `pytest.mark.parametrize`?**
Permitio cubrir varias combinaciones de entrada (cantidades, zonas,
precios y subtotales) reutilizando la misma estructura Arrange-Act-
Assert, sin duplicar codigo ni perder legibilidad, y dejando muy claro
cual escenario especifico fallaba si algo se rompia.

**4. ¿Que problema resolvieron las fixtures?**
Evitaron repetir la construccion de un `InMemoryOrderRepository`, un
`OrderService` y un payload valido en cada prueba, y garantizaron que
cada test recibiera instancias nuevas, evitando estado compartido entre
pruebas.

**5. ¿Como comprobo que las pruebas eran independientes?**
Con una prueba explicita (`test_new_repository_starts_empty_independent_of_other_tests`)
que verifica que un repositorio recien creado por la fixture esta vacio,
sin importar cuantos pedidos hayan guardado otras pruebas antes. Ademas,
la suite completa se ejecuto varias veces (incluyendo con `-k` para
subconjuntos) obteniendo siempre el mismo resultado, sin importar el
orden.

**6. ¿Que prueba detecto el defecto introducido deliberadamente?**
`test_calculate_shipping_cost_at_free_threshold`, en `tests/test_pricing.py`,
al evaluar exactamente el limite de 700000.

**7. ¿Que podria ocurrir si solo se probaran escenarios validos?**
Errores en la validacion de entradas (por ejemplo, aceptar una cantidad
de 0 o un precio negativo) o en los limites exactos de las reglas
pasarian desapercibidos, y solo se descubririan en produccion cuando un
usuario real ingresara datos invalidos o un pedido cayera justo en un
umbral.

**8. ¿Por que este proyecto sigue siendo principalmente de pruebas unitarias y no de integracion?**
Porque cada prueba ejercita una funcion o clase de forma aislada
(un validador, un calculo, el servicio con un repositorio en memoria
inyectado como dependencia), sin levantar un servidor HTTP, sin usar
FastAPI TestClient y sin conectarse a una base de datos real. No se
prueba la interaccion entre sistemas externos, solo la logica de
dominio en memoria.
