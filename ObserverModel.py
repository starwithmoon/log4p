__author__ = 'root'
#coding:utf-8

class Subject(object):
    """
    主题类
    """
    def __init__(self):
        #观察者列表
        self.observerList = []
        self.data = 0

    #增加观察者
    def addObserver(self,observer):
        self.observerList.append(observer)

    #删除观察者
    def deleteObserver(self,observer):
        if observer in self.observerList:
            self.observerList.remove(observer)

    #通知观察者进行更新
    def notifyObservers(self):
        for observer in self.observerList:
            observer.update(self.data)

    #当值改变时通知观察者
    def setValue(self,fansnum):
        self.data = fansnum
        #通知观察者
        self.notifyObservers()

class Observer(object):
    data = ""
    """
     观察者类
    """
    def __init__(self,subject):
        #设定一个主题
        self.subject = subject
        #向这个主题添加这个观察者
        self.subject.addObserver(self)
        #观察者持有数据
        self.data = self.subject.data
    def update(self, data):
        self.data = data
        self.display()

    def display(self):
        print self.data