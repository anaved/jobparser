#!/usr/bin/env python
import time

from core.JobsiteParser import JobsiteParser
from datetime import datetime
from parsers.adicio.config import xdomains
import re
from urlparse import urlparse
from util import common
from util.html2content import get_desc
class Parser(JobsiteParser):
    def __init__(self, keyword, logger, ** kwargs):
        JobsiteParser.__init__(self, logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: get_company(doc)
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find('div', {'class':'jobTitle'}).a.string
        self.fields["company_joburl"].func = lambda doc: get_joburl(doc)
        self.fields["source_joburl"].func = self.fields["company_joburl"].func
        self.fields["city"].func = lambda doc: get_location(doc)['city'].strip()
        self.fields["state"].func = lambda doc: get_location(doc)['state'].strip()
        self.fields["source"].func = lambda doc: "adicio.com"
        self.fields["posting_date"].func = lambda doc: get_date(doc)
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.fields.update(kwargs)
        self.fields["all_text"].func = lambda doc: all_text(doc)

        def all_text(doc):            
            doc=str(doc.find('div',{'class':'remoteJobDescriptionContainer'}))            
            return get_desc(doc,self.url)
        def get_date(doc):
            try:
                d = doc.findAll('td', {'class':'resultsStandard'})[-2].string.strip()
            except:
                x = datetime.now()
                d = "%s/%s/%s" % (x.month, x.day, x.year)
            return d

        def get_company(doc):
            str = doc.find('td', {'class':re.compile('^resultsCompanyUrl.*')})
            x = str.findChild()
            str = x.string if x else str.string
            return str

        def get_location(doc):
            data = urlparse(doc.find('a', id='results.job.location')['href'])
            location_dict = dict(e.split('=')  for e in data.query.split('&'))
            return location_dict

        def get_joburl(doc):
            job_url = 'http://%s%s' % (urlparse(self.url).netloc, doc.find('div', {'class':'jobTitle'}).a['href'])
            return job_url

        def nextpage(doc, page):            
            links = doc.find('ul', {'class':'paginationLineup'})
            if links is None or  links.findAll('a') is None:
                return None            
            return 'http://%s/careers/jobsearch/%s%d' % (urlparse(self.url).netloc, links.findAll('a')[0]['href'][:-2], (page + 1) * 10)
            

        self.nextlink = nextpage        
        self.datafunc = lambda doc: doc.findAll("tbody", {'class':re.compile("^displayTableRow.*")})        
        self.url = xdomains