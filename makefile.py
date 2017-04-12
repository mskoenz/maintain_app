#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    07.12.2016 14:03:38 CET
# File:    make.py


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
