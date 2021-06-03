# Create your tasks here
import time
import yaml
from celery import shared_task
from celery.utils.log import get_task_logger
from .models import MeterType, Meter, ProviderType, Provider, MeterValues
from mosenergosbyt import Account, Session

logger = get_task_logger(__name__)

def extract_param(param_name, string):
    data = yaml.safe_load(string)
    if param_name in data.keys():
        return data[param_name]
    else:
        return ""

def send_mosenergo_values(meter_id, v1, v2, v3):
    logger.info(f"Sending values to Mosenergo")
    meter =  Meter.objects.get(pk=meter_id)
    username = extract_param('username', meter.metertype_id.provider_id.provider_params)
    password = extract_param('password', meter.metertype_id.provider_id.provider_params)
    try:
        logger.info(f"Logging to the API with username={username}")
        ms_acc = Account(Session(login=username, password=password))
        if not ms_acc:
            logger.info(f"Unable to login to the portal with username={username}")
            return False
        ms_acc.get_info(with_measure=True, indications=True, balance=True)
        ms_meter_id = extract_param('meter-id', meter.meter_params)
        logger.info(f"Finding meter with meter-id={ms_meter_id}")
        ms_meter = ms_acc.meter_list.get(ms_meter_id)
        if not meter:
            logger.info(f"Unable to find meter with meter-id={ms_meter_id}")
            return False
        ms_meter.upload_measure(v1, v2, v3)
        logger.info(f"Values ({v1},{v2},{v3}) for meter meter-id={ms_meter_id} uploaded")
        return True
    except SystemExit as e:
        return False
    except BaseException as e:
        logger.info(f"Exception {e}")
        return False

@shared_task(bind=True)
def send_meter_values(self, meter_id, metervalue_id, v1, v2, v3):
    logger.info(f"Initializing meter values transmission for meter with id {meter_id}"
                f"values {v1}, {v2}, {v3}")

    meter =  Meter.objects.get(pk=meter_id)
    logger.info(f"Provider type "
                f"{meter.metertype_id.provider_id.providertype_id.providertype_name}")
    if extract_param('type',
                     meter.metertype_id.provider_id.providertype_id.providertype_params) == 'mosenergo':
        if send_mosenergo_values(meter_id, v1, v2, v3):
            metervalue = MeterValues.objects.get(pk=metervalue_id)
            metervalue.mv_synced = True
            metervalue.save()
            logger.info(f"Meter values uploaded to Mosenergosbyt")
            return (True, f"Meter values uploaded to Mosenergosbyt")
        else:
            logger.info(f"Unable to upload meter values to Mosenergosbyt")
            return (False, f"Unable to upload meter values to Mosenergosbyt")
    return (True, f"Meter values uploaded")

@shared_task
def add(a,b):
    return a + b
