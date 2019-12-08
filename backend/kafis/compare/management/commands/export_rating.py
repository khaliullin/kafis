import json

import redis

from django.core.management.base import BaseCommand

from compare.models import Person
from kafis.settings import BASE_DIR


class Command(BaseCommand):
    help = "Export rating to json file (backend/kafis/rating_export.json)"

    def handle(self, *args, **options):
        r = redis.Redis('localhost')
        result = {'M': dict(), 'F': dict()}
        for gender in ('M', 'F'):
            people = r.zrevrange(f'table_{gender}', 0, -1, True)

            i = 0
            total = len(people)
            print(f'Exporting {gender}. Total count: {total}')

            for person_id, score in people:
                person = Person.objects.filter(id=person_id).first()
                if not person:
                    continue
                photo_name = str(person.photo).split('/')[1]
                result[gender][photo_name] = score

                i += 1
                if i % 100 == 0:
                    print(f'{i}/{total}')

        with open(BASE_DIR + '/rating_export.json', 'w') as f:
            json.dump(result, f)
