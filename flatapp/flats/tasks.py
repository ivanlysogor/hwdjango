# Create your tasks here
import time
import yaml
from celery import shared_task
# from celery import task
from celery.utils.log import get_task_logger
from .models import MeterType, Meter, ProviderType, Provider, MeterValues
from mosenergosbyt import Account, Session
from providers import mfc

logger = get_task_logger(__name__)

def extract_param(param_name, string):
    data = yaml.safe_load(string)
    if param_name in data.keys():
        return data[param_name]
    else:
        return ""


def send_mosenergo_values(meter_id, v1, v2, v3):
    logger.info(f"Sending values to Mosenergo")
    meter = Meter.objects.get(pk=meter_id)
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

def send_mfc_values(meter_id, v1):
    logger.info(f"Sending values to MFC for meter with id={meter_id} and value={v1}")
    meter = Meter.objects.get(pk=meter_id)
    username = extract_param('username', meter.metertype_id.provider_id.provider_params)
    password = extract_param('password', meter.metertype_id.provider_id.provider_params)
    fid = extract_param('fid', meter.metertype_id.provider_id.provider_params)
    try:
        logger.info(f"Logging to the MFC with username={username}")
        mfc_session = mfc(login=username, password=password, fid=fid)
        logger.info(f"MFC Object created {mfc_session}")
        authenticated = mfc_session.auth()
        if not authenticated:
            logger.info(f"Unable to login to the portal with username={username}")
            return False
        logger.info(f"MFC session authenticated")
        meter_id = extract_param('meter-id', meter.meter_params)
        logger.info(f"Uploading data for meter with meter-id={meter_id}")
        data_transferred = mfc_session.set_meter_values(counter_id=meter_id, counter_value=v1)
        if not data_transferred:
            logger.info(f"Unable to find meter with meter-id={meter_id}")
            return False
        logger.info(f"Value ({v1}) for meter meter-id={meter_id} uploaded")
        return True
    except SystemExit as e:
        return False
    except BaseException as e:
        logger.info(f"Exception {e}")
        return False

@shared_task(bind=True)
def send_meter_values(self, meter_id, metervalue_id, v1, v2, v3):
    logger.info(f"Initializing meter values transmission for meter with id {meter_id} "
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
    if extract_param('type',
                     meter.metertype_id.provider_id.providertype_id.providertype_params) == 'mfc':
        if send_mfc_values(meter_id, v1):
            metervalue = MeterValues.objects.get(pk=metervalue_id)
            metervalue.mv_synced = True
            metervalue.save()
            logger.info(f"Meter values uploaded to MFC")
            return (True, f"Meter values uploaded to MFC")
        else:
            logger.info(f"Unable to upload meter values to MFC")
            return (False, f"Unable to upload meter values to MFC")
    return (True, f"Meter values uploaded")


@shared_task(name='sync_meter_values')
def sync_meter_values():
    logger.info(f"Syncing meter values")
    meters = Meter.objects.all()
    values_parsed = values_send = values_updated = 0
    for meter in meters:
        logger.info(f"Parsing meter with id={meter.pk} and "
                    f"name={meter.meter_name}")
        meter_value = MeterValues.objects.filter(meter_id=meter).order_by('-mv_date')[0]
        if meter_value:
            values_parsed += 1
            if not meter_value.mv_synced:
                values_send += 1
                logger.info(f"Meter value with id={meter_value.pk} is not synced")
                (result, text) = send_meter_values(meter_id=meter.pk, metervalue_id=meter_value.pk,
                                  v1=meter_value.mv_v1, v2=meter_value.mv_v2,
                                  v3=meter_value.mv_v3)
                if result:
                    values_updated += 1
            else:
                logger.info(f"Meter value with id={meter_value.pk} is synced")
        else:
            logger.info(f"Meter value for meter with id={meter.pk} is not exist")
    return (True, values_parsed, values_send, values_updated)
