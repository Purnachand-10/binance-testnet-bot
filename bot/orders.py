from .client import BinanceFuturesClient
import logging

logger = logging.getLogger(__name__)


def place_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None
):
    """
    Constructs the payload and places an order on Binance Futures.
    """

    endpoint = "/fapi/v1/order"

    # Normalize inputs
    symbol = symbol.upper()
    side = side.upper()
    order_type = order_type.upper()

    # Build payload
    payload = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity
    }

    # Handle LIMIT order requirements
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders")

        payload["price"] = price
        payload["timeInForce"] = "GTC"

    # Log request
    logger.info(f"[ORDER REQUEST] {payload}")

    try:
        response = client.send_signed_request("POST", endpoint, payload)

        # Log response
        logger.info(f"[ORDER RESPONSE] {response}")

        return response

    except Exception as e:
        logger.error(f"[ORDER ERROR] Failed to place order: {e}")
        raise
