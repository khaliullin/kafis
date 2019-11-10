import redis
import random
from collections import defaultdict, OrderedDict

from compare.models import Person, Compare

r = redis.Redis('localhost')


def set_table_cache(compare):
    """
    Cache of all People and their scores
    :param compare: Person gender filter (M, F of A)
    :return: dict(key=person__id, value=score)
    """
    result = defaultdict(float)
    people = Person.objects.all()
    if compare != 'A':
        people = people.filter(gender=compare)

    for person in people:
        selected = Compare.objects.filter(selected=person).count()
        if selected > 0:
            total = selected + Compare.objects.filter(
                not_selected=person).count()
            score = selected / total
        else:
            score = 0

        result[person.id] = score
    result = OrderedDict(result)

    r.hmset(f'table_{compare}', result)

    return result


def get_random_pair(compare):
    people = r.hkeys(f'table_{compare}')
    if not people:
        table = set_table_cache(compare)
        people = list(table.keys())

    # Max possible distance between person1 and person2 from table
    max_step = len(people) // 4
    if max_step == 0:
        return None, None

    step = random.randint(1, max_step)
    first_position = random.randint(0, len(people) - step - 1)
    second_position = first_position + step

    person1 = Person.objects.filter(
        id=people[first_position]
    ).get()
    person2 = Person.objects.filter(
        id=people[second_position]
    ).get()

    return person1, person2
