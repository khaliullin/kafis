import hashlib
import os

from django.core.files import File
from django.core.management.base import BaseCommand

from compare.models import Person


class Command(BaseCommand):
    help = """
    Fills person database with data from files in directory.
    Usage: ./manage.py load_people -p /path/to/faces/directory
    Image name format: FirstName_LastName_{vk_id}_{M|F}.jpg
    """

    def handle(self, *args, **options):
        dirname = options['path']
        if not dirname.endswith('/'):
            dirname += '/'

        for file in os.listdir(dirname):
            # skip hidden or system files
            if file.startswith('.'):
                continue

            data = file.split('_')
            name = ' '.join(data[:2])
            vk_id = str(data[2])
            gender = str(data[3]).split(".")[0]
            person = Person(
                name=name,
                gender=gender,
                vk_id=vk_id,
            )
            # load image
            reopen = open(f'{dirname}{file}', 'rb')
            django_file = File(reopen)
            new_filename = hashlib.sha1(vk_id.encode()).hexdigest() + '.jpg'
            person.photo.save(new_filename, django_file, save=True)

            print(file)

    def add_arguments(self, parser):
        parser.add_argument(
            '-p',
            '--path',
            action='store',
            default='',
            help='Path to images folder'
        )
