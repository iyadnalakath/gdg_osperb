from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from rest_framework import serializers
from .models import LedgerHead,Ledger,LedgerEntry,Contra
from .choice import EntryTypeChoice,AccountTypeChoice



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
        
    
class LedgerEntrySerializer(serializers.ModelSerializer):
    ledger_name = serializers.CharField(source="ledger.title", read_only=True)
    content_type = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all(), required=False)
    object_id = serializers.IntegerField(required=False)
    
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
            "content_type",
            "object_id",

        ]
        read_only_fields = [
            'created_at',
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

class ContraSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contra
        fields = [

            "id",
            "date",
            "particulars",
            "from_ledger",
            "to_ledger",
            "amount_AED",
            "amount_SAR",
            "conversion_rate",
            "remarks",
            
            ]
        read_only_fields = [
            "date",
            ]
        
    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
        


# <<<<<<<LEDGER>>>>>>>>
    # total_credit_amount_AED = serializers.SerializerMethodField()
    # total_credit_amount_SAR = serializers.SerializerMethodField()
    # total_debit_amount_AED = serializers.SerializerMethodField()
    # total_debit_amount_SAR = serializers.SerializerMethodField()
    # total_balance_amount_AED = serializers.SerializerMethodField()
    # total_balance_amount_SAR = serializers.SerializerMethodField()
         
    
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
   

#    <<<<<<LEDGER HEAD>>>>>>>>

    # total_credit_amount_AED = serializers.SerializerMethodField()
    # total_credit_amount_SAR = serializers.SerializerMethodField()
    # total_debit_amount_AED = serializers.SerializerMethodField()
    # total_debit_amount_SAR = serializers.SerializerMethodField()
    # total_balance_amount_AED = serializers.SerializerMethodField()
    # total_balance_amount_SAR = serializers.SerializerMethodField()


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



# <<<<<<<< CONTRA >>>>>>>>>

# create method for from and to ledger_entry
    # def create(self, validated_data):
    #     contra = super().create(validated_data)
    #     content_type = ContentType.objects.get_for_model(contra)

    #     # Create LedgerEntry for from_ledger
    #     LedgerEntry.objects.create(
    #         particulars=f"Transfer to {contra.to_ledger.title}",
    #         ledger=contra.from_ledger,
    #         entry_type=EntryTypeChoice.DEBIT,
    #         amount_AED=contra.amount_AED,
    #         amount_SAR=contra.amount_SAR,
    #         conversion_rate=contra.conversion_rate,
    #         remarks=contra.remarks,
    #         content_type=content_type,
    #         object_id=contra.id,
    #     )

    #     # Create LedgerEntry for to_ledger
    #     LedgerEntry.objects.create(
    #         particulars=f"Transfer from {contra.from_ledger.title}",
    #         ledger=contra.to_ledger,
    #         entry_type=EntryTypeChoice.CREDIT,
    #         amount_AED=contra.amount_AED,
    #         amount_SAR=contra.amount_SAR,
    #         conversion_rate=contra.conversion_rate,
    #         remarks=contra.remarks,
    #         content_type=content_type,
    #         object_id=contra.id,
    #     )

    #     return contra






