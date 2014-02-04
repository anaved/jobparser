#!/usr/bin/env python

from core.JobsiteParser import JobsiteParser
from util import common
import re

class Parser(JobsiteParser):

    def __init__(self, keyword,logger, **kwargs):
        JobsiteParser.__init__(self,logger)
        self.keyword = keyword
        self.fields["company_name"].func = lambda doc: doc.find("td", {'class': "resultsCompanyUrl resultsStandard"}).string
        self.fields["company_id"].func = self.fields["company_name"].func
        self.fields["title"].func = lambda doc: doc.find("div", {'class': "jobTitle"}).a.string
        self.fields["company_joburl"].func = lambda doc: doc.find("div", {'class': "jobTitle"}).a["href"]
        self.fields["source_joburl"].func = lambda doc: doc.find("div", {'class': "jobTitle"}).a["href"]
        self.fields["city"].func = lambda doc: doc.find("a", id="results.job.location").string
        self.fields["city"].patterns = [r"^([^,]*)"]
        self.fields["city"].process = lambda t: t[0].strip()
        self.fields["state"].func = lambda doc: doc.find("a", id="results.job.location").string
        self.fields["state"].patterns = [r", (.*?)\s+\d", r", ([^,/]*)$"]
        self.fields["state"].process = common.shorten
        self.fields["source"].func = lambda doc: "careercast.com"
        self.fields["posting_date"].func = lambda doc: doc.tr.findAll("td", {'class': "resultsStandard"}, recursive=False).pop().string
        self.fields["posting_date"].patterns = [r"(\d\d?)/(\d\d?)/(\d\d\d\d)"]
        self.fields["posting_date"].process = common.mm_dd_yyyy
        self.fields.update(kwargs)

        def nextpage(doc, page):
            links = doc.find("ul", {'class': "paginationLineup"})
            link=links.find('img',id='pager.pagenext') if links else None
            if link:
               return "http://www.careercast.com/careers/jobsearch/" +link.parent['href']
            return None
        self.nextlink = nextpage
        self.dev_mode=True
        self.datafunc = lambda doc: [tbody for tbody in doc.findAll("tbody") if tbody["class"] == "displayTableRowEven" or tbody["class"] == "displayTableRowOdd"]
        self.url = "http://www.careercast.com/careers/jobsearch/results?searchType=quick;kAndEntire=%s;lastUpdated=-30+days;pageSize=500;sortBy=moddate;lastUpdated_i18n_date_array[month]=9;lastUpdated_i18n_date_array[day]=4;lastUpdated_i18n_date_array[year]=2010;lastUpdated_i18n_date_mysql=2010-09-04;lastUpdated_i18n[date_array][month]=9;lastUpdated_i18n[date_array][day]=4;lastUpdated_i18n[date_array][year]=2010;lastUpdated_i18n[date_mysql]=2010-09-04;lastUpdated_i18n[utc_beginning_mysql]=2010-09-04+05%3A00%3A00;lastUpdated_i18n[utc_end_mysql]=2010-09-05+04%3A59%3A59;lastUpdated_i18n[timezone_used_for_conversion]=CST"