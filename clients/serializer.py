from rest_framework import serializers
from .models import BankDepositCard,ClientBankAccount,Client
from accounts.models import Ledger,LedgerHead

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [

            "id",
            "name",
            "email",
            "country_code",
            "phone",
            "address",
            "transfer_rate_aed",
            "transfer_rate_usd",
            "amount_transfer_rate_aed",
            "amount_transfer_rate_usd",
            "is_service_charge_accountable",
            "ledger_balance",
            "total_transfer_amount",
            "total_client_recieved_aed_amount",
            "total_client_recieved_usd_amount",
            "ledger"

            ]
        
    def create(self, validated_data):
        if 'ledger' not in validated_data or validated_data['ledger'] is None:
            ledger_head = LedgerHead.objects.get(pk=2)
            ledger = Ledger.objects.create(
                ledger_head=ledger_head,
                title=validated_data['name'],
                is_default=True
            )
            validated_data['ledger'] = ledger
        return super(ClientSerializer, self).create(validated_data)
    
class ClientListSerializer(serializers.Serializer):
    clients_count = serializers.IntegerField()
    clients = ClientSerializer(many=True)


class ClientBankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientBankAccount
        fields = [

            "id",
            "client",
            "account_holder_name",
            "account_number",
            "bank_name",
            "bank_address",
            "branch_name",
            "ifsc",
            "iban_number",
            "bic_or_swift_code"
            
            ]



class BankDepositCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDepositCard
        fields = [

            "id",
            "card_number",
            "client",
            # "company_bank_account",
            "title",
            "Note",

            ]
