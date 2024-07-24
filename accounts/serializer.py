from django.db.models import Sum
from rest_framework import serializers
from .models import LedgerHead,Ledger,LedgerEntry
from .choice import EntryTypeChoice,AccountTypeChoice



class LedgerHeadSerializer(serializers.ModelSerializer):
    # total_credit_amount_AED = serializers.SerializerMethodField()
    # total_credit_amount_SAR = serializers.SerializerMethodField()
    # total_debit_amount_AED = serializers.SerializerMethodField()
    # total_debit_amount_SAR = serializers.SerializerMethodField()
    # total_balance_amount_AED = serializers.SerializerMethodField()
    # total_balance_amount_SAR = serializers.SerializerMethodField()



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
        
    # def get_total_credit_amount_AED(self, obj):
    #     return Ledger.objects.filter(ledger_head=obj).aggregate(Sum('total_credit_amount_AED'))['total_credit_amount_AED__sum'] or 0
         
    # def get_total_credit_amount_SAR(self, obj):
    #     return Ledger.objects.filter(ledger_head=obj).aggregate(Sum('total_credit_amount_SAR'))['total_credit_amount_SAR__sum'] or 0

    # def get_total_debit_amount_AED(self, obj):
    #     return Ledger.objects.filter(ledger_head=obj).aggregate(Sum('total_debit_amount_AED'))['total_debit_amount_AED__sum'] or 0

    # def get_total_debit_amount_SAR(self, obj):
    #     return Ledger.objects.filter(ledger_head=obj).aggregate(Sum('total_debit_amount_SAR'))['total_debit_amount_SAR__sum'] or 0

    # def get_total_balance_amount_AED(self, obj):
    #     total_credit_AED = self.get_total_credit_amount_AED(obj)
    #     total_debit_AED = self.get_total_debit_amount_AED(obj)
    #     return total_credit_AED - total_debit_AED

    # def get_total_balance_amount_SAR(self, obj):
    #     total_credit_SAR = self.get_total_credit_amount_SAR(obj)
    #     total_debit_SAR = self.get_total_debit_amount_SAR(obj)
    #     return total_credit_SAR - total_debit_SAR


    
class LedgerEntrySerializer(serializers.ModelSerializer):
    ledger_name = serializers.CharField(source="ledger.title", read_only=True)
    
    class Meta:
        model = LedgerEntry
        fields = [
            "id",
            "date",
            "particulars",
            "ledger",
            "ledger_name",
            "entry_type",
            "amount_AED",
            "amount_SAR",
            "conversion_rate",
            "remarks",
            "created_at",
        ]
        read_only_fields = [
            'created_at',
        ]

class LedgerSerializer(serializers.ModelSerializer):
    # total_credit_amount_AED = serializers.SerializerMethodField()
    # total_credit_amount_SAR = serializers.SerializerMethodField()
    # total_debit_amount_AED = serializers.SerializerMethodField()
    # total_debit_amount_SAR = serializers.SerializerMethodField()
    # total_balance_amount_AED = serializers.SerializerMethodField()
    # total_balance_amount_SAR = serializers.SerializerMethodField()
    
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
    
    # def get_total_credit_amount_AED(self, obj):
    #     return LedgerEntry.objects.filter(ledger=obj, entry_type=EntryTypeChoice.CREDIT).aggregate(Sum('amount_AED'))['amount_AED__sum'] or 0
    
    # def get_total_credit_amount_SAR(self, obj):
    #     return LedgerEntry.objects.filter(ledger=obj, entry_type=EntryTypeChoice.CREDIT).aggregate(Sum('amount_SAR'))['amount_SAR__sum'] or 0

    # def get_total_debit_amount_AED(self, obj):
    #     return LedgerEntry.objects.filter(ledger=obj, entry_type=EntryTypeChoice.DEBIT).aggregate(Sum('amount_AED'))['amount_AED__sum'] or 0

    # def get_total_debit_amount_SAR(self, obj):
    #     return LedgerEntry.objects.filter(ledger=obj, entry_type=EntryTypeChoice.DEBIT).aggregate(Sum('amount_SAR'))['amount_SAR__sum'] or 0
    
    # def get_total_balance_amount_AED(self, obj):
    #     total_credit_AED = self.get_total_credit_amount_AED(obj)
    #     total_debit_AED = self.get_total_debit_amount_AED(obj)
    #     return total_credit_AED - total_debit_AED
    
    # def get_total_balance_amount_SAR(self, obj):
    #     total_credit_SAR = self.get_total_credit_amount_SAR(obj)
    #     total_debit_SAR = self.get_total_debit_amount_SAR(obj)
    #     return total_credit_SAR - total_debit_SAR
   