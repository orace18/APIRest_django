""" import schedule
import time 
from datetime import datetime, timedelta
from models import Performance, ModelsTenue

def collecter_statistiques():
    # Placez ici la logique pour collecter les statistiques.
    # Vous pouvez effectuer des requêtes sur vos modèles pour calculer les données nécessaires.
    # Par exemple :
    date_fin_mois = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    date_debut_mois = date_fin_mois - timedelta(days=1)
    tenues_confectionnees = ModelsTenue.objects.filter(date_creation__range=(date_debut_mois, date_fin_mois)).count()
    argent_genere = ModelsTenue.objects.filter(date_creation__range=(date_debut_mois, date_fin_mois)).aggregate(Sum('prix'))['prix__sum']

    # Enregistrez les statistiques dans le modèle Performance
    performance = Performance.objects.create(
        mois_annee=date_fin_mois,
        tenues_confectionnees=tenues_confectionnees,
        argent_genere=argent_genere,
    )

# Planifiez l'exécution du script à la fin de chaque mois
schedule.every().day.at("23:59").do(collecter_statistiques)

while True:
    schedule.run_pending()
    time.sleep(1)
 """