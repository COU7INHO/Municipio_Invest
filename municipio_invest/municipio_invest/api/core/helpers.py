import requests
from datetime import datetime
from fake_useragent import UserAgent
from municipio_invest.api.core.models import Municipality, Contract
from municipio_invest.api.generic_errors import APIRequestError
from decimal import Decimal


def check_municipality_exists_in_db(municipality_name:str):
    get_municipality = Municipality.objects.filter(name__iexact=municipality_name)
    if get_municipality.exists():
        municipality = get_municipality.first()
        result = {
            "name": municipality.name,
            "_id": municipality._id,
        }
        return result
    
def request_municipality(municipality_name:str, page:int = 0, size:int = 25):

    if page < 0:
        raise ValueError("Page number cannot be negative")
    if size <= 0:
        raise ValueError("Size must be greater than 0")
    
    municipality_name = municipality_name.lower()
    ua = UserAgent() # create a fake user agent
    user_agent = ua.random

    url = "https://www.base.gov.pt/Base4/pt/resultados"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "text/plain, */*; q=0.01",
        "Origin": "https://www.base.gov.pt",
        "User-Agent": user_agent,
    }

    payload = {
        "type": "search_entidades",
        "version": "108.0",
        "query": f"texto={municipality_name}",
        "sort": "+description",
        "page": 0,
        "size": 25,
    }

    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        data = response.json()

        if data.get("items"):
            item = data["items"][0] # The first element could be another company
            municipality = item.get("description")
            id_ = item.get("id")

            _ = Municipality.objects.create(
                name=municipality,
                _id= id_
            )   
            result = {
                "name": municipality,
                "_id": id_,
            }

            return result
        else:
            return None
    else:
        raise APIRequestError(response.status_code, response.text)


def request_contracts(municipality_id: int, size: int = 25):
    if not (isinstance(municipality_id, int) and municipality_id > 0):
        raise ValueError("Invalid municipality id")

    ua = UserAgent()  # Create a fake user agent
    user_agent = ua.random

    url = "https://www.base.gov.pt/Base4/pt/resultados/"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "User-Agent": user_agent,
        "X-Requested-With": "XMLHttpRequest",
    }

    page = 0  # Start from the first page
    while True:
        payload = {
            "type": "search_contratos",
            "version": "108.0",
            "query": f"adjudicanteid={municipality_id}",
            "sort": "-publicationDate",
            "page": page,
            "size": size,
        }

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code != 200:
            break

        contracts = response.json()
        contracts_data = contracts.get("items", [])
        
        if not contracts_data:  # Break if no data is returned (end of pagination)
            break

        municipality = Municipality.objects.get(_id=municipality_id)

        # Create a list of contract instances to be bulk inserted
        contract_instances = []
        existing_contract_ids = set(Contract.objects.filter(contracting_party=municipality).values_list('contract_id', flat=True))

        for item in contracts_data:
            contract_id = item.get("id")

            if contract_id in existing_contract_ids:
                continue  # Skip if contract_id already exists in the database

            contract_price = format_price(item.get("initialContractualPrice"))
            publication_date = format_date(item.get("publicationDate"))
            signing_date = format_date(item.get("signingDate"))

            # Skip if either price or date is invalid (None or empty)
            if contract_price is None or publication_date is None or signing_date is None:
                continue  # Skip this contract and move to the next one

            # If valid, create contract instance and append to list
            contract_instance = Contract(
                contract_id=contract_id,
                contracting_party=municipality,
                contracted=item.get("contracted"),
                contract_type=item.get("contractingProcedureType"),
                description=item.get("objectBriefDescription"),
                contract_price=contract_price,
                publication_date=publication_date,
                signing_date=signing_date,
            )

            contract_instances.append(contract_instance)

        # If there are contracts to insert, perform bulk_create
        if contract_instances:
            Contract.objects.bulk_create(contract_instances)

        page += 1  # Move to the next page

def format_date(date_str):
    return datetime.strptime(date_str, "%d-%m-%Y").strftime("%Y-%m-%d")

def format_price(price_str):
    # Remove the currency symbol and any spaces
    price_str = price_str.replace(" €", "").replace(" ", "")
    
    # Replace the thousands separator (period) with an empty string
    price_str = price_str.replace(".", "")
    
    # Replace the decimal separator (comma) with a period
    price_str = price_str.replace(",", ".")
    
    # Convert to Decimal
    price = Decimal(price_str)
    
    # Round to two decimal places
    return price.quantize(Decimal('0.01'))  # Rounds to 2 decimal places

