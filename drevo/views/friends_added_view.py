import datetime

from django.shortcuts import render

from ..models import FriendsTerm
from ..models import FriendsInviteTerm
from users.models import Profile, User


def friends_added_view(request):
    """
    Контрол страницы "Добавить в друзья"
    """
    context = {'profiles': []}
    first_name_predicate = request.GET.get('first')
    last_name_predicate = request.GET.get('last')

    # Добавление в друзья
    if request.GET.get('add'):
        _add_friend(request.user.id, request.GET.get('add'))

    """
    Исключить:
    - самого себя
    - тех, кто уже друг
    - кто висит в заявках и ожидает подтверждения на дружбу
    """
    array_invite = []
    invite_friend = FriendsInviteTerm.objects.filter(sender_id=request.user.id)
    for one in invite_friend:
        array_invite.append(one.recipient_id)

    exist_friends = FriendsTerm.objects.filter(user_id=request.user.id).first()

    exclude_ids = [request.user.id] + array_invite
    if exist_friends:
        exclude_ids.append(exist_friends.friend_id)
    profiles = Profile.objects.exclude(id__in=exclude_ids)
    for profile in profiles:
        data = {}
        if first_name_predicate and not last_name_predicate:
            user = User.objects.filter(id=profile.user_id, first_name__contains=first_name_predicate).first()
        elif not first_name_predicate and last_name_predicate:
            user = User.objects.filter(id=profile.user_id, last_name__contains=last_name_predicate).first()
        elif first_name_predicate and last_name_predicate:
            user = User.objects.filter(id=profile.user_id, first_name__contains=first_name_predicate,
                                       last_name__contains=last_name_predicate).first()
        else:
            user = User.objects.filter(id=profile.user_id).first()
        if not user:
            continue
        if not user.first_name or not user.last_name:
            continue
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['avatar'] = profile.avatar or ''
        data['user_id'] = profile.user_id
        context['profiles'].append(data)

    template_name = 'drevo/friends_added.html'
    return render(request, template_name, context)


def _add_friend(user_id: int, friend_id: str) -> None:
    """
    Отправить заявку на дружбу
    """
    FriendsInviteTerm.objects.create(
        sender_id=user_id,
        recipient_id=int(friend_id),
        date_added=datetime.datetime.now(),
        accept=False
    )
