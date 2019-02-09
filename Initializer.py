#! /usr/bin/env python3
# -*- coding: utf-8 -*-



import os
import sys
from Utilities import execute_command, error_exit
import Project
import Common
import Output
import Logger
from Builder import build_normal


def load_standard_list():
    with open(Common.FILE_STANDARD_FUNCTION_LIST, "r") as list_file:
        Common.STANDARD_FUNCTION_LIST = [line[:-1] for line in list_file]
    with open(Common.FILE_STANDARD_MACRO_LIST, "r") as list_file:
        Common.STANDARD_MACRO_LIST = [line[:-1] for line in list_file]


def set_env_value():
    Output.normal("setting environment values")
    os.environ["PYTHONPATH"] = "/home/rshariffdeen/workspace/z3/build/python"
    execute_command("export PYTHONPATH=/home/rshariffdeen/workspace/z3/build/python")


def load_values():
    Common.Project_A = Project.Project(Common.VALUE_PATH_A, "Pa", Common.VALUE_EXPLOIT_A)
    Common.Project_B = Project.Project(Common.VALUE_PATH_B, "Pb")
    Common.Project_C = Project.Project(Common.VALUE_PATH_C, "Pc", Common.VALUE_EXPLOIT_C)
    Common.Project_D = Project.Project(Common.VALUE_PATH_C + "-patch", "Pd")
    load_standard_list()


def create_patch_dir():
    patch_dir = Common.VALUE_PATH_C + "-patch"
    if not os.path.isdir(patch_dir):
        create_command = "cp -rf " + Common.VALUE_PATH_C + " " + Common.VALUE_PATH_C + "-patch"
        execute_command(create_command)


def read_conf():
    Output.normal("reading configuration values")
    print(sys.argv)
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if Common.ARG_DEBUG in arg:
                Common.DEBUG = True
            elif Common.ARG_NO_BUILD in arg:
                Common.NO_BUILD = True
            elif Common.ARG_CONF_FILE in arg:
                Common.FILE_CONFIGURATION = str(arg).replace(Common.ARG_CONF_FILE, '')
            elif Common.ARG_NO_SYM_TRACE_GEN in arg:
                Common.NO_SYM_TRACE_GEN = True
            elif "PatchWeave.py" in arg:
                continue
            else:
                Output.error("Invalid argument: " + arg)
                Output.help()
                exit()
    else:
        Output.help()
        exit()

    if not os.path.exists(Common.FILE_CONFIGURATION):
        Output.error("[NOT FOUND] Configuration file " + Common.FILE_CONFIGURATION)
        exit()

    with open(Common.FILE_CONFIGURATION, 'r') as conf_file:
        configuration_list = [i.strip() for i in conf_file.readlines()]

    for configuration in configuration_list:
        if Common.CONF_EXPLOIT_A in configuration:
            Common.VALUE_EXPLOIT_A = configuration.replace(Common.CONF_EXPLOIT_A, '')
        elif Common.CONF_EXPLOIT_C in configuration:
            Common.VALUE_EXPLOIT_C = configuration.replace(Common.CONF_EXPLOIT_C, '')
        elif Common.CONF_PATH_POC in configuration:
            Common.VALUE_PATH_POC = configuration.replace(Common.CONF_PATH_POC, '')
        elif Common.CONF_PATH_A in configuration:
            Common.VALUE_PATH_A = configuration.replace(Common.CONF_PATH_A, '')
        elif Common.CONF_PATH_B in configuration:
            Common.VALUE_PATH_B = configuration.replace(Common.CONF_PATH_B, '')
        elif Common.CONF_PATH_C in configuration:
            Common.VALUE_PATH_C = configuration.replace(Common.CONF_PATH_C, '')
        elif Common.CONF_EXPLOIT_PREPARE in configuration:
            Common.VALUE_EXPLOIT_PREPARE = configuration.replace(Common.CONF_EXPLOIT_PREPARE, '')
        elif Common.CONF_FLAGS_A in configuration:
            Common.VALUE_BUILD_FLAGS_A = configuration.replace(Common.CONF_FLAGS_A, '')
        elif Common.CONF_FLAGS_C in configuration:
            Common.VALUE_BUILD_FLAGS_C = configuration.replace(Common.CONF_FLAGS_C, '')
        elif Common.CONF_BUILD_COMMAND_A in configuration:
            Common.VALUE_BUILD_COMMAND_A = configuration.replace(Common.CONF_BUILD_COMMAND_A, '')
        elif Common.CONF_BUILD_COMMAND_C in configuration:
            Common.VALUE_BUILD_COMMAND_C = configuration.replace(Common.CONF_BUILD_COMMAND_C, '')


def initialize():
    Output.title("Initializing project for Transplantation")
    Output.sub_title("loading configuration")
    read_conf()
    create_patch_dir()
    load_values()
    Output.sub_title("set environment")
    set_env_value()
    Output.sub_title("cleaning residue files")
