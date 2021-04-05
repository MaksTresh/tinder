from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics

from .services import react_to_user, get_match, get_unvisited_user, get_familiar_users
from core.models import User
from core.serializers import MatchSerializer, UserMatchSerializer, UserSerializer


class MatchCreateDetail(APIView):
    def post(self, request, recipient_user_id):
        liked = request.data.get('liked')
        if liked is not None:
            recipient_user = get_object_or_404(User, pk=recipient_user_id)
            match = react_to_user(sender_user=request.user, recipient_user=recipient_user, liked=liked)
            if not match:
                return Response({'detail': 'Success!'}, status=status.HTTP_200_OK)
            else:
                return Response(MatchSerializer(match).data, status=status.HTTP_201_CREATED)

        return Response({"liked": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, recipient_user_id):
        recipient_user = get_object_or_404(User, pk=recipient_user_id)
        match = get_match(sender_user=request.user, recipient_user=recipient_user)
        if not match:
            raise Http404

        return Response(MatchSerializer(match).data, status.HTTP_200_OK)


class UserToMatchDetail(APIView):
    def get(self, request):
        user_to_match = get_unvisited_user(request.user)
        if not user_to_match:
            raise Http404

        user_serializer = UserMatchSerializer(user_to_match)
        return Response(user_serializer.data, status.HTTP_200_OK)


class FamiliarUsers(mixins.ListModelMixin, generics.GenericAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_familiar_users(self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
