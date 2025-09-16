from decimal import Decimal
from typing import Tuple

class DummyGateway:
    def charge(self, amount: Decimal, metadata: dict | None = None) -> Tuple[bool, str]:
        if amount < 0:
            return False, "invalid-amount"
        return True, "dummy-ref"


