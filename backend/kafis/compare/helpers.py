import datetime
import redis
import random
from operator import itemgetter
from collections import defaultdict, OrderedDict

from compare.models import Person, Compare
from kafis.settings import BLOCKS_NUMBER

r = redis.Redis('localhost')


def set_table_cache(compare):
    """
    Cache of all People and their scores
    :param compare: Person gender filter (M or F)
    :return: dict(key=person__id, value=score)
    """
    result = defaultdict(float)
    people = Person.objects.filter(gender=compare)

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
    max_step = len(people) // BLOCKS_NUMBER
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
    # To reduce too big steps
    adj_koef = people_count // 1000

    # range between each position in table
    step = people_count // (10 * adj_koef or 10)
    # number of available positions in table
    display = rates_count // step

    items = r.zrevrange(f'table_{compare}', 0, 9, True)

    result = []
    for i, item in enumerate(reversed(items)):
        person_id = item[0]
        score = round(item[1], 3)
        if i <= display:
            # Shown rating row
            person = Person.objects.get(id=person_id)
            row = dict(
                id=person_id,
                link=f'https://vk.com/id{person.vk_id}',
                name=person.name,
                score=score
            )
        elif i == display + 1:
            # Hidden rating row
            hidden_text = f'Выберите {(i - display) * step} чел.'
            row = dict(
                id=person_id,
                link='',
                name=hidden_text,
                score=score
            )
        else:
            # Hidden rating row
            row = dict(
                id=person_id,
                link='',
                name='Скрыто',
                score=score
            )
        result.append(row)

    return reversed(result)


def get_anon_name():
    return f'anon_{datetime.date.today()}'
