#!/usr/bin/env python3

"""
E-commerce Data Generator
Author: Marvin
Description: Example script demonstrating how to generate and save mock e-commerce orders.

Usage:
    python exmamples/generate_data_example.py --count 500
"""

# -----------------------------------------
# E-commerce Data Generator (Pseudocode)
# -----------------------------------------

# Imports
# Standard library
import argparse  # for command-line arguments
import json  # for exporting data to JSON
import os  # for file operations
import logging  # for logging events

# External libraries
from faker import Faker  # for realistic names, addresses, emails
from data_pipeline.generate_data import generate_order

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

if __name__ == "__main__":
    # Command-line arguments
    parser = argparse.ArgumentParser(description="Generate mock e-commerce orders")
    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Number of orders to generate",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Generate and print a single test order instead of saving many",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed for reproducible fake data (optional)",
    )
    parser.add_argument(
        "--outdir",
        type=str,
        default="data",
        help="Output directory for generated files (default: data)",
    )
    parser.add_argument(
        "--outfile",
        type=str,
        default="orders.json",
        help="Output filename for generated orders (default: orders.json)",
    )
    args = parser.parse_args()

    # Initialize Faker
    fake = Faker()
    if args.seed is not None:
        fake.seed_instance(args.seed)
        logging.info(f"Using seed: {args.seed}")
    else:
        logging.info("No seed provided (random mode)")

    if args.test:
        # Run a single test order
        order = generate_order(fake)
        logging.info("Generated single test order:")
        logging.info(json.dumps(order, indent=2))
    else:
        # Loop to generate N orders
        orders = [generate_order(fake) for _ in range(args.count)]

        # Ensure output directory exists
        os.makedirs(args.outdir, exist_ok=True)

        # Save orders to JSON file
        orders_path = os.path.join(args.outdir, args.outfile)
        with open(orders_path, "w") as f:
            json.dump(orders, f, indent=2)

        # Save metadata (seed + count) with dynamic filename
        metadata = {
            "count": args.count,
            "seed": args.seed,
        }
        meta_filename = args.outfile.replace(".json", "_meta.json")
        meta_path = os.path.join(args.outdir, meta_filename)
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=2)

        logging.info(
            f"Generated {args.count} orders and saved to {orders_path} "
            f"(metadata saved to {meta_path})"
        )
