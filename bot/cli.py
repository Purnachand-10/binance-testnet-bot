import argparse
import os
import sys
from dotenv import load_dotenv

# Optional: Using rich for enhanced CLI UX (Bonus Task)
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
from .validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price

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
    if HAS_RICH:
        table = Table(title="Order Placement Success")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Order ID", str(response.get('orderId', 'N/A')))
        table.add_row("Status", str(response.get('status', 'N/A')))
        table.add_row("Executed Qty", str(response.get('executedQty', 'N/A')))
        if response.get('avgPrice') and float(response.get('avgPrice')) > 0:
            table.add_row("Avg Price", str(response.get('avgPrice')))
            
        console.print(table)
    else:
        print("\n--- Order Success ---")
        print(f"Order ID:     {response.get('orderId')}")
        print(f"Status:       {response.get('status')}")
        print(f"Executed Qty: {response.get('executedQty')}")
        if response.get('avgPrice') and float(response.get('avgPrice')) > 0:
            print(f"Avg Price:    {response.get('avgPrice')}")
        print("---------------------\n")

def main():
    # Initialize file logging
    setup_logging()
    
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True, help="Trading symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=['BUY', 'SELL'], help="BUY or SELL")
    parser.add_argument("--type", required=True, dest="order_type", choices=['MARKET', 'LIMIT'], help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Order price (required for LIMIT orders)")

    args = parser.parse_args()

    # 1. Input Validation
    try:
        symbol = validate_symbol(args.symbol)
        side = validate_side(args.side)
        order_type = validate_order_type(args.order_type)
        quantity = validate_quantity(args.quantity)
        price = validate_price(args.price)

        if order_type == 'LIMIT' and price is None:
            print_error("--price is required for LIMIT orders.")
            sys.exit(1)

    except ValueError as e:
        print_error(f"Validation failed: {e}")
        sys.exit(1)

    # 2. Load API Credentials
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print_error("BINANCE_API_KEY and BINANCE_API_SECRET must be set in your .env file.")
        sys.exit(1)

    # Print requested order info
    print_summary(symbol, side, order_type, quantity, price)

    # 3. Initialize Client
    client = BinanceFuturesClient(api_key, api_secret, testnet=True)

    # 4. Execute Order
    try:
        if HAS_RICH:
            with console.status("[bold green]Placing order on Binance Futures Testnet..."):
                response = place_order(client, symbol, side, order_type, quantity, price)
        else:
            print("Placing order on Binance Futures Testnet...")
            response = place_order(client, symbol, side, order_type, quantity, price)

        # Print success
        print_success(response)

    except Exception as e:
        if HAS_RICH:
            console.print(Panel(f"[bold red]{str(e)}[/bold red]", title="Order Failed", border_style="red"))
        else:
            print(f"\n[!] Order Failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
