import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Tags


class Command(BaseCommand):
    help = 'Загрузка и тегов в базу данных'

    def handle(self, *args, **kwargs):
        with open(
            f'{settings.CSV_FILES_DIR}/tags.csv', encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            next(reader)
            tags = [
                Tags(
                    name=row[0],
                    color=row[1],
                    slug=row[2]
                )
                for row in reader
            ]
            Tags.objects.bulk_create(tags)
        self.stdout.write(self.style.SUCCESS('=== Теги успешно загружены ==='))
