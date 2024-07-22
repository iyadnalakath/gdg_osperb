from rest_framework import serializers
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
            
            ]

class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        fields = [

            "id",
            "default_SAR_to_AED_conversion_rate",
            "default_SAR_to_USD_conversion_rate"
            
            ]
