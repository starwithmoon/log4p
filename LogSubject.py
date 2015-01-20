__author__ = 'root'
#coding:utf8
from ObserverModel import Subject, Observer
import threading, time
from pyetc import load, reload, unload

class LogSubject(Subject):
    timer_log = 0
    config = 0
    t1 = 0
    def __init__(self):
        #观察者列表
        super(LogSubject, self).__init__()
        self.data = 0
        self.start()

    def start(self):
        self.t1 = time.time()
        self.config = load("E://kuaipan//Code_Dev//Code_Libraries//Python//libs//log//config.py")
        self.timer_log = threading.Timer(self.config.config['interval'], self.reload_config)
        self.timer_log.start()

    def reload_config(self):
        print "used time:" + str(int(time.time() - self.t1))
        print "hello world"
        # reload new log config
        self.config = reload(self.config)
        self.data = self.config
        # notification all observers
        self.notifyObservers()
        self.timer_log = threading.Timer(self.config.config['interval'], self.reload_config)
        self.timer_log.start()
        self.t1 = time.time()


if __name__ == '__main__':
    log = LogSubject()
    log.start()
