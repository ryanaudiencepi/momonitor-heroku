import subprocess


def call_service_check_cron():
    subprocess.Popen("python manage.py service_check_cron", shell=True)