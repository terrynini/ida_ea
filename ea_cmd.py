# -*- coding: utf-8 -*-

from .api_funcs import *
from copy import copy
from .ea_UI import Cmd_UI
from .ea_utils import QtWidgets, ea_warning, get_bits, get_mem_recursive, parse_mem, style
from idaapi import *
from idautils import *
from idc import *
from re import match
from time import sleep, time


def get(addr, int_size, n=20):

    string = copy(style[0])
    string += "<p>"

    for x in range(n):
        regions = []
        get_mem_recursive(addr + x * 4, regions, int_size=int_size)
        string += parse_mem(regions) + "<br>"

    string += "</p>"

    form.textEdit.append(string)
    form.textEdit.verticalScrollBar().setValue(form.textEdit.verticalScrollBar().maximum())


def find(arg, int_size):

    matches = []
    addr = 0

    for x in range(100):
        newAddr = FindText(addr, SEARCH_DOWN, 0, 0, arg)
        if newAddr != 0xffffffffffffffff:
            if newAddr > addr:
                addr = newAddr
                matches.append(addr)
            else:
                addr += 0x4
        else:
            break

    string = copy(style[0])
    string += "<p>"

    for addr in matches:
        regions = []
        get_mem_recursive(addr, regions, int_size=int_size)
        string += parse_mem(regions) + "<br>"

    string += "</p>"

    form.textEdit.append(string)
    form.textEdit.verticalScrollBar().setValue(form.textEdit.verticalScrollBar().maximum())


def do_cmd():

    int_size = 4 if get_bits() else 8
    cmd = form.lineEdit.text()
    form.textEdit.append(copy(style) + "<span>&#x25B6; " + cmd +"</span><br>")

    match_read = match(r"(x\\|x)([0-9]*) *(.*)", cmd)
    match_search = match(r"searchmem *(.*)", cmd)
    match_step = match(r"step|si", cmd)
    match_continue = match(r"continue|c", cmd)
    match_run = match(r"run|r", cmd)
    match_finish = match(r"finish|fini", cmd)
    match_break = match(r"(break|b) *(.*)", cmd)
    match_delete = match(r"(delete|delet|del) *(.*)", cmd)


    if match_read:
        length = to_int(match_read.group(2))
        addr = to_int(match_read.group(3))

        get(addr, int_size, length)

    elif match_search:
        cmd = match_search.group(1)

        if cmd[0] == "\"" and cmd[-1] == "\"":
            cmd = cmd[1:-1]

        find(str(cmd), int_size)

    elif match_step:
        step_into()

    elif match_finish:
        step_until_ret()

    elif match_continue:
        continue_process()

    elif match_break:
        add_bp(to_int(match_break.group(2)))

    elif match_delete:
        del_bpt(to_int(match_delete.group(2)))

    elif match_run:
        if get_process_state() != 0:
            StopDebugger()
            # TODO: find way to asynchronously restart debugger without crashing IDA
            # a_sync(restart)
        else:
            ProcessUiAction("ProcessStart")


def restart():

    start = time()
    timeout = False

    while get_process_state() != 0:
        sleep(0.5)
        if start - time() > 4:
            timeout = True
            ea_warning("Restart operation timed out")
            break

    runDebugger(get_input_file_path())


def to_int(i):

    if "0x" in i or "0X" in i:
        return int(i[2:],16)
    else:
        return int(i)


def ea_cmd():

    global a
    global form

    a = QtWidgets.QFrame()
    form = Cmd_UI()
    form.setupUi(a)
    form.textEdit.setReadOnly(True)
    form.lineEdit.returnPressed.connect(do_cmd)
    form.pushButton.clicked.connect(do_cmd)
    a.show()


addresses = 0
max_iterations = 10
iterations = 0
a = None
form = None
