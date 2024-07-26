from django.db import models
from django.apps import apps
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from accounts.models import Ledger,LedgerHead

class CompanyBankAccount(models.Model):
    title = models.CharField(max_length=125, null=False, blank=False)
    account_holder_name = models.CharField(max_length=125, null=True, blank=True)
    account_number = models.DecimalField(max_digits=25, decimal_places=3)
    bank_name = models.CharField(max_length=125, null=True, blank=True)
    bank_address = models.CharField(max_length=125, null=True, blank=True)
    branch_name = models.CharField(max_length=125, null=True, blank=True)
    ifsc = models.CharField(max_length=125, null=True, blank=True)
    iban_number = models.CharField(max_length=125, null=True, blank=True)
    bic_or_swift_code = models.CharField(max_length=125, null=False, blank=False)
    note = models.TextField(null=True, blank=True)
    international_transfer_charge = models.DecimalField(max_digits=10, decimal_places=3)
    international_receipt_charge = models.DecimalField(max_digits=10, decimal_places=3)
    domestic_intra_transfer_charge = models.DecimalField(max_digits=10, decimal_places=3)
    bank_cash_withdrawal_fee_percentage = models.DecimalField(max_digits=10, decimal_places=3)
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, null=True, blank=True)
    # ledger_balance = models.DecimalField(max_digits=10, decimal_places=3)
    
    def __str__(self):
        return self.title
    
class Settings(models.Model):
    default_SAR_to_AED_conversion_rate = models.DecimalField(max_digits=10, decimal_places=3)
    default_SAR_to_USD_conversion_rate = models.DecimalField(max_digits=10, decimal_places=3)
    # default_client_ledger_head = models.ForeignKey(LedgerHead, on_delete=models.CASCADE, related_name='client_ledger_head')
    # default_bank_ledger_head = models.ForeignKey(LedgerHead, on_delete=models.CASCADE, related_name='bank_ledger_head')
    # default_cash_ledger_head = models.ForeignKey(LedgerHead, on_delete=models.CASCADE, related_name='cash_ledger_head')
    # default_expense_ledger_head = models.ForeignKey(LedgerHead, on_delete=models.CASCADE, related_name='expense_ledger_head')
    # default_cash_in_hand_ledger = models.ForeignKey(LedgerHead, on_delete=models.CASCADE, related_name='cash_in_hand_ledger')

class Country(models.Model):
    name = models.CharField(max_length=125, null=False, blank=False)
    latitude = models.CharField(max_length=125, null=True, blank=True)
    longitude = models.CharField(max_length=125, null=True, blank=True)
    code = models.CharField(max_length=25, null=True, blank=True)
    dial_code = models.CharField(max_length=125, null=True, blank=True)

    def __str__(self):
        return self.name
    

class ActivityLog(models.Model):
    user = models.ForeignKey('user.User', null=True, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=125, null=False, blank=False)
    timestamp = models.DateTimeField(default=now, editable=True)
    url = models.CharField(max_length=125, null=False, blank=False)
    method = models.CharField(max_length=125, null=False, blank=False)
    request_data = models.TextField(null=True, blank=True)
    response_data = models.TextField(null=True, blank=True)
    status_code = models.IntegerField()
    execution_time = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f'{self.user} - {self.action_type} at {self.timestamp}'