#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from datetime import datetime
from parsers.indeed.conf import domains
from parsers.indeed.conf import ignore_list
import re
import urllib2
from urlparse import urlparse
from util import common
class Parser(JobsiteParser):

    def __init__(self, keyword, logger, ** kwargs):
        JobsiteParser.__init__(self, logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.company.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.jobtitle.string
        self.fields["company_joburl"].func = lambda doc: get_company_url(doc)
        self.fields["source_joburl"].func = lambda doc: doc.url.string
        self.fields["city"].func = lambda doc: doc.city.string        
        self.fields["state"].func = lambda doc: doc.state.string
        self.fields["source"].func = lambda doc: "indeed.com"
        self.fields["posting_date"].func = lambda doc: datetime.strptime(doc.date.string,'%a, %d %b %Y %H:%M:%S %Z')
        self.fields.update(kwargs)         
        self.cookie=False
        def get_company_url(doc):
            try:
                url = 'http://www.indeed.com/rc/clk?jk=%s&from=vj' % doc.jobkey.string
                request = urllib2.Request(url)
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
                u = opener.open(request, timeout=10)
                url=u.url
                urlp=urlparse(url)
                for e in ignore_list:
                    m=re.search(e,urlp.netloc)
                    if m:
                        self.logger.info(" Ignoring : "+url+"  For : "+e)
                        return None
                return url
            except Exception as ex:                
                self.logger.warning(str(ex))
                return doc.url.string
            

        self.datafunc = lambda doc: doc.findAll('result') or None
        self.nextlink = lambda x, y: None            
        self.url=domains

        self.dev_mode=True