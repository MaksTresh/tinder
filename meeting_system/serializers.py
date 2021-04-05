from rest_framework import serializers


class ReactionDetailSerializer(serializers.Serializer):
    to_user = serializers.IntegerField()


class ReactionCreateSerializer(ReactionDetailSerializer):
    liked = serializers.BooleanField()
