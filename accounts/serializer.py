from rest_framework import serializers
from .models import LedgerHead,Ledger,LedgerEntry



class LedgerHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerHead
        fields = [

            "id",
            "account_head",
            "title",
            "description",
            "total_credit_amount_AED",
            "total_credit_amount_SAR",
            "total_debit_amount_AED",
            "total_debit_amount_SAR",
            "total_balance_amount_AED",
            "total_balance_amount_SAR",
            "is_default",
            "created_at",
            
            
            ]
        read_only_fields = [
            'created_at',
            "is_default",
            "total_credit_amount_AED",
            "total_credit_amount_SAR",
            "total_debit_amount_AED",
            "total_debit_amount_SAR",
            "total_balance_amount_AED",
            "total_balance_amount_SAR",
            
            ]
        
class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ledger
        fields = [

            "id",
            "ledger_head",
            "title",
            "description",
            "total_credit_amount_AED",
            "total_credit_amount_SAR",
            "total_debit_amount_AED",
            "total_debit_amount_SAR",
            "total_balance_amount_AED",
            "total_balance_amount_SAR",
            "opening_balance",
            "is_default",
            "created_at",
            
            
            ]
        read_only_fields = [
            'created_at',
            "is_default",
            "total_credit_amount_AED",
            "total_credit_amount_SAR",
            "total_debit_amount_AED",
            "total_debit_amount_SAR",
            "total_balance_amount_AED",
            "total_balance_amount_SAR",
            
            ]
        

class LedgerEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerEntry
        fields = [

            "id",
            "date",
            "particulars",
            "ledger",
            "entry_type",
            "amount_AED",
            "amount_SAR",
            "conversion_rate",
            "remarks",
            "created_at",
            
            ]
        
        read_only_fields = [
            'created_at' 
            ]