from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from .models import Deposit
from accounts.models import LedgerEntry
from accounts.choice import EntryTypeChoice

@receiver(post_save, sender=Deposit)
def create_or_update_ledger_entries(sender, instance, created, **kwargs):
    LedgerEntry.objects.update_or_create(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id,
        particulars=f"Deposit for {instance.client.name}",
        defaults={
            'date': now(),
            'ledger': instance.client.ledger,
            'entry_type': EntryTypeChoice.CREDIT,
            'amount_AED': 0,
            'amount_SAR': instance.amount,
            'conversion_rate': 1,
            'remarks': instance.note,
            'created_at': now()
        }
    )

    LedgerEntry.objects.update_or_create(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id,
        particulars=f"Deposit from {instance.client.name} to Company Bank Account",
        defaults={
            'date': now(),
            'ledger': instance.company_bank_account.ledger,
            'entry_type': EntryTypeChoice.CREDIT,
            'amount_AED': 0,
            'amount_SAR': instance.amount,
            'conversion_rate': 1,
            'remarks': instance.note,
            'created_at': now()
        }
    )

@receiver(post_delete, sender=Deposit)
def delete_ledger_entries(sender, instance, **kwargs):
    LedgerEntry.objects.filter(
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id
    ).delete()


# signals.py
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

