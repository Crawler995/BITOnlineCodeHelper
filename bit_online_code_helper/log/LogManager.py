from enum import Enum


class HelperBaseInfoLogs(Enum):
    NAME = 'BIT Online Code Helper'
    AUTHOR = 'Developed by Zhang'


class LoginLogs(Enum):
    HAS_LOGIN = '你已登录！'
    NEED_LOGIN = '你需要登录你的账号！'
    USERNAME = '学号：'
    PASSWORD = '密码（密码输入时不会显示，放心输入）: '
    LOGIN_PENDING = '登录中……'
    LOGIN_SUCCESS = '登录成功！'
    LOGIN_FAILED_VIA_USERINFO = '登录失败！请检查你的账号信息。'
    LOGIN_FAILED_VIA_NETWORK = '登录失败！请检查网络。'


class ProblemLogs(Enum):
    PROBLEM_GET_PENDING = '获取题目基本信息中……'
    GET_PROBLEM_INFO_FAILED = '获取问题基本信息失败，请重试！'


class LocalTestCodeLogs(Enum):
    SOURCE_FILE_NOT_FOUND = '源文件未找到！请检查文件路径。'
    COMPILE_PENDING = '源文件编译中……'
    COMPILE_SUCCESS = '编译成功！'
    COMPILE_FAILED = '编译失败！'
    LOCAL_TEST_BEGIN = '开始本地测试……'
    TEST_SUCCESS = '本地测试通过！'
    TEST_FAILURE_CASE = '本地测试未通过！未通过用例：'


class OnlineTestCodeLogs(Enum):
    COMMIT_START = '提交乐学中……'
    DEADLINE_PASS = '截止时间已过，你不能再提交程序了。'
    COMMIT_SUCCESS = '提交成功！正在等待测试结果。'
    COMMIT_FAILED = '提交失败，请重试！'
    COMPILE_FAILED = '乐学编译失败！'
    TEST_SUCCESS = '乐学测试完全正确！'
    TEST_FAILED = '乐学测试未完全通过！'


def divide_line():
    print('-----------------------------------------')


def tip(log):
    print(log.value)


def get_str(log):
    return log.value
