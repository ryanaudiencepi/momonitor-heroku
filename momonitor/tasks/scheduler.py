import schedule
import time
from job import run_service_check_cron


schedule.every().minute.do(run_service_check_cron)


while True:
    schedule.run_pending()
    time.sleep(1)