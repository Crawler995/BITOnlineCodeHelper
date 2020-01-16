import re
import getpass
from bit_online_code_helper.log.LogManager import *


class _LoginManager:
    def __init__(self):
        self.__login_url = 'https://login.bit.edu.cn/cas/login?service=http%3A%2F%2Fonline.bit.edu.cn%2Fmoodle'
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/77.0.3865.120 Safari/537.36 '
        }
        self.__session = None
        self.__is_login = False

    def set_session(self, session):
        self.__session = session

    def __get_post_data(self, name, page_text):
        regx = re.compile('<input type=\"hidden\" name=\"' + name + '\" value=\"(.+?)\"')
        return regx.findall(page_text)[0]

    def get_is_login(self):
        return self.__is_login

    def login(self):
        if self.__is_login:
            tip(LoginLogs.HAS_LOGIN)
            return

        try:
            login_page = self.__session.get(self.__login_url, headers=self.__headers)
            if '北理在线 - 网络教室' in login_page.text:
                self.__is_login = True
                tip(LoginLogs.HAS_LOGIN)
                return

            tip(LoginLogs.NEED_LOGIN)
            username = input(get_str(LoginLogs.USERNAME))
            password = getpass.getpass(get_str(LoginLogs.PASSWORD))
            tip(LoginLogs.LOGIN_PENDING)

            login_page_text = login_page.text
            data = {
                'username': username,
                'password': password,
                'lt': self.__get_post_data('lt', login_page_text),
                'execution': self.__get_post_data('execution', login_page_text),
                '_eventId': self.__get_post_data('_eventId', login_page_text),
                'rmShown': self.__get_post_data('rmShown', login_page_text),
            }

            bit_online_page = self.__session.post(self.__login_url, data=data, headers=self.__headers)
            if '北理在线 - 网络教室' in bit_online_page.text:
                self.__is_login = True
                tip(LoginLogs.LOGIN_SUCCESS)
            else:
                tip(LoginLogs.LOGIN_FAILED_VIA_USERINFO)

        except:
            tip(LoginLogs.LOGIN_FAILED_VIA_NETWORK)


login_manager = _LoginManager()
