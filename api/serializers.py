from rest_framework import serializers
from api.models import Tier, User, RequestType, Request, RequestImage

class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tier
        fields = ['id', 'rank', 'name', 'color']

class UserSerializer(serializers.ModelSerializer):
    tier = TierSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'created', 'last_updated', 'username', 'email', 'phone', 'hash', 'tier']

class UserRequestSerializer(serializers.ModelSerializer):
    tier = TierSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'created', 'last_updated', 'username', 'email', 'phone', 'tier']

class RequestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestType
        fields = ['id', 'type', 'color', "identification_number"]

class RequestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestImage
        fields = ['id', 'added', 'image']

class RequestSerializer(serializers.ModelSerializer):
    user = UserRequestSerializer(read_only=True)
    type = RequestTypeSerializer(read_only=True)
    images = RequestImageSerializer(read_only=True, many=True)

    class Meta:
        model = Request
        fields = ['id', 'created', 'last_updated', 'user', 'title', 'description', 'type', 'images', 'email_contact', 'phone_contact']