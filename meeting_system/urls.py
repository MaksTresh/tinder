from django.urls import path, include

from .views import MatchCreateDetail, UserToMatchDetail, FamiliarUsers

urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.urls')),
    path('match/<int:recipient_user_id>/', MatchCreateDetail.as_view()),
    path('user-to-match/', UserToMatchDetail.as_view()),
    path('familiar-users/', FamiliarUsers.as_view())
]
