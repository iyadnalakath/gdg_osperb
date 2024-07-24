from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import LedgerEntry,Ledger
from .choice import EntryTypeChoice

# signals for calculating ledger data
@receiver(post_save, sender=LedgerEntry)
def update_ledger_totals(sender, instance, **kwargs):
    ledger = instance.ledger
    
    # Calculate totals in ledger
    total_credit_AED = LedgerEntry.objects.filter(
        ledger=ledger, entry_type=EntryTypeChoice.CREDIT
    ).aggregate(Sum('amount_AED'))['amount_AED__sum'] or 0
    
    total_credit_SAR = LedgerEntry.objects.filter(
        ledger=ledger, entry_type=EntryTypeChoice.CREDIT
    ).aggregate(Sum('amount_SAR'))['amount_SAR__sum'] or 0
    
    total_debit_AED = LedgerEntry.objects.filter(
        ledger=ledger, entry_type=EntryTypeChoice.DEBIT
    ).aggregate(Sum('amount_AED'))['amount_AED__sum'] or 0
    
    total_debit_SAR = LedgerEntry.objects.filter(
        ledger=ledger, entry_type=EntryTypeChoice.DEBIT
    ).aggregate(Sum('amount_SAR'))['amount_SAR__sum'] or 0
    
    # Update ledger instance
    ledger.total_credit_amount_AED = total_credit_AED
    ledger.total_credit_amount_SAR = total_credit_SAR
    ledger.total_debit_amount_AED = total_debit_AED
    ledger.total_debit_amount_SAR = total_debit_SAR
    ledger.total_balance_amount_AED = total_credit_AED - total_debit_AED
    ledger.total_balance_amount_SAR = total_credit_SAR - total_debit_SAR
    ledger.save()


# signals for calculating ledger_head data
def update_ledger_head_totals(ledger_head):
    total_credit_amount_AED = Ledger.objects.filter(ledger_head=ledger_head).aggregate(Sum('total_credit_amount_AED'))['total_credit_amount_AED__sum'] or 0
    total_credit_amount_SAR = Ledger.objects.filter(ledger_head=ledger_head).aggregate(Sum('total_credit_amount_SAR'))['total_credit_amount_SAR__sum'] or 0
    total_debit_amount_AED = Ledger.objects.filter(ledger_head=ledger_head).aggregate(Sum('total_debit_amount_AED'))['total_debit_amount_AED__sum'] or 0
    total_debit_amount_SAR = Ledger.objects.filter(ledger_head=ledger_head).aggregate(Sum('total_debit_amount_SAR'))['total_debit_amount_SAR__sum'] or 0
    
    ledger_head.total_credit_amount_AED = total_credit_amount_AED
    ledger_head.total_credit_amount_SAR = total_credit_amount_SAR
    ledger_head.total_debit_amount_AED = total_debit_amount_AED
    ledger_head.total_debit_amount_SAR = total_debit_amount_SAR
    ledger_head.total_balance_amount_AED = total_credit_amount_AED - total_debit_amount_AED
    ledger_head.total_balance_amount_SAR = total_credit_amount_SAR - total_debit_amount_SAR
    ledger_head.save()

@receiver(post_save, sender=Ledger)
def ledger_post_save(sender, instance, **kwargs):
    update_ledger_head_totals(instance.ledger_head)