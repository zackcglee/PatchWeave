# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import Logger
import Output
import Common

WLLVM_EXTRACTOR = "extract-bc"
FILE_PARTIAL_DIFF = Common.DIRECTORY_TMP + "/gen-patch"


def execute_command(command, show_output=True):
    # Print executed command and execute it in console
    Output.command(command)
    command = "{ " + command + " ;} 2> " + Common.FILE_ERROR_LOG
    if not show_output:
        command += " > /dev/null"
    # print(command)
    process = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (output, error) = process.communicate()
    # out is the output of the command, and err is the exit value
    return str(process.returncode)


def create_directories():
    if not os.path.isdir(Common.DIRECTORY_LOG):
        os.makedirs(Common.DIRECTORY_LOG)

    if not os.path.isdir(Common.DIRECTORY_OUTPUT_BASE):
        os.makedirs(Common.DIRECTORY_OUTPUT_BASE)

    if not os.path.isdir(Common.DIRECTORY_BACKUP):
        os.makedirs(Common.DIRECTORY_BACKUP)

    if not os.path.isdir(Common.DIRECTORY_TMP):
        os.makedirs(Common.DIRECTORY_TMP)


def error_exit(*args):
    print("\n")
    for i in args:
        Logger.error(i)
        Output.error(i)
    raise Exception("Error. Exiting...")


def find_files(src_path, extension, output):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    # Save paths to all files in src_path with extension extension to output
    find_command = "find " + src_path + " -name '" + extension + "' > " + output
    execute_command(find_command)


def clean_files():
    # Remove other residual files stored in ./output/
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Output.information("Removing other residual files...")
    if os.path.isdir("output"):
        clean_command = "rm -rf " + Common.DIRECTORY_OUTPUT
        execute_command(clean_command)


def get_file_extension_list(src_path, output_file_name):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    extensions = set()
    find_command = "find " + src_path + " -type f -not -name '*\.c' -not -name '*\.h'" + \
        " > " + output_file_name
    execute_command(find_command)
    with open(output_file_name, 'r') as f:
        a = f.readline().strip()
        while(a):
            a = a.split("/")[-1]
            if "." in a:
                extensions.add("*." + a.split(".")[-1])
            else:
                extensions.add(a)
            a = f.readline().strip()
    return extensions


def backup_file(file_path, backup_name):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    backup_command = "cp " + file_path + " " + Common.DIRECTORY_BACKUP + "/" + backup_name
    execute_command(backup_command)


def restore_file(file_path, backup_name):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    restore_command = "cp " + Common.DIRECTORY_BACKUP + "/" + backup_name + " " + file_path
    execute_command(restore_command)


def reset_git(source_directory):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    reset_command = "cd " + source_directory + ";git reset --hard HEAD"
    execute_command(reset_command)


def extract_bitcode(binary_path):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    binary_name = str(binary_path).split("/")[-1]
    binary_directory = "/".join(str(binary_path).split("/")[:-1])
    extract_command = WLLVM_EXTRACTOR + " " + binary_path
    # print(extract_command)
    execute_command(extract_command)
    return binary_directory, binary_name


def show_partial_diff(source_path_a, source_path_b):
    Logger.trace(__name__ + ":" + sys._getframe().f_code.co_name, locals())
    Output.normal("\t\tTransplanted Code:")
    diff_command = "diff -ENZBbwr " + source_path_a + " " + source_path_b + " > " + FILE_PARTIAL_DIFF
    execute_command(diff_command)
    with open(FILE_PARTIAL_DIFF, 'r') as diff_file:
        diff_line = diff_file.readline().strip()
        while diff_line:
            Output.normal("\t\t\t" + diff_line)
            diff_line = diff_file.readline().strip()


def is_intersect(start_a, end_a, start_b, end_b):
    return not (end_b < start_a or start_b > end_a)


def get_file_list(dir_name):
    current_file_list = os.listdir(dir_name)
    full_list = list()
    for entry in current_file_list:
        full_path = os.path.join(dir_name, entry)
        if os.path.isdir(full_path):
            full_list = full_list + get_file_list(full_path)
        else:
            full_list.append(full_path)
    return full_list


def get_code(source_path, line_number):
    if os.path.exists(source_path):
        with open(source_path, 'r') as source_file:
            content = source_file.readlines()
            # print(len(content))
            return content[line_number-1]
    return None
