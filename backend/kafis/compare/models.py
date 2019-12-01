from django.db import models


GENDER_MALE = 'M'
GENDER_FEMALE = 'F'
GENDER_CHOICES = (
    (GENDER_MALE, 'Male'),
    (GENDER_FEMALE, 'Female'),
)


class Person(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    vk_id = models.CharField(max_length=12, unique=True)
    photo = models.ImageField(upload_to='faces/')

    def __str__(self):
        return f'{self.name} ({self.gender})'


class Expert(models.Model):
    session_id = models.CharField(max_length=128, default='')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)

    def __str__(self):
        return f'{self.gender}_{self.session_id[:5]}'


class Compare(models.Model):
    expert = models.ForeignKey(Expert, null=True, on_delete=models.CASCADE)
    selected = models.ForeignKey(Person, related_name='selected', null=True,
                                 on_delete=models.CASCADE)
    not_selected = models.ForeignKey(Person, related_name='not_selected',
                                     on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.selected} - {self.not_selected} ({self.expert})'


class Report(models.Model):
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    reason = models.CharField(max_length=150)

    def __str__(self):
        return f'{self.person} ({self.reason[:30]})'
