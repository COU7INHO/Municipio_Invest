from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from municipio_invest.api.core.serializers import (
    MunicipalitySerializer,
    ContractSerializer
)
from municipio_invest.api.core.models import (
    Municipality,
    Contract
)
from municipio_invest.api.core.helpers import (
    check_municipality_exists_in_db,
    request_municipality
)
from municipio_invest.api.generic_errors import APIRequestError


class MunicipalityView(GenericAPIView):
    serializer_class = MunicipalitySerializer
    queryset = Municipality.objects.all()

    def get(self, request: Request):
        municipality_name = request.query_params.get("municipality", None)
        
        if not municipality_name:
            return Response(
                {
                    "error": "Municipality name must be provided"
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        municipality_in_db = check_municipality_exists_in_db(
            municipality_name=municipality_name
        )

        if municipality_in_db:
            serializer = self.get_serializer(municipality_in_db)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                municipality_request = request_municipality(
                    municipality_name=municipality_name
                )
            except APIRequestError:
                return Response(
                    {
                        "error": "Failed to get a valid API response"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

            if municipality_request:
                serializer = self.get_serializer(municipality_request)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {
                        "error": "No data found"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )


class MunicipalitiesView(GenericAPIView):
    """
    View to manage multiple municipalities
    """
    serializer_class = MunicipalitySerializer
    queryset = Municipality.objects.all()

    def get(self, request: Request):        
        """
        Method to return all available municipalities with pagination
        """
        page_size = request.query_params.get("page_size", 20)
        paginator = PageNumberPagination()
        paginator.page_size = page_size

        paginated_contracts = paginator.paginate_queryset(self.get_queryset(), request)
        serializer = self.get_serializer(paginated_contracts, many=True)
        return paginator.get_paginated_response(serializer.data)


class ContractsView(GenericAPIView):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()

    def get(self, request: Request):
        municipality_id = request.query_params.get("municipality_id", None)
        if not municipality_id:
            return Response(
                {"error": "Municipality id must be provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            municipality = Municipality.objects.get(_id=municipality_id)
        except Municipality.DoesNotExist:
            return Response(
                {"error": "Failed to find municipality"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Fazer o raise da resposta errada da api
        #request_contracts(municipality_id=int(municipality_id))
        contracts = Contract.objects.filter(contracting_party=municipality).order_by("-signing_date")
        
        page_size = request.query_params.get("page_size", 10)
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        paginated_contracts = paginator.paginate_queryset(contracts, request)

        serializer = self.serializer_class(paginated_contracts, many=True)
        return paginator.get_paginated_response(serializer.data)