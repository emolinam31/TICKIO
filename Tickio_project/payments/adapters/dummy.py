from payments.interfaces import PaymentGateway


class DummyPaymentGateway:
    def charge(self, amount):
        print(f"[Dummy] Charging {amount}")
        return True

