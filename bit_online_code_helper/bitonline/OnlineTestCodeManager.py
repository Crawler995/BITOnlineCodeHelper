import re
import time
from bit_online_code_helper.log.LogManager import *


class _CompileStatus(Enum):
    PENDING = '正等待编译'
    COMPILE_ERROR = '程序编译失败'
    COMPILE_SUCCESS = '程序已处理完毕'


class _OnlineTestCodeManager:
    def __init__(self):
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/77.0.3865.120 Safari/537.36 '
        }
        self.__session = None

    def set_session(self, session):
        self.__session = session

    def __get_post_data(self, name, page_text):
        regx = re.compile('<input[\\s\\S]+?name=\"' + name + '\"[\\s\\S]+?value=\"(.+?)\"')
        return regx.findall(page_text)[0]

    def run(self, source_file_path, problem_url):
        if self.__commit_online(source_file_path, problem_url):
            self.__is_commit_pass(problem_url)

    def __commit_online(self, source_file_path, problem_url):
        tip(OnlineTestCodeLogs.COMMIT_START)

        commit_page_url = problem_url.replace('view', 'submit')
        data_item = ['sesskey', '_qf__submit_form', 'sourcefile', 'submitbutton']
        data = {}

        try:
            commit_page_text = self.__session.get(commit_page_url, headers=self.__headers).text

            if '时间已到' in commit_page_text:
                tip(OnlineTestCodeLogs.DEADLINE_PASS)
                return False

            for item in data_item:
                data[item] = self.__get_post_data(item, commit_page_text)

            data['id'] = re.compile('php\\?id=(\\d+)').findall(commit_page_url)[0]
            data['code'] = open(source_file_path, 'rb').read().decode()
            data['language'] = '1'

            commit_url = 'http://online.bit.edu.cn/moodle/mod/programming/submit.php'
            self.__session.post(commit_url, data=data, headers=self.__headers)
            tip(OnlineTestCodeLogs.COMMIT_SUCCESS)
            divide_line()

            return True

        except:
            tip(OnlineTestCodeLogs.COMPILE_FAILED)
            return False

    def __get_compile_status(self, test_res_page_text):
        if _CompileStatus.PENDING.value in test_res_page_text:
            return _CompileStatus.PENDING
        elif _CompileStatus.COMPILE_ERROR.value in test_res_page_text:
            return _CompileStatus.COMPILE_ERROR
        elif _CompileStatus.COMPILE_SUCCESS.value in test_res_page_text:
            return _CompileStatus.COMPILE_SUCCESS

    def __is_commit_pass(self, problem_url):
        test_res_url = problem_url.replace('view', 'result')
        test_res_page_text = ''

        while True:
            test_res_page_text = self.__session.get(test_res_url, headers=self.__headers).text
            compile_status = self.__get_compile_status(test_res_page_text)
            if compile_status == _CompileStatus.COMPILE_ERROR:
                tip(OnlineTestCodeLogs.COMPILE_FAILED)
                return False
            elif compile_status == _CompileStatus.COMPILE_SUCCESS:
                break
            else:
                time.sleep(1)
                continue

        total_test_case_num, \
        test_case_pass_num, \
        test_case_fail_num = self.__parse_test_res_baseinfo(test_res_page_text)

        if total_test_case_num == test_case_pass_num:
            tip(OnlineTestCodeLogs.TEST_SUCCESS)
        else:
            tip(OnlineTestCodeLogs.TEST_FAILED)
            print('通过%d个用例，失败%d个用例。' % (test_case_pass_num, test_case_fail_num))

    def __parse_test_res_baseinfo(self, test_res_page_text):
        test_res_baseinfo_regx = re.compile('测试结果：共 (\\d+?) 个测试用例，'
                                            '您的程序通过了其中的 (\\d+?) 个，未能通过的有 (\\d+?) 个')
        regx_res = test_res_baseinfo_regx.findall(test_res_page_text)

        total_test_case_num = int(regx_res[0][0])
        test_case_pass_num = int(regx_res[0][1])
        test_case_fail_num = int(regx_res[0][2])

        return total_test_case_num, test_case_pass_num, test_case_fail_num


commit_online_manager = _OnlineTestCodeManager()
