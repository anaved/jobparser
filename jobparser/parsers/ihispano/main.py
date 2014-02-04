#!/usr/bin/env python

from util import common
from core.JobsiteParser import JobsiteParser
import re

class Parser(JobsiteParser):

    def __init__(self, keyword, logger, ** kwargs):
        JobsiteParser.__init__(self, logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find('td', {'class': 'results_company'}).a.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find('td',{'class':'results_title'}).a.string
        self.fields["company_joburl"].func = lambda doc: doc.a["href"]
        self.fields["source_joburl"].func = lambda doc: doc.a["href"]
        self.fields["city"].func = lambda doc: doc.find('td',{'class':'results_location'}).findAll('a')[0].string
        self.fields["city"].process = lambda t: t.strip()
        self.fields["state"].func = lambda doc: doc.find('td',{'class':'results_location'}).findAll('a')[1].string
        self.fields["state"].process = lambda t: t.strip()
        self.fields["source"].func = lambda doc: "ihispano.com"
        self.fields["posting_date"].func = lambda doc: doc.find('td', {'class':'results_create'}).string.strip()
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
#        self.fields["posting_date"].depth = 2
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            links = doc.find("span", {'class': "pager-list"})
            if links.findChildren()[-1].name!='strong':
                url= 'http://www.ihispano.com' + links.find('strong').findNext('a')['href']                
                return url
            return None                        
        
        self.datafunc = lambda doc: doc.findAll('tr', {'class':'top-result-row'})
        self.dev_mode=True
        self.url = "http://www.ihispano.com/careers/searchjob/results?key_words=%s&country=USA&state=&city=&searchtype=qck&Save=save&zip_code=&jobs_within_miles=10&category=&op=Search&form_id=candidate_searchjob_quick"
        self.nextlink = nextpage
    
    