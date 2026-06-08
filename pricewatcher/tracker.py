import asyncio
import aiohttp
import aiosqlite
from bs4 import BeautifulSoup
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    url: str
    selector: str
    target_price: float
    currency: str = "USD"


async def fetch_price(session: aiohttp.ClientSession, product: Product) -> float | None:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        async with session.get(product.url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as r:
            html = await r.text()
        soup = BeautifulSoup(html, "html.parser")
        el = soup.select_one(product.selector)
        if not el:
            return None
        text = el.get_text(strip=True).replace(",", "").replace("$", "").replace("£", "")
        return float("".join(c for c in text if c.isdigit() or c == "."))
    except Exception:
        return None


async def check_products(products: list[Product], db_path: str = "prices.db") -> list[tuple[Product, float]]:
    drops: list[tuple[Product, float]] = []

    async with aiosqlite.connect(db_path) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS prices (name TEXT, price REAL, ts TEXT)"
        )
        await db.commit()

        async with aiohttp.ClientSession() as session:
            tasks = [fetch_price(session, p) for p in products]
            results = await asyncio.gather(*tasks)

        for product, price in zip(products, results):
            if price is None:
                continue
            await db.execute("INSERT INTO prices VALUES (?, ?, ?)", (product.name, price, datetime.utcnow().isoformat()))
            await db.commit()
            if price <= product.target_price:
                drops.append((product, price))

    return drops
