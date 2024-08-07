from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from rest_framework import serializers
from .models import Transfer,Deposit
from accounts.models import LedgerEntry
from accounts.choice import EntryTypeChoice
from accounts.serializer import LedgerEntrySerializer


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
        
        
class DepositSerializer(serializers.ModelSerializer):
    ledger_entries = LedgerEntrySerializer(many=True, read_only=True)

    class Meta:
        model = Deposit
        fields = [

            "id",
            "bank_deposit_card",
            "company_bank_account",
            "client",
            "amount",
            "ledger_entries",
            "note"

            ]




   
        
    # def create(self, validated_data):
    #     deposit = super().create(validated_data)
    #     LedgerEntry.objects.create(
    #         date=now(),
    #         particulars=f"Deposit for {deposit.client.name}",
    #         ledger=deposit.client.ledger,
    #         entry_type=EntryTypeChoice.CREDIT,
    #         amount_AED=0,
    #         amount_SAR=deposit.amount,
    #         conversion_rate=1,
    #         remarks=deposit.note,
    #         created_at=now(),
    #         content_type=ContentType.objects.get_for_model(deposit),
    #         object_id=deposit.id
    #     )

    #     LedgerEntry.objects.create(
    #         date=now(),
    #         particulars=f"Deposit from {deposit.client.name} to Company Bank Account",
    #         ledger=deposit.company_bank_account.ledger,
    #         entry_type=EntryTypeChoice.CREDIT,
    #         amount_AED=0,
    #         amount_SAR=deposit.amount,
    #         conversion_rate=1,
    #         remarks=deposit.note,
    #         created_at=now(),
    #         content_type=ContentType.objects.get_for_model(deposit),
    #         object_id=deposit.id
    #     )
    #     return deposit