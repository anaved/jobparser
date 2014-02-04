
#!/usr/bin/env python
from util import common
from core.JobsiteParser import JobsiteParser


class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.company.string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.jobtitle.string
        self.fields["company_joburl"].func = lambda doc: 'http://www.careerbuilder.com/JobSeeker/Jobs/JobDetails.aspx?job_did=%s'%(doc.did.string)
        self.fields["source_joburl"].func = self.fields["company_joburl"].func
        self.fields["city"].func = lambda doc: doc.location.string.split('-')[-1]
        self.fields["state"].func = lambda doc: doc.location.string.split('-')[0]
        self.fields["source"].func = lambda doc: "careerbuilder.com"
        self.fields["posting_date"].func = lambda doc: doc.posteddate.string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy        
        self.fields.update(kwargs)   

        def nextpage(doc, page):               
               url='http://api.careerbuilder.com/v1/jobsearch?DeveloperKey=WDAX88L6VM2F0BQG99WX&PostedWithin=1&Keywords=%s&PerPage=100&PageNumber=%d'%(self.query,page+1)
               return url

        self.nextlink=nextpage        
        self.datafunc = lambda doc: doc.findAll('jobsearchresult')
        self.cookie=False
        self.url=['http://api.careerbuilder.com/v1/jobsearch?DeveloperKey=WDAX88L6VM2F0BQG99WX&PostedWithin=1&Keywords=%s&PerPage=100&PageNumber=1']
        self.query_sleeptime=3600
