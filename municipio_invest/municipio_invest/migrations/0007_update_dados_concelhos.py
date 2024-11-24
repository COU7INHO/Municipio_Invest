from django.db import migrations

def populate_municipality_relations(apps, schema_editor):
    # Get the models
    Municipality = apps.get_model('municipio_invest', 'Municipality')
    District = apps.get_model('municipio_invest', 'District')
    NUTSIII = apps.get_model('municipio_invest', 'NUTSIII')

    # Mapping of municipality names to their district and NUTS III IDs
    municipality_data = {
        "Município de Baião": {"district": "Porto", "nuts_III": "Tâmega e Sousa"},
        "Município de Penafiel": {"district": "Porto", "nuts_III": "Tâmega e Sousa"},
        "Município de Amarante": {"district": "Porto", "nuts_III": "Tâmega e Sousa"},
        "Município de Paços de Ferreira": {"district": "Porto", "nuts_III": "Tâmega e Sousa"},
        "Município de Marco de Canaveses": {"district": "Porto", "nuts_III": "Tâmega e Sousa"},
        "Município de Lousada": {"district": "Porto", "nuts_III": "Tâmega e Sousa"},
        "Município de Cinfães": {"district": "Viseu", "nuts_III": "Tâmega e Sousa"},
        "Município de Castelo de Paiva": {"district": "Aveiro", "nuts_III": "Tâmega e Sousa"},
        "Município de Celorico de Basto": {"district": "Braga", "nuts_III": "Tâmega e Sousa"},
        "Câmara Municipal de Resende": {"district": "Viseu", "nuts_III": "Tâmega e Sousa"},
        "Câmara Municipal de Felgueiras": {"district": "Porto", "nuts_III": "Tâmega e Sousa"},
    }

    # Update municipalities with the corresponding district and NUTS III foreign keys
    for municipality_name, relations in municipality_data.items():
        try:
            municipality = Municipality.objects.get(name=municipality_name)
            district = District.objects.get(name=relations["district"])
            nuts_iii = NUTSIII.objects.get(name=relations["nuts_III"])
            
            municipality.district = district
            municipality.nuts_III = nuts_iii
            municipality.save()
        except (Municipality.DoesNotExist, District.DoesNotExist, NUTSIII.DoesNotExist) as e:
            print(f"Error updating {municipality_name}: {e}")

class Migration(migrations.Migration):

    dependencies = [
        ('municipio_invest', '0006_municipality_district_municipality_nuts_iii'),
    ]

    operations = [
        migrations.RunPython(populate_municipality_relations),
    ]
