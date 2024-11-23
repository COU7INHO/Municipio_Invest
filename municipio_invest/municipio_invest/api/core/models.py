from django.db import models


class Municipality(models.Model):
    name = models.CharField(max_length=200, unique=True)
    _id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Contract(models.Model):
    contract_id = models.CharField(max_length=20, unique=True)
    contracting_party = models.ForeignKey(Municipality, on_delete=models.CASCADE)
    contracted = models.CharField(max_length=255)
    contract_type = models.CharField(max_length=255)
    description = models.TextField()
    contract_price = models.DecimalField(max_digits=10, decimal_places=2)
    publication_date = models.DateField()
    signing_date = models.DateField()

    def __str__(self):
        return str(self.contracting_party) + " - " + self.description

