def validate_symbol(symbol: str) -> str:
    """Validates the trading symbol format."""
    if not symbol or not symbol.isalnum() or len(symbol) < 3:
        raise ValueError("Invalid symbol format. Example: BTCUSDT")
    return symbol.upper()

def validate_side(side: str) -> str:
    """Validates the order side (BUY/SELL)."""
    s = side.upper()
    if s not in ['BUY', 'SELL']:
        raise ValueError("Side must be BUY or SELL.")
    return s

def validate_order_type(order_type: str) -> str:
    """Validates the order type (MARKET/LIMIT)."""
    ot = order_type.upper()
    if ot not in ['MARKET', 'LIMIT']:
        raise ValueError("Order type must be MARKET or LIMIT.")
    return ot

def validate_quantity(quantity: str) -> float:
    """Validates that the quantity is a positive number."""
    try:
        q = float(quantity)
        if q <= 0:
            raise ValueError("Quantity must be greater than 0.")
        return q
    except ValueError:
        raise ValueError("Quantity must be a valid positive number.")

def validate_price(price: str) -> float:
    """Validates that the price is a positive number if provided."""
    if price is None:
        return None
    try:
        p = float(price)
        if p <= 0:
            raise ValueError("Price must be greater than 0.")
        return p
    except ValueError:
        raise ValueError("Price must be a valid positive number.")
