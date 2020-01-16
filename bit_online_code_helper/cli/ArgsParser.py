from bit_online_code_helper.bitonline.BITOnlineManager import *
import argparse


class _ArgsParser:
    def __init__(self):
        self.__parser = argparse.ArgumentParser()
        self.__init_parser()

    def __init_parser(self):
        group = self.__parser.add_mutually_exclusive_group()
        group.add_argument('-l', '--local', help='本地测试', action='store_true')
        group.add_argument('-o', '--online', help='上传乐学测试', action='store_true')
        group.add_argument('-lo', '--local_online', help='本地测试成功后上传乐学测试', action='store_true')

        self.__parser.add_argument('problem_url', help='乐学上题目的地址')
        self.__parser.add_argument('source_file_path', help='源代码文件路径')

    def run(self):
        args = self.__parser.parse_args()

        bit_online_manager.output_helper_baseinfo()
        bit_online_manager.login()

        if args.local:
            bit_online_manager.local_test_code(args.problem_url, args.source_file_path)
        elif args.online:
            bit_online_manager.online_test_code(args.problem_url, args.source_file_path)
        elif args.local_online:
            bit_online_manager.local_and_online_test_code(args.problem_url, args.source_file_path)


args_parser = _ArgsParser()