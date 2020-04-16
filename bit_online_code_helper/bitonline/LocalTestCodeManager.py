import subprocess
import os
import time

from bit_online_code_helper.log.LogManager import *
from tqdm import tqdm


class _LocalTestCodeManager:
    def __remove_existed_exe(self):
        if os.path.exists('a.exe'):
            os.remove('a.exe')

    def __compile_source_file(self, source_file_path):
        self.__remove_existed_exe()

        if not os.path.exists(source_file_path):
            tip(LocalTestCodeLogs.SOURCE_FILE_NOT_FOUND_FAILED)
            return False

        tip(LocalTestCodeLogs.COMPILE_PENDING)
        compile_process = subprocess.Popen(['g++', source_file_path, '-std=c++11'], shell=True, stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = compile_process.communicate()
        compile_process.terminate()

        if len(err.decode()) != 0:
            tip(LocalTestCodeLogs.COMPILE_FAILED)
            return False
        else:
            tip(LocalTestCodeLogs.COMPILE_SUCCESS)
            divide_line()
            return True

    def __local_test_code(self, problem_info):
        is_pass = True

        tip(LocalTestCodeLogs.LOCAL_TEST_BEGIN)

        index = 1
        test_failed_case_index = []
        your_wrong_output = []
        pbar = tqdm(total=len(problem_info.test_cases_and_results),
                    unit='cases')

        for test_case in problem_info.test_cases_and_results:
            test_process = subprocess.Popen(['a.exe'], shell=True, stdin=subprocess.PIPE,
                                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = test_process.communicate(test_case['test_case'].encode())

            is_case_pass = out.decode() == test_case['result']
            if not is_case_pass:
                test_failed_case_index.append(index)
                your_wrong_output.append(out.decode())
                is_pass = False

            index += 1
            pbar.update(1)
            test_process.terminate()

        pbar.close()
        time.sleep(1)

        if is_pass:
            tip(LocalTestCodeLogs.TEST_SUCCESS)
            divide_line()
        else:
            tip(LocalTestCodeLogs.TEST_FAILED_CASE)
            for index in test_failed_case_index:
                print('第%d个用例：' % index)
                print('输入：')
                print(problem_info.test_cases_and_results[index - 1]['test_case'], end='')
                print('期望输出：')
                print(problem_info.test_cases_and_results[index - 1]['result'], end='')
                print('你的输出：')
                print(your_wrong_output[index - 1])
                divide_line()

        return is_pass

    def run(self, source_file_path, problem_info):
        if self.__compile_source_file(source_file_path):
            return self.__local_test_code(problem_info)
        return False


local_test_code_manager = _LocalTestCodeManager()
