from django.db import models



class WithdrawalTypeChoice(models.TextChoices):
  BANK = 'bank', 'Bank'
  CASH = 'cash', 'Cash'

class TransferCurrencyChoice(models.TextChoices):
    AED = 'aed', 'Aed'
    USD = 'usd', 'Usd'

class ClientTransferRateTypeChoice(models.TextChoices):
   CURRENCY = 'currency', 'Currency'
   AMOUNT = 'amount', 'Amount'

class StatusChoices(models.TextChoices):
    PENDING = 'pending', 'Pending'
    DEPOSITED = 'deposited', 'Deposited'
    TRANSFERRED = 'transfered', 'Transfered'
    RECEIVED = 'received', 'Received'
    WITHDRAWN = 'withdrawn', 'Withdrawn'
    COMPLETED = 'completed', 'Completed'
