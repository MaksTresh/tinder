from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django_countries.serializers import CountryFieldMixin
from django_countries.serializer_fields import CountryField

from .models import User, Match


class UserMatchSerializer(serializers.ModelSerializer, CountryFieldMixin):
    gender = serializers.CharField(source='get_gender_display')
    country = CountryField(name_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'gender', 'country', 'personal_information', 'birthday']


class UserSerializer(UserCreateSerializer, UserMatchSerializer):
    class Meta(UserMatchSerializer.Meta):
        fields = ['email', 'social_network_page'] + UserMatchSerializer.Meta.fields[1:]


class UserRegisterSerializer(UserSerializer):
    gender = None
    country = None

    class Meta(UserSerializer.Meta):
        fields = ['username',  'password'] + UserSerializer.Meta.fields


class MatchSerializer(serializers.ModelSerializer):
    sender_user = UserMatchSerializer()
    recipient_user = UserMatchSerializer()
    acquaintance_state = serializers.CharField(source='get_acquaintance_state_display')

    class Meta:
        model = Match
        exclude = ['id']
