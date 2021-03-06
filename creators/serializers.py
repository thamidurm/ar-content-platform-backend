from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Creator

class SubCreatorSerializer(DocumentSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = Creator
        fields = ['id']
        read_only_fields = ['id']

class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_('Email'))
    password = serializers.CharField(label=_('Password'), style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password= attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            
            if user:
                pass
                # if not user.is_active:
                #   msg = _('User account is inactive')
                #   raise serializers.ValidationError(msg)
            else:
                msg = _('Invalid credentials')
                raise serializers.ValidationError(msg)
        else:
                msg = _('Empty credentials')
                raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs

class ShallowCreatorSerializer(DocumentSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Creator
        fields = ['id', 'name']

class UserSerializer(DocumentSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Creator
        fields = '__all__'  

        extra_kwargs = {
            'password': {
                'write_only': True,
            },
            'email': {
                'write_only': True
            }
        }
