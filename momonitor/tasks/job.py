from rq import Queue
from worker import conn
from call_commands import call_service_check_cron

def run_service_check_cron():
    q = Queue(connection=conn)
    result = q.enqueue(call_service_check_cron)