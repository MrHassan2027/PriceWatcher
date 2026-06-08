# PriceWatcher

> Async price tracker that alerts you via email or Discord when a product drops below your target

## What it does
Monitors product pages (Amazon, Noon, or any custom CSS selector) using `aiohttp` + `BeautifulSoup`. Stores price history in SQLite, and fires an alert when the price drops below your configured threshold. Runs as a background service or one-shot cron job.

## Quick Start
```bash
git clone https://github.com/MrHassan2027/PriceWatcher
cd PriceWatcher
pip install -e .
cp config.example.yml config.yml   # add your URLs + thresholds
python -m pricewatcher
```

## Config
```yaml
alerts:
  discord_webhook: "https://discord.com/api/webhooks/..."
  email: "you@example.com"

products:
  - name: "RTX 4070"
    url: "https://www.amazon.com/dp/XXXXXXXX"
    selector: "#priceblock_ourprice"
    target_price: 550.00
    currency: USD
  - name: "Custom product"
    url: "https://example.com/product"
    selector: ".product-price"
    target_price: 100.00
```

## Features
- Async multi-product checking with `asyncio` + `aiohttp`
- Price history stored in SQLite with timestamps
- Discord webhook + SMTP email alerts
- Custom CSS selector per product (works on any site)
- `--once` flag for cron, or runs as a polling loop
- Price history chart export (matplotlib PNG)

## Tech Stack
| Tool | Why |
|------|-----|
| Python 3.11+ | `asyncio` for concurrent fetching |
| `aiohttp` | Async HTTP client |
| `BeautifulSoup4` | HTML price extraction |
| `aiosqlite` | Async SQLite price history |
| `PyYAML` | Config file parsing |
