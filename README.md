# Binance Futures Testnet Trading Bot

A Python application to place orders on the Binance Futures Testnet (USDT-M), fulfilling the application task requirements.

## Features
- **Proper Structure:** Clean separation of API client layer, order placement logic, validation, and CLI.
- **Bonus Feature (Enhanced CLI UX):** Utilizes the `rich` library to present beautiful summary tables, validation errors, and clear response formats.
- **Logging:** All API requests, responses, and errors are cleanly logged to `bot.log`.
- **Error Handling:** Graceful handling of standard input validation errors and raw API error responses.

## Assumptions
- You have registered a Binance Futures Testnet account and generated API credentials.
- Python 3.8+ is installed.
- Stable network connectivity to `https://testnet.binancefuture.com` is available.

## Setup Steps

1. **Install Requirements:**
   Make sure you are in the project root directory (`trading_bot/`), then install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Credentials:**
   Copy the provided `.env.example` file to a new file named `.env`:
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and insert your Binance Futures Testnet API Key and Secret:
   ```env
   BINANCE_API_KEY=your_testnet_api_key_here
   BINANCE_API_SECRET=your_testnet_api_secret_here
   ```

## How to Run Examples

The CLI takes the following arguments:
- `--symbol` (e.g., BTCUSDT)
- `--side` (BUY or SELL)
- `--type` (MARKET or LIMIT)
- `--quantity` (e.g., 0.001)
- `--price` (Required if type is LIMIT)

### Example 1: Place a MARKET Order
Will buy 0.002 BTC at the current market price.
```bash
python -m bot.cli --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
```

### Example 2: Place a LIMIT Order
Will place a limit sell order for 0.01 ETH at a price of $4000.
```bash
python -m bot.cli --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.01 --price 4000
```

## Logs
After running the script, a `bot.log` file will automatically be generated in your project root containing a detailed trace of the HTTP requests, responses, and any raised exceptions.
