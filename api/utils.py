from datetime import datetime, timedelta
from apns import APNs, Frame, Payload
from decouple import config

from api.models import Schedule, Stats, DeviceToken
import api.constants as constants


def calculate_state(date):
    try:
        game = Schedule.objects.get(date=date)
    except Schedule.DoesNotExist:
        return 'none'

    if not game.has_started:
        return 'none'

    if game.has_finished:
        return 'none'

    if is_god_mode(date=date):
        return 'god'

    if is_hot(date=date):
        return 'hot'

    if has_made_three_pointer(date=date):
        return 'shot'

    return 'none'


def is_god_mode(date):
    try:
        points_scored = Stats.objects.filter(
            created_date__range=(date, date + timedelta(days=1)),
            minutes_elapsed__lte=constants.god_mode_minute_threshold
        ).order_by(
            '-created_date'
        )[0].points
    except Stats.DoesNotExist:
        return False
    except IndexError:
        return False
    except KeyError:
        return False

    return points_scored >= constants.god_mode_point_threshold


def is_hot(date):
    return is_current_stat_greater_than_before(
        date=date,
        stat='three_pointers_made',
        stat_threshold=constants.hot_mode_three_pointer_threshold,
        minute_threshold=constants.hot_mode_minute_threshold
    )


def has_made_three_pointer(date):
    return is_current_stat_greater_than_before(
        date=date,
        stat='three_pointers_made',
        stat_threshold=constants.shot_mode_three_pointer_threshold,
        minute_threshold=constants.shot_mode_minute_threshold
    )


def is_current_stat_greater_than_before(date, stat, stat_threshold, minute_threshold):
    try:
        current_stats = Stats.objects.filter(
            created_date__range=(date, date + timedelta(days=1))
        ).order_by(
            '-created_date'
        )[0]
        current_stat = current_stats[stat]
        minutes_elapsed = current_stats['minutes_elapsed']

        prior_stats = Stats.objects.filter(
            created_date__range=(date, date + timedelta(days=1)),
            minutes_elapsed__gte=(minutes_elapsed - minute_threshold)
        ).order_by(
            'created_date'
        )[0]
        prior_stat = prior_stats[stat]
    except Stats.DoesNotExist:
        return False
    except IndexError:
        return False
    except KeyError:
        return False

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
