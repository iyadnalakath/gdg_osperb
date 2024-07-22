from django.db import models
from companies.models import CompanyBankAccount,Country
from accounts.models import Ledger

# Create your models here.


class Client(models.Model):
    name = models.CharField(max_length=125, null=False, blank=False)
    email = models.EmailField(verbose_name="email", max_length=60)
    # country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='client_country')
    country_code = models.CharField(max_length=25, null=False, blank=False)
    phone = models.DecimalField(max_digits=10, decimal_places=0)
    address = models.TextField(null=True, blank=True)
    transfer_rate_aed = models.DecimalField(max_digits=10, decimal_places=3)
    transfer_rate_usd = models.DecimalField(max_digits=10, decimal_places=3)
    amount_transfer_rate_aed = models.DecimalField(max_digits=10, decimal_places=3)
    amount_transfer_rate_usd = models.DecimalField(max_digits=10, decimal_places=3)
    is_service_charge_accountable = models.BooleanField(default=False)
    ledger_balance = models.DecimalField(max_digits=25, decimal_places=3)
    # ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    total_transfer_amount = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
    total_client_recieved_aed_amount = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
    total_client_recieved_usd_amount = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)

    def __str__(self):
        return self.name
    

class ClientBankAccount(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    account_holder_name = models.CharField(max_length=125, null=False, blank=False)
    account_number = models.DecimalField(max_digits=25, decimal_places=0)
    bank_name = models.CharField(max_length=125, null=True, blank=True)
    bank_address = models.CharField(max_length=125, null=True, blank=True)
    branch_name = models.CharField(max_length=125, null=True, blank=True)
    ifsc = models.TextField(null=True, blank=True)
    iban_number = models.CharField(max_length=125, null=True, blank=True)
    # country = models.ForeignKey(Country, on_delete=models.CASCADE)
    bic_or_swift_code = models.CharField(max_length=125, null=True, blank=True)
    
    def __str__(self):
        return self.account_holder_name
    
class BankDepositCard(models.Model):
    card_number = models.CharField(max_length=125, null=False, blank=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    # company_bank_account = models.ForeignKey(CompanyBankAccount, on_delete=models.CASCADE)
    title = models.CharField(max_length=125, null=True, blank=True)
    Note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.account_holder_name

    def __str__(self):
        return self.title
    