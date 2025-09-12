import csv
import datetime
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from ...models import Deal

class Command(BaseCommand):
    help = "Backup Deal data"

    def handle(self, *args, **options):
        date = datetime.date.today().strftime("%Y%m%d")
        file_path = settings.BACKUP_PATH + 'deal_' + date + '.csv'
        os.makedirs(settings.BACKUP_PATH, exist_ok=True)

        with open(file_path, 'w') as file:
            writer = csv.writer(file)

            header = [field.name for field in Deal._meta.fields]
            writer.writerow(header)

            deals = Deal.objects.all()

            for deal in deals:
                writer.writerow([str(deal.user),
                                 str(deal.deal_type),
                                 str(deal.amount),
                                 deal.content,
                                 str(deal.updated_at)])
                
            files = os.listdir(settings.BACKUP_PATH)
            if len(files) >= settings.NUM_SAVED_BACKUP:
                files.sort()
                os.remove(settings.BACKUP_PATH + files[0])