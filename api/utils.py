from apns import APNs, Payload
from decouple import config
import os

from api.models import Stats, DeviceToken
import api.constants as constants


def calculate_state(game):
    if not game:
        return 'none'

    if not game.has_started:
        return 'none'

    if game.has_finished:
        return 'none'

    if is_god_mode(game_id=game.id):
        return 'god'

    if is_hot(game_id=game.id):
        return 'hot'

    if has_made_three_pointer(game_id=game.id):
        return 'shot'

    return 'none'


def is_god_mode(game_id):
    try:
        points_scored = Stats.objects.filter(
            game_id=game_id,
            minutes_elapsed__lte=constants.god_mode_minute_threshold
        ).order_by(
            '-created_date'
        )[0].points
    except:
        return False

    return points_scored >= constants.god_mode_point_threshold


def is_hot(game_id):
    return is_current_stat_greater_than_before(
        game_id=game_id,
        stat='three_pointers_made',
        stat_threshold=constants.hot_mode_three_pointer_threshold,
        minute_threshold=constants.hot_mode_minute_threshold
    )


def has_made_three_pointer(game_id):
    return is_current_stat_greater_than_before(
        game_id=game_id,
        stat='three_pointers_made',
        stat_threshold=constants.shot_mode_three_pointer_threshold,
        minute_threshold=constants.shot_mode_minute_threshold
    )


def is_current_stat_greater_than_before(game_id, stat, stat_threshold, minute_threshold):
    try:
        current_stats = Stats.objects.filter(
            game_id=game_id
        ).order_by(
            '-created_date'
        )[0]
        current_stat = getattr(current_stats, stat)
        minutes_elapsed = getattr(current_stats, 'minutes_elapsed')
    except:
        return False

    try:
        prior_stats = Stats.objects.filter(
            game_id=game_id,
            minutes_elapsed__gte=(minutes_elapsed - minute_threshold)
        ).order_by(
            'created_date'
        )[0]
        prior_stat = getattr(prior_stats, stat)
    except:
        prior_stat = 0

    return (current_stat - stat_threshold) >= prior_stat


def send_notification(state):
    device_tokens = DeviceToken.objects.values_list('token', flat=True)
    payload = get_payload(state)

    cert = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config('CERT_PEM'))
    key = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), config('KEY_PEM'))

    apns = APNs(use_sandbox=True, cert_file=cert, key_file=key)

    for token in device_tokens:
        apns.gateway_server.send_notification(token, payload)


def get_payload(state):
    if state == 'god' or state == 'hot':
        return Payload(alert=constants.APNs_messages[state], custom={'type': state})

    return Payload(custom={'type': state})
