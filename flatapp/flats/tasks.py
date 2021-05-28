# Create your tasks here
from celery import shared_task
import time


@shared_task
def send_meter_values(meter_id, v1, v2, v3):
    with open('values.txt', 'w', encoding='utf-8') as f:
            f.write(f"Sending meter {meter_id} values ({v1},{v2},{v3})\n")
    return True
