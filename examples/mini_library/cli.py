"""Command-line interface for mini_library."""

from __future__ import annotations

import argparse
import sys

from mini_library.config import Settings
from mini_library.models import Item
from mini_library.services import OrderService
from mini_library.storage import InMemoryStorage


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mini_library")
    parser.add_argument("customer", help="Customer name for a new order")
    parser.add_argument("--sku", default="SKU-1")
    parser.add_argument("--price", type=float, default=9.99)
    return parser


def main(args: list[str] | None = None) -> int:
    """Run a demo order flow and print the quoted total."""
    parser = build_parser()
    ns = parser.parse_args(args)
    service = OrderService(InMemoryStorage(), Settings())
    order = service.create_order(ns.customer)
    service.add_item(order.order_id, Item(sku=ns.sku, title="Demo", price=ns.price))
    print(service.quote_total(order.order_id))
    return 0


if __name__ == "__main__":
    sys.exit(main())
