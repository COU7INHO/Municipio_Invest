from django.core.management.base import BaseCommand
from municipio_invest.api.core.models import Municipality
from municipio_invest.api.core.helpers import request_contracts


class Command(BaseCommand):
    help = 'Fetch contracts for each municipality and save them to the database'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting to fetch contracts for all municipalities..."))

        municipalities = Municipality.objects.all()  # Get all municipalities from the database
        
        for municipality in municipalities:
            self.stdout.write(self.style.SUCCESS(f'Fetching contracts for municipality: {municipality._id}'))

            try:
                request_contracts(municipality_id=municipality._id)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching contracts for municipality {municipality._id}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("Finished fetching contracts for all municipalities"))
