# -*- coding: utf-8 -*-

import time
import datetime
import os
from common import Vault


def create():
    log_file_name = "log-" + str(time.time())
    log_file_path = Vault.DIRECTORY_LOG + "/" + log_file_name
    Vault.FILE_MAIN_LOG = log_file_path
    with open(Vault.FILE_MAIN_LOG, 'w+') as log_file:
        log_file.write("[Start] PatchWeave started at " + str(datetime.datetime.now()) + "\n")
    if os.path.exists(Vault.FILE_LAST_LOG):
        os.remove(Vault.FILE_LAST_LOG)
    if os.path.exists(Vault.FILE_ERROR_LOG):
        os.remove(Vault.FILE_ERROR_LOG)
    if os.path.exists(Vault.FILE_COMMAND_LOG):
        os.remove(Vault.FILE_COMMAND_LOG)
    with open(Vault.FILE_LAST_LOG, 'w+') as last_log:
        last_log.write("[Start] PatchWeave started at " + str(datetime.datetime.now()) + "\n")


def log(log_message):
    if "COMMAND" in log_message:
        with open(Vault.FILE_COMMAND_LOG, 'a') as log_file:
            log_file.write(log_message)
    with open(Vault.FILE_MAIN_LOG, 'a') as log_file:
        log_file.write(log_message)
    with open(Vault.FILE_LAST_LOG, 'a') as log_file:
        log_file.write(log_message)


def information(message):
    message = "[INFO]: " + str(message) + "\n"
    log(message)


def trace(function_name, arguments):
    message = "[TRACE]: " + function_name + ": " + str(arguments.keys()) + "\n"
    log(message)


def command(message):
    message = "[COMMAND]: " + str(message) + "\n"
    log(message)


def error(message):
    message = "[ERROR]: " + str(message) + "\n"
    log(message)


def output(message):
    log(message + "\n")


def warning(message):
    message = "[WARNING]: " + str(message) + "\n"
    log(message)


def end(time_duration):
    output("[END] PatchWeave ended at " + str(datetime.datetime.now()) + "\n\n")
    output("\nTime duration\n----------------------\n\n")
    output("Initialization: " + time_duration[Vault.KEY_DURATION_INITIALIZATION] + " seconds")
    output("Build: " + time_duration[Vault.KEY_DURATION_BUILD] + " seconds")
    output("Diff Analysis: " + time_duration[Vault.KEY_DURATION_DIFF_ANALYSIS] + " seconds")
    output("Trace Analysis: " + time_duration[Vault.KEY_DURATION_TRACE_ANALYSIS] + " seconds")
    output("Symbolic Trace Analysis: " + time_duration[Vault.KEY_DURATION_SYMBOLIC_TRACE_ANALYSIS] + " seconds")
    output("Slicing: " + time_duration[Vault.KEY_DURATION_SLICE] + " seconds")
    output("Transplantation: " + time_duration[Vault.KEY_DURATION_TRANSPLANTATION] + " seconds")
    output("Verification: " + time_duration[Vault.KEY_DURATION_VERIFICATION] + " seconds")
    output("\nPatchWeave finished successfully after " + time_duration[Vault.KEY_DURATION_TOTAL] + " seconds\n")

