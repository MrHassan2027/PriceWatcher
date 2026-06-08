import asyncio
import json
import click
from rich.console import Console
from .tracker import Product, check_products

console = Console()

@click.command()
@click.option("--config", default="products.json", help="JSON file with products to watch")
@click.option("--once", is_flag=True, help="Run once and exit")
def main(config: str, once: bool):
    """Watch product prices and alert when they drop below target."""
    try:
        with open(config) as f:
            data = json.load(f)
        products = [Product(**p) for p in data]
    except FileNotFoundError:
        console.print(f"[red]Config file '{config}' not found.[/red]")
        console.print("Create a products.json with a list of product objects.")
        return

    async def run():
        console.print(f"[cyan]Checking {len(products)} product(s)...[/cyan]")
        drops = await check_products(products)
        if drops:
            for product, price in drops:
                console.print(f"[green]ALERT: {product.name} dropped to {price} {product.currency}![/green]")
        else:
            console.print("[dim]No price drops found.[/dim]")

    asyncio.run(run())

if __name__ == "__main__":
    main()
