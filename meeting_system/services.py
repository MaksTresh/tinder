from django.db.models import Q
from typing import Union

from core.models import User, Match


def react_to_user(sender_user: User, recipient_user: User, liked: bool) -> Union[Match, None]:
    try:
        reverse_match = Match.objects.get(sender_user=recipient_user, recipient_user=sender_user)
    except Match.DoesNotExist:
        reverse_match = None

    if reverse_match:
        if liked:
            reverse_match.acquaintance_state = '2'
        else:
            reverse_match.acquaintance_state = '1'
        reverse_match.save()
        return reverse_match

    if liked:
        return Match.objects.get_or_create(sender_user=sender_user, recipient_user=recipient_user)[0]
    else:
        sender_user.disliked_users.add(recipient_user)

    return None


def get_match(sender_user: User, recipient_user: User) -> Union[Match, None]:
    match = Match.objects.filter(sender_user=sender_user).filter(recipient_user=recipient_user).first()
    return match


def get_unvisited_user(current_user: User) -> Union[User, None]:
    user_to_match = User.objects.exclude(pk=current_user.pk) \
        .exclude(pk__in=current_user.disliked_users.all()) \
        .exclude(received_match_requests__sender_user=current_user) \
        .exclude(Q(sent_match_requests__recipient_user=current_user) &
                 ~Q(sent_match_requests__acquaintance_state='0')).first()

    return user_to_match


def get_familiar_users(current_user: User) -> Union[User, None]:
    familiar_users = User.objects.filter((Q(sent_match_requests__recipient_user=current_user) &
                         Q(sent_match_requests__acquaintance_state='2')) |
                        (Q(received_match_requests__sender_user=current_user) &
                         Q(received_match_requests__acquaintance_state='2')))

    return familiar_users
