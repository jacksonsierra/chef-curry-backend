from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import date

from api.models import Schedule, Stats
from api.utils_html import parse_html
from api.utils import calculate_state, send_notification


logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*', hour='12-1')), name="get_stats", ignore_result=True)
def get_stats():
    today = date.today()
    try:
        game = Schedule.objects.get(date=today)
    except Schedule.DoesNotExist:
        return

    current_stats, has_started, has_finished = parse_html(url=game.url)

    if not has_started:
        return

    if has_finished and game.has_finished:
        return

    Stats.objects.create(current_stats)

    new_state = calculate_state(date=today)

    if has_started and not game.has_started:
        Schedule.objects.filter(date=today).update(has_started=has_started)

    if has_finished and not game.has_finished:
        Schedule.objects.filter(date=today).update(has_finished=has_finished)

    if new_state != game.state:
        Schedule.objects.filter(date=today).update(state=new_state)
        send_notification(state=new_state)


