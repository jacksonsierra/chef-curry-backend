

from api.models import Schedule, Stats


def calculate_state(date):
    try:
        s = Schedule.objects.get(date=date)
        has_game_started = s.started
        has_game_finished = s.finished
    except Schedule.DoesNotExist:
        return 'none'
    except KeyError:
        return 'none'

    if not has_game_started:
        return 'none'

    if has_game_finished:
        return 'none'

    if is_god_mode(date=date):
        return 'god'

    if is_hot(date=date):
        return 'hot'

    if has_made_three_pointer(date=date):
        return 'shot'

    return 'none'


def is_god_mode(date):
    # filter Stats on created_date being date, and minutes_elapsed <= minute threshold in constants.py
    # order by created_date and take max record
    # return if points > point threshold in constants.py


def is_hot(date):
    # filter Stats on created_date being date
    # order by created_date and take max record

    # find min created_date record within 5 minutes of max minutes elapsed
    # compare if three_pointers_made from max - 2 >= three_pointers_made from min


def has_made_three_pointer(date):
    # filter Stats on created_date being date
    # order by created_date and take max two records

    # compare if three_pointers_made from max - 1 >= three_pointers_made from min