from conf.app_settings import LOGGING_CONFIG
from job.models import Job
import logging
import logging.config
from threadpool import *

__author__="naved"
__date__ ="$27 Oct, 2010 8:02:42 PM$"


if __name__ == "__main__":
    logging.config.fileConfig(LOGGING_CONFIG)
    ADMIN_LOGGER = logging.getLogger('admin_logger')
    sourse_list=['detroitrecruiter.com','austinrecruiter.com','seattlerecruiter.com','hirefinders.com','jobpath.com',
'nationjob.com','miracleworkers.com','mlive.com','al.com']
    for source in sourse_list:
        jo= Job.objects.filter(source=source)
        for job in jo:
            ADMIN_LOGGER.debug(job.__dict__)
