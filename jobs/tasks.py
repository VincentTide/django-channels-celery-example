from __future__ import absolute_import
import time
import json
import logging

from example.celery import app
from .models import Job
from channels import Channel


log = logging.getLogger(__name__)

@app.task
def sec3(task_id, reply_channel):
    # time sleep represent some long running process
    time.sleep(3)
    # Change task status to completed
    task = Job.objects.get(pk=task_id)
    log.debug("Running task_name=%s", task.name)
    # If status is cancelled, suppress the reply update to client
    if task.status == "cancelled":
        return
    else:
        task.status = "completed"
        task.save()
        # Send status update back to browser client
        if reply_channel is not None:
            Channel(reply_channel).send({
                "text": json.dumps ({
                    "action": "completed",
                    "task_id": task.id,
                    "task_name": task.name,
                    "task_status": task.status,
                })
            })
