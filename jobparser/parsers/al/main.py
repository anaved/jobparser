#!/usr/bin/env python

import time

from core.JobsiteParser import JobsiteParser
from util import common
from util.html2content import get_desc
import re
class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: "".join(doc.find("td", {'class': "resultsCompanyUrl resultsStandard"}).findAll(text=True))
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("div", {'class': "jobTitle"}).a.string
        self.fields["company_joburl"].func = lambda doc: "http://jobs.al.com" + doc.find("div", {'class': "jobTitle"}).a["href"]
        self.fields["source_joburl"].func = lambda doc: "http://jobs.al.com" + doc.find("div", {'class': "jobTitle"}).a["href"]
        self.fields["city"].func = lambda doc: doc.find("a", id="results.job.location").string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("a", id="results.job.location").string
        self.fields["state"].patterns = [r", (.*?)\s+\d", r", ([^,/]*)$"]
        self.fields["state"].process = common.shorten
        self.fields["source"].func = lambda doc: "al.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("td", {'class': "resultsStandard"})[2].string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.filterfields["zipcode"].func = lambda doc: doc.find("a", id="results.job.location").string
        self.filterfields["zipcode"].patterns = [r"(\d{5})"]
        self.filterfields["zipcode"].process = lambda t: t[0].strip()
        self.fields.update(kwargs)
#        self.fields["all_text"].func = lambda doc: all_text(doc)
        
        def all_text(doc):
            doc=str(doc.find('div',{'class':'remoteJobDescriptionContainer'}))
            return get_desc(doc,self.url)

        def nextpage(doc, page):
            links = doc.find("ul", {'class': "paginationLineup"})
            link=links.find('img',id='pager.pagenext') if links else None
            if link:
               return "http://jobs.al.com/careers/jobsearch/" +link.parent['href']
            return None
        
        self.datafunc = lambda doc: doc.findAll("tbody", {'class': re.compile("^displayTableRow")})
        self.url = "http://jobs.al.com/careers/jobsearch/results?searchType=quick;kAndEntire=%s;lastUpdated=-30+days;pageSize=100;sortBy=moddate;lastUpdated_i18n_date_array[month]=9;lastUpdated_i18n_date_array[day]=4;lastUpdated_i18n_date_array[year]=2010;lastUpdated_i18n_date_mysql=2010-09-04;lastUpdated_i18n[date_array][month]=9;lastUpdated_i18n[date_array][day]=4;lastUpdated_i18n[date_array][year]=2010;lastUpdated_i18n[date_mysql]=2010-09-04;lastUpdated_i18n[utc_beginning_mysql]=2010-09-04+05%3A00%3A00;lastUpdated_i18n[utc_end_mysql]=2010-09-05+04%3A59%3A59;lastUpdated_i18n[timezone_used_for_conversion]=CST"
        self.nextlink = nextpage
        self.dev_mode=True


