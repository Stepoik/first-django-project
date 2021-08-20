from django_cron import CronJobBase, Schedule
from .models import Session, Game, Players
from datetime import datetime

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'bunker.my_cron_job'    # a unique code

    def do(self):
        for session in Session.objects.all():
            if session.expire_date < datetime.utcnow():
                session.delete()
        for game in Game.objects.all():
            if len(Players.objects.filter(lobby = game.lobby)) == 0:
                game.delete()
        print('crons')