from rest_framework import serializers
from .models import Transfer


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = [

            "id",
            "transfer_id",
            "client",
            "client_data",
            "date",
            "deposit_amount",
            "withdrawal_type",
            "transfer_currency",
            "client_transfer_rate_type",
            "client_transfer_rate",
            "client_amount_transfer_rate",
            "client_recieved_amount",
            "transfer_amount",
            "source_company_bank_account",
            "recieved_client_bank_account",
            "recieved_company_bank_account",
            "SR_to_AED_conversion_rate",
            "international_bank_receipt_charge_AED",
            "international_bank_receipt_charge_SAR",
            "bank_cash_withdrawal_charge_AED",
            "bank_cash_withdrawal_charge_SAR",
            "company_cash_withdrawal_fee_percentage",
            "company_cash_withdrawal_fee_AED",
            "company_cash_withdrawal_fee_SAR",
            "status",
            "pending_at",
            "deposited_at",
            "transferred_at",
            "received_at",
            "withdrawn_at",
            "completed_at",
            "is_service_charge_accountable_by_client",
            "transfer_profit",
            "total_company_expense",
            "net_profit"

            ]