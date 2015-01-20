#!/usr/local/python/bin
# coding=utf-8
from LogObserver import log

xxlog = log("xxx")

while True:
    xxlog.info("info")
    xxlog.error("yyy")
    xxlog.debug("debug")
