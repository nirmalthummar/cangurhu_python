import os
from celery import Celery
from celery.schedules import crontab

# this code copied from manage.py
# set the default Django settings module for the 'celery' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cangurhu.settings')

# you change change the name here
app = Celery("cangurhu")

# read config from Django settings, the CELERY namespace would make celery
# config keys has `CELERY` prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# load tasks.py in django apps
app.autodiscover_tasks()
# app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'
#
# app.conf.beat_schedule = {
#     # 'add-every-minute-contrab': {
#     #     'task': 'multiply_two_numbers',
#     #     'schedule': crontab(hour=7, minute=30, day_of_week=1),
#     #     'args': (16, 16),
#     # },
#     'add-every-5-seconds': {
#         'task': 'my_first_task',
#         'schedule': 5.0,
#         'args': (100)
#     },
#     # 'add-every-30-seconds': {
#     #     'task': 'tasks.add',
#     #     'schedule': 30.0,
#     #     'args': (16, 16)
#     # },
# }

# from __future__ import absolute_import

# from celery import Celery
# from django.conf import settings
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE','cangurhu.settings')
# app = Celery('cangurhu')
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
# from celery import shared_task
# from time import sleep
# @shared_task
# def my_first_task():
#     print("I am here")
#     Translator=TranslateData()
#     data = TranslateData.objects.all()
#     print(data)
#     print("done")
#     for i in data:
#         translator = Translator(to_lang="German")
#         translation = translator.translate(i.data)
#         print(i.id)
#         TranslateData.objects.filter(id=i.id).update(translated=translation)
#     # sleep(duration)
#     return('first_task_done')