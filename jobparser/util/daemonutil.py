from __future__ import with_statement
import os, sys
import daemon
import signal
import lockfile
import subprocess
import time

class Daemon:
  """
    Daemon utility class.
    Args:
      name  : Name of the process. Used to name the pid file
      working_directory : The working directory for the daemon
      proc_class  :  The main class of the process which needs to be daemonized. 
                      It should define main() function which would be called by daemon
  """
  def __init__(self, name, working_directory, proc_class):
    self.name = name
    self.working_directory = working_directory
    self.proc_class = proc_class
    self.pidfile = os.path.join(working_directory+'/tmp/', name)

  # Utility function for getting the state of the daemon process
  def ps(self, pid):
    if not pid:
      return None
    try:
      proc = subprocess.Popen(['ps', '-p',str(pid),'-fl'], stdout=subprocess.PIPE)
      output = proc.communicate()[0].split('\n')[1].split()
      proc.poll()
      return output[1]
    except:
      return None

  # Function for starting the daemon
  def Run(self):
    context = daemon.DaemonContext(
            working_directory=self.working_directory,
            pidfile=lockfile.FileLock(self.pidfile)
            )
    # To get print output if any
    context.stdout=open(os.path.join(self.working_directory,'logs/daemonerror.log'),'w+')
    context.stderr = context.stdout

    with context:
      # Write the pid of the daemon process in the pidfile.
      # This will be used later for stopping or getting the stat
      #   of the process via admin.
      proc_pid_file = open(self.pidfile+'.lock','w')
      proc_pid_file.write('%d\n'%(os.getpid()))
      proc_pid_file.close()
      # Instantiate the process class and call its main method
      obj = self.proc_class()
      obj.main()


  def start(self):
    if os.path.exists(self.pidfile+'.lock'):
      print 'Process already running'
      return 0
    self.Run()

  def stop(self):
    pid = self.getpid()
    if pid:
      try:
        # Send SIGINT to the daemon process
        os.kill(pid, signal.SIGINT)
      except OSError:
        # We assume that though the process has died, 
        #   it may not have removed its pidfile
        try:
          os.remove(self.pidfile+'.lock')
        except:pass
        return 0
      
      # Wait till the process exits
      while self.ps(pid):
        time.sleep(0.1)
      return 1

    print "Process Not Running"
    return 0

  def restart(self):
      self.stop()
      self.start()

  def stat(self):
    StatDict = {
                'S' : 'Sleeping', 'R' : 'Running',
                'D' : 'Sleep', 'T'  : 'Stopped',
                'X' : 'Dead', 'Z' : 'Defunct',
                }
    pid = self.getpid()
    status = self.ps(pid)
    if status:
      print StatDict.get(status[0], 'Unknown')
      return 0
    
    print 'Not Running'
    return 0

  def sigusr(self):
    pid = self.getpid()
    if pid:
      os.kill(pid, signal.SIGUSR1)

  def getpid(self):
    pid = None
    if os.path.exists(self.pidfile+'.lock'):
      with open(self.pidfile+'.lock') as inf:
        pid = int(inf.next().strip())
    return pid

  def help(self):
    print 'Usage: <daemon-process> [start | restart | stop | stat | sigusr]'
    sys.exit(1)

  def main(self, args):
    if not os.path.exists(self.working_directory):
      os.mkdir(self.working_directory)
    if not os.path.isdir(self.working_directory):
      print "%s is not a directory" % (self.working_directory)
      return 1
    FuncDict = {'start' : self.start, 'stop' : self.stop, 'restart' : self.restart, 'stat'  : self.stat, 
                  'sigusr'  : self.sigusr}
    if not len(args) >= 2:
      self.help()

    FuncDict.get(args[1], self.help)()
