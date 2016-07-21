# Django Channels and Celery Example

This project shows how to setup a Django Channels project with a Celery task queue. The user can start a long running background task and get immediate notification when the task completes without a browser refresh.

You can see an example deployment at <http://tasker.vincenttide.com>. Note that this deployment contains some extra stuff not covered in this repository.

To run this project you will need to install Redis as the Channels layer backend and RabbitMQ as the Celery broker.

Then just run:

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver  # Start daphne and workers
celery worker -A example -l info  # Start celery workers
```

## How to Send Reply Back to Browser Client
The code block below shows how to send a reply back to the browser that originated the task request. `reply_channel` contains a unique address in the form of `websocket.send!hjnsMbQPiefT`.
```
Channel(reply_channel).send({
    "text": json.dumps ({
        "action": "completed",
        "task_id": job.id,
        "task_name": job.name,
        "task_status": job.status,
    })
})
```
