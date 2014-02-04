import traceback

#!/usr/bin/env python
from util import common
from core.JobsiteParser import JobsiteParser
from parsers.taleo.conf import xdomains
from parsers.taleo.helper import get_subdomain
import urllib2
from datetime import datetime
from urlparse import urlparse
class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: get_company(doc)
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc['title']
        self.fields["company_joburl"].func = lambda doc: doc['company_joburl']
        self.fields["source_joburl"].func = self.fields["company_joburl"].func
        self.fields["city"].func = lambda doc: get_loc(doc)[0]#doc['location'].split('-')[2]
        self.fields["state"].func = lambda doc: get_loc(doc)[1]#doc['location'].split('-')[1]
        self.fields["source"].func = lambda doc: get_company(doc)#"taleo.com"
        self.fields["posting_date"].func= lambda doc: datetime.now().strftime('%m/%d/%Y')
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.fields["all_text"].func = lambda doc: all_text(doc)
        self.fields["all_text"].depth = 1        
        self.fields.update(kwargs)        
        self.nextlink=lambda x,y : None
        self.dev_mode=True

        def loc(x):
             return x["city"] + "-" + x["state"]
         
        self.fields["location"].func = loc

        def get_loc(doc):
            data= doc['location'].split('-')
            city=""
            state=""
            if len(data)>2:
                city=data[2]
            if len(data)>1:
                state='%s-%s'%(data[1],data[0])
            return [city,state]


        def all_text(doc):
            return doc['all_text']

        def get_company(doc):
            x=urlparse(doc['company_joburl']).netloc.split('.')[0]
            url= 'http://%s.taleo.net'%(x,)
            if not xdomains[url][0]:
                 return x
            return xdomains[url][0]
        
        def create_sd_url(sd):
            url = 'https://%s.taleo.net/careersection/jobsearch.ftl' % sd            
            try:
                return urllib2.urlopen(url).url
            except:
                self.logger.warn("Error opening : "+url)
#                self.logger.error(traceback.format_exc())
                return None
        
        def create_urls():
            urls=[]
            for e in xdomains.keys():
               url= create_sd_url(urlparse(e).netloc.split('.')[0])
               urls.append(url) and url            
            return urls

        self.url= create_urls()
        self.datafunc =  lambda doc: get_subdomain(self.url)

