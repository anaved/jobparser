#!/usr/bin/python
from __future__ import with_statement

import sys
import traceback
import os
import readline
import signal
import process_manager as pm
import time


# IF NO CORRESPONDING METHOD FOUND SHOW : NOT IMPLEMENTED
# IN TEST MODE, DONT START DAEMONS
# CAN HAVE TWO RUNNING MODES DEV, PROD. LOAD DIFFERENT FUNCTIONS FOR BOTH

def status():
    """
    Exposed method.
    Provide status of all the current running/sleeping procs

    Usage:  status
    Output: Prints Process Name and Status of all active processes    
  """
    output = ['Process Name\t\t\t\tStatus\n']
    output.append('%s\t\t\t\t%s' % (config['producername']['value'], producer('stat')))
    consout = consumer('stat')
    for i in range(config['numconsumers']['value']):
        output.append('%s\t\t\t\t%s' % (config['consumername']['value'] + '-' + str(i), consout[i]))
    output.append('Memcache\t\t\t\t%s' % queue_ops(''))
    return '\n'.join(output)

def listall():
    """
    Exposed method.
    Prints the names of all the processes available to run

    Usage : listall
    Output: Prints the names : description of processes
  """
    return pm.process_list()


def listrunning():
    """
    Exposed method.
    Prints the names of all the processes available to run

    Usage : listall
    Output: Prints the names : description of processes
    """
    return pm.active_process_list()

def startall():
    """
    Exposed method.
    Call to start producer and consumer pair as configured in the configuration file

    Usage : startall
    Output: Prints the result
    """
    print  pm.start_all()

    

def start(*arg):
    """
    Exposed method.
    Call to start a process

    Usage : start <process name>
    Output: operation status, pid
    """    

    if pm.process_list().__contains__(arg[0]):
        if arg.__contains__('-d'):
            return startdaemon(arg)
        else:
            return startnormal(arg)
    else:
        return "No process with name : %s" %(arg[0],)

def startnormal(arg):
        name=arg[0]
        pid= pm.start_process(name,False)
        if pid:
            return "Process with name : %s started with pid : %s" %(name,pid)
        else:
            return "Error occured starting Process : %s ,Check logs for details" %(name,)

def startdaemon(arg):
        name=arg[0]
        pid= pm.start_process(name,True)
        if pid:
            return "Daemon with name : %s, started with pid : %s" %(name,pid)
        else:
            return "Error occured starting Process : %s ,Check logs for details" %(name,)

def stopall():
    """
    Exposed method.
    Call to stop all processes. 

    Usage : stopall
    Output: Nothing
  """
    for parser in parserlist.parser_list(""):
        procrun([os.getcwd() + "/" + parser.__module__ + 'd.py', 'stop'])
    return ''

def stop(arg):
    """
    Exposed method.
    Call to stop a running process

    Usage : stop <process name>
    Output: operation status
    """
    if pm.process_list().__contains__(arg):
        if pm.stop_process(arg):
            return "Process with name : %s stopped .." %(arg,)
        else:
            return "Error occured stopping Process : %s ,Check logs for details" %(arg,)
    else:
        return "No process with name : %s !!" %(arg,)

def restartall():
    """
    Exposed method.
    Call to restart producer and consumer pair as configured in the configuration file

    Usage : restartall
    Output: Prints the result
  """
    for parser in parserlist.parser_list(""):
        procrun([os.getcwd() + "/" + parser.__module__ + 'd.py', 'restart'])
    return 'Restarted'

def restart(arg):
    for parser in parserlist.parser_list(""):
        if arg.lower() in parser.__module__.lower():
            procrun([os.getcwd() + "/" + parser.__module__ + 'd.py', 'restart'])
    return 'Restarted'

def sendsignal(signum=10):
    """
    Exposed method
    Send signals to producer and consumer

    Usage : sendsignal [signum]
    Args  : signum = sig number to be sent. This signal will be sent to both
              producer and consumer. Default is 10 (SIGUSR1)
    Output: Nothing
  """
    for parser in parserlist.parser_list(""):
        procrun([os.getcwd() + "/" + parser.__module__ + 'd.py', 'sigusr'])
    return ''

def signal(arg):
    for parser in parserlist.parser_list(""):
        if arg.lower() in parser.__module__.lower():
            procrun([os.getcwd() + "/" + parser.__module__ + 'd.py', 'signal'])
    return ''
 
def default():
    """
    Unknown command.
  """

def Help(arg='all'):
    """
    Usage : help [commandname]
    Args  : Name of the command for which help is sought. Defaults to all
    Output: To prin the help message
  """
    if arg.lower() == 'all':
        for k, v in FuncDict.items():
            print k
            print v.__doc__
    else:
        print FuncDict.get(arg, default).__doc__
    return ''

FuncDict = {
    'listall':listall,
    'listactive':listrunning,
    'startall': startall,
    'stopall': stopall,
    'help': Help,
    'restartall': restartall,
    'sendsignal': sendsignal,
    'start': start,
    'stop': stop,
    'restart': restart,
    'signal': signal,

}

def execute(arg):
    try:
        if len(arg) > 1:
            print FuncDict[arg[0]](*arg[1:])
        else:
            print FuncDict[arg[0]]()
    except:
        traceback.print_exc(file=sys.stdout)
        print 'Invalid command/syntax'


values = FuncDict.keys()

completions = {}

def completer(text, state):
    try:
        matches = completions[text]
    except KeyError:
        matches = [value for value in values
            if value.upper().startswith(text.upper())]
        completions[text] = matches
    try:
        return matches[state]
    except IndexError:
        return None

readline.set_completer(completer)
readline.parse_and_bind('tab: complete')

if __name__ == '__main__':
    print "Starting ..."
    if len(sys.argv) >= 2:
        execute(sys.argv[1:])
        sys.exit(0)

    while 1:
        inp = ''
        try:
            inp = raw_input('>> ')
            if not inp:
                continue
            if inp.lower() in ['quit', 'q', 'exit']:
                break
            inp = inp.strip().split(' ')
            execute(inp)
        except (KeyboardInterrupt, EOFError):
            print '\nExiting'
            break
