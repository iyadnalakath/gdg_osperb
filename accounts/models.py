from django.db import models
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .choice import AccountTypeChoice,EntryTypeChoice


# Create your models here.


class LedgerHead(models.Model):
    account_head = models.CharField(max_length=25, choices=AccountTypeChoice, default=AccountTypeChoice.ASSET)
    title = models.CharField(max_length=125, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    total_credit_amount_AED = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    total_credit_amount_SAR = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    total_debit_amount_AED = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    total_debit_amount_SAR = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    total_balance_amount_AED = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    total_balance_amount_SAR = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    is_default = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now, editable=True)


    def __str__(self):
        return self.title
    

class Ledger(models.Model):
    ledger_head = models.ForeignKey(LedgerHead, on_delete=models.CASCADE,related_name='ledger_head')
    title = models.CharField(max_length=125, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    total_credit_amount_AED = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    total_credit_amount_SAR = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    total_debit_amount_AED = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    total_debit_amount_SAR = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    total_balance_amount_AED = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    total_balance_amount_SAR = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    opening_balance = models.DecimalField(max_digits=15, decimal_places=3, default=0)
    is_default = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=now, editable=True)


    def __str__(self):
        return self.title
    



class LedgerEntry(models.Model):
    date = models.DateField(auto_now=True)
    particulars = models.CharField(max_length=125, null=False, blank=False)
    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE)
    entry_type = models.CharField(max_length=25, choices=EntryTypeChoice, default=EntryTypeChoice.CREDIT)
    amount_AED = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    amount_SAR = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    conversion_rate = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=now, editable=True)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id') 
    
    def __str__(self):
        return self.particulars



class Contra(models.Model):
    date = models.DateField(auto_now_add=True)
    particulars = models.CharField(max_length=125, null=False, blank=False)
    from_ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE,related_name='from_ledger_contra')
    to_ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE,related_name='to_ledger_contra')
    amount_AED = models.DecimalField(max_digits=25, decimal_places=3)
    amount_SAR = models.DecimalField(max_digits=25, decimal_places=3)
    conversion_rate = models.DecimalField(max_digits=10, decimal_places=2)
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.particulars
    
