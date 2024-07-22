from django.db import models



class AccountTypeChoice(models.TextChoices):
  ASSET = 'asset', 'Asset'
  LIABILITY = 'liability', 'Liability'

class EntryTypeChoice(models.TextChoices):
  DEBIT = 'debit', 'Debit'
  CREDIT = 'credit', 'Credit'