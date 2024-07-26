from rest_framework import serializers
from accounts.models import Ledger,LedgerHead
from .models import ActivityLog,CompanyBankAccount,Settings

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'

class CompanyBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyBankAccount
        fields = [

            "id",
            "title",
            "account_holder_name",
            "account_number",
            "bank_name",
            "bank_address",
            "branch_name",
            "ifsc",
            "iban_number",
            "bic_or_swift_code",
            "note",
            "international_transfer_charge",
            "international_receipt_charge",
            "domestic_intra_transfer_charge",
            "bank_cash_withdrawal_fee_percentage",
            "ledger"
            
            ]
        
    def create(self, validated_data):
        if 'ledger' not in validated_data or validated_data['ledger'] is None:
            ledger_head = LedgerHead.objects.get(pk=2)
            ledger = Ledger.objects.create(
                ledger_head=ledger_head,
                title=validated_data['title'],
                is_default=True
            )
            validated_data['ledger'] = ledger
        return super(CompanyBankAccountSerializer, self).create(validated_data)
    
class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = [

            "id",
            "default_SAR_to_AED_conversion_rate",
            "default_SAR_to_USD_conversion_rate"
            
            ]
