from django.contrib import admin
from django.utils.html import format_html
from .models import Deposit

# Register your models here.
class DepositAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "bank_deposit_card",
        "company_bank_account",
        "client",
        "amount",
        "note",
        "display_ledger_entries"
    ]
    
    def display_ledger_entries(self, obj):  
        entries = obj.ledger_entries.all()
        entry_display = ', '.join([f"ID: {entry.id}, Amount (SAR): {entry.amount_SAR}" for entry in entries])
        return format_html(entry_display or "No Entries")
    
    display_ledger_entries.short_description = "Ledger Entries"

admin.site.register(Deposit, DepositAdmin)