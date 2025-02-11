#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os

Project_A = None
Project_B = None
Project_C = None
Project_D = None

DEBUG = False
SKIP_TRACE_GEN = False
SKIP_SYM_TRACE_GEN = False
SKIP_EXPLOIT = False
SKIP_WEAVE = False
SKIP_ANALYSE = False
SKIP_VERIFY = False
SKIP_SLICE = False
SKIP_RESTORE = False
ONLY_VERIFY = False
BACKPORT = False

STANDARD_FUNCTION_LIST = list()
STANDARD_MACRO_LIST = list()

PROJECT_A_FUNCTION_LIST = ""
PROJECT_B_FUNCTION_LIST = ""
PROJECT_C_FUNCTION_LIST = ""
DIFF_FUNCTION_LIST = ""
DIFF_LINE_LIST = dict()
DIVERGENT_POINT_LIST = list()
FUNCTION_MAP = ""
CRASH_LINE_LIST = dict()
TRACE_LIST = dict()


# ------------------ Configuration Values ---------------
PATH_A = ""
PATH_B = ""
PATH_C = ""
EXPLOIT_A = ""
EXPLOIT_C = ""
BUILD_FLAGS_A = ""
BUILD_FLAGS_C = ""
CONFIG_COMMAND_A = ""
CONFIG_COMMAND_C = ""
BUILD_COMMAND_A = ""
BUILD_COMMAND_C = ""
PATH_POC = ""
EXPLOIT_PREPARE = ""
ASAN_FLAG = ""
KLEE_FLAG_A = ""
KLEE_FLAG_C = ""
FILE_CONFIGURATION = ""
AST_DIFF_SIZE = "10"

silence_emitter = False

header_file_list_to_patch = []
c_file_list_to_patch = []

generated_script_for_header_files = dict()
generated_script_for_c_files = dict()

translated_script_for_files = dict()
variable_map = dict()
diff_info = dict()

non_localized_function_list = list()
localized_function_list = list()
fuzz_results = dict()
original_patch = ""
transplanted_patch = ""
localization_iteration_no = 0