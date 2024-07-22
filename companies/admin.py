from django.contrib import admin
from .models import ActivityLog,CompanyBankAccount

# Register your models here.


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = [

        'id',
        'user',
        'action_type',
        'timestamp',
        'url',
        'method',
        'request_data',
        'response_data',
        'status_code',
        'execution_time'

    ]
    search_fields = ['user__username', 'action_type', 'url', 'method']
    list_filter = ['action_type', 'timestamp', 'status_code']
    readonly_fields = ['timestamp']

admin.site.register(ActivityLog, ActivityLogAdmin)


class CompanyBankAccountAdmin(admin.ModelAdmin):
    list_display = [

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

admin.site.register(CompanyBankAccount, CompanyBankAccountAdmin)