from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from .models import LedgerEntry,Ledger,Contra
from .choice import EntryTypeChoice

#<<<<<<< signals for calculating ledger data >>>>>>>>>

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

# <<<<<<< SIGNALS FOR CONTRA >>>>>>>>>
# <<<<<<< create and update signals for contra >>>>>>>
@receiver(post_save, sender=Contra)
def create_or_update_ledger_entries(sender, instance, created, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)

    # Create or update LedgerEntry for from_ledger
    LedgerEntry.objects.update_or_create(
        content_type=content_type,
        object_id=instance.id,
        ledger=instance.from_ledger,
        defaults={
            'particulars': f"Transfer to {instance.to_ledger.title}",
            'entry_type': EntryTypeChoice.DEBIT,
            'amount_AED': instance.amount_AED,
            'amount_SAR': instance.amount_SAR,
            'conversion_rate': instance.conversion_rate,
            'remarks': instance.remarks,
        }
    )

    # Create or update LedgerEntry for to_ledger
    LedgerEntry.objects.update_or_create(
        content_type=content_type,
        object_id=instance.id,
        ledger=instance.to_ledger,
        defaults={
            'particulars': f"Transfer from {instance.from_ledger.title}",
            'entry_type': EntryTypeChoice.CREDIT,
            'amount_AED': instance.amount_AED,
            'amount_SAR': instance.amount_SAR,
            'conversion_rate': instance.conversion_rate,
            'remarks': instance.remarks,
        }
    )

# <<<<<<< delete signal for contra >>>>>
@receiver(pre_delete, sender=Contra)
def delete_ledger_entries(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(instance)

    # Delete LedgerEntry for from_ledger
    LedgerEntry.objects.filter(
        content_type=content_type,
        object_id=instance.id,
        ledger=instance.from_ledger,
    ).delete()

    # Delete LedgerEntry for to_ledger
    LedgerEntry.objects.filter(
        content_type=content_type,
        object_id=instance.id,
        ledger=instance.to_ledger,
    ).delete()




# @receiver(post_save, sender=LedgerEntry)
# def update_deposit_from_ledger_entry(sender, instance, **kwargs):
#     if instance.deposit:
#         deposit = instance.deposit
        
#         # Example: Recalculate the total amount from all related ledger entries
#         deposit.amount = LedgerEntry.objects.filter(deposit=deposit).aggregate(Sum('amount_SAR'))['amount_SAR__sum'] or 0
#         deposit.note = instance.remarks  # Or another appropriate update mechanism
#         deposit.save()

#         # Update the corresponding ledger entry (company bank account or client)
#         if "Deposit for" in instance.particulars:
#             LedgerEntry.objects.filter(
#                 deposit=deposit,
#                 particulars=f"Deposit from {deposit.client.name} to Company Bank Account"
#             ).update(
#                 date=instance.date,
#                 ledger=deposit.company_bank_account.ledger,
#                 entry_type=EntryTypeChoice.CREDIT,
#                 amount_AED=instance.amount_AED,
#                 amount_SAR=instance.amount_SAR,
#                 conversion_rate=instance.conversion_rate,
#                 remarks=instance.remarks,
#                 created_at=instance.created_at
#             )
#         else:
#             LedgerEntry.objects.filter(
#                 deposit=deposit,
#                 particulars=f"Deposit for {deposit.client.name}"
#             ).update(
#                 date=instance.date,
#                 ledger=deposit.client.ledger,
#                 entry_type=EntryTypeChoice.CREDIT,
#                 amount_AED=instance.amount_AED,
#                 amount_SAR=instance.amount_SAR,
#                 conversion_rate=instance.conversion_rate,
#                 remarks=instance.remarks,
#                 created_at=instance.created_at
#             )

# @receiver(post_delete, sender=LedgerEntry)
# def handle_ledger_entry_delete(sender, instance, **kwargs):
#     if instance.deposit:
#         deposit = instance.deposit
        
#         # Update the deposit based on remaining ledger entries
#         remaining_entries = LedgerEntry.objects.filter(deposit=deposit)
#         if remaining_entries.exists():
#             deposit.amount = remaining_entries.aggregate(Sum('amount_SAR'))['amount_SAR__sum'] or 0
#             deposit.note = remaining_entries.first().remarks  # Or another appropriate update mechanism
#             deposit.save()
#         else:
#             # If no remaining ledger entries, you may want to delete the deposit or handle it accordingly
#             deposit.delete()

