from requests import Session
from celery.utils.log import get_task_logger


class mfc():
    def __init__(self, login, password, fid, *args, **kwargs):
        self.login = login
        self.password = password
        self.fid = fid
        self.authenticated = 0
        self.session = Session()
        self.logger = get_task_logger(__name__)

    def auth(self):
        try:
            self.logger.info(f'MFC trying to authenticate with username={self.login}')
            request = self.session.post('https://oplata.ooo/response.php?chp=regform_smp&act=login',
                      data={'login': self.login,
                            'password': self.password})
            if request.text == "1":
                self.authenticated = 1
                self.logger.info(f'MFC user authentication sucessfull with login={self.login}')
                return True
            else:
                self.logger.info(f'MFC user authentication invalid with login={self.login}')
                return False
        except BaseException as e:
            self.logger.warning(f'Exception during authentication with login={self.login}')
            raise e

    def set_meter_values(self, counter_id, counter_value):
        if self.authenticated:
            try:
                request = self.session.post(f'https://oplata.ooo/response.php?chp=account&act=enter&aid={self.fid}',
                                    data={'fid': self.fid,
                                          f'{counter_id}':  counter_value})
                if request.status_code == 200:
                    self.logger.info(f'Meter values stored')
                    return True
                else:
                    self.logger.info(f'Meter values transmission failed')
                    return False
            except BaseException as e:
                self.logger.warning(f'Exception meter values transmission')
                raise e
        else:
            self.logger.warning("User is not authenticated")
            return False
