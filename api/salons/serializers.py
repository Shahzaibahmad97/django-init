from rest_framework import serializers

from api.users.models import SalonProfile, Stylist


class ReturnShortSalonProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalonProfile
        fields = ('id', 'salon_name', 'contact_name', )


class ReturnStylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stylist
        fields = ('id', 'fullname', )


class StylistSerializer(serializers.ModelSerializer):
    salon = serializers.IntegerField(required=False)

    class Meta:
        model = Stylist
        fields = '__all__'
