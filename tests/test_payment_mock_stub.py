import pytest
from unittest.mock import Mock, patch

from services.library_service import pay_late_fees, refund_late_fee_payment
from services.payment_service import PaymentGateway


# ---------- pay_late_fees tests ----------

def test_pay_late_fees_success():
    # stub the fee calculation
    with patch("services.library_service.calculate_late_fee_for_book",
               return_value={"fee_amount": 7.5, "days_overdue": 5}):
        gateway = Mock(spec=PaymentGateway)
        gateway.process_payment.return_value = True

        result = pay_late_fees("123456", 1, gateway)

        assert result["status"] == "success"
        assert result["amount"] == 7.5
        gateway.process_payment.assert_called_once_with(7.5)


def test_pay_late_fees_declined():
    with patch("services.library_service.calculate_late_fee_for_book",
               return_value={"fee_amount": 7.5, "days_overdue": 5}):
        gateway = Mock(spec=PaymentGateway)
        gateway.process_payment.return_value = False

        result = pay_late_fees("123456", 1, gateway)

        assert result["status"] == "declined"
        gateway.process_payment.assert_called_once_with(7.5)


def test_pay_late_fees_invalid_patron_id():
    with patch("services.library_service.calculate_late_fee_for_book",
               return_value={"fee_amount": 7.5, "days_overdue": 5}):
        gateway = Mock(spec=PaymentGateway)

        result = pay_late_fees("abcxyz", 1, gateway)

        assert result["status"] == "error"
        gateway.process_payment.assert_not_called()


def test_pay_late_fees_zero_fee():
    with patch("services.library_service.calculate_late_fee_for_book",
               return_value={"fee_amount": 0.0, "days_overdue": 0}):
        gateway = Mock(spec=PaymentGateway)

        result = pay_late_fees("123456", 1, gateway)

        assert result["status"] == "error"
        assert "No fees due" in result["message"]
        gateway.process_payment.assert_not_called()


def test_pay_late_fees_network_error():
    with patch("services.library_service.calculate_late_fee_for_book",
               return_value={"fee_amount": 5.0, "days_overdue": 3}):
        gateway = Mock(spec=PaymentGateway)
        gateway.process_payment.side_effect = ConnectionError("network down")

        result = pay_late_fees("123456", 1, gateway)

        assert result["status"] == "error"
        assert "network" in result["message"].lower()


# ---------- refund_late_fee_payment tests ----------

def test_refund_success():
    gateway = Mock(spec=PaymentGateway)
    gateway.refund_payment.return_value = True

    result = refund_late_fee_payment("txn_1001", 5.0, gateway)

    assert result["status"] == "success"
    assert result["amount"] == 5.0
    gateway.refund_payment.assert_called_once_with("txn_1001", 5.0)


def test_refund_gateway_failure():
    gateway = Mock(spec=PaymentGateway)
    gateway.refund_payment.return_value = False

    result = refund_late_fee_payment("txn_1001", 5.0, gateway)

    assert result["status"] == "error"
    gateway.refund_payment.assert_called_once_with("txn_1001", 5.0)


@pytest.mark.parametrize("amount", [0, -1, 16.0])
def test_refund_invalid_amount(amount):
    gateway = Mock(spec=PaymentGateway)

    result = refund_late_fee_payment("txn_1001", amount, gateway)

    assert result["status"] == "error"
    gateway.refund_payment.assert_not_called()


def test_refund_invalid_transaction_id():
    gateway = Mock(spec=PaymentGateway)

    result = refund_late_fee_payment("", 5.0, gateway)

    assert result["status"] == "error"
    gateway.refund_payment.assert_not_called()
