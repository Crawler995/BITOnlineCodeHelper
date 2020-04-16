import re
import time
from bit_online_code_helper.log.LogManager import *


class _Problem:
    title = ''
    deadline = None
    test_cases_and_results = []


class _ProblemManager:
    def __init__(self):
        self.__headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/77.0.3865.120 Safari/537.36 '
        }
        self.__session = None

    def set_session(self, session):
        self.__session = session

    def __get_problem_title(self, page_text):
        title_regx = re.compile('</ul><h2>(.+?)</h2><div class=\"box time-table\">')
        return title_regx.findall(page_text)[0]

    def __get_problem_deadline(self, page_text):
        deadline_regx = re.compile('<tr class=\"lastrow\">[\\s\\S]+?<td class=\"cell c3 lastcol\" style=\"\">(.+?)</td>')
        deadline_str = deadline_regx.findall(page_text)[0]
        weekday_regx = re.compile('星期.')
        deadline_str = weekday_regx.sub('', deadline_str)

        return time.strptime(deadline_str, '%Y年%m月%d日  %H:%M')

    def __get_problem_test_cases(self, page_text):
        res = []

        test_case_and_result_regx = re.compile('<a class=\"showasplaintext small\" href=\"(.+?)\"')
        test_cases_and_results_regx_res = test_case_and_result_regx.findall(page_text)

        test_case_num = int(len(test_cases_and_results_regx_res) / 2)
        for i in range(test_case_num):
            test_case_and_result = {}

            test_case_url = test_cases_and_results_regx_res[i * 2].replace('amp;', '')
            result_url = test_cases_and_results_regx_res[i * 2 + 1].replace('amp;', '')

            test_case_and_result['test_case'] = self.__session.get(test_case_url, headers=self.__headers).text
            test_case_and_result['result'] = self.__session.get(result_url, headers=self.__headers).text
            if test_case_and_result['result'][-2:] != '\r\n':
                test_case_and_result['result'] += '\r\n'

            res.append(test_case_and_result)

        return res

    def get_problem_info(self, problem_url):
        tip(ProblemLogs.PROBLEM_GET_PENDING)
        try:
            problem_page_text = self.__session.get(problem_url, headers=self.__headers).text

            problem = _Problem()
            problem.title = self.__get_problem_title(problem_page_text)
            problem.deadline = self.__get_problem_deadline(problem_page_text)
            problem.test_cases_and_results = self.__get_problem_test_cases(problem_page_text)

            info_output(problem.title)
            divide_line()

            return problem

        except:
            tip(ProblemLogs.GET_PROBLEM_INFO_FAILED)


problem_manager = _ProblemManager()
