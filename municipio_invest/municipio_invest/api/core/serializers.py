from rest_framework import serializers
from municipio_invest.api.core.models import Municipality

class MunicipalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = "__all__"


class ContractSerializer(serializers.Serializer):
    contract_id = serializers.CharField(max_length=30)
    contracting_party = serializers.CharField()
    contracted = serializers.CharField(max_length=255)
    contract_type = serializers.CharField(max_length=255)
    description = serializers.CharField()
    contract_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    publication_date = serializers.DateField()
    signing_date = serializers.DateField()
