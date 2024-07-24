from django.contrib import admin
from .models import *

# Register your models here.


class LedgerHeadAdmin(admin.ModelAdmin):
    list_display = [
        
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
admin.site.register(LedgerHead, LedgerHeadAdmin)

class LedgerAdmin(admin.ModelAdmin):
    list_display = [
        
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
admin.site.register(Ledger, LedgerAdmin)


class LedgerEntryAdmin(admin.ModelAdmin):
    list_display = [
        
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
admin.site.register(LedgerEntry, LedgerEntryAdmin)