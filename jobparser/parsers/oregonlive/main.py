#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: "".join(doc.find("td", {'class': "resultsCompanyUrl resultsStandard"}).findAll(text=True))
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("a", id="results.job.title").string
        self.fields["company_joburl"].func = lambda doc: "http://jobs.oregonlive.com" + doc.find("a", id="results.job.title")["href"]
        self.fields["source_joburl"].func = lambda doc: "http://jobs.oregonlive.com" + doc.find("a", id="results.job.title")["href"]
        self.fields["city"].func = lambda doc: doc.find("a", id="results.job.location").string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("a", id="results.job.location").string
        self.fields["state"].patterns = [r", (.*?)\s+\d", r", ([^,/]*)$"]
        self.fields["state"].process = common.shorten
        self.fields["source"].func = lambda doc: "oregonlive.com"
        self.fields["posting_date"].func = lambda doc: doc.findAll("td")[3].string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.filterfields["zipcode"].func = lambda doc: doc.find("a", id="results.job.location").string
        self.filterfields["zipcode"].patterns = [r"(\d{5})"]
        self.filterfields["zipcode"].process = lambda t: t[0].strip()
        self.fields.update(kwargs)
        
        self.datafunc = lambda doc: doc.findAll("tbody", {'class': re.compile("displayTableRow")})
        self.url = "http://jobs.oregonlive.com/careers/jobsearch/results?searchType=quick;kAndEntire=%s;lastUpdated=-30+days;pageSize=50;sortBy=moddate;lastUpdated_i18n_date_array[month]=8;lastUpdated_i18n_date_array[day]=30;lastUpdated_i18n_date_array[year]=2010;lastUpdated_i18n_date_mysql=2010-08-30;lastUpdated_i18n[date_array][month]=8;lastUpdated_i18n[date_array][day]=30;lastUpdated_i18n[date_array][year]=2010;lastUpdated_i18n[date_mysql]=2010-08-30;lastUpdated_i18n[utc_beginning_mysql]=2010-08-30+07%3A00%3A00;lastUpdated_i18n[utc_end_mysql]=2010-08-31+06%3A59%3A59;lastUpdated_i18n[timezone_used_for_conversion]=PST"
        
    