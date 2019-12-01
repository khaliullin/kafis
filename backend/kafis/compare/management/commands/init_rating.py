from django.core.management.base import BaseCommand

from compare.models import Person, Compare


class Command(BaseCommand):
    help = """
    Set rating for every Person 0.5
    """

    def handle(self, *args, **options):
        people = Person.objects.all()
        for person in people:
            Compare.objects.create(
                not_selected=person
            )
