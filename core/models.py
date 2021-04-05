from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    GENDERS = [
        ('M', 'Male'),
        ('F', 'Female')
    ]

    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    gender = models.CharField(max_length=1, choices=GENDERS)
    country = CountryField()
    personal_information = models.CharField(max_length=1000)
    birthday = models.DateField()
    social_network_page = models.URLField(max_length=100, null=True, blank=True)
    disliked_users = models.ManyToManyField('User', blank=True)

    REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['first_name', 'last_name', 'gender', 'country',
                                                      'personal_information', 'birthday']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Match(models.Model):
    ACQUAINTANCE_STATES = [
        ('0', 'Not answered'),
        ('1', 'Not liked'),
        ('2', 'Both liked')
    ]

    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_match_requests')
    recipient_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_match_requests')
    acquaintance_state = models.CharField(max_length=1, choices=ACQUAINTANCE_STATES, default='0')

    def __str__(self):
        return f'{self.sender_user} to {self.recipient_user} - {self.get_acquaintance_state_display()}'
