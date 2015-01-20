# log4p
log for python like log4j2

use config file [log4p.py], in the application root directory.

----------------------------------
App Example:
from log4p import log
TestLog = log(__name__)
TestLog.debug("Debug Log")
TestLog.info("Info Log")

out put like this:
2015-01-20 16:18:47,692 DEBUG [Thread-3] data.LogInsert (LogInsert.py:172) - Debug Log
2015-01-20 16:18:47,692 DEBUG [Thread-3] data.LogInsert (LogInsert.py:173) - Info Log

----------------------------------
Config Example:
"log4j2.xml
<?xml version="1.0" encoding="UTF-8"?>
<Configuration monitorInterval="60">
    <Appenders>
        <File name="A1" fileName="A1.log" append="false">
            <PatternLayout pattern="%d %-5p [%t] %C{2} (%F:%L) - %m%n"/>
        </File>
        <Console name="STDOUT" target="SYSTEM_OUT">
            <PatternLayout pattern="%d %-5p [%t] %C{2} (%F:%L) - %m%n"/>
        </Console>
    </Appenders>
    <Loggers>
        <Logger name="data" level="error" additivity="false">
            <AppenderRef ref="A1"/>
        </Logger>
        <Root level="debug">
            <AppenderRef ref="A1"/>
        </Root>
    </Loggers>
</Configuration>"

config ={
    'monitorInterval' : 10,
    'loggers' :{
        'LogThread' :{
            'level': "DEBUG",
            'additivity' : False,
            'AppenderRef' : ['A1']
            },
        'root' :{
            #'level' : "CRITICAL",
            'level' : "ERROR",
            'AppenderRef' : ['output_root']
        }
    },

    'appenders' :{
        'output_root' :{
            'type' :"file",
            'FileName' :"root_error.log",
            'PatternLayout' :"[level:%(levelname)s-file:%(filename)s-lineno:%(lineno)d] %(asctime)s %(message)s"
        },
        'A1' :{
            'type' :"file",
            'FileName' :"A2.log",
            'PatternLayout' :"[level:%(levelname)s-file:%(filename)s-lineno:%(lineno)d] %(asctime)s %(message)s"
        },
        'console' :{
            'type' :"console",
            'target' :"console",
            'PatternLayout' :"[%(levelname)s] %(asctime)s %(message)s"
        }
    }
}


