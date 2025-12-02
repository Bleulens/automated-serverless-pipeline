# src/__init__.py

# Expose the main generator function
from .generate_data import generate_order

# Expose constants that define validity
from .generate_data import payment_methods, order_statuses

# Optional: expose catalog if you want strict validation downstream
from .products import products

# Define what "from src import *" will bring in
__all__ = ["generate_order", "payment_methods", "order_statuses", "products"]
