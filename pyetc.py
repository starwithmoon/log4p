__author__ = 'root'
#coding:utf-8

# pyetc.py
# Python 格式的配置文件支持库
#
import sys, os.path

Module = type(sys) # 故技重演
modules = {}       # 缓存已经导入的 etc (配置) 模块

# 导入任意符合 Python 语法的文件
# 用法:
# module = pyetc.load(完整文件路径并包含扩展名, 预载入变量, 自定义返回模块类型)
#
def load(fullpath, env={}, module=Module):
    try:
        code = open(fullpath).read()
    except IOError:
        raise ImportError, 'No module named  %s' %fullpath

    filename = os.path.basename(fullpath)

    try:
        return modules[filename]
    except KeyError:
        pass

    m = module(filename)
    m.__module_class__ = module
    m.__file__ = fullpath

    m.__dict__.update(env)

    exec compile(code, filename, 'exec') in m.__dict__
    modules[filename] = m

    return m

# 移除已经导入的模块
# 用法:
# module = unload(module)
#
def unload(m):
    filename = os.path.basename(m.__file__)
    del modules[filename]

    return None

# 重新导入模块
# 用法:
# module = pyetc.reload(module)
def reload(m):
    fullpath = m.__file__

    try:
        code = open(fullpath).read()
    except IOError:
        raise ImportError, 'No module named  %s' %fullpath

    env = m.__dict__
    module_class = m.__module_class__

    filename = os.path.basename(fullpath)
    m = module_class(filename)

    m.__file__ = fullpath
    m.__dict__.update(env)
    m.__module_class__ = module_class

    exec compile(code, filename, 'exec') in m.__dict__
    modules[filename] = m

    return m