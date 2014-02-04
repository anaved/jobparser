import sys
import time

import conf.app_settings as LOCAL_SET
from conf.app_settings import ADMIN_LOGGER
from conf.app_settings import APP_LOGGER
from conf.app_settings import GLOBAL_SLEEP_TIME
from conf.app_settings import KEYWORDS
from conf.app_settings import PARSER_THREAD_COUNT
from conf.app_settings import P_ROOT
from threadpool import ThreadPool
from threadpool import WorkRequest
import traceback

__author__="naved"
__date__ ="$27 Oct, 2010 8:02:42 PM$"

def run_prod():
    cycle_count=1
    main = ThreadPool(num_workers=PARSER_THREAD_COUNT)
    while True:
        ADMIN_LOGGER.info("Starting cycle : "+str(cycle_count))
        reload(P_ROOT)
        process_list = [[e, __import__(P_ROOT.__name__ + '.' + e + '.main', fromlist=e)]  for e in P_ROOT.__all__]
        process_dict=dict(process_list)
        ADMIN_LOGGER.info("Executing process list : "+str(process_dict.items()))
        for proc_name in process_dict.keys():                
                proc=getattr(process_dict.get(proc_name),'Parser','None')
                main.putRequest(WorkRequest(proc_runner, args=(1,proc),callback=None))
                ADMIN_LOGGER.info("Started thread : "+proc_name)
                try:                    
                    main.poll()
                except NoResultsPending:
                        pass
                except :
                    ADMIN_LOGGER.error(traceback.format_exc())        
        main.wait()
        ADMIN_LOGGER.info("Sleeping for default LISTING_SLEEP_TIME : "+str(GLOBAL_SLEEP_TIME))
        time.sleep(GLOBAL_SLEEP_TIME)
        cycle_count= 1 if cycle_count > 9999 else cycle_count+1


def run_dev():
    cycle_count=1
    while True:
        ADMIN_LOGGER.info("Starting cycle : "+str(cycle_count))
        reload(P_ROOT)
        process_list = [[e, __import__(P_ROOT.__name__ + '.' + e + '.main', fromlist=e)]  for e in P_ROOT.__all__]
        process_dict=dict(process_list)
        ADMIN_LOGGER.info("Executing process list : "+str(process_dict.items()))
        for proc_name in process_dict.keys():
             ADMIN_LOGGER.info("Starting : "+proc_name)
             proc=getattr(process_dict.get(proc_name),'Parser','None')
             proc_runner(1,proc)
             ADMIN_LOGGER.info("Done : "+proc_name)
        ADMIN_LOGGER.info("Sleeping for default LISTING_SLEEP_TIME : "+str(GLOBAL_SLEEP_TIME))
        time.sleep(GLOBAL_SLEEP_TIME)
        cycle_count= 1 if cycle_count > 9999 else cycle_count+1

def proc_runner(dummy,proc):
        APP_LOGGER.info('Running : %s'%(proc.__module__,))
        proc(KEYWORDS,APP_LOGGER).run()

def log_app_params(settings):
      d= settings.__dict__
      ADMIN_LOGGER.info("With following parms...")
      for e in d.keys():
          if e.isupper():
            ADMIN_LOGGER.info("%s : %s"%(e,d[e]))
      ADMIN_LOGGER.info("Param list end")

if __name__ == "__main__":      
      ADMIN_LOGGER.info("Application initiated with path : "+sys.argv[0])
      if len(sys.argv)>1:
        ADMIN_LOGGER.info("Going to run in mode : "+sys.argv[1].upper())
      else:
        print "Invalid run arguments, Exiting!!"
        sys.exit(0)
      log_app_params(LOCAL_SET)

      if sys.argv[1]=='dev':
          run_dev()
      if sys.argv[1]=='prod':
          run_prod()
