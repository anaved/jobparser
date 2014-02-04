#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        
        self.fields["company_name"].func = lambda doc: doc.find("div", {'class': "instName"}).string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("div", {'class': "jobTitle"}).a.string
        self.fields["company_joburl"].func = lambda doc: "http://higheredjobs.com/" + doc.find("div", {'class': "jobTitle"}).a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://higheredjobs.com/" + doc.find("div", {'class': "jobTitle"}).a["href"]
        self.fields["city"].func = lambda doc: doc.find("div", {'class': "jobLocation"}).string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("div", {'class': "jobLocation"}).string
        self.fields["state"].patterns = [r", (\w\w)\W", r", (\w\w)$"]
        self.fields["state"].process = lambda t: t[0].strip()
        self.fields["state"].mandatory = True
        self.fields["source"].func = lambda doc: "higheredjobs.com"
        self.fields["posting_date"].func = lambda doc: doc.find("div", {'class': "jobDetails"}).string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yy
        self.fields.update(kwargs)        
        self.cookie = False
        
        self.keyword = ['intern']#'college', 'intern', 'student', 'internship', 'major', 'coop', '"co-op"', 'bachelors', 'gpa']
        def get_data(doc):
            data=doc.find("div", {'id': "jobResults"})
            if data:
                return data.table.findAll("tr", {'valign': "top"}, recursive=False)
            return None

        self.datafunc = lambda doc: get_data(doc)#doc.find("div", {'id': "jobResults"}).table.findAll("tr", {'valign': "top"}, recursive=False)
        #shows all results in a page
        self.url = "http://higheredjobs.com/search/advanced_action.cfm?Keyword=%s&PosType=&InstType=&JobCat=&Region=0&SubRegions=&Metros=&OnlyTitle=0&SortBy=1&ShowAll=yes"
        