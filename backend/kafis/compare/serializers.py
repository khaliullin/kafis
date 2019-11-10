from rest_framework import serializers

from compare.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'photo', 'name')
