import json
import logging
from channels import Channel
from channels.sessions import channel_session
from .models import Job
from .tasks import sec3
from example.celery import app

log = logging.getLogger(__name__)


@channel_session
def ws_receive(message):
    try:
        data = json.loads(message['text'])
    except ValueError:
        log.debug("ws message isn't json text=%s", message['text'])
        return

    if data:
        reply_channel = message.reply_channel.name

        if data['action'] == "start_sec3":
            start_sec3(data, reply_channel)


def start_sec3(data, reply_channel):
    log.debug("Task Name=%s", data['task_name'])
    # Save model to our database
    task = Job(
        name=data['task_name'],
        status="started",
    )
    task.save()

    # Start long running task here (using Celery)
    sec3_task = sec3.delay(task.id, reply_channel)

    # Store the celery task id into the database if we wanted to
    # do things like cancel the task in the future
    task.celery_id = sec3_task.id
    task.save()

    # Tell client task has been started
    Channel(reply_channel).send({
        "text": json.dumps({
            # Tell client task is in progress
            "action": "started",
            "task_id": task.id,
            "task_name": task.name,
            "task_status": task.status,
        })
    })