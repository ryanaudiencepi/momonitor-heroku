web: python manage.py run_gunicorn -b 0.0.0.0:\$PORT -w 1 -k gevent --max-requests 250 --preload
worker: python momonitor/tasks/worker.py
clock: python momonitor/tasks/scheduler.py