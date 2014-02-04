import logging
import logging.config

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


LOCAL_DEV=False
BASE_PATH=os.getcwd()

import parsers as P_ROOT
PROCESS_LIST = [[e, __import__(P_ROOT.__name__ + '.' + e, fromlist=e)]  for e in P_ROOT.__all__]
PROCESS_NAME_LIST = P_ROOT.__all__
PROCESS_DICT = dict(PROCESS_LIST)

#Logger settings
LOGGING_CONFIG = BASE_PATH+'/conf/logging.conf'
logging.config.fileConfig(LOGGING_CONFIG)
ADMIN_LOGGER = logging.getLogger('admin_logger')
APP_LOGGER = logging.getLogger('job_parser_logger')


KEYWORDS = ['']#college', 'intern', 'student', 'internship', 'major', 'coop', '"co-op"', 'bachelors', 'gpa']

#Total number of listings to be fetched in a go
TOTAL_FETCH_LIMIT=5000

#Sleep timings
LISTING_SLEEP_TIME=1
KEYWORD_SLEEP_TIME=5
URL_SLEEP_TIME=10
GLOBAL_SLEEP_TIME=3000

COOKIEFILE=BASE_PATH+'/tmp/cookie'


PARSER_THREAD_COUNT=5


os.environ['DJANGO_SETTINGS_MODULE'] = 'job.settings'