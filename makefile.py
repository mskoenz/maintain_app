#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    07.12.2016 14:03:38 CET
# File:    make.py

from addon import core
from addon.util import make


def job(param, db):
    js = core.namespace()

    js.reso_indep = [
        "git@github.com:mskoenz/maintain_app.git"]

    js.cmd = "maintain_app/build/maintain_core/main"
    js.cmd_version = "1.0"

    js.postprocess = "maintain_app/maintain_core/main_sql.py"
    js.sql_db = "{build}/data.s3db"
    js.sql_table = "testing"

    js.prepare = [("maintain_app", "mkdir build"),
                  ("maintain_app/build", "cmake .."),
                  ("maintain_app/build", "make main")
                  ]

    js.time_limit = 60
    js.cmd_param = param

    return js


@make.out("{build}/data/{opt_path}/maintain.m5c")
@make.asz("zurkon.launch")
def launch():
    make.mkdir("{build}/data/{opt_path}")
    db = make.parse("{build}/data.s3db")

    param, job = make.assoz_param.output_all

    todo = []

    js = job(dict(input=1), db)
    todo.append(zurkon.submit(js))

    zurkon.launch_jobs(
        make.zurkon.output,
        todo,
        make.output)


@make.out("{build}/data/{opt_path}/maintain.s3db")
@make.dep("launch")
@make.asz("zurkon.launch")
@make.lbl("collect")
def collect():
    make.mkdir("{build}/data/{opt_path}")
    m5c_file = make.depend.output
    if zurkon.open_jobs(m5c_file) > 0:
        if not zurkon.collect_jobs(make.assoz.output):  # cancel
            return make.stop

    util.transfer_table(make.parse("{build}/data.s3db"),
                        make.output,
                        m5c_file,
                        make.opt.bind)

if __name__ == "__main__":
    make.main()
