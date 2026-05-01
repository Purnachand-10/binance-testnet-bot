def validate_symbol(symbol: str) -> str:
    if not symbol or not symbol.isalnum() or len(symbol) < 3:
        raise ValueError("Invalid symbol. Example: BTCUSDT")
    return symbol.upper()


def validate_side(side: str) -> str:
    if not side:
        raise ValueError("Side is required (BUY or SELL)")

    side = side.upper()
    if side not in ["BUY", "SELL"]:
        raise ValueError("Invalid side. Must be BUY or SELL")

    return side


def validate_order_type(order_type: str) -> str:
    if not order_type:
        raise ValueError("Order type is required")

    order_type = order_type.upper()
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Invalid order type. Must be MARKET or LIMIT")

    return order_type


def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
    except ValueError:
        raise ValueError("Quantity must be a valid number")

    if qty <= 0:
        raise ValueError("Quantity must be greater than 0")

    return qty


def validate_price(price: str) -> float:
    if price is None:
        return None

    try:
        p = float(price)
    except ValueError:
        raise ValueError("Price must be a valid number")

    if p <= 0:
        raise ValueError("Price must be greater than 0")

    return p


def validate_limit_requirements(order_type: str, price: float):
    if order_type.upper() == "LIMIT" and price is None:
        raise ValueError("LIMIT order requires a price")
