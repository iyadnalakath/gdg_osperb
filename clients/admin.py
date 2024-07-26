from django.contrib import admin
from .models import Client,BankDepositCard,ClientBankAccount
# Register your models here.


class ClientAdmin(admin.ModelAdmin):
    list_display = [

        "id", 
        "name",
        "country_code",
        "phone",
        "address",
        "transfer_rate_aed",
        "transfer_rate_usd",
        "amount_transfer_rate_aed",
        "amount_transfer_rate_usd",
        "is_service_charge_accountable",
        "ledger_balance",
        "total_transfer_amount",
        "total_client_recieved_aed_amount",
        "total_client_recieved_usd_amount",
        "ledger"
        
        ]
admin.site.register(Client, ClientAdmin)

class ClientBankAccountAdmin(admin.ModelAdmin):
    list_display = [
        
        "id", 
        "client",
        "account_holder_name",
        "account_number",
        "bank_name",
        "bank_address",
        "branch_name",
        "ifsc",
        "iban_number",
        "bic_or_swift_code"

        ]
admin.site.register(ClientBankAccount, ClientBankAccountAdmin)

class BankDepositCardAdmin(admin.ModelAdmin):
    list_display = [
        
        "id", 
        "card_number",
        "client",
        "title",
        "Note",

        ]
admin.site.register(BankDepositCard, BankDepositCardAdmin)
