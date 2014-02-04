#!/usr/bin/env python

import time

from core.JobsiteParser import JobsiteParser
import re
from util import common

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: "".join(doc.findAll("td")[1].findAll(text=True))
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("a", {'class': "jt"}).string
        self.fields["company_joburl"].func = lambda doc: doc.find("a", {'class': "jt"})["href"]
        self.fields["source_joburl"].func = lambda doc: doc.find("a", {'class': "jt"})["href"]
        self.fields["city"].func = lambda doc: doc.find("td", id=re.compile(r"Location")).string
        self.fields["city"].patterns = [r"-([^-]*)$"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("td", id=re.compile(r"Location")).string
        self.fields["state"].patterns = [r"-(\w\w)-"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["latitude"].func = lambda doc: doc.find("a", id=re.compile("MapJob"))["href"]
        self.fields["latitude"].patterns = [r"lat=(.*?),"]
        self.fields["latitude"].process = lambda t: float(t[0].strip())
        self.fields["latitude"].depth = 2
        self.fields["longitude"].func = lambda doc: doc.find("a", id=re.compile("MapJob"))["href"]
        self.fields["longitude"].patterns = [r"lon=(.*?),"]
        self.fields["longitude"].process = lambda t: float(t[0].strip())
        self.fields["longitude"].depth = 2
        self.fields["source"].func = lambda doc: "careerrookie.com"
        self.fields["posting_date"].func = lambda doc: doc.find("span", id=re.compile(r"Posted")).string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.fields.update(kwargs)
        
        def nextpage(doc, page):
            link = doc.find("td", {'class': "nav_btm_cell"}).span.a
            if link is None:
                return None
            return link["href"]

        self.datafunc = lambda doc: doc.findAll("tr", {'class': re.compile(r"^jl_\w+_row$")})
        self.url = "http://www.careerrookie.com/CC/jobseeker/jobs/jobresults.aspx?mxjobsrchcriteria_rawwords=%s&s_freeloc=&_SearchJobBySkills%3As_jobtypes=ALL&s_emptype=JTFT&s_emptype=JTPT&s_emptype=JTIN&s_emptype=JTSE&s_emptype=JTIO&_SearchJobBySkills%3AImage1.x=64&_SearchJobBySkills%3AImage1.y=26&subtbtn=true"
        self.nextlink = nextpage
    
    