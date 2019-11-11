from rest_framework import viewsets
from rest_framework.response import Response

from compare.helpers import set_table_cache, get_random_pair, get_rating_table
from compare.models import Person, Expert, Compare
from compare.serializers import PersonSerializer


class PersonView(viewsets.ReadOnlyModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()


class StartViewSet(viewsets.ViewSet):
    def list(self, request):
        data = {}
        if request.session.session_key:
            data['first'] = False
        else:
            data['first'] = True
        return Response(data=data)

    def create(self, request):
        if not request.session.session_key:
            request.session.save()
            Expert.objects.create(
                session_id=request.session.session_key,
                gender=request.data.get('gender')
            )
        else:
            print('hey there')
        person1, person2 = get_random_pair(request.data.get('compare'))
        person1 = PersonSerializer(person1, context={"request": request})
        person2 = PersonSerializer(person2, context={"request": request})

        response = {
            'person1': person1.data,
            'person2': person2.data}

        print('SESSION: ' + request.session.session_key)

        return Response(data=response)


class RateViewSet(viewsets.ViewSet):
    def create(self, request):
        print('SESSION: ' + request.session.session_key)
        if not request.session.session_key:
            return Response()
        expert = Expert.objects.get(session_id=request.session.session_key)
        selected = request.data.get('selected')
        not_selected = request.data.get('not_selected')
        Compare.objects.create(
            expert=expert,
            selected_id=selected,
            not_selected_id=not_selected
        )

        person1, person2 = get_random_pair(request.data.get('compare'))
        person1 = PersonSerializer(person1, context={"request": request})
        person2 = PersonSerializer(person2, context={"request": request})

        response = {
            'person1': person1.data,
            'person2': person2.data}

        return Response(data=response)


class RatingViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk):
        if not request.session.session_key:
            request.session.save()
            return Response()

        expert = Expert.objects.get(session_id=request.session.session_key)
        rates_count = Compare.objects.filter(expert=expert).count()

        table = get_rating_table(pk, rates_count)
        return Response(data=table)

