from decimal import Decimal
from typing import Tuple


class PaymentGateway:
    def charge(self, amount: Decimal, metadata: dict | None = None) -> Tuple[bool, str]:
        raise NotImplementedError


