import argparse
import os
import sys
from dotenv import load_dotenv

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from .logging_config import setup_logging
from .client import BinanceFuturesClient
from .orders import place_order
from .validators import (
    validate_symbol,
    validate_side,
    validate_order_type,
    validate_quantity,
    validate_price,
    validate_limit_requirements
)

if HAS_RICH:
    console = Console()


def print_error(msg: str):
    if HAS_RICH:
        console.print(f"[bold red]Error:[/bold red] {msg}")
    else:
        print(f"Error: {msg}")


def print_summary(symbol, side, order_type, quantity, price):
    if HAS_RICH:
        table = Table(title="Order Request Summary", show_header=False)
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="magenta")

        table.add_row("Symbol", symbol)
        table.add_row("Side", side)
        table.add_row("Type", order_type)
        table.add_row("Quantity", str(quantity))
        if price:
            table.add_row("Price", str(price))

        console.print(table)
    else:
        print("\n--- Order Request Summary ---")
        print(f"Symbol:   {symbol}")
        print(f"Side:     {side}")
        print(f"Type:     {order_type}")
        print(f"Quantity: {quantity}")
        if price:
            print(f"Price:    {price}")
        print("-----------------------------\n")


def print_success(response):
    status = response.get("status", "UNKNOWN")

    if HAS_RICH:
        table = Table(title="Order Response")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Order ID", str(response.get("orderId", "N/A")))
        table.add_row("Status", status)
        table.add_row("Executed Qty", str(response.get("executedQty", "N/A")))

        if response.get("avgPrice") and float(response.get("avgPrice")) > 0:
            table.add_row("Avg Price", str(response.get("avgPrice")))

        console.print(table)

        if status == "NEW":
            console.print("[yellow]Note: Order placed but not filled yet.[/yellow]")
        else:
            console.print("[bold green]Order placed successfully![/bold green]")

    else:
        print("\n--- Order Response ---")
        print(f"Order ID:     {response.get('orderId')}")
        print(f"Status:       {status}")
        print(f"Executed Qty: {response.get('executedQty')}")

        if response.get("avgPrice") and float(response.get("avgPrice")) > 0:
            print(f"Avg Price:    {response.get('avgPrice')}")

        if status == "NEW":
            print("Note: Order placed but not filled yet.")
        else:
            print("Order placed successfully!")

        print("-----------------------\n")


def main():
    setup_logging()

    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot"
    )

    parser.add_argument("--symbol", required=True, help="e.g., BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Required for LIMIT orders")

    args = parser.parse_args()

    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price)

        validate_limit_requirements(order_type, price)

    except ValueError as e:
        print_error(f"{e}")
        sys.exit(1)

    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print_error("Missing API keys in .env file")
        sys.exit(1)

    print_summary(symbol, side, order_type, quantity, price)

    client = BinanceFuturesClient(api_key, api_secret, testnet=True)

    try:
        if HAS_RICH:
            with console.status("[bold green]Placing order..."):
                response = place_order(client, symbol, side, order_type, quantity, price)
        else:
            print("Placing order...")
            response = place_order(client, symbol, side, order_type, quantity, price)

        print_success(response)

    except Exception as e:
        if HAS_RICH:
            console.print(Panel(str(e), title="Order Failed", border_style="red"))
        else:
            print(f"\nOrder Failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
