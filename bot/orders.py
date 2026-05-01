from .client import BinanceFuturesClient

def place_order(client: BinanceFuturesClient, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """
    Constructs the payload and places an order on Binance Futures.
    """
    endpoint = "/fapi/v1/order"
    
    payload = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity
    }
    
    # Specific parameter requirements for LIMIT orders
    if order_type.upper() == "LIMIT":
        if price is None:
            raise ValueError("Price is explicitly required for LIMIT orders")
        payload["price"] = price
        payload["timeInForce"] = "GTC" # Good Till Canceled
        
    return client.send_signed_request("POST", endpoint, payload)
