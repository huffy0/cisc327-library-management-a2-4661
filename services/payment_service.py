"""
Payment Service - Simulated payment gateway for assignment 3
"""

import random

class PaymentGateway:
    def __init__(self):
        self.transactions = {}

    def process_payment(self, amount: float) -> bool:
        """Simulate payment processing."""
        if amount <= 0:
            return False
        if random.random() < 0.1:
            raise ConnectionError("Network error during payment")
        transaction_id = f"txn_{random.randint(1000,9999)}"
        self.transactions[transaction_id] = amount
        return True

    def refund_payment(self, transaction_id: str, amount: float) -> bool:
        """Simulate refund processing."""
        if transaction_id not in self.transactions:
            return False
        if amount <= 0 or amount > self.transactions[transaction_id]:
            return False
        return True
