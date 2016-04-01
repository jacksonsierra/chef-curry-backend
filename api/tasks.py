from celery.decorators import periodic_task
from celery.task.schedules import crontab
from celery.utils.log import get_task_logger
from datetime import date

from api.models import Game, Stats
from api.utils_html import parse_html
from api.utils import calculate_state, send_notification


logger = get_task_logger(__name__)


@periodic_task(run_every=(crontab(minute='*', hour='12-1')), name="get_stats", ignore_result=True)
def get_stats():
    today = date.today()
    try:
        game = Game.objects.get(date=today)
    except Game.DoesNotExist:
        return

    current_stats, has_started, has_finished = parse_html(url=game.url)

    if not has_started:
        return

    if has_finished and game.has_finished:
        return

    if current_stats:
        current_stats['game'] = game
        Stats.objects.create(**current_stats)

    new_state = calculate_state(game=game)

    if has_started and not game.has_started:
        Game.objects.filter(id=game.id).update(has_started=has_started)

    if has_finished and not game.has_finished:
        Game.objects.filter(id=game.id).update(has_finished=has_finished)

    if new_state != game.state:
        Game.objects.filter(id=game.id).update(state=new_state)
        send_notification(state=new_state)


