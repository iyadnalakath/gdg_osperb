from django.db import models
from django.utils.timezone import now
from clients.models import Client,ClientBankAccount,BankDepositCard
from companies.models import CompanyBankAccount
from .choice import WithdrawalTypeChoice,TransferCurrencyChoice,ClientTransferRateTypeChoice,StatusChoices



# Create your models here.
class Transfer(models.Model):
    transfer_id = models.CharField(max_length=125, null=False, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    client_data = models.JSONField()
    date = models.DateField(auto_now=True)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=3)
    withdrawal_type = models.CharField(max_length=25, choices=WithdrawalTypeChoice, default=WithdrawalTypeChoice.BANK)
    transfer_currency = models.CharField(max_length=25, choices=TransferCurrencyChoice, default=TransferCurrencyChoice.AED)
    client_transfer_rate_type = models.CharField(max_length=25, choices=ClientTransferRateTypeChoice, default=ClientTransferRateTypeChoice.CURRENCY)
    client_transfer_rate = models.DecimalField(max_digits=10, decimal_places=3)
    client_amount_transfer_rate = models.DecimalField(max_digits=10, decimal_places=3)
    client_recieved_amount = models.DecimalField(max_digits=10, decimal_places=3)
    transfer_amount = models.DecimalField(max_digits=10, decimal_places=3)
    source_company_bank_account = models.ForeignKey(CompanyBankAccount, on_delete=models.CASCADE,related_name='source_comp_bank_account')
    recieved_client_bank_account = models.ForeignKey(ClientBankAccount, on_delete=models.CASCADE)
    recieved_company_bank_account = models.ForeignKey(CompanyBankAccount, on_delete=models.CASCADE,related_name='recieved_comp_bank_account')
    SR_to_AED_conversion_rate = models.DecimalField(max_digits=10, decimal_places=3)
    international_bank_receipt_charge_AED = models.DecimalField(max_digits=10, decimal_places=3)
    international_bank_receipt_charge_SAR = models.DecimalField(max_digits=10, decimal_places=3)
    bank_cash_withdrawal_charge_AED = models.DecimalField(max_digits=10, decimal_places=3)
    bank_cash_withdrawal_charge_SAR = models.DecimalField(max_digits=10, decimal_places=3)
    company_cash_withdrawal_fee_percentage = models.DecimalField(max_digits=10, decimal_places=3)
    company_cash_withdrawal_fee_AED = models.DecimalField(max_digits=10, decimal_places=3)
    company_cash_withdrawal_fee_SAR = models.DecimalField(max_digits=10, decimal_places=3)
    status = models.CharField(max_length=25, choices=StatusChoices, default=StatusChoices.PENDING)
    pending_at = models.DateTimeField(default=now, editable=True)
    deposited_at = models.DateTimeField(default=now, editable=True)
    transferred_at = models.DateTimeField(default=now, editable=True)
    received_at = models.DateTimeField(default=now, editable=True)
    withdrawn_at = models.DateTimeField(default=now, editable=True)
    completed_at = models.DateTimeField(default=now, editable=True)
    is_service_charge_accountable_by_client = models.BooleanField(default=False)
    transfer_profit = models.DecimalField(max_digits=10, decimal_places=3)
    total_company_expense = models.DecimalField(max_digits=10, decimal_places=3)
    net_profit = models.DecimalField(max_digits=10, decimal_places=3)


class Deposit(models.Model):
    bank_deposit_card = models.ForeignKey(ClientBankAccount, on_delete=models.CASCADE)
    company_bank_account = models.ForeignKey(CompanyBankAccount, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    Note = models.TextField(null=True, blank=True)
