from operator import itemgetter

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
    result = OrderedDict(
        sorted(result.items(), key=itemgetter(1), reverse=True)
    )

    r.zadd(f'table_{compare}', result)

    return result


def get_random_pair(compare):
    people = r.zrevrange(f'table_{compare}', 0, -1)
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


def get_rating_table(compare, rates_count):
    people_count = Person.objects.count()
    # range between each position in table
    step = people_count // 10
    # number of available positions in table
    display = rates_count // step

    items = r.zrevrange(f'table_{compare}', 0, 10, True)

    result = []
    for i, item in enumerate(reversed(items)):
        person_id = item[0]
        score = round(item[1], 3)
        if i <= display:
            person = Person.objects.get(id=person_id)
            row = dict(
                id=person_id,
                link=f'https://vk.com/id{person.vk_id}',
                name=person.name,
                score=score
            )
        else:
            row = dict(
                id=person_id,
                link='',
                name='Скрыто',
                score=score
            )
        result.append(row)

    return reversed(result)
